from rest_framework.response import Response
from rest_framework.decorators import api_view, parser_classes, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework import status
from django.db.models import Count, Avg, TextField
from django.db.models.functions import Cast
from django.shortcuts import get_object_or_404, get_list_or_404

from . models import Book, Category, Comment, Thread, BookRating
from .serializers import BookListSerializer, BookSerializer, CommentSerializer, CategoryListSerializer, BookLikeSerializer
from .serializers import ThreadListSerializer, ThreadSerializer , ThreadCreateSerializer, ThreadDetailSerializer, ThreadLikeSerializer
from .serializers import BookRatingSerializer, BookRatingInfoSerializer, RecommendationBookSerializer, ThreadHomeSerializer, BookHomeSerializer

from django.db.models import Q
import random

from .utils import decode_embedding, cosine_similarity, enhance_content
import numpy as np

## 홈을 보여주는 페이지
@api_view(['GET'])
def home_data(request):
    # 1) 베스트셀러: 리뷰 순 상위 10권
    # bestsellers = Book.objects.order_by('-customer_review_rank')[:10]
    bestsellers = Book.objects.order_by('pk')[:10]
    

    # 2) 랜덤 키워드 뽑기
    #    (Book.keywords는 리스트이므로, 전체 keywords flatten 후 랜덤 선택)
    # all_keywords = set(
    #     kw
    #     for kws in Book.objects.values_list('keywords', flat=True)
    #     for kw in kws
    # )
    # random_keyword = random.choice(list(all_keywords)) if all_keywords else None
    
    # qs = Book.objects.annotate(
    #     keywords_text=Cast('keywords', TextField())
    # )

    # # if random_keyword:
    # #     recommended = qs.filter(
    # #         keywords_text__icontains=random_keyword
    # #     )[:10]
    # if random_keyword:
    #     recommended = qs.filter(
    #         keywords_text__icontains=random_keyword
    #     )[:10]
    # else:
    #     recommended = Book.objects.none()
    # print(recommended)
        
    # # 2) 배열 안에 "foo"라는 키워드가 들어있으면, JSON의 `"foo"` 문자열이 나타나기 때문에
    # #    f'"{random_keyword}"' 형태로 검색
    # recommended = qs.filter(keywords_text__icontains=f'"{random_keyword}"')[:10]

    ranking_book = Book.objects.order_by('-customer_review_rank')[:10]
    # 3) 최신 쓰레드 3개
    latest_threads = Thread.objects.order_by('-created_at')[:3]

    return Response({
        'bestsellers': BookHomeSerializer(bestsellers, many=True).data,
        # 'recommended': {
        #     'keyword': random_keyword,
        #     'books': BookSerializer(recommended, many=True).data,
        # },
        'ranking_book': BookHomeSerializer(ranking_book, many=True).data,
        'latest_threads': ThreadHomeSerializer(latest_threads, many=True).data,
    })


# book_list : 전체 도서 데이터 목록 제공 (id, title, author, isbn, cover)
@api_view(['GET'])
def book_list(request):
    books = get_list_or_404(Book)
    categories = get_list_or_404(Category)

    serialized_books = BookListSerializer(books, many=True).data
    serialized_categories = CategoryListSerializer(categories, many=True).data

    books_data = [
        {
            "model": "books.book",
            "pk": book["id"],
            "fields": {k: v for k, v in book.items() if k != "id"}
        }
        for book in serialized_books
    ]

    categories_data = [
        {
            "model": "books.category",
            "pk": category["id"],
            "fields": {k: v for k, v in category.items() if k != "id"}
        }
        for category in serialized_categories
    ]

    return Response({
        "categories": categories_data,
        "books": books_data,
    }, status=status.HTTP_200_OK)

# book_detail : 단일 도서 정보 제공 (카테고리 및 쓰레드 개수 정보 등 포함)
@api_view(['GET'])
def book_detail(request, book_pk):
    book = get_object_or_404(
        Book.objects.annotate(num_of_threads=Count('threads')),
        pk=book_pk
    )
    serializer = BookSerializer(book)
    return Response(serializer.data, status=status.HTTP_200_OK)

# thread_list : 전체 쓰레드 목록 제공
@api_view(['GET'])
def thread_list(request):
    thread = get_list_or_404(Thread)
    serializer = ThreadListSerializer(thread, many=True)
    return Response(serializer.data,status=status.HTTP_200_OK)

# thread_detail : 단일 쓰레드 조회 & 수정 & 삭제 (도서 제목 및 댓글 목록 포함)
@api_view(['GET', 'PUT', 'DELETE'])
def thread_detail(request, book_pk, thread_pk):
    thread = get_object_or_404(
        Thread.objects.annotate(num_of_comments=Count('comments')),
        pk=thread_pk
    )

    # 조회
    if request.method == 'GET':
        serializer = ThreadSerializer(thread)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    # 수정
    elif request.method == 'PUT':
        # 권한 확인 추가
        if thread.user != request.user:
            return Response(
                {'error': '수정 권한이 없습니다.'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        # partial=True로 부분 업데이트 허용
        serializer = ThreadSerializer(thread, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            # user 필드는 기존 값 유지
            serializer.save(user=thread.user)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    # 삭제
    elif request.method == 'DELETE':
        # 권한 확인 추가
        if thread.user != request.user:
            return Response(
                {'error': '삭제 권한이 없습니다.'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        thread.delete()
        return Response({'message': f'thread {thread_pk} is deleted.'}, status=status.HTTP_200_OK)

# create_thread : 쓰레드 생성
@api_view(['POST'])
@parser_classes([JSONParser, MultiPartParser, FormParser])
def create_thread(request, book_pk):
    book = get_object_or_404(Book, pk=book_pk)
    serializer = ThreadCreateSerializer(data=request.data, context={'request': request})
    serializer.is_valid(raise_exception=True)
    # 파일과 user, book 모두 save에 전달
    serializer.save(book=book, user=request.user)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

# create_comment : 댓글 생성
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_comment(request, book_pk, thread_pk):
    thread = get_object_or_404(Thread, pk=thread_pk)
    # request.user 를 읽어올 수 있도록 context 추가
    serializer = CommentSerializer(
        data=request.data,
        context={'request': request}
    )
    serializer.is_valid(raise_exception=True)
    # thread 와 user 를 함께 넘겨줍니다
    serializer.save(thread=thread, user=request.user)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

# create_detail : 댓글 조회 & 수정 & 삭제 (쓰레드 제목 포함)
@api_view(['GET', 'PUT', 'DELETE'])
def comment_detail(request, book_pk, thread_pk, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)

    # 조회
    if request.method == 'GET':
        serializer = CommentSerializer(comment)
        return Response(serializer.data)
    
    # 수정
    elif request.method == 'PUT':
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    
    # 삭제
    elif request.method == 'DELETE':
        comment.delete()
        return Response({'message': f'comment {comment_pk} is deleted.'}, status=status.HTTP_201_CREATED)
    



@api_view(['GET'])
def book_search(request):
   
    query = request.query_params.get('query', '').strip()
    if not query:
        return Response({'message': '검색어를 입력해 주세요'}, status=status.HTTP_400_BAD_REQUEST)
    books = Book.objects.filter(
        Q(title__icontains=query) | Q(author__icontains=query)
    )
    if not books.exists():
        return Response({'message': '검색 결과가 없습니다'}, status=status.HTTP_200_OK)
    serializer = BookListSerializer(books, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def retrieve_thread(request, thread_pk):
    thread = get_object_or_404(Thread, pk=thread_pk)
    serializer = ThreadDetailSerializer(thread, context={'request': request})
    return Response(serializer.data, status=status.HTTP_200_OK)



# 관심 정보 설정에 필요

@api_view(['GET'])
def category_list(request):
    categories = Category.objects.all()
    serializer = CategoryListSerializer(categories, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def simple_book_list(request):
    books = Book.objects.all()[:20]  
    serializer = BookListSerializer(books, many=True)
    return Response(serializer.data)


# 내 관심 장르/작가/책 기반 내가 가진 데이터 중 유사한 책 추천
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def recommend_books(request):
    user = request.user
    favorite_authors = user.favorite_authors.values_list('author', flat=True)
    favorite_books = user.favorite_books.values_list('title', flat=True)
    favorite_categories = user.favorite_topics.values_list('name', flat=True)

    all_books = Book.objects.exclude(users_who_liked=user)

    scored_books = []
    for book in all_books:
        score = 0
        if book.author in favorite_authors:
            score += 2
        if book.category.name in favorite_categories:
            score += 1
        if book.title in favorite_books:
            score += 1
        if score > 0:
            scored_books.append((book, score))

    top_books = sorted(scored_books, key=lambda x: -x[1])[:3]
    top_books_data = BookListSerializer([b[0] for b in top_books], many=True).data

    return Response(top_books_data, status=status.HTTP_200_OK)


# 책 좋아요
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def toggle_book_like(request, book_pk):
    book = get_object_or_404(Book, pk=book_pk)

    if request.method == 'GET':
        serializer = BookLikeSerializer(book, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        if not request.user.is_authenticated:
            return Response(
                {'error': '로그인이 필요합니다.'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        user = request.user
        if book.likes.filter(pk=user.pk).exists():
            book.likes.remove(user)
        else:
            book.likes.add(user)

        serializer = BookLikeSerializer(book, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)



# 책 좋아요
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def toggle_book_like(request, book_pk):
    book = get_object_or_404(Book, pk=book_pk)
    
    if request.method == 'GET':
        # GET 요청: 좋아요 정보 조회
        serializer = BookLikeSerializer(book, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        # POST 요청: 좋아요 토글 (로그인 필요)
        if not request.user.is_authenticated:
            return Response(
                {'error': '로그인이 필요합니다.'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        user = request.user
        if book.likes.filter(pk=user.pk).exists():
            book.likes.remove(user)
        else:
            book.likes.add(user)

        serializer = BookLikeSerializer(book, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])  # GET은 비로그인도 가능, POST는 로그인 필요
def toggle_thread_like(request, thread_pk):
    thread = get_object_or_404(Thread, pk=thread_pk)

    if request.method == 'GET':
        # GET 요청: 좋아요 정보 조회
        serializer = ThreadLikeSerializer(thread, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        # POST 요청: 좋아요 토글 (로그인 필요)
        if not request.user.is_authenticated:
            return Response(
                {'error': '로그인이 필요합니다.'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        user = request.user
        if thread.likes.filter(pk=user.pk).exists():
            thread.likes.remove(user)
        else:
            thread.likes.add(user)

        serializer = ThreadLikeSerializer(thread, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)



############ 별점먹이기
class BookRatingAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, book_id):
        book = Book.objects.get(pk=book_id)
        user = request.user

        # 내 평점
        try:
            r = BookRating.objects.get(user=user, book=book)
            user_score = float(r.score)
        except BookRating.DoesNotExist:
            user_score = None

        # 평균 평점
        avg = BookRating.objects.filter(book=book).aggregate(avg=Avg('score'))['avg'] or 0
        data = {
            'user_score': user_score,
            'average_score': round(avg, 1)
        }
        return Response(data)

    def post(self, request, book_id):
        book = Book.objects.get(pk=book_id)
        serializer = BookRatingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        score = serializer.validated_data['score']
        rating, created = BookRating.objects.update_or_create(
            user=request.user, book=book,
            defaults={'score': score}
        )

        # Book.customer_review_rank 갱신
        avg = BookRating.objects.filter(book=book).aggregate(avg=Avg('score'))['avg'] or 0
        book.customer_review_rank = avg
        book.save(update_fields=['customer_review_rank'])

        data = {
            'user_score': round(score, 1),
            'average_score': round(avg, 1)
        }
        return Response(data, status=status.HTTP_201_CREATED)
    


### 유사도 책 추천
class RecommendationAPIView(APIView):
    """
    POST /api/v1/recommend/embb
    """
    def post(self, request):
        embedding_str = request.data.get('embedding')
        if not embedding_str:
            return Response({'error': 'Missing embedding field.'}, status=400)

        target_vec = decode_embedding(embedding_str)
        if target_vec is None or target_vec.size == 0:
            return Response({'error': 'Invalid embedding format.'}, status=400)

        dim = target_vec.size
        similarities = []

        for book in Book.objects.only('id', 'embedding'):
            book_vec = decode_embedding(book.embedding)
            if book_vec is None or book_vec.size == 0:
                continue

            # 1) 차원 맞추기 (padding or truncate)
            if book_vec.size != dim:
                if book_vec.size < dim:
                    # 부족한 부분은 0으로 채움
                    book_vec = np.pad(book_vec, (0, dim - book_vec.size), mode='constant')
                else:
                    # 긴 부분은 잘라냄
                    book_vec = book_vec[:dim]

            # 2) 노름 계산 및 0 노름 방지
            norm_target = np.linalg.norm(target_vec)
            norm_book   = np.linalg.norm(book_vec)
            if norm_target == 0 or norm_book == 0:
                continue

            # 3) 코사인 유사도 계산
            sim = float(np.dot(target_vec, book_vec) / (norm_target * norm_book))

            # 4) “양의 유사도” 필터
            if sim > 0:
                similarities.append((sim, book))

        # 유사도가 높은 순으로 정렬 후 상위 5개
        similarities.sort(key=lambda x: x[0], reverse=True)
        top_books = [book for _, book in similarities[:5]]

        serializer = RecommendationBookSerializer(top_books, many=True)
        return Response(serializer.data)
    
    
## AI추천 목록
@api_view(['POST'])
def enhance_thread(request, book_id=None):
    """
    POST body: { "content": "원본문장..." }
    응답: { "enhancedContent": "...", "diffResult": "..." }
    """
    content = request.data.get("content", "").strip()
    if not content:
        return Response({"error": "content 필드가 필요합니다."}, status=status.HTTP_400_BAD_REQUEST)

    enhanced, diff = enhance_content(content)
    return Response({
        "enhancedContent": enhanced,
        "diffResult": diff
    })

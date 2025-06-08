from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.shortcuts import get_object_or_404

from .models import MarketPost, MarketComment
from .serializers import MarketPostSerializer, MarketCommentSerializer

# 마켓 게시글 리스트 / 생성
class MarketPostListCreateView(generics.ListCreateAPIView):
    queryset = MarketPost.objects.all().order_by('-created_at')
    serializer_class = MarketPostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'request': self.request})
        return context

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# 마켓 게시글 디테일 (조회 / 수정 / 삭제)
class MarketPostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MarketPost.objects.all()
    serializer_class = MarketPostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'request': self.request}) 
        return context

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

# 마켓 게시글 좋아요 토글
class MarketPostLikeToggleView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        post = get_object_or_404(MarketPost, pk=pk)
        if request.user in post.likes.all():
            post.likes.remove(request.user)
            liked = False
        else:
            post.likes.add(request.user)
            liked = True
        return Response({'liked': liked, 'likes_count': post.likes.count()})

# 마켓 댓글 리스트 / 생성
class MarketCommentListCreateView(generics.ListCreateAPIView):
    serializer_class = MarketCommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        market_post_pk = self.kwargs['market_post_pk']
        return MarketComment.objects.filter(market_post_id=market_post_pk).order_by('created_at')

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'request': self.request})
        return context

    def perform_create(self, serializer):
        market_post_pk = self.kwargs['market_post_pk']
        reply_to_id = self.request.data.get('reply_to')  # 대댓글 ID 받기

        serializer.save(
            user=self.request.user,
            market_post_id=market_post_pk,
            reply_to_id=reply_to_id  
        )

# 마켓 댓글 디테일 (조회 / 수정 / 삭제)
class MarketCommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MarketComment.objects.all()
    serializer_class = MarketCommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'request': self.request})
        return context

# 마켓 댓글 좋아요 토글
class MarketCommentLikeToggleView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        comment = get_object_or_404(MarketComment, pk=pk)
        if request.user in comment.likes.all():
            comment.likes.remove(request.user)
            liked = False
        else:
            comment.likes.add(request.user)
            liked = True

        return Response({'liked': liked, 'likes_count': comment.likes.count()})

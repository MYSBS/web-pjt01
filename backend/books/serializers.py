from rest_framework import serializers 
from .models import Book, Comment, Category, Thread, BookRating

# 
class ThreadTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Thread
        fields = ('title',)

class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name',)

class BookListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('id', 'title', 'author', 'isbn', 'cover', 'category', 'pub_date', 'publisher', 'subTitle')

class BookTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('title',)

class BookSerializer(serializers.ModelSerializer):
    class ThreadDetailSerializer(serializers.ModelSerializer):
        class Meta:
            model = Thread
            fields = ('id', 'title', 'content', 'reading_date',)

    category = CategoryListSerializer(read_only=True)
    threads = ThreadDetailSerializer(many=True, read_only=True)
    num_of_threads = serializers.SerializerMethodField()
    class Meta:
        model = Book
        fields = (
            'id', 'category', 'threads', 'num_of_threads',
            'title', 'description', 'isbn', 'cover',
            'publisher', 'pub_date', 'author', 'author_info', 'author_photo', 'customer_review_rank',
            'keywords', 'embedding',
        )

    def get_num_of_threads(self, obj):
        return obj.threads.count()

# 책에 관한 좋아요
class BookLikeSerializer(serializers.ModelSerializer):
    likes_count = serializers.IntegerField(source='likes.count', read_only=True)
    liked       = serializers.SerializerMethodField()
    
    class Meta:
        model = Book
        fields = ('id', 'likes_count', 'liked')

    def get_liked(self, obj):
        user = self.context['request'].user
        # 비로그인 사용자는 항상 False 반환
        if not user.is_authenticated:
            return False
        return obj.likes.filter(pk=user.pk).exists()



class CommentSerializer(serializers.ModelSerializer):
    thread = ThreadTitleSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'thread', 'content', 'created_at', 'updated_at',)
        extra_kwargs = {
            'thread': {'read_only': True},
        }

class ThreadListSerializer(serializers.ModelSerializer):
    class BookAllSerializer(serializers.ModelSerializer):
        class Meta:
            model = Book
            fields = '__all__'  # 또는 원하는 필드 명시

    book = BookAllSerializer(read_only=True)  # 전체 Book 직렬화

    class Meta:
        model = Thread
        fields = '__all__'  # 또는 ('id', 'title', 'content', 'book', ...)



class ThreadSerializer(serializers.ModelSerializer):
    class BookMiniSerializer(serializers.ModelSerializer):
        class Meta:
            model =Book
            fields = '__all__'
            read_only_fields = ['user', 'created_at', 'updated_at']
    
    class CommentDeatilSerializer(serializers.ModelSerializer):

        thread = ThreadTitleSerializer(read_only=True)

        class Meta:
            model = Comment
            fields = ('id', 'thread', 'content', 'created_at', 'updated_at','user')

    book = BookMiniSerializer(read_only=True)
    comments = CommentDeatilSerializer(read_only=True, many=True)
    num_of_comments = serializers.SerializerMethodField()
    class Meta:
        model = Thread
        # fields = ('id', 'book', 'comments', 'num_of_comments', 'title', 'content', 'reading_date', 'created_at', 'updated_at',)
        fields = '__all__'
        

    def get_num_of_comments(self, obj):
        # 여기서 obj는 특정 게시글 인스턴스 (3번 게시글이면 3번객체, ...)
        # view 함수에서 annoate 해서 생긴 새로운 속성 결과를 사용할 수 있게 됨
        return obj.num_of_comments

class ThreadCreateSerializer(serializers.ModelSerializer):
    cover_img = serializers.ImageField(required=False)
    user      = serializers.HiddenField(default=serializers.CurrentUserDefault())
    book      = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Thread
        fields = (
            'id', 'book', 'user',
            'title', 'content', 'reading_date', 'cover_img',
            'created_at', 'updated_at',
        )
        read_only_fields = ('id', 'created_at', 'updated_at')
        
class ThreadDetailSerializer(serializers.ModelSerializer):
    class ThreadLikeSerializer(serializers.ModelSerializer):
        likes_count = serializers.IntegerField(source='likes.count', read_only=True)
        liked       = serializers.SerializerMethodField()
        class Meta:
            model = Thread
            fields = ('id', 'likes_count', 'liked')

        def get_liked(self, obj):
            user = self.context['request'].user
            return user.is_authenticated and obj.likes.filter(pk=user.pk).exists()
    
    # nested object 대신 PK만
    book = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Thread
        fields = ('id', 'book', 'title', 'content', 'reading_date', 'cover_img', 'created_at', 'updated_at')


class ThreadLikeSerializer(serializers.ModelSerializer):
    likes_count = serializers.IntegerField(source='likes.count', read_only=True)
    liked       = serializers.SerializerMethodField()
    
    class Meta:
        model = Thread
        fields = ('id', 'likes_count', 'liked')

    def get_liked(self, obj):
        user = self.context['request'].user
        # 비로그인 사용자는 항상 False 반환
        if not user.is_authenticated:
            return False
        return obj.likes.filter(pk=user.pk).exists()
    
    ## 별점 등록 수정을 위한 시리얼라이저
class BookRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookRating
        fields = ['score']

class BookRatingInfoSerializer(serializers.Serializer):
    user_score = serializers.FloatField(allow_null=True)
    average_score = serializers.FloatField()



### 임베딩 직렬화를 위한 시리얼 라이져

class RecommendationBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('id', 'title', 'cover', 'keywords', 'author')
        
        
### 홈페이지를 위한 임시 씨리얼 라이저
class ThreadHomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Thread
        fields = '__all__'
        
class BookHomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        exclude = ('embedding',)

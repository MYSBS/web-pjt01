from rest_framework import serializers
from .models import MarketPost, MarketComment
from books.models import Book
from accounts.models import User  # 작성자 정보

# 책 정보를 보여주기 위한 Book Serializer (간략 버전)
class BookSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('id', 'title', 'author', 'cover')


# 작성자 정보 (프로필 사진 포함)
class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'profile_img')


# 마켓 게시글 Serializer
class MarketPostSerializer(serializers.ModelSerializer):
    book = BookSimpleSerializer(read_only=True)
    book_id = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all(), source='book', write_only=True)
    user = AuthorSerializer(read_only=True)
    likes_count = serializers.IntegerField(source='likes.count', read_only=True)
    comments_count = serializers.IntegerField(source='comments.count', read_only=True)
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = MarketPost
        fields = (
            'id', 'status', 'title', 'content', 'price', 'image',
            'created_at', 'book', 'book_id', 'user',
            'likes_count', 'comments_count', 'is_liked', 'latitude', 'longitude',
        )

    def get_is_liked(self, obj):
        user = self.context.get('request').user
        return user.is_authenticated and obj.likes.filter(id=user.id).exists()


# 댓글 Serializer
class MarketCommentSerializer(serializers.ModelSerializer):
    user = AuthorSerializer(read_only=True)
    likes_count = serializers.IntegerField(source='likes.count', read_only=True)
    is_liked = serializers.SerializerMethodField()
    likes_users = serializers.SerializerMethodField()

    class Meta:
        model = MarketComment
        fields = (
            'id', 'market_post', 'content', 'user', 'created_at',
            'likes_count', 'is_liked', 'reply_to', 'likes_users',
        )
        read_only_fields = ('market_post',)

    def get_is_liked(self, obj):
        user = self.context.get('request').user
        return user.is_authenticated and obj.likes.filter(id=user.id).exists()

    def get_likes_users(self, obj):
        return list(obj.likes.values_list('id', flat=True))
    

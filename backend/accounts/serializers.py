from rest_framework import serializers
from django.templatetags.static import static
from django.contrib.auth import get_user_model
from dj_rest_auth.registration.serializers import RegisterSerializer
from .models import User, UserRecommendation
from books.models import Book, Category
from books.serializers import BookListSerializer, CategoryListSerializer

User = get_user_model()

class BookSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('id', 'title', 'author')

class CategorySummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')

class CustomUserSerializer(serializers.ModelSerializer):
    profile_img = serializers.SerializerMethodField()

    favorite_authors = BookSummarySerializer(many=True, read_only=True)
    favorite_topics = CategorySummarySerializer(many=True, read_only=True)
    favorite_books = BookSummarySerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = (
            'id', 'username', 'age', 'gender',
            'weekly_avg_reading_time', 'annual_reading_amount',
            'profile_img', 'interested_genres',
            'favorite_authors', 'favorite_topics', 'favorite_books'
        )

    def get_profile_img(self, obj):
        request = self.context.get('request')
        if obj.profile_img:
            return request.build_absolute_uri(obj.profile_img.url)
        return request.build_absolute_uri(static('img/user_profile/default.png'))

    def update(self, instance, validated_data):
        instance.age = validated_data.get('age', instance.age)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.weekly_avg_reading_time = validated_data.get('weekly_avg_reading_time', instance.weekly_avg_reading_time)
        instance.annual_reading_amount = validated_data.get('annual_reading_amount', instance.annual_reading_amount)
        instance.profile_img = validated_data.get('profile_img', instance.profile_img)

        if 'favorite_authors' in validated_data:
            instance.favorite_authors.set(validated_data['favorite_authors'][:3])
        if 'favorite_topics' in validated_data:
            instance.favorite_topics.set(validated_data['favorite_topics'][:3])
        if 'favorite_books' in validated_data:
            instance.favorite_books.set(validated_data['favorite_books'][:3])

        instance.save()
        return instance

class CustomRegisterSerializer(RegisterSerializer):
    gender = serializers.CharField(required=False)
    age = serializers.IntegerField(required=False)
    weekly_avg_reading_time = serializers.IntegerField(required=False)
    annual_reading_amount = serializers.IntegerField(required=False)
    profile_img = serializers.ImageField(required=False)
    interested_genres = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=User._meta.get_field('interested_genres').remote_field.model.objects.all(),
        required=False
    )

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data['gender'] = self.validated_data.get('gender', '')
        data['age'] = self.validated_data.get('age', None)
        data['weekly_avg_reading_time'] = self.validated_data.get('weekly_avg_reading_time', None)
        data['annual_reading_amount'] = self.validated_data.get('annual_reading_amount', None)
        data['profile_img'] = self.validated_data.get('profile_img', None)
        data['interested_genres'] = self.validated_data.get('interested_genres', [])
        return data

    def save(self, request):
        user = super().save(request)
        cleaned_data = self.get_cleaned_data()

        user.gender = cleaned_data.get('gender', '')
        user.age = cleaned_data.get('age')
        user.weekly_avg_reading_time = cleaned_data.get('weekly_avg_reading_time')
        user.annual_reading_amount = cleaned_data.get('annual_reading_amount')
        user.profile_img = cleaned_data.get('profile_img')
        user.save()

        return user

class UserRecommendationSerializer(serializers.ModelSerializer):
    recommended_books = BookListSerializer(many=True, read_only=True)

    class Meta:
        model = UserRecommendation
        fields = ['id', 'recommended_books', 'created_at']

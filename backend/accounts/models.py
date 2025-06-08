from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from books.models import Category, Book

from django.core.files import File
from django.conf import settings  # static_img_path 만들 때 필요
import os


class User(AbstractUser):
    # 성별
    GENDER_CHOICES = (
        ('M', '남성'),
        ('F', '여성'),
    )
    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        blank=True,
        null=True,
    )

    # 나이
    age = models.PositiveIntegerField(
        blank=True,
        null=True,
    )

    # 주간 평균 독서 시간
    weekly_avg_reading_time = models.PositiveIntegerField(
        blank=True,
        null=True,
    )

    # 연간 독서량
    annual_reading_amount = models.PositiveIntegerField(
        blank=True,
        null=True,
    )

    # 프로필 사진
    profile_img = models.ImageField(
        upload_to='user_profile_img/',
        blank=True,
        null=True,
    )

    # 관심 장르 (다중 선택, M:N 관계)
    interested_genres = models.ManyToManyField(
        Category,
        blank=True,
        related_name="users",
    )

    # 팔로잉
    followings = models.ManyToManyField(
        'self', symmetrical=False, related_name='followers'
    )

    # 좋아하는 작가
    favorite_authors = models.ManyToManyField(
        Book, related_name='fans_of_author', blank=True
    )

    # 좋아하는 주제
    favorite_topics = models.ManyToManyField(
        Category, related_name='interested_users', blank=True
    )

    # 좋아하는 책
    favorite_books = models.ManyToManyField(
        Book, related_name='users_who_liked', blank=True
    )

    def save(self, *args, **kwargs):
        # 새로 생성된 사용자이고 이미지가 없는 경우
        if not self.pk or not self.profile_img:
            static_img_path = os.path.join(settings.BASE_DIR, 'static', 'img', 'user_profile', 'default.png')
            media_img_path = os.path.join(settings.MEDIA_ROOT, 'user_profile_img', 'default_copy.png')

            # media 폴더에 복사된 디폴트 이미지가 없으면 복사
            if not os.path.exists(media_img_path):
                os.makedirs(os.path.dirname(media_img_path), exist_ok=True)
                with open(static_img_path, 'rb') as src_file:
                    with open(media_img_path, 'wb') as dst_file:
                        dst_file.write(src_file.read())

            # self.profile_img가 비어있다면 복사된 파일을 이미지 필드에 넣음
            if not self.profile_img:
                with open(media_img_path, 'rb') as f:
                    self.profile_img.save('default_copy.png', File(f), save=False)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.username


class UserRecommendation(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='recommendation'
    )

    # 추천된 책 (Book 객체와 연결)
    recommended_books = models.ManyToManyField(
        Book,
        related_name='recommended_to_users'
    )

    # GPT 응답 전체 (책 id, title, author, cover, similarity_reason, recommend_reason 포함)
    reasons = models.JSONField(default=list)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}님의 추천 도서"
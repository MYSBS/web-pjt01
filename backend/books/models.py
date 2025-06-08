import datetime
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from .utils import extract_keywords, get_embedding
import struct


class Category(models.Model):
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name


class Book(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, related_name='books'
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    isbn = models.CharField(max_length=20)
    cover = models.URLField()  
    publisher = models.CharField(max_length=100)
    pub_date = models.DateField()
    author = models.CharField(max_length=100)
    author_info = models.TextField()
    author_photo = models.URLField()  
    customer_review_rank = models.FloatField()
    subTitle = models.CharField(max_length=100)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="liked_books", blank=True)
    keywords = models.JSONField(default=list)  # 추출된 키워드 저장
    embedding = models.BinaryField(null=True)

    def save(self, *args, **kwargs):
        if self.description:
            # 키워드 추출
            self.keywords = extract_keywords(self.description)

            # 임베딩 저장 (Binary로)
            embedding_vector = get_embedding(self.description)
            self.embedding = struct.pack(f'{len(embedding_vector)}f', *embedding_vector)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Thread(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    reading_date = models.DateField(default=datetime.date.today)
    cover_img = models.ImageField(upload_to="thread_cover_img/", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='threads')
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="liked_threads", blank=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='userthreads'
    )

    def __str__(self):
        return self.title
    
class Comment(models.Model):
    content = models.CharField(max_length=100)
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content
    


class BookRating(models.Model):
    user       = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    book       = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='ratings')
    score      = models.DecimalField(
        max_digits=2,           # e.g. “5.0”
        decimal_places=1,       # 소수점 1자리
        validators=[
            MinValueValidator(0.5),
            MaxValueValidator(5.0)
        ]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  # 수정 이력 추적

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'book'], name='unique_user_book_rating')
        ]
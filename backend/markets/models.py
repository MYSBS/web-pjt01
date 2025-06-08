from django.db import models
from django.conf import settings
from books.models import Book

class MarketPost(models.Model):
    STATUS_CHOICES = (
        ('판매중', '판매중'),
        ('판매완료', '판매완료'),
        ('예약중', '예약중'),
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='판매중')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='market_posts')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='market_posts')
    title = models.CharField(max_length=100)
    content = models.TextField()
    price = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='market_post_images/', blank=True, null=True)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_market_posts', blank=True)
    latitude = models.FloatField(null=True, blank=True)   # 위도
    longitude = models.FloatField(null=True, blank=True)  # 경도

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class MarketComment(models.Model):
    market_post = models.ForeignKey(MarketPost, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField(max_length=300)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_market_comments', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    reply_to = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')

    def __str__(self):
        return f"{self.user.username}의 댓글"

from django.contrib import admin
from .models import Book, Thread, Comment, BookRating

# Register your models here.
admin.site.register(Book)
admin.site.register(Thread)
admin.site.register(Comment)
admin.site.register(BookRating)
## 테스트

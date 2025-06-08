from django.urls import path
from . import views


app_name = "books"
urlpatterns = [
    path('home/', views.home_data),
    path('books/', views.book_list),
    path('books/<int:book_pk>/', views.book_detail),
    path('threads/', views.thread_list),
    path('books/<int:book_pk>/threads/<int:thread_pk>/', views.thread_detail),
    path('books/<int:book_pk>/threads/', views.create_thread),
    path('books/<int:book_pk>/threads/<int:thread_pk>/comment/', views.create_comment),
    path('books/<int:book_pk>/threads/<int:thread_pk>/comment/<int:comment_pk>/', views.comment_detail),  
    path('books/<int:book_pk>/like/', views.toggle_book_like),
    path('books/search/', views.book_search),  
    # 신규 독립 조회용
    path('threads/<int:thread_pk>/', views.retrieve_thread),
    path('threads/<int:thread_pk>/like/', views.toggle_thread_like),

    # 관심정보 설정에 필요
    path('categories/', views.category_list, name='category-list'), 
    path('books/simple/', views.simple_book_list, name='simple-book-list'),

    ## 별점먹이기
    path('books/<int:book_id>/rating/', views.BookRatingAPIView.as_view(), name='book-rating'),
    
    # 추천도서에 필요 (관심 장르/책/작가 기반) 
    path('recommend/', views.recommend_books, name='recommend-books'),
    
    path('recommend/embb', views.RecommendationAPIView.as_view(), name='recommend-emb'),
    # 글쓰기 ai보완
    path('books/<int:book_id>/enhance/', views.enhance_thread, name='enhance-thread'),
]

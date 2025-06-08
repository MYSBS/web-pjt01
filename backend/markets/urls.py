from django.urls import path
from . import views

urlpatterns = [
    # 마켓 게시글
    path('', views.MarketPostListCreateView.as_view(), name='market_list_create'),
    path('<int:pk>/', views.MarketPostDetailView.as_view(), name='market_detail'),

    # 게시글 좋아요 토글
    path('<int:pk>/like/', views.MarketPostLikeToggleView.as_view(), name='market_like'),

    # 댓글
    path('<int:market_post_pk>/comments/', views.MarketCommentListCreateView.as_view(), name='market_comment_list_create'),
    path('comments/<int:pk>/', views.MarketCommentDetailView.as_view(), name='market_comment_detail'),
    
    # 댓글 좋아요 토글
    path('comments/<int:pk>/like/', views.MarketCommentLikeToggleView.as_view(), name='market_comment_like'),
]

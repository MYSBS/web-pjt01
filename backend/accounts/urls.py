from django.urls import path
from . import views
from django.urls import include

app_name = 'accounts'
urlpatterns = [
    # Vue용 API
    path('recommend/gpt/', views.recommend_gpt_books, name='gpt_book_recommendation'),
    
    path('', include('dj_rest_auth.urls')),  # 로그인/로그아웃
    path('signup/', include('dj_rest_auth.registration.urls')),  # 회원가입
    path('profile/update/', views.update_profile, name='update_profile'),
    path('password/update/', views.update_password, name='update_password'),
    path('profile/<int:user_pk>/follow/', views.follow, name='follow'),
    
    # userId 숫자를 기준으로 username을 받아올 엔드포인트
    path('profile/getusername/<int:user_pk>/', views.get_user_name, name='get_user_name'),
    
    # 맨 아래로 유지
    path('profile/<str:username>/', views.profile, name='profile'),
    path('delete/', views.delete_account, name='delete_account'),
]

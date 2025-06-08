from django.http.response import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.views.decorators.http import (require_http_methods,require_POST)
from django.views.decorators.csrf import csrf_exempt

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .serializers import CustomUserSerializer
from books.serializers import BookListSerializer, ThreadListSerializer
from books.models import Book
from .utils import build_recommend_prompt, call_gpt_api, parse_gpt_response
from .models import UserRecommendation

from rest_framework.decorators import api_view, permission_classes, parser_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
import os
from django.core.files.base import File
from django.conf import settings


User = get_user_model()

@require_http_methods(["GET", "POST"])
def login(request):
    if request.user.is_authenticated:
        return redirect('books:index')

    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('books:index')
    else:
        form = AuthenticationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/login.html', context)


@require_POST
def logout(request):
    auth_logout(request)
    return redirect('books:index')


def signup(request):
    if request.user.is_authenticated:
        return redirect('books:index')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            selected_categories = form.cleaned_data.get('interested_genres')
            if selected_categories:
                user.interested_genres.set(selected_categories)
            auth_login(request, user)
            return redirect('books:index')
    else:
        form = CustomUserCreationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/signup.html', context)

@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def profile(request, username):
    person = get_object_or_404(User, username=username)
    serializer = CustomUserSerializer(person, context={'request': request})

    data = serializer.data
    data['follower_count'] = person.followers.count()
    data['following_count'] = person.followings.count()

    if request.user.is_authenticated and request.user != person:
        data['is_followed'] = person.followers.filter(pk=request.user.pk).exists()
    else:
        data['is_followed'] = False

    data['liked_books'] = BookListSerializer(person.liked_books.all(), many=True, context={'request': request}).data
    data['liked_threads'] = ThreadListSerializer(person.liked_threads.all(), many=True, context={'request': request}).data

    return Response(data, status=status.HTTP_200_OK)


@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_password(request):
    user = request.user
    current_password = request.data.get('current_password')
    new_password = request.data.get('new_password')

    if not user.check_password(current_password):
        return Response({'detail': '현재 비밀번호가 올바르지 않습니다. 다시 시도해주세요.'}, status=status.HTTP_400_BAD_REQUEST)

    # if not new_password or len(new_password) < 6:
    #     return Response({'detail': '새 비밀번호는 6자 이상이어야 합니다.'}, status=status.HTTP_400_BAD_REQUEST)

    user.set_password(new_password)
    user.save()
    update_session_auth_hash(request, user)  # 로그인 유지

    return Response({'detail': '비밀번호가 성공적으로 변경되었습니다.'}, status=status.HTTP_200_OK)



# @login_required
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def follow(request, user_pk):
    User = get_user_model()
    person = User.objects.get(pk=user_pk)
    if person != request.user:
        if person.followers.filter(pk=request.user.pk).exists():
            person.followers.remove(request.user)
            is_follow = False
        else:
            person.followers.add(request.user)
            is_follow = True
    context = {
        # 현재 팔로우 여부
        'is_follow': is_follow,
        # person의 팔로워 수
        'follower_count': person.followers.count()
    }
    # context 정보를 JSON으로 바꿔서 반환 -> django가 지원 import
    return Response(context, status=status.HTTP_200_OK)


'''
Vue는 SPA라서 Django의 기본 CSRF 흐름과 맞지 않음
기본적으로 Django는 SessionAuthentication을 쓸 때 CSRF를 검사함
'''
@csrf_exempt
@api_view(['PUT'])
@authentication_classes([TokenAuthentication]) 
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def update_profile(request):
    user = request.user

    # 프로필 이미지 처리 
    if request.data.get('reset_profile') == 'true':
        # static 에 있는 기본 이미지를 media 로 복사
        static_path = os.path.join(settings.BASE_DIR, 'statics', 'img', 'user_profile', 'default.png')
        media_path = os.path.join(settings.MEDIA_ROOT, 'user_profile_img', f'default_{user.pk}.png')

        # media에 복사 (없을 경우)
        if not os.path.exists(media_path):
            os.makedirs(os.path.dirname(media_path), exist_ok=True)
            with open(static_path, 'rb') as src, open(media_path, 'wb') as dst:
                dst.write(src.read())

        # 유저의 프로필 이미지 덮어쓰기
        with open(media_path, 'rb') as f:
            user.profile_img.save(f'default_{user.pk}.png', File(f), save=False)

    else:
        if request.FILES.get('profile_img'):
            user.profile_img = request.FILES.get('profile_img')

    user.age = request.data.get('age')
    user.weekly_avg_reading_time = request.data.get('weekly_avg_reading_time')
    user.annual_reading_amount = request.data.get('annual_reading_amount')
    user.save()

    serializer = CustomUserSerializer(user, data=request.data, context={'request': request}, partial=True)
    if serializer.is_valid():
        serializer.save()

        # M2M 필드 직접 set 해주기
        user.favorite_authors.set(request.data.getlist('favorite_authors'))
        user.favorite_topics.set(request.data.getlist('favorite_topics'))
        user.favorite_books.set(request.data.getlist('favorite_books'))

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_user_name(request, user_pk):
    person = get_object_or_404(User, pk=user_pk)
    profile_url = person.profile_img.url if person.profile_img else None
    return Response(
        {'username': person.username,
        'profile_img': profile_url},
        status=status.HTTP_200_OK
    )


@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_account(request):
    user = request.user
    password = request.data.get('password')

    if not password:
        return Response({'detail': '비밀번호를 입력해주세요.'}, status=status.HTTP_400_BAD_REQUEST)

    if not user.check_password(password):
        return Response({'detail': '비밀번호가 틀렸습니다. 다시 시도해주세요.'}, status=status.HTTP_400_BAD_REQUEST)

    user.delete()
    return Response({'detail': '회원 탈퇴가 완료되었습니다.'}, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def recommend_gpt_books(request):
    user = request.user

    has_interest = (
        user.favorite_books.exists() or
        user.favorite_authors.exists() or
        user.favorite_topics.exists()
    )

    if not has_interest:
        return Response({'status': 'no_interest'}, status=status.HTTP_200_OK)

    if request.method == 'GET':
        if hasattr(user, 'recommendation'):
            rec = user.recommendation
            return Response({'status': 'exists', 'recommendations': rec.reasons}, status=status.HTTP_200_OK)
        else:
            return Response({'status': 'no_recommend'}, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        prompt = build_recommend_prompt(user)
        result = call_gpt_api(prompt)
        parsed = parse_gpt_response(result)

        books = []
        response_data = []

        for item in parsed:
            book = Book.objects.filter(pk=item['id']).first()
            if book:
                books.append(book)
                cover_url = book.cover if book.cover else ''
                response_data.append({
                    'id': book.id,
                    'title': book.title,
                    'author': book.author,
                    'cover': cover_url,
                    'recommend_reason': item.get('recommend_reason'),
                    'similarity_reason': item.get('similarity_reason')
                })

        if hasattr(user, 'recommendation'):
            rec = user.recommendation
            rec.recommended_books.set(books)
            rec.reasons = response_data
            rec.save()
        else:
            rec = UserRecommendation.objects.create(user=user, reasons=response_data)
            rec.recommended_books.set(books)

        return Response({'status': 'updated', 'recommendations': response_data}, status=status.HTTP_200_OK)
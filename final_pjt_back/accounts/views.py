from django.shortcuts import render
from .serializers import ProfileSerializer

from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.http import JsonResponse
from django.contrib.auth.models import User


# Create your views here.
User = get_user_model()


@api_view(['GET', 'POST'])
def profile_follow(request, username):
    # 팔로우할 유저
    user = get_object_or_404(User, username=username)
    # GET 요청시 프로파일 보여주기
    print('팔로우할 유저', user)
    print('로그인유저',  request.user)
    if request.method == 'GET':
        serializer = ProfileSerializer(user)
        return Response(serializer.data)
    # POST 요청시 팔로우 기능 사용
    elif request.method == 'POST':

        # 나 자신에게는 팔로우 차단
        if user != request.user:

            # 이전에 팔로후했다면 제거
            print('post까지가능', username)
            print(user.followers.filter(username=request.user).exists())
            if user.followers.filter(username=request.user).exists():
                user.followers.remove(request.user)
                print('언팔로우')
                follow = True
            else:
                print('post까지가능', username)
                # 팔로우하기
                user.followers.add(request.user)
                follow = False
            serializer = ProfileSerializer(user)
            return Response(serializer.data)


def check_username_availability(username):
    try:
        # 사용자 이름으로 데이터베이스 조회
        user = User.objects.get(username=username)
        # 중복된 아이디가 존재하는 경우
        print(username)
        return False
    except User.DoesNotExist:
        # 중복된 아이디가 존재하지 않는 경우
        return True


def profile_view(request, username):
    # username을 사용하여 아이디 중복 여부 등을 확인하는 로직을 작성합니다.
    # 예시로서 isAvailable 값만 반환하도록 작성합니다.
    is_available = check_username_availability(username)
    data = {
        'isAvailable': is_available,
    }
    return JsonResponse(data)

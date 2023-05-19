from django.shortcuts import render
from .serializers import ProfileSerializer

from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from rest_framework.decorators import api_view
from rest_framework.response import Response

# Create your views here.
User = get_user_model()


@api_view(['GET', 'POST'])
def profile_follow(request, username):
    user = get_object_or_404(User, username=username)
    # GET 요청시 프로파일 보여주기
    if request.method == 'GET':
        serializer = ProfileSerializer(user)
        return Response(serializer.data)
    # POST 요청시 팔로우 기능 사용
    elif request.method == 'POST':
        # 나 자신에게는 팔로우 차단
        if user != request.user:
            # 이전에 팔로후했다면 제거
            if user.followers.filter(pk=user.pk).exists():
                user.followers.remove(request.user)
                follow = True
            else:
                # 팔로우하기
                user.followers.add(request.user)
                follow = False
            serializer = ProfileSerializer(user)
        return Response(serializer.data)

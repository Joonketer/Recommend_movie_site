"""final_pjt_back URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path, include
from . import views

app_name = 'boards'

urlpatterns = [
    path("boards/", views.index, name="board_list"),    # 전체 게시글
    path("boards/<int:board_pk>/", views.board_detail,
         name="board_detail"),    # 단일 게시글 조회, 삭제, 수정
    path('boards/<int:board_pk>/like/', views.board_like),  # 게시글 좋아요


    path("comments/", views.comment_list, name="comment_list"),  # 전체 댓글
    path("comments/<int:board_pk>/comments/",
         views.comment_create, name="comment_create"),  # 댓글 생성
    path("comments/<int:comment_pk>/",
         views.comment_detail, name="comment_detail"),  # 단일 댓글 조회, 삭제, 수정
    path('comments/<int:comment_pk>/like/', views.comment_like),  # 댓글 좋아요

]

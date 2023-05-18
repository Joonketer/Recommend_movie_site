from django.db import models
from django.conf import settings
# Create your models here.


class Board(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,  # 게시글 작성한 유저
                             on_delete=models.CASCADE)
    like_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='like_boards', blank=True, null=True)   # 좋아요한 사람들
    title = models.CharField(max_length=100)    # 제목
    board_type = models.IntegerField(default=0)  # 말머리(기본값 0 : 자유게시판)
    content = models.TextField()    # 내용
    created_at = models.DateTimeField(auto_now_add=True)    # 생성일
    updated_at = models.DateTimeField(auto_now=True)    # 수정일


class Comment(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE)  # 어떤 게시글인지
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)  # 댓글 작성한 유저
    content = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)    # 생성일
    updated_at = models.DateTimeField(auto_now=True)    # 수정일

    def __str__(self):
        return self.content

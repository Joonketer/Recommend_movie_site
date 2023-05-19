from rest_framework import serializers
from boards.models import Board, Comment
from django.contrib.auth import get_user_model


class ProfileSerializer(serializers.ModelSerializer):

    class BoardSerializer (serializers.ModelSerializer):
        class Meta:
            model = Board
            # 게시글번호, 타입, 제목, 내용
            fields = ('id', 'board_type', 'title', 'content')
    like_boards = BoardSerializer(many=True)
    boards = BoardSerializer(many=True)

    class CommentSerializer (serializers.ModelSerializer):
        class Meta:
            model = Comment
            # 댓글 번호, 게시글, 내용
            fields = ('id', 'board' 'content')
    like_comments = CommentSerializer(many=True)
    comments = CommentSerializer(many=True)

    # 프로필에서 보여야할 것들
    # pk값, id, 이메일, 이름, 성, 팔로잉한 사람, 팔로우한 사람,
    # 좋아요 누른 게시글, 좋아요 받은 게시글, 좋아요한 댓글,
    # 좋아요 받은 댓글
    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'followings', 'followers',
                  'like_boards', 'boards', 'like_comments', 'comments',)

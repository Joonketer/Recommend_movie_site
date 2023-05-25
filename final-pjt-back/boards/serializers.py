from rest_framework import serializers
from .models import Board, Comment
from django.contrib.auth import get_user_model


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('username', )


# 모든 게시글


class BoardListSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Board
        fields = '__all__'

# 상세 게시글


class BoardSerializer(serializers.ModelSerializer):
    # 댓글에서 가져올 것들
    class CommentSerializer(serializers.ModelSerializer):
        user = UserSerializer(read_only=True)

        class Meta:
            model = Comment
            fields = ('id', 'user', 'content', 'created_at',
                      'updated_at', 'like_users')
    comments = CommentSerializer(many=True, read_only=True)
    user = UserSerializer(read_only=True)
    like_users = UserSerializer(read_only=True, many=True)

    class Meta:
        model = Board
        fields = '__all__'

# 모든 댓글


class CommentListSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'

# 단일 댓글


class CommentSerializer(serializers.ModelSerializer):
    class BoardSerializer(serializers.ModelSerializer):
        class Meta:
            model = Board
            fields = ('id', 'title', )
    board = BoardSerializer(read_only=True)
    user = UserSerializer(read_only=True)
    like_users = UserSerializer(read_only=True, many=True)

    class Meta:
        model = Comment
        fields = '__all__'

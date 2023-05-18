from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.decorators import api_view

from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

from rest_framework import status
from django.shortcuts import get_object_or_404, get_list_or_404

from .models import Board, Comment
from .serializers import BoardListSerializer, BoardSerializer, CommentListSerializer, CommentSerializer
# Create your views here.


@api_view(['GET', 'POST'])
def index(reqeust):
    # 모든 게시글
    if reqeust.method == 'GET':
        boards = Board.objects.all()
        serializer = BoardListSerializer(boards, many=True)
        return Response(serializer.data)
    # 게시글 생성
    elif reqeust.method == 'POST':
        serializer = BoardSerializer(data=reqeust.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=reqeust.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'DELETE', 'PUT'])
def board_detail(request, board_pk):
    board = get_object_or_404(Board, pk=board_pk)
    # 단일 게시글 보여주기
    if request.method == 'GET':
        serializer = BoardSerializer(board)
        return Response(serializer.data)
    # 게시글 삭제
    elif request.method == 'DELETE':
        board.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    # 게시글 수정
    elif request.method == 'PUT':
        serializer = BoardSerializer(board, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)


@api_view(['GET'])
def comment_list(reqeust):

    # 모든 댓글
    comments = Comment.objects.all()
    serializer = CommentListSerializer(comments, many=True)
    return Response(serializer.data)

# 게시글 생성


@api_view(['POST'])
def comment_create(reqeust, board_pk):
    # 게시글 가져오기
    board = get_object_or_404(Board, pk=board_pk)

    # 댓글 작성

    serializer = CommenntSerializer(data=reqeust.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(board=board, user=reqeust.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'DELETE', 'PUT'])
def comment_detail(request, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    # 단일 댓글 보여주기
    if request.method == 'GET':
        serializer = CommentSerializer(comment)
        return Response(serializer.data)
    # 댓글 삭제
    elif request.method == 'DELETE':
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    # 댓글 수정
    elif request.method == 'PUT':
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

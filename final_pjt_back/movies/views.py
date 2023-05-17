from django.shortcuts import render
from .models import Movie

from rest_framework.response import Response
from rest_framework.decorators import api_view

from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

from rest_framework import status
from django.shortcuts import get_object_or_404, get_list_or_404
from .serializers import MovieListSerializer, MovieSerializer
# Create your views here.


@api_view(['GET', 'POST'])
# @permission_classes([IsAuthenticated])
def movie_list(request):
    if request.method == 'GET':
        # movies = movie.objects.all()
        movies = get_list_or_404(Movie)
        serializer = MovieListSerializer(movies, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = MovieSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            # serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'DELETE', 'PUT'])
def movie_detail(request, movie_pk):
    # movie = Movie.objects.get(pk=movie_pk)
    movie = get_object_or_404(movie, pk=movie_pk)

    if request.method == 'GET':
        serializer = MovieSerializer(movie)
        print(serializer.data)
        return Response(serializer.data)

    elif request.method == 'DELETE':
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    elif request.method == 'PUT':
        serializer = MovieSerializer(movie, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

from django.shortcuts import render
from .models import Movie, Review, Photo

from rest_framework.response import Response
from rest_framework.decorators import api_view

from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

from rest_framework import status
from django.shortcuts import get_object_or_404, get_list_or_404
from .serializers import MovieListSerializer, MovieSerializer, ReviewListSerializer, ReviewSerializer, PhotoSerializer

from django.db.models import Q
# Create your views here.

# 전체 영화


@api_view(['GET',])
# @permission_classes([IsAuthenticated])
def movie_list(request):
    if request.method == 'GET':
        # movies = movie.objects.all()
        movies = get_list_or_404(Movie)
        serializer = MovieListSerializer(movies, many=True)
        # print(serializer.data)
        return Response(serializer.data)

# 영화 상세


@api_view(['GET'])
def movie_detail(request, movie_pk):
    # movie = Movie.objects.get(pk=movie_pk)
    movie = get_object_or_404(Movie, pk=movie_pk)

    if request.method == 'GET':
        serializer = MovieSerializer(movie)
        return Response(serializer.data)

# 전체 리뷰


@api_view(['GET'])
def review_list(request):
    if request.method == 'GET':
        # reviews = review.objects.all()
        reviews = get_list_or_404(Review)
        serializer = ReviewListSerializer(reviews, many=True)
        return Response(serializer.data)

# 상세 리뷰


@api_view(['GET', 'DELETE', 'PUT'])
def review_detail(request, review_pk):
    # review = Review.objects.get(pk=review_pk)
    review = get_object_or_404(Review, pk=review_pk)
    # 상세 리뷰 보기
    if request.method == 'GET':
        serializer = ReviewSerializer(review)
        return Response(serializer.data)
    # 삭제
    elif request.method == 'DELETE':
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    # 리뷰 수정
    elif request.method == 'PUT':
        serializer = ReviewSerializer(review, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

# 리뷰 작성


@api_view(['POST'])
def review_create(request, movie_pk):
    # @permission_classes([IsAuthenticated])
    movie = get_object_or_404(Movie, pk=movie_pk)
    serializer = ReviewSerializer(data=request.data)
    print(request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(movie=movie)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

# 영화 좋아요


@api_view(['POST'])
def movie_like(request, movie_pk):
    movie = Movie.objects.get(pk=movie_pk)
    # 좋아요 했었다면
    if movie.like_users.filter(pk=request.user.pk).exists():
        # 좋아요 제거
        movie.like_users.remove(request.user)
    else:
        # 좋아요 추가
        movie.like_users.add(request.user)
    serializer = MovieSerializer(movie)
    return Response(serializer.data)


# 리뷰 좋아요

@api_view(['POST'])
def review_like(request, review_pk):
    review = Review.objects.get(pk=review_pk)
    # 좋아요 했었다면
    if review.like_users.filter(pk=request.user.pk).exists():
        # 좋아요 제거
        review.like_users.remove(request.user)
    else:
        # 좋아요 추가
        review.like_users.add(request.user)
    serializer = ReviewSerializer(review)
    return Response(serializer.data)

# 추천알고리즘1 (최근 클릭한 10개의 디테일 영화의 장르 3개 가져와서 추천)
# 추천알고리즘2 (마지막으로 본 상세 영화와 비슷한 영화 추천, tmdb Recommendations api 사용)
# 추천알고리즘3 (OpenWeatherMap api를 사용해서 현재 날씨와 비슷한 장르의 영화 추천)


@api_view(['POST', 'GET'])
# @permission_classes([IsAuthenticated])
def handle_clicked_photo(request):
    # 영화를 클릭했다면
    if request.method == 'POST':
        if request.user.is_authenticated:
            print(request.data)
            serializer = PhotoSerializer(data=request.data)
            if serializer.is_valid():
                
                user = request.user
                photo_count = Photo.objects.filter(user=user).count()
                # print(photo_count,'here')
                if photo_count >= 10:
                    # 가장 처음에 저장된 클릭 데이터 삭제
                    oldest_photo = Photo.objects.filter(
                        user=user).order_by('clicked_at').first()
                    oldest_photo.delete()

                serializer.save(user=user)
                return Response({'message': 'Photo saved successfully.'}, status=201)
            else:
                return Response(serializer.errors, status=400)
        else:
            return Response({'message': 'User authentication required.'}, status=401)
    elif request.method == 'GET':
        user = request.user
        photos = Photo.objects.filter(
            user=user).order_by('-clicked_at')[:10]
        serializer = PhotoSerializer(photos, many=True)
        return Response(serializer.data, status=200)

        # photos = get_list_or_404(Photo)
        # serializer = PhotoSerializer(photos, many=True)
        # return Response(serializer.data)
        return Response({'message': 'User authentication required.'}, status=401)

# 장르 추천
def getMoviesByGenre(genre):
    # print(genre)
    movies = Movie.objects.filter(genre_ids__in=[genre])
    return movies

@api_view(['GET'])
def movie_genre(request, genre_id):
    if genre_id:
        movies = getMoviesByGenre(genre_id)
    else:
        movies = Movie.objects.all()

    serializer = MovieListSerializer(movies, many=True)
    return Response(serializer.data)


# # 코사인 유사도 사용


# @api_view(['GET'])
# def liked_movies(request):
#     user = request.user  # 현재 인증된 사용자

#     if user.is_authenticated:  # 인증된 사용자인지 확인
#         liked_movies = user.like_movies.all()  # 사용자가 좋아요한 영화 목록
#         serializer = UserLikedMoviesSerializer(liked_movies)
#         return Response(serializer.data)
#     else:
#         return Response({'detail': 'User not authenticated'}, status=401)

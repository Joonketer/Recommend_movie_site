from rest_framework.decorators import api_view, permission_classes
from django.http import QueryDict
from django.shortcuts import render
from .models import Movie, Review, Photo

from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt

from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

from rest_framework import status
from django.shortcuts import get_object_or_404, get_list_or_404
from .serializers import MovieListSerializer, MovieSerializer, ReviewListSerializer, ReviewSerializer, PhotoSerializer
from django.http import JsonResponse
from django.db.models import Q

# Create your views here.

# 영화 존재 여부


def check_if_movie_exists(request, movie_id):
    try:
        movie = Movie.objects.get(
            movie_id=movie_id)
        print(movie)
        exists = True
    except Movie.DoesNotExist:
        exists = False

    return JsonResponse({"exists": exists})

# 전체 영화


@api_view(['GET', 'POST'])
# @permission_classes([IsAuthenticated])
def movie_list(request):
    if request.method == 'GET':
        # movies = movie.objects.all()
        movies = get_list_or_404(Movie)
        serializer = MovieListSerializer(movies, many=True)
        # print(serializer.data)
        return Response(serializer.data)
    elif request.method == 'POST':
        print(request.data)
        serializer = MovieSerializer(data=request.data)
        # 중복된 데이터 체크
        if serializer.is_valid(raise_exception=True):
            title = serializer.validated_data['title']
            existing_movies = Movie.objects.filter(title=title)
            if existing_movies.exists():
                return Response({'error': '영화가 이미 존재합니다.'}, status=status.HTTP_400_BAD_REQUEST)

            serializer.save()
            # serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def get(request, movie_id):
    try:
        movie = Movie.objects.filter(
            movie_id=movie_id).order_by('-release_date').first()
        serializer = MovieSerializer(movie)
        return Response(serializer.data)
    except Movie.DoesNotExist:
        return Response({"error": "Movie not found"}, status=404)

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
@permission_classes([IsAuthenticated])
def review_create(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    serializer = ReviewSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(movie=movie, user=request.user)
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

            serializer = PhotoSerializer(data=request.data)
            if serializer.is_valid():
                user = request.user
                photo_count = Photo.objects.filter(user=user).count()
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
        # 마지막으로 클릭한 사진과 관련된 정보를 가져오는 코드
        last_clicked_photo = Photo.objects.filter(
            user_id=request.user.id).order_by('-clicked_at').first()
        print(request.user.id)
        if last_clicked_photo:
            # 마지막으로 클릭한 사진과 관련된 영화를 추천하는 코드
            photos = Photo.objects.filter(user_id=last_clicked_photo.user_id)
            # 나머지 코드 추가

            serializer = PhotoSerializer(photos, many=True)
            return Response(serializer.data, status=200)
        else:
            # 마지막으로 클릭한 사진이 없는 경우에 대한 처리
            return Response({'message': 'No last clicked photo found.'}, status=404)


# 장르 추천
def getMoviesByGenre(genre):
    # print(genre)
    movies = Movie.objects.filter(
        genre_ids__in=[genre]).order_by('-popularity')[:10]
    return movies


@api_view(['GET'])
def movie_genre(request, genre_id):
    if genre_id:
        movies = getMoviesByGenre(genre_id)
    else:
        movies = Movie.objects.all()

    serializer = MovieListSerializer(movies, many=True)
    return Response(serializer.data)

# 장르 추천


def getMoviesByMovie(movie):
    # print(genre)
    movies = Movie.objects.filter(movie_id=movie)
    return movies


@api_view(['GET'])
def movie_movie(request, movie_id):
    if movie_id:
        movies = getMoviesByMovie(movie_id)
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

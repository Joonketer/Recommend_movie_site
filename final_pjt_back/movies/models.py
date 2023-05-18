from django.db import models
from django.conf import settings

# Create your models here.


class Genre(models.Model):
    # genre_id = models.IntegerField(unique=True, null=True)
    genre_id = models.IntegerField(primary_key=True)
    genre_name = models.CharField(max_length=50)

    def __str__(self):
        return self.genre_name


class Movie(models.Model):
    movie_id = models.IntegerField(primary_key=True)  # 키 값
    title = models.CharField(max_length=100)    # 영화제목
    release_date = models.DateField()   # 개봉일
    popularity = models.FloatField()    # 인기도
    vote_average = models.FloatField()  # 평점
    vote_count = models.IntegerField()
    overview = models.TextField()  # 줄거리
    poster_path = models.CharField(max_length=200)  # 사진
    backdrop_path = models.CharField(max_length=200, null=True)
    genre_ids = models.ManyToManyField(Genre)   # 장르
    like_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='like_movies', blank=True)   # 좋아요한 사람

    def __str__(self):
        return self.title


class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)    # 작성자
    like_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='like_review', blank=True)
    movie = models.ForeignKey(
        "Movie", related_name="reviews", on_delete=models.CASCADE)  # 영화
    content = models.CharField(max_length=500)  # 내용
    user_vote_average = models.FloatField()  # 평점
    created_at = models.DateTimeField(auto_now_add=True)  # 작성일
    updated_at = models.DateTimeField(auto_now=True)  # 수정일

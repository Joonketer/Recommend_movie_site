from rest_framework import serializers
from .models import Movie, Genre, Review
from django.contrib.auth import get_user_model


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('username', )

# # 장르 가져올 것


# Main 영화 리스트


class MovieListSerializer(serializers.ModelSerializer):

    class GenreListSerializer(serializers.ModelSerializer):
        class Meta:
            model = Genre
            fields = ('genre_id', 'genre_name',)

    genre_ids = GenreListSerializer(many=True, read_only=True)

    class Meta:
        model = Movie
        # fields = ('id', 'like_users', 'title', 'overview', 'poster_path',
        #           'genre_ids',)
        fields = '__all__'

# 영화 상세


class MovieSerializer(serializers.ModelSerializer):
    # 영화에 작성된 리뷰 가져오기
    class ReviewSerializer(serializers.ModelSerializer):
        user = UserSerializer(read_only=True)

        class Meta:
            model = Review
            fields = '__all__'
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Movie
        fields = '__all__'


class ReviewListSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Review
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    class MovieSerializer(serializers.ModelSerializer):
        class Meta:
            model = Movie
            fields = ('id', 'title', )
    movie = MovieSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Review
        fields = '__all__'

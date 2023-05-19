from rest_framework import serializers
from .models import Movie, Genre, Review, Photo
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
    # 장르 보여주기
    class GenreListSerializer(serializers.ModelSerializer):
        class Meta:
            model = Genre
            fields = ('genre_id', 'genre_name',)

    genre_ids = GenreListSerializer(many=True, read_only=True)

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

# 전체 리뷰


class ReviewListSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Review
        fields = '__all__'

# 상세 리뷰


class ReviewSerializer(serializers.ModelSerializer):
    class MovieSerializer(serializers.ModelSerializer):
        class Meta:
            model = Movie
            fields = ('id', 'title', )

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('user', 'movie',)

# 추천알고리즘
# - 최근 클릭한 10개의 디테일 영화의 장르 3개 가져와서 추천
# - 마지막으로 본 상세 영화와 비슷한 영화 추천, tmdb Recommendations api 사용
# - OpenWeatherMap api를 사용해서 현재 날씨와 비슷한 장르의 영화 추천


class PhotoSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Photo
        fields = ['id', 'user', 'genre_ids', 'movie', 'clicked_at']
        read_only_fields = ('user', 'movie',)

# # 코사인 유사도를 통해 좋아요를 누른 영화들 중 유사도가 높은 영화 가져오기


# class LikedMovieSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Movie
#         fields = '__all__'


# class UserLikedMoviesSerializer(serializers.Serializer):
#     user_liked_movies = LikedMovieSerializer(many=True)

#     def to_representation(self, instance):
#         data = super().to_representation(instance)
#         return data['user_liked_movies']

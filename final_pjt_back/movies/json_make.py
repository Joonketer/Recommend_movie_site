import requests
import json
import os
# from django.http.response import JsonResponse


def get_movies():
    movies_json = []

    for page in range(1, 100):
        url = f"https://api.themoviedb.org/3/movie/popular?language=ko-KOR&page={page}"

        headers = {
            "accept": "application/json",
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIzYTRmODVmMDA1ZDExODVkNjg3Y2Q1ZjE3NTRjY2MyZCIsInN1YiI6IjYzZDIyZDFiY2I3MWI4MDA3YzFiOGNlYyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.zwYescz-jNoCc_X2jDOxOz90oofdYLmxwwkH5XuDmGs"
        }

        movies = requests.get(url, headers=headers).json()

        for movie in movies['results']:
            if movie.get('release_date', '') and movie.get('poster_path', '') and not movie['adult']:
                fields = {
                    'movie_id': movie['id'],
                    'title': movie['title'],
                    'release_date': movie['release_date'],
                    'popularity': movie['popularity'],
                    'vote_average': movie['vote_average'],
                    'vote_count': movie['vote_count'],
                    'overview': movie['overview'],
                    'poster_path': movie['poster_path'],
                    'backdrop_path': movie['backdrop_path'],
                    'genre_ids': movie['genre_ids']

                }

                data = {
                    "pk": movie['id'],
                    "model": "movies.movie",
                    "fields": fields,
                }

                movies_json.append(data)

    with open("movie_data.json", "w", encoding="utf-8") as make_json:
        json.dump(movies_json, make_json, indent="\t", ensure_ascii=False)


get_movies()


def get_genres():
    genres_json = []

    url = "https://api.themoviedb.org/3/genre/movie/list?language=ko-KOR"

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIzYTRmODVmMDA1ZDExODVkNjg3Y2Q1ZjE3NTRjY2MyZCIsInN1YiI6IjYzZDIyZDFiY2I3MWI4MDA3YzFiOGNlYyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.zwYescz-jNoCc_X2jDOxOz90oofdYLmxwwkH5XuDmGs"
    }

    genres_response = requests.get(url, headers=headers)
    genres_data = genres_response.json()  # JSON 형식으로 변환

    for genre in genres_data['genres']:
        fields = {
            'genre_id': genre['id'],
            'genre_name': genre['name']
        }

        data = {
            "pk": genre['id'],
            "model": "movies.genre",
            "fields": fields,
        }

        genres_json.append(data)

    with open("genre_data.json", "w", encoding="utf-8") as w:
        json.dump(genres_json, w, indent="\t", ensure_ascii=False)


get_genres()

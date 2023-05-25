<template>
  <div class="article-list">
    <h3 class="text-center">지금 날씨와 어울리는 영화</h3>
    <h2 class="text-center">Weather : {{ weather }}</h2>
    <hr>
    <br>
    <h3 class="text-center">추천 영화 장르 :</h3>
    <div v-if="isLoading">Loading...</div>
    <div v-else>
      <div v-for="genre in movieGenres" :key="genre.id">
        <div class="text-center">
          <h2>{{ genre.name }}</h2>
        </div>
        <b-row>
          <div v-for="movie in recommendedMovies[genre.id]" :key="movie.movie_id" class="card-wrapper">
            <b-card
              class="movie-card bg-dark h-100 d-flex align-items-stretch"
              @mouseenter="hovering = true"
              @mouseleave="hovering = false"
            >
              <router-link
                :to="{
                  name: 'DetailView',
                  params: { id: movie.movie_id },
                }"
              >
                <div class="movie-poster" @click="handleMovieClick(movie)">
                  <b-card-img
                    :src="getBackdropUrl(movie.poster_path || movie.backdrop_path)"
                    alt="Backdrop Image"
                  ></b-card-img>
                  <b-card-title v-show="hovering" class="movie-title">
                    {{ movie.title }}
                  </b-card-title>
                </div>
              </router-link>
            </b-card>
          </div>
        </b-row>
      </div>
    </div>
  </div>
</template>


<script>
import axios from "axios";

export default {
  name: "WeatherList",
  data() {
    return {
      weather: "",
      movieGenres: [],
      recommendedMovies: {},
      isLoading: true, // 추가된 isLoading 속성
      hovering: false,
    };
  },
  mounted() {
    this.fetchWeather();
  },
  methods: {
    handleMovieClick(article) {
      const payload = {
        movie: article.movie_id,
        genre_ids: article.genre_ids.map((genre) => genre.genre_id),
      };

      // 서버로 영화 클릭 정보 전송
      axios
        .post("http://127.0.0.1:8000/api/v1/recent_moives/", payload, {
          headers: {
            Authorization: `Token ${this.token}`,
          },
        })
        .then(() => {
          // 처리 성공 시 로직
          // console.log(response.data);
        })
        .catch((error) => {
          // 에러 처리 로직
          console.error(error);
        });
    },
    fetchWeather() {
      // Make an API request to OpenWeatherMap to get the current weather
      const API_KEY = "da84d14f5b0aa15df43c26b699b795bf";
      const lat = "37.56667";
      const lon = "126.97806";
      const API_URL = `https://api.openweathermap.org/data/2.5/weather?lat=${lat}&lon=${lon}&appid=${API_KEY}`;

      axios
        .get(API_URL)
        .then((response) => {
          const weather = response.data.weather[0].main;
          this.weather = weather;
          this.fetchMovieGenres(weather);
        })
        .catch((error) => {
          console.error("Error fetching weather:", error);
        });
    },
    fetchMovieGenres(weather) {
      // Define movie genres based on weather conditions
      const genreMap = {
        Clear: [28, 12, 16, 99, 10751, 35, 878],
        Clouds: [18, 14, 36, 10752, 9648, 53],
        Rain: [80, 18, 10749, 10402, 53],
        Snow: [28, 16, 10751, 10770, 35, 18],
        Thunderstorm: [28, 27, 878, 99],
        Drizzle: [18, 35, 9648, 10402, 16],
        Mist: [53, 27, 9648, 80, 10770],
        Smoke: [53, 27, 9648, 80, 10770],
        Haze: [28, 18, 10749, 9648, 53],
        Dust: [28, 18, 9648, 53],
        Fog: [18, 27, 53, 9648, 80],
        Sand: [28, 18, 9648, 37, 878],
        Ash: [53, 27, 9648, 80, 10770],
        Squall: [80, 18, 10749, 10402, 53],
        Tornado: [28, 878, 53, 10752],
      };

      // Fetch movie genres based on the weather condition
      const movieGenres = genreMap[weather] || [];
      const shuffledGenres = this.shuffleArray(movieGenres);
      const selectedGenres = shuffledGenres.slice(0, 3);

      this.movieGenres = selectedGenres.map((genreId) => {
        return {
          id: genreId,
          name: this.getGenreName(genreId),
        };
      });

      // Fetch recommended movies for each genre
      this.fetchRecommendedMovies(selectedGenres);
    },
    fetchRecommendedMovies(genres) {
      const movieIds = genres.map((genreId) => {
        return this.getMovieIdsByGenreId(genreId);
      });

      Promise.all(movieIds)
        .then((results) => {
          results.forEach((movies, index) => {
            const genreId = genres[index];
            this.recommendedMovies[genreId] = movies;
          });
          this.isLoading = false; // 데이터 로딩이 완료됨을 표시
        })
        .catch((error) => {
          console.error("Error fetching recommended movies:", error);
          this.isLoading = false; // 데이터 로딩 중 오류 발생 시에도 isLoading을 false로 설정
        });
    },
    getMovieIdsByGenreId(genreId) {
      // Make an API request to fetch movie IDs by genre ID
      const API_URL = `http://127.0.0.1:8000/api/v1/movies/${genreId}/genre/`;

      return axios.get(API_URL).then((response) => {
        const movies = response.data;
        // console.log(movies);
        return movies.map((movie) => {
          return {
            movie_id: movie.movie_id,
            title: movie.title,
            poster_path: movie.poster_path,
          };
        });
      });
    },
    shuffleArray(array) {
      // Fisher-Yates 알고리즘을 사용하여 배열을 무작위로 섞습니다.
      for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]];
      }
      return array;
    },
    getGenreName(genreId) {
      // Map genre IDs to genre names
      const genreMap = {
        28: "액션",
        12: "모험",
        16: "애니메이션",
        35: "코미디",
        80: "범죄",
        99: "다큐멘터리",
        18: "드라마",
        10751: "가족",
        14: "판타지",
        36: "역사",
        27: "공포",
        10402: "음악",
        9648: "미스터리",
        10749: "로맨스",
        878: "SF",
        10770: "TV 영화",
        53: "스릴러",
        10752: "전쟁",
        37: "서부",
      };

      return genreMap[genreId] || "Unknown";
    },
    getBackdropUrl(backdropPath) {
      const baseUrl = "https://image.tmdb.org/t/p/original";
      return `${baseUrl}${backdropPath}`;
    },
  },
};
</script>

<style scoped>
ul {
  margin-left: 1rem;
}
img {
  width: 100px;
  height: 100px;
}

/* 추가 스타일 */
.article-list {
  text-align: start;
  flex-direction: column;
}
.card-wrapper {
  width: 500px;
  padding-left: 8px;
  margin-left: 50px;
  padding-bottom:20px;
}
.movie-poster {
  position: relative;
}
.movie-card {
  position: relative;
  box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);
  transition: 0.3s;
  width: 100%;
  border-radius: 5px;
  padding: 2%;
  margin-bottom: 2rem;
  padding:0;
}
.movie-title {
  position: absolute;
  bottom: 0;
  color: white;
  background-color: rgba(0, 0, 0, 0.5);
  width: 100%;
}
.movie-card img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: opacity 0.3s ease-in-out;

}
.movie-card:hover img {
  opacity: 0.5;
}
.movie-card .movie-poster {
  position: relative;
}
.movie-card:hover:before {
  content: "";
  position: absolute;
  top: 0;
  bottom: 0;
  left: 0;
  right: 0;
  background: rgba(0, 0, 0, 0.7); /* 50% transparent black */
  border-radius: 5px;
}
.movie-title {
  position: absolute;
  top: 60%;
  left: 50%;
  transform: translate(-50%, -50%);
  text-align: center;
  opacity: 0;
  transition: opacity 0.3s ease-in-out;
}
.movie-card:hover .movie-title {
  opacity: 1;
}
.movie-card h2 {
  text-align: center;

  transform: translate(-50%, -50%);
  color: black;
  text-align: center;
  opacity: 0;
  transition: opacity 0.3s ease-in-out;
}
.movie-card:hover h2 {
  opacity: 1;
}
.movie-card h5 {
  font-family: "Nanum Gothic", sans-serif;
  font-weight: 400;
  color: white;
}
</style>

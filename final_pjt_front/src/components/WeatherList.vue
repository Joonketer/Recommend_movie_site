<template>
  <div>
    <h3>날씨 api</h3>
    <h2>Current Weather: {{ weather }}</h2>
    <h3>Suggested Movie Genres:</h3>
    <div v-if="isLoading">
      Loading...
    </div>
    <div v-else>
      <div v-for="genre in movieGenres" :key="genre.id">
        <h2>{{ genre.name }}</h2>
        <p v-for="movie in recommendedMovies[genre.id]" :key="movie.movie_id">
          {{ movie.title }}
          <img :src="getBackdropUrl(movie.poster_path)" alt="Backdrop Image" />
          
        </p>
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
    };
  },
  mounted() {
    this.fetchWeather();
  },
  methods: {
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
        Clear: [28, 12, 16, 99, 10751],
        Clouds: [18, 14, 36, 10752],
        Rain: [80, 18, 10749, 10402],
        Snow: [28, 16, 10751, 10770],
        Thunderstorm: [28, 27, 878],
        Drizzle: [18, 35, 9648, 10402],
        Mist: [18, 27, 53],
        Smoke: [53, 27, 9648],
        Haze: [28, 18, 10749],
        Dust: [28, 18, 9648],
        Fog: [18, 27, 53],
        Sand: [28, 18, 9648, 37],
        Ash: [28, 18, 9648],
        Squall: [28, 18, 9648],
        Tornado: [28, 878, 53],
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
        console.log(movies)
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
img{
  width: 100px;
  height: 100px;
}
</style>
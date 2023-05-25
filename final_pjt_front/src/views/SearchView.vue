<template>
  <div>
    <div class="search-result-title d-flex justify-content-center">
      <h2>검색 결과</h2>
    </div>
    <div v-if="filteredSearchResults" class="result-container">
      <div
        v-for="movie in filteredSearchResults"
        :key="movie.id"
        class="movie-card"
        @mouseenter="showDetails(movie)"
        @mouseleave="hideDetails(movie)"
      >
        <img
          :src="getBackdropUrl(movie.poster_path || movie.backdrop_path)"
          alt="Backdrop Image"
          @click="checkMovieExistence(movie)"
        />
        <div
          class="movie-info"
          v-if="movie.showDetails"
          @click="checkMovieExistence(movie)"
        >
          <h3>{{ movie.title }}</h3>
          <p>★ : {{ movie.vote_average }}</p>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import axios from "axios";
import { mapState } from "vuex";

export default {
  data() {
    return {
      searchResults: [],
      Movies_title: "",
      movie_detail: null,
    };
  },
  created() {
    this.getArticles();
  },
  props: {
    searchQuery: {
      type: String,
      default: "",
    },
  },
  computed: {
    isLogin() {
      return this.$store.getters.isLogin; // 로그인 여부
    },
    ...mapState(["token"]),
    filteredSearchResults() {
      return this.searchResults.filter((movie) =>
        movie.title.includes(this.searchQuery)
      );
    },
  },
  mounted() {
    const savedSearchResults = localStorage.getItem("searchResults");
    if (savedSearchResults) {
      this.searchResults = JSON.parse(savedSearchResults);
    }
    this.searchMovies();
  },
  watch: {
    searchQuery() {
      this.searchMovies();
    },
  },
  methods: {
    getArticles() {
      if (this.isLogin) {
        this.$store.dispatch("getArticles");
      } else {
        alert("로그인이 필요한 페이지입니다...");
        this.$router.push({ name: "LogInView" });
      }

      // 로그인이 되어 있으면 getArticles action 실행
      // 로그인 X라면 login 페이지로 이동
    },
    showDetails(movie) {
      this.$set(movie, "showDetails", true);
    },
    hideDetails(movie) {
      this.$set(movie, "showDetails", false);
    },
    searchMovies() {
      const url = `https://api.themoviedb.org/3/search/movie?query=${this.searchQuery}&include_adult=false&language=ko-KOR&page=1`;

      const headers = {
        accept: "application/json",
        Authorization:
          "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIzYTRmODVmMDA1ZDExODVkNjg3Y2Q1ZjE3NTRjY2MyZCIsInN1YiI6IjYzZDIyZDFiY2I3MWI4MDA3YzFiOGNlYyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.zwYescz-jNoCc_X2jDOxOz90oofdYLmxwwkH5XuDmGs",
      };

      axios
        .get(url, { headers })
        .then((response) => {
          this.searchResults = response.data.results;
          localStorage.setItem(
            "searchResults",
            JSON.stringify(this.searchResults)
          );
        })
        .catch((error) => {
          console.error("검색 중 오류 발생:", error);
        });
    },
    getBackdropUrl(backdropPath) {
      const baseUrl = "https://image.tmdb.org/t/p/original";
      return `${baseUrl}${backdropPath}`;
    },
    checkMovieExistence(movie) {
      const movieId = movie.id;
      const API_URL = `http://127.0.0.1:8000/api/v1/movies/${movieId}/exists/`;

      axios
        .get(API_URL)
        .then((response) => {
          const movieData = response.data;
          if (!movieData.exists) {
            // 선택한 영화가 존재하지 않을 경우에 대한 처리

            console.log("영화가 존재하지 않습니다.");
            this.addMovieToDatabase(movieId);
          } else {
            // 선택한 영화가 존재할 경우에 대한 처리
            console.log("영화가 존재합니다.");
            this.navigateToDetail(movieId);
          }
        })
        .catch((error) => {
          console.error("영화 존재 여부 확인 중 오류 발생:", error);
        });
    },
    addMovieToDatabase(movie_id) {
      // 데이터베이스에 영화를 추가하기 위해 API 요청을 수행합니다.
      const API_URL = `http://127.0.0.1:8000/api/v1/movies/`;

      const movie_detail = this.searchResults.find(
        (movie) => movie.id === movie_id
      );

      if (!movie_detail) {
        console.error("영화 정보를 찾을 수 없습니다.");
        return;
      }

      const movieData = {
        movie_id: movie_detail.id,
        overview: movie_detail.overview,
        popularity: movie_detail.popularity,
        poster_path: movie_detail.poster_path,
        backdrop_path: movie_detail.backdrop_path,
        release_date: movie_detail.release_date,
        title: movie_detail.title,
        vote_average: movie_detail.vote_average,
        vote_count: movie_detail.vote_count,
        genre_ids: movie_detail.genres,
        // 필요한 다른 영화 정보도 추가할 수 있습니다.
      };

      axios
        .post(API_URL, movieData)
        .then(() => {
          console.log("영화를 데이터베이스에 추가했습니다.");
          this.navigateToDetail(movie_id);
        })
        .catch((error) => {
          alert("영화 데이터가 아닙니다");
          console.error("영화 추가 중 오류가 발생했습니다:", error);
        });
    },
    navigateToDetail(movie_id) {
      // 영화의 상세 보기(detail view)로 이동합니다.
      const API_URL = `http://127.0.0.1:8000/api/v1/movies/${movie_id}/make/`;

      return axios
        .get(API_URL)
        .then((response) => {
          const movieData = response.data;

          this.$router.push({
            name: "DetailView",
            params: movieData,
          });
        })
        .catch((error) => {
          console.error("최종오류", error);
        });
    },
  },
};
</script>

<style scoped>
/* ul {
  margin-left: 1rem;
}
img {
  width: 100px;
  height: 100px;
} */
.result-container {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-around;
}
.movie-card {
  position: relative;
  width: 200px;
  height: 300px;
  margin: 10px;
  overflow: hidden;
}
.movie-card img {
  width: 100%;
  height: 100%;
  transition: 0.5s ease;
  backface-visibility: hidden;
}
.movie-card:hover img {
  opacity: 0.3;
}
.movie-info {
  transition: 0.5s ease;
  opacity: 0;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  -ms-transform: translate(-50%, -50%);
  text-align: center;
}
.movie-card:hover .movie-info {
  opacity: 1;
}
</style>

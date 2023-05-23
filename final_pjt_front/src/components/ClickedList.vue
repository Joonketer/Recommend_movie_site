<template>
  <div class="article-list">
    <h3>마지막 클릭한 사진과 관련된 정보</h3>
    <div v-if="isLoading">Loading...</div>
    <div v-else>
      <div v-if="lastClickedPhoto">
        <p>{{ lastClickedPhoto.movie }}</p>
        <p>{{ Movies_title }}</p>
      </div>
      <div v-if="movie_list">
        <div v-for="movie in movie_list" :key="movie.id">
          {{ movie.title }}
          {{ movie.id }}
          <div v-if="movie_detail">
            <img
              :src="getBackdropUrl(movie.poster_path)"
              alt="Backdrop Image"
              @click="fetchDetail(movie.id)"
            />
          </div>
          <div v-else>
            <img
              :src="getBackdropUrl(movie.poster_path)"
              alt="Backdrop Image"
              @click="fetchDetail(movie.id)"
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { mapState } from "vuex";

export default {
  name: "ClickedList",
  data() {
    return {
      isLoading: true,
      lastClickedPhoto: {},
      Movies_title: "",
      movie_list: null,
      movie_detail: null,
    };
  },
  mounted() {
    this.fetchLastClickedPhoto();
  },
  computed: {
    ...mapState(["token"]),
  },
  methods: {
    fetchDetail(movie_id) {
      const API_URL = `https://api.themoviedb.org/3/movie/${movie_id}?language=ko-kor`;

      const headers = {
        accept: "application/json",
        Authorization:
          "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIzYTRmODVmMDA1ZDExODVkNjg3Y2Q1ZjE3NTRjY2MyZCIsInN1YiI6IjYzZDIyZDFiY2I3MWI4MDA3YzFiOGNlYyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.zwYescz-jNoCc_X2jDOxOz90oofdYLmxwwkH5XuDmGs",
      };
      axios
        .get(API_URL, { headers })
        .then((response) => {
          this.movie_detail = response.data;

          console.log("영화 디테일");
          console.log(this.movie_detail);
          // 영화가 데이터베이스에 존재하는지 확인합니다.
          this.checkIfMovieExists(movie_id)
            .then((exists) => {
              if (!exists) {
                // 영화가 데이터베이스에 존재하지 않는 경우, 데이터베이스에 추가합니다.
                console.log("영화없음");
                this.addMovieToDatabase(movie_id);
              } else {
                // 영화가 이미 존재하는 경우, 상세 보기로 이동합니다.
                console.log("영화 존재");
                this.navigateToDetail(movie_id);
              }
            })
            .catch((error) => {
              console.error(
                "영화 존재 여부 확인 중 오류가 발생했습니다:",
                error
              );
            });
        })
        .catch((error) => {
          console.error("영화를 가져오는 중 오류가 발생했습니다:", error);
        });
    },
    fetchSearch() {
      console.log(this.Movies_title);
      const API_URL = `https://api.themoviedb.org/3/search/movie?query=${this.Movies_title}&include_adult=false&language=ko-KOR&page=1`;

      const headers = {
        accept: "application/json",
        Authorization:
          "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIzYTRmODVmMDA1ZDExODVkNjg3Y2Q1ZjE3NTRjY2MyZCIsInN1YiI6IjYzZDIyZDFiY2I3MWI4MDA3YzFiOGNlYyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.zwYescz-jNoCc_X2jDOxOz90oofdYLmxwwkH5XuDmGs",
      };

      axios
        .get(API_URL, { headers })
        .then((response) => {
          const movie_datas = response.data;
          this.movie_list = movie_datas.results.slice(0, 10);
          console.log("영화목록");
          console.log(this.movie_list);
        })
        .catch((error) => {
          console.error("Error fetching movie:", error);
        });
    },
    fetchLastClickedPhoto() {
      const API_URL = "http://127.0.0.1:8000/api/v1/recent_moives/";

      axios
        .get(API_URL, { headers: { Authorization: `Token ${this.token}` } })
        .then((response) => {
          const photos = response.data;
          console.log("포토", photos);
          console.log("포토", photos.length);
          if (photos.length > 0) {
            this.lastClickedPhoto = photos[0];
            console.log(photos[0]);

            // lastClickedPhoto가 설정된 후에 fetchSearch()를 호출하여 Movies_title을 업데이트합니다.
            const movieId = this.lastClickedPhoto.movie;
            this.fetchMoviesByMovie(movieId);
          }
          this.isLoading = false;
        })
        .catch((error) => {
          console.error(
            "최근 클릭한 사진을 가져오는 중 오류가 발생했습니다:",
            error
          );
          this.isLoading = false;
        });
    },

    fetchMoviesByMovie(movie_id) {
      const API_URL = `http://127.0.0.1:8000/api/v1/movies/${movie_id}/`;
      axios
        .get(API_URL)
        .then((response) => {
          const movies = response.data.title;
          console.log("여기입니다", movies);
          this.Movies_title = movies;

          // Movies_title이 업데이트된 후에 fetchSearch()를 호출하여 API를 요청합니다.
          this.fetchSearch();
        })
        .catch((error) => {
          console.error("Error fetching recommended movies:", error);
        });
    },
    getBackdropUrl(backdropPath) {
      const baseUrl = "https://image.tmdb.org/t/p/original";
      return `${baseUrl}${backdropPath}`;
    },
    checkIfMovieExists(movie_id) {
      // 주어진 ID의 영화가 데이터베이스에 존재하는지 확인하기 위해 API 요청을 수행합니다.
      const API_URL = `http://127.0.0.1:8000/api/v1/movies/${movie_id}/exists/`;

      return axios
        .get(API_URL)
        .then((response) => {
          const movieData = response.data;
          console.log("영화 데이터:", movieData);
          console.log(movieData !== null);
          return movieData.exists; // 영화가 존재하는 경우 true를 반환하고, 그렇지 않은 경우 false를 반환합니다.
        })
        .catch((error) => {
          console.error("영화 존재 여부 확인 중 오류가 발생했습니다:", error);
        });
    },
    addMovieToDatabase(movie_id) {
      // 데이터베이스에 영화를 추가하기 위해 API 요청을 수행합니다.
      const API_URL = `http://127.0.0.1:8000/api/v1/movies/`;

      const movieData = {
        movie_id: this.movie_detail.id,
        overview: this.movie_detail.overview,
        popularity: this.movie_detail.popularity,
        poster_path: this.movie_detail.poster_path,
        backdrop_path: this.movie_detail.backdrop_path,
        release_date: this.movie_detail.release_date,
        title: this.movie_detail.title,
        vote_average: this.movie_detail.vote_average,
        vote_count: this.movie_detail.vote_count,
        genre_ids: this.movie_detail.genres,
        // 필요한 다른 영화 정보도 추가할 수 있습니다.
      };
      console.log("확인", this.movie_detail);
      console.log("내부", movieData);
      axios
        .post(API_URL, movieData)
        .then(() => {
          console.log("영화를 데이터베이스에 추가했습니다.");
          this.navigateToDetail(movie_id);
        })
        .catch((error) => {
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
          console.log("최종", movieData);
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
ul {
  margin-left: 1rem;
}
img {
  width: 100px;
  height: 100px;
}
</style>
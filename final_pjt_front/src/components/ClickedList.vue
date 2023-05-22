<template>
  <div class="article-list">
    <h3>마지막 클릭한 사진과 관련된 정보</h3>
    <div v-if="isLoading">
      Loading...
    </div>
    <div v-else>
      <div v-if="lastClickedPhoto">
        <p>{{ lastClickedPhoto.movie }}</p>
        <p>{{ Movies_title }}</p>
      </div>
      <div v-if="movie_list">
        <div v-for="movie in movie_list" :key="movie.id">
          {{ movie.title }}
          <router-link
      :to="{
        name: 'DetailView',
        params: { id: movie.movie_id },
      }" >
          <img :src="getBackdropUrl(movie.poster_path)" alt="Backdrop Image" />
          </router-link>
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
      lastClickedPhoto: null,
      Movies_title: null,
      movie_list: null,
    };
  },
  mounted() {
    this.fetchLastClickedPhoto();
  },
  computed: {
    ...mapState(["token"]),
  },
  methods: {
    fetchSearch() {
      console.log(this.Movies_title);
      const API_URL = `https://api.themoviedb.org/3/search/movie?query=${this.Movies_title}&include_adult=false&language=ko-KOR&page=1`;

      const headers = {
        accept: "application/json",
        Authorization: "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIzYTRmODVmMDA1ZDExODVkNjg3Y2Q1ZjE3NTRjY2MyZCIsInN1YiI6IjYzZDIyZDFiY2I3MWI4MDA3YzFiOGNlYyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.zwYescz-jNoCc_X2jDOxOz90oofdYLmxwwkH5XuDmGs",
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
          console.error("최근 클릭한 사진을 가져오는 중 오류가 발생했습니다:", error);
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

<template>
  <div class="movie-list-item">
    <img
      :src="getImageUrl(movie.poster_path)"
      alt="Movie poster"
      @click="
        toDetail();
        handleMovieClick(movie);
      "
    />
    <h3>{{ movie.title }}</h3>
    <p>{{ movie.overview }}</p>
  </div>
</template>
  
  <script>
import axios from "axios";
import { mapState } from "vuex";
export default {
  name: "MovieListItem",
  props: {
    movie: Object,
  },
  computed: {
    ...mapState(["token"]),
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
        .then((response) => {
          // 처리 성공 시 로직
          console.log(response.data);
        })
        .catch((error) => {
          // 에러 처리 로직
          console.error(error);
        });
    },
    getImageUrl(path) {
      return "https://image.tmdb.org/t/p/w500" + path;
    },
    toDetail() {
      this.$router.push({
        name: "DetailView",
        params: { id: this.movie.movie_id },
      });
    },
  },
};
</script>
  
  <style>
/* CSS styles for your component */
</style>
  
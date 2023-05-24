<template>
  <div>
    <div v-for="(movies, title) in categories" :key="title">
      <h2>{{ title }}</h2>
      <img
        src="../assets/left.png"
        alt="Previous page"
        @click="previousPage(title)"
      />
      <div class="movie-list">
        <MovieListItem v-for="movie in movies" :key="movie.pk" :movie="movie" />
      </div>
      <img src="../assets/right.png" alt="Next page" @click="nextPage(title)" />
    </div>
  </div>
</template>
  
  <script>
import MovieListItem from "./MovieListItem.vue";

export default {
  name: "MovieList",
  components: {
    MovieListItem,
  },
  computed: {
    categories() {
      return {
        Popular: this.$store.state.popularMovies,
        "Top Rated": this.$store.state.topRatedMovies,
      };
    },
  },
  methods: {
    nextPage(title) {
      const action =
        title === "Popular" ? "nextPopularPage" : "nextTopRatedPage";
      this.$store.dispatch(action);
    },
    previousPage(title) {
      const action =
        title === "Popular" ? "previousPopularPage" : "previousTopRatedPage";
      this.$store.dispatch(action);
    },
  },
  mounted() {
    if (this.$store.state.popularMovies.length === 0) {
      this.$store.dispatch("getPopularMovies");
    }
    if (this.$store.state.topRatedMovies.length === 0) {
      this.$store.dispatch("getTopRatedMovies");
    }
  },
};
</script>
  
  <style>
/* 스타일링 */
</style>
  
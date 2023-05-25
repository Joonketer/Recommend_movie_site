<template>
  <div>
    <!-- 최신 영화 carousel (fade 효과) -->
    <h2 class="movie-list-title">HOME</h2>


    <!-- Popular Movies carousel (fade 효과) -->
    <div class="container-div" v-if="popularMovies && popularMovies.length > 0">
      <h2 class="movie-list-title">POPULAR</h2>
      <b-carousel
        :id="'popular-carousel'"
        v-model="popularSlide"
        :interval="4000"
        fade
        controls
        indicators
        style="text-shadow: 1px 1px 2px #333"
      >
        <b-carousel-slide
          v-for="movie in popularMovies"
          :key="movie.id"
          :img-src="getImageUrl(movie.poster_path)"
        >
          <img
            slot="img"
            :src="getImageUrl(movie.poster_path)"
            alt="Movie poster"
            class="carousel-image"
          />
          <div slot="img-overlay" class="overlay">
            <h3>{{ movie.title }}</h3>
            <p>★ : {{ movie.vote_average }}</p>
          </div>
        </b-carousel-slide>
      </b-carousel>
    </div>

    <!-- Top Rated Movies carousel (fade 효과) -->
    <div class="container-div" v-if="topRatedMovies && topRatedMovies.length > 0">
      <h2 class="movie-list-title">Top Rated Movies</h2>
      <b-carousel
        :id="'top-rated-carousel'"
        v-model="topRatedSlide"
        :interval="4000"
        fade
        controls
        indicators
        style="text-shadow: 1px 1px 2px #333"
      >
        <b-carousel-slide
          v-for="movie in topRatedMovies"
          :key="movie.id"
          :img-src="getImageUrl(movie.poster_path)"
        >
          <img
            slot="img"
            :src="getImageUrl(movie.poster_path)"
            alt="Movie poster"
            class="carousel-image"
          />
          <div slot="img-overlay" class="overlay">
            <h3>{{ movie.title }}</h3>
            <p>★ : {{ movie.vote_average }}</p>
          </div>
        </b-carousel-slide>
      </b-carousel>
    </div>
  </div>
</template>


<script>
import { mapState } from "vuex";
import { BCarousel, BCarouselSlide } from "bootstrap-vue";

export default {
  name: "MovieList",
  components: {
    BCarousel,
    BCarouselSlide,
  },
  data() {
    return {
      slide: 0,
      popularSlide: 0,
      topRatedSlide: 0,
    };
  },
  computed: {
    ...mapState(["token"]),

    popularMovies() {
      return this.$store.state.popularMovies;
    },
    topRatedMovies() {
      return this.$store.state.topRatedMovies;
    },
  },
  methods: {
    getImageUrl(path) {
      return "https://image.tmdb.org/t/p/w500" + path;
    },
    handleMovieClick(movie) {
      this.$router.push({
        name: "DetailView",
        params: { id: movie.movie_id },
      });
    },
  },
  mounted() {

  if (this.popularMovies && this.popularMovies.length === 0) {
    this.$store.dispatch("getPopularMovies");
  }
  if (this.topRatedMovies && this.topRatedMovies.length === 0) {
    this.$store.dispatch("getTopRatedMovies");
  }
},
  beforeDestroy() {
    this.$store.commit("RESET_PAGE");
  },
};
</script>

<style scoped>
.carousel-image {
  object-fit: cover;
  width: 100%; /* 이미지가 부모 요소에 100% 너비로 맞게 됨 */
  height: 50%;
}

.overlay {
  background: rgba(0, 0, 0, 0.4);
  color: white;
  padding: 1rem;
  font-size: 1.2rem;
}

.container-div {
  padding: 30px;
}

.movie-list-title {
  text-align: left;
  color: #e5e5e5;
  font-weight: 800;
  font-size: 30px;
  padding-bottom: 10px;
}

/* popular-carousel와 top-rated-carousel에 대한 스타일 */
#popular-carousel .carousel-image,
#top-rated-carousel .carousel-image {
  width: 100%;
  height:50%;
}
</style>
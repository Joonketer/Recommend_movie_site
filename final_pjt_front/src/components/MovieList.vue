<template>
  <div>
    <h2>Upcoming Movies</h2>
    <div class="carousel-container">
      <!-- 최신 영화 carousel -->

      <b-carousel
        v-model="slide"
        :interval="4000"
        controls
        indicators
        fade
        img-width="1600"
        img-height="400"
        style="text-shadow: 1px 1px 2px #333"
      >
        <b-carousel-slide
          v-for="movie in latestMovies"
          :key="movie.id"
          :img-src="getImageUrl(movie.poster_path)"
        >
          <img
            slot="img"
            :src="getImageUrl(movie.poster_path)"
            alt="Image"
            class="carousel-image"
          />
          <div slot="img-overlay" class="overlay">
            <h3>{{ movie.title }}</h3>
          </div>
        </b-carousel-slide>
      </b-carousel>

      <div class="container-div" v-if="popularMovies">
        <h2 class="movie-list-title">POPULAR</h2>
        <swiper class="swiper" :options="swiperOption" v-if="popularMovies">
          <swiper-slide v-for="movie in popularMovies" :key="movie.id">
            <movie-card :movie="movie"></movie-card>
          </swiper-slide>
          <div class="swiper-button-prev" slot="button-prev"></div>
          <div class="swiper-button-next" slot="button-next"></div>
        </swiper>
      </div>

      <h2>Top Rated Movies</h2>
      <b-carousel
        v-model="slide"
        :interval="4000"
        controls
        indicators
        fade
        img-width="1600"
        img-height="400"
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
            alt="Image"
            class="carousel-image"
          />
          <div slot="img-overlay" class="overlay">
            <h3>{{ movie.title }}</h3>
          </div>
        </b-carousel-slide>
      </b-carousel>
    </div>
  </div>
</template>
  
  <script>
import axios from "axios";
import { mapState } from "vuex";
import { BCarousel, BCarouselSlide } from "bootstrap-vue";
import movieCard from "@/components/movieCard";
import { Swiper, SwiperSlide } from "vue-awesome-swiper";
import "swiper/swiper-bundle.css";
export default {
  name: "MovieList",
  components: {
    Swiper,
    SwiperSlide,
    BCarousel,
    BCarouselSlide,
    movieCard,
  },
  computed: {
    ...mapState(["token"]),

    latestMovies() {
      return this.$store.state.latestMovies;
    },
    popularMovies() {
      return this.$store.state.popularMovies;
    },
    topRatedMovies() {
      return this.$store.state.topRatedMovies;
    },
  },
  data() {
    return {
      hovering: false,
      slide: 0,
      swiperOption: {
        slidesPerView: 6,
        spaceBetween: 0,
        loop: true,
        navigation: {
          nextEl: ".swiper-button-next",
          prevEl: ".swiper-button-prev",
        },
      },
    };
  },

  methods: {
    getImageUrl(path) {
      return "https://image.tmdb.org/t/p/w500" + path;
    },
    handleMovieClick(movie) {
      const payload = {
        movie: movie.movie_id,
        genre_ids: movie.genre_ids.map((genre) => genre.genre_id),
      };

      axios
        .post("http://127.0.0.1:8000/api/v1/recent_moives/", payload, {
          headers: {
            Authorization: `Token ${this.token}`,
          },
        })
        .then((response) => {
          console.log(response.data);
        })
        .catch((error) => {
          console.error(error);
        });
    },
  },
  mounted() {
    if (this.$store.state.popularMovies.length === 0) {
      this.$store.dispatch("getPopularMovies");
    }
    if (this.$store.state.topRatedMovies.length === 0) {
      this.$store.dispatch("getTopRatedMovies");
    }
    if (this.latestMovies.length === 0) {
      this.$store.dispatch("getMovies");
    }
  },
  beforeDestroy() {
    this.$store.commit("RESET_PAGE");
  },
};
</script>
  
<style scoped>
.carousel-container {
  display: flex;
  justify-content: space-around;
}

.carousel-item {
  width: 100%;
  height: 100%;
}

.overlay {
  background: rgba(0, 0, 0, 0.4);
  color: white;
  padding: 1rem;
  font-size: 1.2rem;
}

.carousel-image {
  object-fit: cover;
  width: auto;
  height: 100%;
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
.swiper-button-next,
.swiper-button-prev {
  color: rgba(255, 255, 255, 0.7);
}
</style>
  

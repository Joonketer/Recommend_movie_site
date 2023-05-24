<template>
  <div class="container">
    <div class="my-3">
      <b-form-checkbox-group
        stacked
        v-model="selectedGenres"
        :options="genres"
        @change="handleGenreSelection"
      ></b-form-checkbox-group>
    </div>
    <label for="year">개봉년도 : </label>
    <select id="year" v-model="selectedYear">
      <option v-for="year in years" :key="year">{{ year }}</option>
    </select>
    <label for="rating">Rating : </label>
    <select id="rating" v-model="selectedRating">
      <option value="">선택하지 않음</option>
      <option v-for="rating in ratings" :key="rating" :value="rating">
        {{ rating }}
      </option>
    </select>
    <hr />
    <b-button
      variant="primary"
      @click="searchMovies"
      :disabled="selectedGenres.length === 0"
    >
      Search Movies
    </b-button>
    <div class="movies">
      <div
        class="movie"
        v-for="movie in movies"
        :key="movie.id"
        @click="goToDetail(movie.id)"
      >
        <h2>{{ movie.title }}</h2>
        <img
          :src="'https://image.tmdb.org/t/p/w500' + movie.poster_path"
          alt="Movie poster"
        />
        <p>{{ movie.overview }}</p>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
const API_URL = "http://127.0.0.1:8000";

export default {
  data() {
    return {
      genres: [],
      selectedGenres: [],
      movies: [],
      years: [...Array(new Date().getFullYear() - 1969).keys()]
        .map((i) => i + 1970)
        .reverse(),
      ratings: Array.from({ length: 11 }, (_, i) => i),
      selectedYear: null,
      selectedRating: "",
      API_KEY: "93ed8c8631dfd36c74cab19d569d6745",
    };
  },
  computed: {
    isLogin() {
      return this.$store.getters.isLogin; // 로그인 여부
    },
  },
  async created() {
    this.getArticles();
    try {
      const response = await axios.get(
        `https://api.themoviedb.org/3/genre/movie/list?api_key=${this.API_KEY}&language=ko-KR`
      );
      this.genres = response.data.genres.map((genre) => ({
        text: genre.name,
        value: genre.id,
      }));
    } catch (error) {
      console.error(error);
    }
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
    handleGenreSelection() {
      if (this.selectedGenres.length > 3) {
        alert("최대 3개의 장르만 선택할 수 있습니다.");
        this.selectedGenres = this.selectedGenres.slice(0, 3);
      }
    },
    async searchMovies() {
      try {
        let url = `https://api.themoviedb.org/3/discover/movie?api_key=${
          this.API_KEY
        }&with_genres=${this.selectedGenres.join(",")}&language=ko-KR&year=${
          this.selectedYear
        }`;

        if (this.selectedYear) {
          url += `&primary_release_year=${this.selectedYear}`;
        }

        if (this.selectedRating) {
          url += `&vote_average.gte=${this.selectedRating}`;
        }

        const response = await axios.get(url);

        const moviesWithDetails = await Promise.all(
          response.data.results.map(async (movie) => {
            try {
              await axios.get(`${API_URL}/api/v1/movies/${movie.id}/`);
              return movie;
            } catch (error) {
              return null;
            }
          })
        );
        this.movies = moviesWithDetails.filter(Boolean);
      } catch (error) {
        console.error(error);
      }
    },
    goToDetail(movieId) {
      this.$router.push({ name: "DetailView", params: { id: movieId } });
    },
  },
};
</script>

<style scoped>
.movies {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
}
.movie {
  width: 30%;
  margin-bottom: 2rem;
}
</style>

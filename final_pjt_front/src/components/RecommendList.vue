<template>
  <div class="article-list">
    <h3>10번 클릭한 것들 중 가장 많은 장르</h3>
    <div v-if="isLoading">
      Loading...
    </div>
    <div v-else>
      <div v-for="genre in sortedGenres" :key="genre.id">
        <h2>{{ getGenreName(genre.id) }}</h2>
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
  name: "ArticleList",
  data() {
    return {
      recommendedMovies: {},
      isLoading: true,
    };
  },
  computed: {
    sortedGenres() {
      // Count the occurrence of each genre ID
      const genreCountMap = {};
      this.$store.state.photos.forEach((photo) => {
        if (photo.genre_ids && Array.isArray(photo.genre_ids)) {
          photo.genre_ids.forEach((id) => {
            if (typeof id === "number") {
              if (genreCountMap[id]) {
                genreCountMap[id]++;
              } else {
                genreCountMap[id] = 1;
              }
            }
          });
        }
      });

      // Convert genreCountMap to an array of objects
      const genreCountArray = Object.keys(genreCountMap).map((id) => ({
        id: parseInt(id),
        count: genreCountMap[id],
      }));

      // Sort the array in descending order based on count
      genreCountArray.sort((a, b) => b.count - a.count);

      // Return the top 3 genres
      return genreCountArray.slice(0, 3);
    },
  },
  mounted() {
    this.fetchRecommendedMovies();
  },
  methods: {
    fetchRecommendedMovies() {
      const genreIds = this.sortedGenres.map((genre) => genre.id);
      const movieIdsPromises = genreIds.map((genreId) =>
        this.getMovieIdsByGenreId(genreId)
      );

      Promise.all(movieIdsPromises)
        .then((results) => {
          results.forEach((movies, index) => {
            const genreId = genreIds[index];
            this.recommendedMovies[genreId] = movies;
          });
          this.isLoading = false;
        })
        .catch((error) => {
          console.error("Error fetching recommended movies:", error);
          this.isLoading = false;
        });
    },
    getMovieIdsByGenreId(genreId) {
      // Make an API request to fetch movie IDs by genre ID
      const API_URL = `http://127.0.0.1:8000/api/v1/movies/${genreId}/genre/`;

      return axios.get(API_URL).then((response) => {
        const movies = response.data;
        return movies.map((movie) => ({
          movie_id: movie.movie_id,
          title: movie.title,
          poster_path: movie.poster_path,
        }));
      });
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
.article-list {
  text-align: start;
}
ul {
  margin-left: 1rem;
}
img{
  width: 100px;
  height: 100px;
}
</style>
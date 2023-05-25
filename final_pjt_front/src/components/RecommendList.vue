<template>
  <div class="article-list">
    <div class="text-center">
    <h3>10번 클릭한 것들 중 가장 많은 장르</h3>
    </div>  
    <div v-if="isLoading">Loading...</div>
    <div v-else>
      <div v-if="sortedGenres.length === 0">정보없음</div>
      <div v-else>
        <div v-for="genre in sortedGenres" :key="genre.id">
          <div class="text-center">
          <h2>{{ getGenreName(genre.id) }}</h2>
          </div>
          <b-row>
            <b-col md="4" v-for="movie in recommendedMovies[genre.id]" :key="movie.movie_id">
              <b-card
                class="movie-card bg-dark"
                @mouseenter="hovering = true"
                @mouseleave="hovering = false"
              >
                <router-link
                  :to="{
                    name: 'DetailView',
                    params: { id: movie.movie_id },
                  }"
                >
                  <div class="movie-poster" @click="handleMovieClick(movie)">
                    <b-card-img
                      :src="'https://image.tmdb.org/t/p/w500' + movie.poster_path"
                      alt="Movie poster"
                    ></b-card-img>
                    <b-card-title v-show="hovering" class="movie-title">
                      {{ movie.title }} <br />
                      ★ : {{ movie.vote_average }}
                    </b-card-title>
                  </div>
                </router-link>
              </b-card>
            </b-col>
          </b-row>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { mapState } from "vuex";
export default {
  name: "ArticleList",
  data() {
    return {
      nothing: false,
      recommendedMovies: {},
      isLoading: true,
      hovering: false,
    };
  },
  computed: {
    ...mapState(["token"]),
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

          this.nothing = true;
        });
    },
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
  flex-direction: column;
}
ul {
  margin-left: 1rem;
}
.movie-poster {
  position: relative;
}
.movie-card {
  position: relative;
  box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);
  transition: 0.3s;
  width: 30%;
  border-radius: 5px;
  padding: 2%;
  margin-bottom: 2rem;
}
.movie-title {
  position: absolute;
  bottom: 0;
  color: white;
  background-color: rgba(0, 0, 0, 0.5);
  width: 100%;
}
.movie-card img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: opacity 0.3s ease-in-out;
}
.movie-card:hover img {
  opacity: 0.5;
}
.movie-card .movie-poster {
  position: relative;
}
.movie-card:hover:before {
  content: "";
  position: absolute;
  top: 0;
  bottom: 0;
  left: 0;
  right: 0;
  background: rgba(0, 0, 0, 0.7); /* 50% transparent black */
  border-radius: 5px;
}
.movie-title {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  text-align: center;
  opacity: 0;
  transition: opacity 0.3s ease-in-out;
}
.movie-card:hover .movie-title {
  opacity: 1;
}
.movie-card h2 {
  text-align: center;

  transform: translate(-50%, -50%);
  color: black;
  text-align: center;
  opacity: 0;
  transition: opacity 0.3s ease-in-out;
}
.movie-card:hover h2 {
  opacity: 1;
}
.movie-card h5 {
  font-family: "Nanum Gothic", sans-serif;
  font-weight: 400;
  color: white;
}
</style>
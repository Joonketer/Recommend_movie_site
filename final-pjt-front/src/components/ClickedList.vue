
<template>
  <div class="article-list text-center">
    <h3>방금 본 영화와 비슷한 영화</h3>
    <div v-if="nothing">정보없음</div>
    <div v-else>
      <div v-if="isLoading">Loading...</div>
      <div v-else>
        <div v-if="lastClickedPhoto">
          <b-card class="bg-dark text-white">
            <h4>방금 검색한 영화는?</h4>
            <br>
            <p class="card-text">{{ Movies_title }}</p>
            <br>
          </b-card>
        </div>
        <div v-else>
          <b-card class="bg-dark text-white">
            <p class="card-text">정보를 찾을 수 없습니다.</p>
          </b-card>
        </div>
        <div v-if="movie_list">
          <b-row>
            <div v-for="movie in movie_list" :key="movie.id" class="card-wrapper">
              <b-card class="movie-card bg-dark text-white h-100 d-flex align-items-stretch">
                <div v-if="movie_detail">
                  <b-card-img
                    :src="getBackdropUrl(movie.poster_path || movie.backdrop_path)"
                    alt="Backdrop Image"
                    @click="fetchDetail(movie.id); handleMovieClick(movie);"
                  ></b-card-img>
                </div>
                <div v-else>
                  <b-card-img
                    :src="getBackdropUrl(movie.poster_path || movie.backdrop_path)"
                    alt="Backdrop Image"
                    @click="fetchDetail(movie.id); handleMovieClick(movie);"
                  ></b-card-img>
                </div>
                <b-card-title class="movie-title">{{ movie.title }}</b-card-title>
                <b-card-text>{{ movie.id }}</b-card-text>
              </b-card>
            </div>
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
  name: "ClickedList",
  data() {
    return {
      nothing: false,
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
        .then(() => {
          // 처리 성공 시 로직
          // console.log(response.data);
        })
        .catch((error) => {
          // 에러 처리 로직
          console.error(error);
        });
    },
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
            // console.log(photos[0]);

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
          this.nothing = true;
          this.isLoading = false;
        });
    },

    fetchMoviesByMovie(movie_id) {
      const API_URL = `http://127.0.0.1:8000/api/v1/movies/${movie_id}/`;
      axios
        .get(API_URL)
        .then((response) => {
          const movies = response.data.title;

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
.article-list {
  text-align: start;
  flex-direction: column;
}
ul {
  margin-left: 1rem;
}
.card-wrapper {
  width: 500px;
  padding-left: 8px;
  margin-left: 50px;
  padding-bottom:20px;
}
.movie-poster {
  position: relative;
}
.movie-card {
  position: relative;
  box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);
  transition: 0.3s;
  width: 100%;
  border-radius: 5px;
  padding: 2%;
  margin-bottom: 2rem;
  padding:0;
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
  top: 60%;
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
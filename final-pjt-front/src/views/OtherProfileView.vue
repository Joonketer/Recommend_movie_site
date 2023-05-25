<template>
  <b-container fluid class="d-flex align-items-center justify-content-center vh-100 bg-#333 text-white">
    <b-card class="text-white bg-dark" style="width: 30rem;">
      <h1 class="text-center">{{ profileInfo && profileInfo.username }}님의 프로필</h1>
      
      <b-card-body>

        <p>팔로잉: {{ profileInfo && profileInfo.followings && profileInfo.followings.length }}     <button v-if="isLogin && !isFollowing" @click="followUser">팔로우</button>
    <button v-if="isLogin && isFollowing" @click="unfollowUser">
      언팔로우
    </button></p>
        <hr />

        <!-- <li v-for="following in profileInfo.followings" :key="following.id">
          {{ following.following }}
          </li>
        <hr> -->

        <p>팔로워: {{ profileInfo && profileInfo.followers && profileInfo.followers.length }}</p>
        <hr />

        <!-- <li v-for="follower in profileInfo.followers" :key="follower.id">
          {{ follower.follower }}
          </li>
        <hr> -->

        <p>좋아요 수: {{ profileInfo && profileInfo.like_boards && profileInfo.like_boards.length }}</p>
        <hr/>
        
        <li v-for="board in profileInfo && profileInfo.like_boards" :key="board.id">
      {{ board.title }} : {{ board.content }}
    </li>
    <hr>
        
    <p>게시물 수: {{ profileInfo && profileInfo.boards && profileInfo.boards.length }}</p>
    <hr />

    <li v-for="board in profileInfo && profileInfo.boards" :key="board.id">
      {{ board.title }} : {{ board.content }}
    </li>
    <hr>

    <p>좋아요 댓글 수: {{ profileInfo && profileInfo.like_comments && profileInfo.like_comments.length }}</p>
    <hr />
    <li v-for="comment in profileInfo && profileInfo.like_comments" :key="comment.id">
      {{ comment.content }}
    </li>
    <hr>

    <p>댓글 수: {{ profileInfo && profileInfo.comments && profileInfo.comments.length }}</p>
    <div>
      <li v-for="comment in profileInfo && profileInfo.comments" :key="comment.id" >
        {{ comment.content }}
      </li>
      <hr>
    </div>

    <!-- 좋아요 영화 수 , 좋아요 한 영화 목록  -->
    <p>좋아요 영화 수: {{ profileInfo && profileInfo.like_movies && profileInfo.like_movies.length }}</p>
    <hr>
    <div v-for="movie in profileInfo.like_movies" :key="movie.id">
        <li @click="checkMovieExistence(movie)" class="movie-item">{{ movie.title }},</li>
      </div>
        <hr />
      </b-card-body>
    </b-card>
  </b-container>
</template>

<script>
import { mapState } from "vuex";
import axios from "axios";
export default {
  props: {
    username: {
      type: String,
      required: true,
    },
  },
  computed: {
    isLogin() {
      return this.$store.getters.isLogin;
    },
    isFollowing() {
      return this.profileInfo && this.profileInfo.following;
    },
    ...mapState(["profileInfo"]),
  },
  created() {
    this.$store.dispatch("getUserProfile", this.username);
  },
  methods: {
    checkMovieExistence(movie) {
      const movieId = movie.id;
      const API_URL = `http://127.0.0.1:8000/api/v1/movies/${movieId}/exists/`;

      axios
        .get(API_URL)
        .then((response) => {
          const movieData = response.data;
          if (!movieData.exists) {
            // 선택한 영화가 존재하지 않을 경우에 대한 처리

            console.log("영화가 존재하지 않습니다.");
            this.addMovieToDatabase(movieId);
          } else {
            // 선택한 영화가 존재할 경우에 대한 처리
            console.log("영화가 존재합니다.");
            this.navigateToDetail(movieId);
          }
        })
        .catch((error) => {
          console.error("영화 존재 여부 확인 중 오류 발생:", error);
        });
    },
    addMovieToDatabase(movie_id) {
      // 데이터베이스에 영화를 추가하기 위해 API 요청을 수행합니다.
      const API_URL = `http://127.0.0.1:8000/api/v1/movies/`;

      const movie_detail = this.searchResults.find(
        (movie) => movie.id === movie_id
      );

      if (!movie_detail) {
        console.error("영화 정보를 찾을 수 없습니다.");
        return;
      }

      const movieData = {
        movie_id: movie_detail.id,
        overview: movie_detail.overview,
        popularity: movie_detail.popularity,
        poster_path: movie_detail.poster_path,
        backdrop_path: movie_detail.backdrop_path,
        release_date: movie_detail.release_date,
        title: movie_detail.title,
        vote_average: movie_detail.vote_average,
        vote_count: movie_detail.vote_count,
        genre_ids: movie_detail.genres,
        // 필요한 다른 영화 정보도 추가할 수 있습니다.
      };

      axios
        .post(API_URL, movieData)
        .then(() => {
          console.log("영화를 데이터베이스에 추가했습니다.");
          this.navigateToDetail(movie_id);
        })
        .catch((error) => {
          alert("영화 데이터가 아닙니다");
          console.error("영화 추가 중 오류가 발생했습니다:", error);
        });
    },
    navigateToDetail(movie_id) {
      // 현재 위치와 동일한 위치로 이동하는 것을 피합니다.
      if (this.$router.currentRoute.params.id !== movie_id) {
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
      }
    },
    followUser() {
      this.$store
        .dispatch("followUser", this.username)
        .then(() => {
          console.log("유저를 팔로우했습니다.");
          this.$store.commit("SET_FOLLOWING", true); // 팔로우 상태 변경
        })
        .catch((error) => {
          console.error("유저 팔로우 중 오류가 발생했습니다.", error);
        });
    },
    unfollowUser() {
      this.$store
        .dispatch("unfollowUser", this.username)
        .then(() => {
          console.log("유저를 언팔로우했습니다.");
          this.$store.commit("SET_FOLLOWING", false); // 팔로우 상태 변경
        })
        .catch((error) => {
          console.error("유저 언팔로우 중 오류가 발생했습니다.", error);
        });
    },
  },
};
</script>

<style scoped>
.movie-item {
  cursor: pointer;
}
</style>
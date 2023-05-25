<template>
  <div class="profile">
    <h1>{{ userinfo.username }}님의 사용자 프로필</h1>
    <hr />
    <p>{{ userinfo.username }}님의 팔로잉: {{ userinfo.followings.length }}</p>
    <hr />
    <p>{{ userinfo.username }}님의 팔로워: {{ userinfo.followers.length }}</p>
    <hr />
    <p>{{ userinfo.username }}님의 좋아요 수: {{ userinfo.like_boards }}</p>
    <hr />
    <p>{{ userinfo.username }}님의 게시물 수: {{ userinfo.boards }}</p>
    <hr />
    <p>
      {{ userinfo.username }}님의 좋아요 댓글 수: {{ userinfo.like_comments }}
    </p>
    <hr />
    <p>{{ userinfo.username }}님의 댓글 수: {{ userinfo.comments }}</p>
    <hr />
    <div>
      {{ userinfo.username }}님의 좋아요 영화 수:
      <div v-for="movie in userinfo.like_movies" :key="movie.id">
        <span @click="checkMovieExistence(movie)">{{ movie.title }},</span>
      </div>
    </div>
    <div>
      <h1>가입된 사용자 목록</h1>
      <ul>
        <li v-for="user in randomUsers" :key="user.id">
          <router-link :to="`/profile/${user.username}`">{{
            user.username
          }}</router-link>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
import { mapState } from "vuex";
import axios from "axios";
export default {
  data() {
    return {
      users: [],
    };
  },
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
      return this.userinfo && this.userinfo.following === true;
    },
    ...mapState(["userinfo"]),
    randomUsers() {
      const shuffledUsers = [...this.users].sort(() => Math.random() - 0.5);
      return shuffledUsers.slice(0, 5);
    },
  },
  created() {
    if (this.isLogin) {
      this.$store.dispatch("getMyProfile");
      this.fetchUsers();
      this.getArticles();
    } else {
      alert("로그인이 필요한 페이지입니다...");
      this.$router.push({ name: "LogInView" });
    }
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
    fetchUsers() {
      axios
        .get("http://127.0.0.1:8000/profile/allusers/check/") // Django API 엔드포인트를 설정하세요
        .then((response) => {
          this.users = response.data;
        })
        .catch((error) => {
          console.error(error);
        });
    },
  },
};
</script>

<style>
</style>

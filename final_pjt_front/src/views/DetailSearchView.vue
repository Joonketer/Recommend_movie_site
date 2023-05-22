<template>
  <div>
    <h1>Detail</h1>
    <p>글 번호: {{ movieDetail?.id }}</p>
    <p>제목: {{ movieDetail?.title }}</p>
    <p>내용: {{ movieDetail?.overview }}</p>
    <p>개봉일: {{ movieDetail?.release_date }}</p>
    <p>장르: {{ movieDetail?.genres }}</p>
    <p>
      포스터:
      <img
        :src="getBackdropUrl(movieDetail?.poster_path)"
        alt="Backdrop Image"
      />
    </p>
    <!-- 영화 좋아요 버튼 -->
    <button @click="likeMovie(article.movie_id)">
      좋아요 {{ article?.like_users.length || 0 }}개
    </button>
    <hr />
    <!-- 리뷰 작성 폼 -->
    <form @submit.prevent="submitReview">
      <textarea
        v-model="reviewContent"
        placeholder="리뷰를 작성하세요"
      ></textarea>
      <label for="user_vote_average">평점:</label>
      <select id="user_vote_average" v-model="user_vote_average">
        <option value="1">1점</option>
        <option value="2">2점</option>
        <option value="3">3점</option>
        <option value="4">4점</option>
        <option value="5">5점</option>
      </select>
      <p>작성자: {{ currentUser }}</p>
      <button type="submit">리뷰 작성</button>
    </form>

    <!-- 작성된 리뷰 목록 -->
    <div v-if="movieDetail.reviews && movieDetail.reviews.length > 0">
      <h2>리뷰 목록</h2>
      <ul>
        <li v-for="review in movieDetail.reviews" :key="review.id">
          {{ review.content }} - 평점: {{ review.user_vote_average }} - 작성자:
          {{ review.user }}
        </li>
      </ul>
    </div>
    <div v-else>
      <p>리뷰가 없습니다.</p>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { mapState } from "vuex";

const API_URL = "http://127.0.0.1:8000";
export default {
  name: "DetailSearchView",
  data() {
    return {
      movieDetail: null,
      reviewContent: "",
      user_vote_average: 1,
      currentUser: "",
      user_id: null,
    };
  },
  computed: {
    ...mapState(["token"]),
  },
  created() {
    this.getCurrentUser();
    const movieDetailParam = this.$route.query.movieDetail;
    if (movieDetailParam) {
      this.movieDetail = JSON.parse(movieDetailParam);
    }
  },
  methods: {
    likeMovie(movieId) {
      axios({
        method: "post",
        url: `${API_URL}/api/v1/movies/${movieId}/like/`,
        headers: { Authorization: `Token ${this.token}` },
      })
        .then(() => {
          this.getArticleDetail();
        })
        .catch((err) => {
          console.log(err);
        });
    },
    getBackdropUrl(backdropPath) {
      const baseUrl = "https://image.tmdb.org/t/p/original";
      return `${baseUrl}${backdropPath}`;
    },
    getCurrentUser() {
      axios({
        method: "get",
        url: `${API_URL}/accounts/user/`,
        headers: { Authorization: `Token ${this.token}` },
      })
        .then((res) => {
          console.log("로그인");
          console.log(res);
          this.currentUser = res.data.username;
          this.user_id = res.data.pk;
        })
        .catch((err) => {
          console.log(err);
        });
    },
    submitReview() {
      console.log("아이디", this.user_id);
      console.log("무비아이디", this.movieDetail?.id);
      if (this.reviewContent) {
        const movie_id = this.movieDetail?.id;
        const content = this.reviewContent;
        const user_vote_average = this.user_vote_average;
        const user_id = this.user_id;

        const payload = {
          movie_id,
          content,
          user_vote_average,
          user_id,
        };
        console.log(payload);
        axios({
          method: "post",
          url: `${API_URL}/api/v1/movies/search/`,
          headers: {
            Authorization: `Token ${this.token}`,
          },
          data: payload,
        })
          .then(() => {
            this.fetchDetail(this.movieDetail?.id);
            this.reviewContent = "";
            this.user_vote_average = 1;
          })
          .catch((err) => {
            console.log(err);
          });
      }
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
          this.movieDetail = response.data;

          console.log("영화 디테일");
          console.log(this.movieDetail);
        })
        .catch((error) => {
          console.error("Error fetching movie:", error);
        });
    },
  },
};
</script>

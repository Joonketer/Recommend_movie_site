<template>
  <div>
    <h1>Detail</h1>
    <p>여기: {{ article }}</p>
    <p>글 번호: {{ article?.movie_id }}</p>
    <p>제목: {{ article?.title }}</p>
    <p>내용: {{ article?.overview }}</p>
    <p>개봉일: {{ article?.release_date }}</p>
    <p>장르: {{ article?.genre_ids }}</p>
    <p>
      포스터:
      <img
        :src="getBackdropUrl(article?.poster_path || article?.backdrop_path)"
        alt="Backdrop Image"
      />
    </p>
    <!-- 영화 좋아요 버튼 -->
    <button @click="likeMovie(article.id)">
      좋아요
      {{
        (Array.isArray(article?.like_users) && article?.like_users.length) || 0
      }}개
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
    <hr />

    <!-- 작성된 리뷰 목록 -->
    <div v-if="article.reviews && article.reviews.length > 0">
      <h2>리뷰 목록</h2>
      <ul>
        <li v-for="review in article.reviews" :key="review.id">
          {{ review.content }} - 평점: {{ review.user_vote_average }} - 작성자:
          {{ review.user }}
          <button @click="likeReview(review.id)">
            좋아요
            {{
              (Array.isArray(review?.like_users) && review.like_users.length) ||
              0
            }}개
          </button>
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
  created() {
    this.getArticles();
    this.getCurrentUser(); // 현재 로그인된 사용자 정보를 가져오는 메소드 호출
    this.getArticleDetail();
    // $route.params에서 전달된 movieData 객체를 가져옵니다.
    // this.article = this.$route.params;
  },
  data() {
    return {
      article: {},
      reviewContent: "",
      user_vote_average: 1,
      currentUser: "", // 현재 로그인된 사용자 이름
      user_id: null,
    };
  },
  computed: {
    isLogin() {
      return this.$store.getters.isLogin; // 로그인 여부
    },
    ...mapState(["token"]),
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
    likeReview(reviewId) {
      axios({
        method: "post",
        url: `${API_URL}/api/v1/reviews/${reviewId}/like/`,
        headers: { Authorization: `Token ${this.token}` },
      })
        .then(() => {
          this.getArticleDetail();
        })
        .catch((err) => {
          console.log(err);
        });
    },
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
    getArticleDetail() {
      axios({
        method: "get",
        url: `${API_URL}/api/v1/movies/${this.$route.params.id}/`,
      })
        .then((res) => {
          console.log(res);
          this.article = res.data;
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
      // 현재 로그인된 사용자 정보를 가져오는 API 호출
      axios({
        method: "get",
        url: `${API_URL}/accounts/user/`, // 사용자 정보를 반환하는 API 엔드포인트
        headers: { Authorization: `Token ${this.token}` },
      })
        .then((res) => {
          this.currentUser = res.data.username; // 사용자 이름을 데이터에 저장
          this.user_id = res.data.pk;

          // 사용자 정보를 가져온 후에 리뷰를 가져오는 메소드 호출
          this.getArticleDetail();
        })
        .catch((err) => {
          console.log(err);
        });
    },
    submitReview() {
      if (this.reviewContent) {
        const formData = new FormData();
        formData.append("movie", this.article.id);
        formData.append("content", this.reviewContent);
        formData.append("user_vote_average", this.user_vote_average);
        formData.append("user_id", this.user_id);

        axios({
          method: "post",
          url: `${API_URL}/api/v1/movies/${this.article?.id}/review/`,
          headers: { Authorization: `Token ${this.token}` },
          data: formData,
        })
          .then(() => {
            this.getArticleDetail();
            this.reviewContent = "";
            this.user_vote_average = 1;
          })
          .catch((err) => {
            console.log(err);
          });
      }
    },
  },
};
</script>

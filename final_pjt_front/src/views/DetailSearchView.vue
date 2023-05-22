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

axios.defaults.xsrfCookieName = "csrftoken"; // Django에서 설정한 CSRF 토큰 쿠키 이름
axios.defaults.xsrfHeaderName = "X-CSRFToken"; // Django에서 설정한 CSRF 토큰을 전송할 헤더 이름

const API_URL = "http://127.0.0.1:8000";
export default {
  name: "DetailSearchView",
  data() {
    return {
      movieDetail: null,
      reviewContent: "",
      user_vote_average: 1,
      currentUser: "", // 현재 로그인된 사용자 이름
      user_id: null,
      csrftoken: "", // CSRF 토큰 값
    };
  },
  computed: {
    ...mapState(["token"]),
  },
  created() {
    this.getCurrentUser(); // 현재 로그인된 사용자 정보를 가져오는 메소드 호출
    const movieDetailParam = this.$route.query.movieDetail;
    if (movieDetailParam) {
      this.movieDetail = JSON.parse(movieDetailParam);
    }
    this.setCSRFToken(); // CSRF 토큰 값을 설정하는 메소드 호출
  },
  methods: {
    setCSRFToken() {
      // Django에서 제공하는 csrf_token 템플릿 태그를 사용하여 CSRF 토큰 값을 가져옴
      const csrfToken = document
        .getElementsByName("csrfmiddlewaretoken")[0]
        .getAttribute("value");
      this.csrftoken = csrfToken; // CSRF 토큰 값을 데이터에 저장
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
          console.log("로그인");
          console.log(res);
          this.currentUser = res.data.username; // 사용자 이름을 데이터에 저장
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
        const movie = this.movieDetail?.id;
        const content = this.reviewContent;
        const user_vote_average = this.user_vote_average;
        const user_id = this.user_id;

        const payload = {
          movie,
          content,
          user_vote_average,
          user_id,
        };
        console.log(payload);
        axios({
          method: "post",
          url: `${API_URL}/api/v1/movies/search/review/`,
          headers: {
            Authorization: `Token ${this.token}`,
            "X-CSRFToken": this.csrftoken, // CSRF 토큰 값을 헤더에 추가
          },
          data: payload,
        })
          .then(() => {
            this.fetchDetail(this.movieDetail.id);
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
          this.movie_detail = response.data;

          console.log("영화 디테일");
          console.log(this.movie_detail);

          // 영화 정보를 가져온 후에 router-link를 사용하여 이미지를 렌더링합니다.
          // 이로써 movie.id가 null이 되지 않습니다.
        })
        .catch((error) => {
          console.error("Error fetching movie:", error);
        });
    },
  },
};
</script>

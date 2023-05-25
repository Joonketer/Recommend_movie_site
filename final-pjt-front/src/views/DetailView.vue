<template>
  <div class="container">
    <h1>Movie Detail</h1>
    <div class="movie-details">
      <div class="movie-poster">
        <img
          :src="getBackdropUrl(article?.poster_path || article?.backdrop_path)"
          alt="Backdrop Image"
        />
      </div>
      <div class="movie-info">
        <p>영화 번호: {{ article?.movie_id }}</p>
        <p>제목: {{ article?.title }}</p>
        <p>내용: {{ article?.overview }}</p>
        <p>개봉일: {{ article?.release_date }}</p>
        <p>
          장르:
          <span v-for="(genre, index) in article.genre_ids" :key="index">
            {{ genre.genre_name
            }}{{ index < article.genre_ids.length - 1 ? ", " : "" }}
          </span>
        </p>
        <!-- 영화 좋아요 버튼 -->
        <button @click="likeMovie(article.id)">
          좋아요
          {{
            (Array.isArray(article?.like_users) &&
              article?.like_users.length) ||
            0
          }}개
        </button>
      </div>
    </div>
    <p>예고편:</p>
    <div v-if="trailerId">
      <iframe
        :src="'https://www.youtube.com/embed/' + trailerId"
        frameborder="0"
        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
        allowfullscreen
      ></iframe>
    </div>
    <div v-else>
      <p>예고편이 없습니다.</p>
    </div>

    <!-- 리뷰 작성 폼 -->
    <div class="review-area">
    <form @submit.prevent="submitReview"  class="review-form">
      <p>작성자: {{ currentUser }}</p>
      <label for="user_vote_average">평점:</label>
      <select id="user_vote_average" v-model="user_vote_average">
        <option value="1">1점 ★</option>
        <option value="2">2점 ★★</option>
        <option value="3">3점 ★★★</option>
        <option value="4">4점 ★★★★</option>
        <option value="5">5점 ★★★★★</option>
      </select>
      <br />
      <div class="form-group">
        <textarea
          v-model="reviewContent"
          placeholder="리뷰를 작성하세요"
        ></textarea>
        <button type="submit">작성</button>
      </div>
    </form>
    <hr />

    <hr />
    <!-- 작성된 리뷰 목록 -->
    <div class="writtenReviews">
      <div v-if="article.reviews && article.reviews.length > 0">
        <h2>리뷰 목록</h2>
        <ul>
          <li v-for="review in article.reviews" :key="review.id">
            {{ review.content }}  | 
            평점:
            <span
              v-for="star in getStars(review.user_vote_average)"
              :key="star"
              class="star"
              >★</span> |
             작성자:
            {{ review.user.username }}
            <button @click="likeReview(review.id)">
              좋아요
              {{
                (Array.isArray(review?.like_users) &&
                  review.like_users.length) ||
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
  </div>
</div>
</template>


<script>
import axios from "axios";
import { mapState } from "vuex";
const API_URL = "http://127.0.0.1:8000";

export default {
  name: "DetailView",
  data() {
    return {
      article: {},
      reviewContent: "",
      user_vote_average: 1,
      currentUser: "", // 현재 로그인된 사용자 이름
      user_id: null,
      trailerId: "",
    };
  },
  computed: {
    isLogin() {
      return this.$store.getters.isLogin; // 로그인 여부
    },
    ...mapState(["token"]),
  },
  created() {
    this.getArticles();
    this.getCurrentUser(); // 현재 로그인된 사용자 정보를 가져오는 메소드 호출
    this.getArticleDetail();
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
    fetchTrailer() {
      const YOUTUBEAPIKEY = "AIzaSyBynVLUf5yjYB01BF3oODlyJeEKhOcKKiQ"; // replace with your YouTube API key
      const movieTitle = this.article.title; // replace with the actual movie title
      if (movieTitle === undefined) {
        console.log("제목없음");
        return;
      }
      const searchUrl = `https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=1&q=${movieTitle}+trailer&type=video&key=${YOUTUBEAPIKEY}`;
      axios
        .get(searchUrl)
        .then((res) => {
          console.log(res);
          if (res.data.items.length > 0) {
            this.trailerId = res.data.items[0].id.videoId;
          }
        })
        .catch((err) => {
          console.error("Error fetching YouTube video", err);
        });
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
        .then((res) => {
          console.log(res);
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
          this.fetchTrailer();
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
        formData.append("movie", this.article.movie_id);
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
    getStars(count) {
      return Array(count).fill("★");
    },
  },
};
</script>
<style scoped>
/* .detail-container {
  font-family: 'Nanum Gothic', sans-serif;
  background-color: #333;
  color: #fff;
} */
.container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background-color: #fff;
  padding: 20px;
  /* color: #333; */
  font-family: "Nanum Gothic", sans-serif;
  background-color: #333;
  color: #fff;
}
.review-area {
  display: flex; /* form과 writtenReviews가 동일한 y축을 공유하도록 설정 */
  flex-direction: column;
  justify-content: space-between; /* form과 writtenReviews 사이에 공간을 균등하게 배분 */
  align-items: start; /* form과 writtenReviews의 y축 시작 위치를 동일하게 설정 */
  width: 80%; /* form과 writtenReviews의 너비 합이 80%가 되도록 설정 */
  padding: 20px 0; /* form과 writtenReviews 주위에 패딩 추가 */
}
.review-form {
  flex: 1; /* form이 가능한 모든 공간을 차지하도록 설정 */
  /* ... */
}
iframe {
  width: 1000px;
  height: 750px;
}

.movie-details {
  display: flex;
  justify-content: space-between;
  width: 80%;
}

.movie-poster img {
  width: 400px;
  height: auto;
  padding: 15px;
}

.movie-info {
  display: flex;
  flex-direction: column;
  justify-content: center;
  width: 60%;
}

form,
.review-section {
  padding-right: 60px;
  margin-left: 15px;
  justify-content: left;
}
form {
  width: 720px;
  flex-direction: column;
  align-items: flex-start;
}
.form-group {
  display: flex;
  align-items: stretch; /* textarea와 버튼이 같은 높이를 가지도록 합니다. */
}
.form-group textarea {
  flex: 1; /* textarea가 가능한 모든 공간을 차지하도록 합니다. */
  min-height: 100px; /* textarea의 최소 높이를 설정합니다. 원하는대로 조절하실 수 있습니다. */
  margin-right: 10px; /* textarea와 버튼 사이의 간격을 설정합니다. */
  width: 100%;
}

.form-group button {
  flex-shrink: 0; /* 버튼 크기가 줄어드는 것을 방지합니다. */
  width: 50px; /* 버튼의 너비를 설정합니다. 원하는대로 조절하실 수 있습니다. */
}

.writtenReviews {
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  padding-right: 220px;
  width: 100%; /* div.writtenReviews의 너비를 늘립니다. */
}
.writtenReviews li {
  display: flex;
  flex-direction: row;
  width: 1600px; /* li 항목의 너비를 자동으로 설정합니다. */
  /* ... */
}
</style>
<template>
  <div>
    <h1>Detail</h1>
    <p>글 번호 : {{ article?.movie_id }}</p>
    <p>제목 : {{ article?.title }}</p>
    <p>내용 : {{ article?.overview }}</p>
    <p>개봉일 : {{ article?.release_date }}</p>
    <p>장르 : {{ article?.genre_ids }}</p>
    <p>
      포스터 :
      <img :src="getBackdropUrl(article?.backdrop_path)" alt="Backdrop Image" />
    </p>
  </div>
</template>

<script>
import axios from "axios";
const API_URL = "http://127.0.0.1:8000";

export default {
  name: "DetailView",
  data() {
    return {
      article: null,
    };
  },
  created() {
    this.getArticleDetail();
  },
  methods: {
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
  },
};
</script>

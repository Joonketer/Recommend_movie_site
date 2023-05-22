<template>
  <div>
    <h5>{{ article.id }}</h5>
    <p>{{ article.title }}</p>
    <router-link
      :to="{
        name: 'DetailView',
        params: { id: article.movie_id },
      }" 
    >
    <button @click="handleMovieClick(article)">
      [DETAIL]
    </button>
    </router-link>
    <hr />
  </div>
</template>

<script>
import axios from "axios";
import { mapState } from "vuex";

export default {
  name: "ArticleListItem",
  props: {
    article: Object,
  },
  computed: {
    ...mapState(["token"]),
  },
  methods: {
    handleMovieClick(article) {
      const payload = {
      movie: article.movie_id,
      genre_ids: article.genre_ids.map(genre => genre.genre_id),
    };

      // 서버로 영화 클릭 정보 전송
      axios.post('http://127.0.0.1:8000/api/v1/recent_moives/', payload,{headers: {
          Authorization: `Token ${this.token}`,
        },})
        .then(response => {
          // 처리 성공 시 로직
          console.log(response.data);
        })
        .catch(error => {
          // 에러 처리 로직
          console.error(error);
        });
      }
  }
};
</script>

<style>
</style>

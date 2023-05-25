<template>
  <div
    class="movie-card"
    @mouseenter="hovering = true"
    @mouseleave="hovering = false"
  >
    <router-link
      :to="{
        name: 'DetailView',
        params: { id: article.movie_id },
      }"
    >
      <div class="movie-poster" @click="handleMovieClick(article)">
        <img
          :src="'https://image.tmdb.org/t/p/w500' + article.poster_path"
          alt="Movie poster"
        />
        <h5 v-show="hovering" class="movie-title">
          {{ article.title }}
          <br />
          ★ : {{ article.vote_average }}
        </h5>
      </div>
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
  data() {
    return {
      hovering: false,
    };
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
        });
    },
  },
};
</script>


<style scoped>
.movie-card {
  position: relative;
  box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);
  transition: 0.3s;
  width: 30%;
  border-radius: 5px;
  padding: 2%;
  margin-bottom: 2rem;
}
.movie-poster {
  position: relative;
}
.movie-card img {
  width: 100%;
  height: auto;
  transition: opacity 0.3s ease-in-out;
}
.movie-card:hover img {
  opacity: 0.5;
}
.movie-card .movie-poster {
  position: relative;
}
.movie-card:hover {
  box-shadow: 0 8px 16px 0 rgba(0, 0, 0, 0.2);
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
  top: 50%;
  left: 50%;
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


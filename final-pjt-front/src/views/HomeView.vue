<template>
  <div>
<<<<<<< HEAD:final-pjt-front/src/views/HomeView.vue
=======
    <h1>home page</h1>
    <br />
>>>>>>> 9faf8fac298b3c987e01663d3941a22f084d3d49:final_pjt_front/src/views/HomeView.vue
    <MovieList />
  </div>
</template>

<script>
import MovieList from "@/components/MovieList.vue";
export default {
  name: "HomeView",
  components: {
    MovieList,
  },
  computed: {
    isLogin() {
      return this.$store.getters.isLogin;
    },
  },
  created() {
    this.getMovies();
  },
  methods: {
    getMovies() {
      if (this.isLogin) {
        this.$store.dispatch("getMovies");
      } else {
        alert("로그인이 필요한 페이지입니다...");
        this.$router.push({ name: "LogInView" });
      }
    },
  },
};
</script>

<style>
</style>
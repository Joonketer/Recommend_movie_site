<template>
  <div>
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
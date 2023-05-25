<template>
  <div>
    <h1>영화 추천 페이지</h1>
    <RecommendList />
    <hr>
    <ClickedList />
    <hr />
    <WeatherList />
  </div>
</template>

<script>
import RecommendList from "@/components/RecommendList.vue";
import WeatherList from "@/components/WeatherList.vue";
import ClickedList from "@/components/ClickedList.vue";
export default {
  name: "RecommendView",
  components: {
    RecommendList,
    WeatherList,
    ClickedList
  },
  computed: {
    isLogin() {
      return this.$store.getters.isLogin; // 로그인 여부
    },
  },

  created() {
    this.getPhotos();
  },
  methods: {
    getPhotos() {
      if (this.isLogin) {
        this.$store.dispatch("getPhotos");
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
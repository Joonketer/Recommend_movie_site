<template>
  <div>
    <div class="d-flex align-items-center justify-content-center bg-#333 text-white">
    <h1>추천영화</h1>
  </div>
   <hr>
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
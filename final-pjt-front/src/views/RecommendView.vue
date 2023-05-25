<template>
  <div>
<<<<<<< HEAD:final-pjt-front/src/views/RecommendView.vue
    <div class="d-flex align-items-center justify-content-center bg-#333 text-white">
    <h1>추천영화</h1>
  </div>
   <hr>
=======
    <h1>영화 추천 페이지</h1>
>>>>>>> 9faf8fac298b3c987e01663d3941a22f084d3d49:final_pjt_front/src/views/RecommendView.vue
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
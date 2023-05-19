<template>
  <div>
    <h1>추천페이지입니다</h1>
    <RecommendList />
  </div>
</template>

<script>
import RecommendList from "@/components/RecommendList.vue";

export default {
  name: "RecommendView",
  components: {
    RecommendList,
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
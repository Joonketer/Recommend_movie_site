<template>
  <div>
    <h1>BoxOffice</h1>
    <br />
    <hr />
    <h2>DailyBoxOffice</h2>
    <DailyBoxoffice />
    <hr />
    <h2>WeeklyBoxOffice</h2>
    <WeeklyBoxoffice />
  </div>
</template>
  
  <script>
import DailyBoxoffice from "@/components/DailyBoxoffice.vue";
import WeeklyBoxoffice from "@/components/WeeklyBoxoffice.vue";

export default {
  components: {
    DailyBoxoffice,
    WeeklyBoxoffice,
  },
  computed: {
    isLogin() {
      return this.$store.getters.isLogin; // 로그인 여부
    },
  },
  created() {
    this.getArticles();
  },
  methods: {
    getArticles() {
      if (this.isLogin) {
        this.$store.dispatch("getArticles");
      } else {
        alert("로그인이 필요한 페이지입니다...");
        this.$router.push({ name: "LogInView" });
      }
    },
  },
};
</script>
  
  <style>
/* Add your custom styles here */
</style>
  
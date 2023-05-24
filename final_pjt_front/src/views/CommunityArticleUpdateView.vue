<template>
  <div>
    <h1>게시글 수정</h1>
    <form @submit.prevent="updateBoard">
      <label for="title">제목 : </label>
      <input type="text" id="title" v-model.trim="title" /><br />
      <label for="content">내용 : </label>
      <textarea id="content" cols="30" rows="10" v-model="content"></textarea
      ><br />
      <input type="submit" id="submit" />
    </form>
  </div>
</template>
  
<script>
import axios from "axios";
import { mapState } from "vuex";
const API_URL = "http://127.0.0.1:8000";

export default {
  name: "UpdateView",
  data() {
    return {
      title: null,
      content: null,
    };
  },
  computed: {
    ...mapState(["token"]),
    isLogin() {
      return this.$store.getters.isLogin; // 로그인 여부
    },
  },
  created() {
    this.getArticles();
    const id = this.$route.params.id;
    axios({
      method: "get",
      url: `${API_URL}/api/v1/community/boards/${id}/`,
    })
      .then((res) => {
        this.title = res.data.title;
        this.content = res.data.content;
      })
      .catch((err) => {
        console.log(err);
      });
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
    updateBoard() {
      const id = this.$route.params.id;
      axios({
        method: "PUT",
        url: `${API_URL}/api/v1/community/boards/${id}/`,
        data: { title: this.title, content: this.content },
        headers: { Authorization: `Token ${this.token}` },
      })
        .then(() => {
          this.$router.push({
            name: "CommunityArticleDetailView",
            params: { id: id },
          });
        })
        .catch((err) => {
          console.log(err);
        });
    },
  },
};
</script>

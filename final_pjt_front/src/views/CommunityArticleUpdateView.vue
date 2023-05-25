<template>
<b-container class="d-flex align-items-center justify-content-center vh-100">
  <b-card border-variant="light" class="bg-dark" style="width: 30rem;">
    <h1 class="text-center variant-dark">게시글 수정</h1>
    <b-card-body>
      <form @submit.prevent="updateBoard">
        <b-form-group label-for="title">
          <label class="form-label">제목 :</label>
          <b-form-input id="title" v-model.trim="title" />
        </b-form-group>
        
        <b-form-group label-for="content">
          <label class="form-label">내용 :</label>
          <b-form-textarea id="content" cols="30" rows="10" v-model="content" />
        </b-form-group>
        
        <div class="d-flex justify-content-center">
          <b-button type="submit" variant="success" id="submit">제출</b-button>
        </div>
        <router-link to="/community">Back to Community</router-link><br />
      </form>
    </b-card-body>
  </b-card>
</b-container>
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

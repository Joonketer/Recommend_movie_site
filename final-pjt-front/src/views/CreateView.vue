<template>
  <b-container fluid class="d-flex align-items-center justify-content-center vh-100 bg-dark text-white">
    <b-card  border-variant=light class="text-white bg-dark " style="width: 50rem; ">
      <h1 class="text-center">게시글 작성</h1>
      <b-card-body>
        <form @submit.prevent="createArticle">
          <b-form-group label="카테고리 : " label-for="type" label-class="text-white">
            <b-form-select id="type" v-model="type">
              <option value="talk">Talk</option>
              <option value="review">Review</option>
            </b-form-select>
          </b-form-group>

          <b-form-group label="제목 : " label-for="title" label-class="text-white">
            <b-form-input id="title" v-model.trim="title"></b-form-input>
          </b-form-group>

          <b-form-group label="내용 : " label-for="content" label-class="text-white">
            <b-form-textarea id="content" cols="30" rows="10" v-model="content"></b-form-textarea>
          </b-form-group>

          <div class="d-flex justify-content-center">
            <b-button type="submit" variant="light">Submit</b-button>
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
  name: "CreateView",
  data() {
    return {
      title: null,
      content: null,
      type: "talk",
    };
  },
  computed: {
    isLogin() {
      return this.$store.getters.isLogin; // 로그인 여부
    },
    ...mapState({
      token: (state) => state.token,
    }),
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

      // 로그인이 되어 있으면 getArticles action 실행
      // 로그인 X라면 login 페이지로 이동
    },
    createArticle() {
      const title = this.title;
      const content = this.content;
      const board_type = this.type === "talk" ? 0 : 1;

      if (!title) {
        alert("제목 입력해주세요");
        return;
      } else if (!content) {
        alert("내용 입력해주세요");
        return;
      }
      axios({
        method: "post",
        url: `${API_URL}/api/v1/community/boards/`,
        data: { title, content, board_type },
        //이 부분은 백엔드에서 요청하는 부분이므로 백엔드와 같은 항목명이어야 함
        headers: { Authorization: `Token ${this.token}` },
      })
        .then(() => {
          // console.log(res)
          this.$router.push({ name: "CommunityView" });
        })
        .catch((err) => {
          console.log(err);
        });
    },
  },
};
</script>
<style scoped>
.form-container {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.create-article-form {
  width: 80%;
}
</style>

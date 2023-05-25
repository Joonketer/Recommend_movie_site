<template>
  <div class="community-board-container d-flex">
    <div class="community-board-title d-flex justify-content-center">
    <h1>Community Board</h1>
    </div>
    <hr/>
    <div class="table d-flex justify-content-center color-light">
    <table>
      <thead>
        <tr>
          <th>ID</th> 
          <th>작성자</th> 
          <th>Title</th> 
          <th>Board Type</th> 
          <th>Created At</th> 
          <th>Updated At</th> 
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="Communityarticle in Communityarticles"
          :key="Communityarticle.id"
        >
          <td>{{ Communityarticle.id }}</td>
          <td>{{ Communityarticle.user.username }}</td>
          <td>
            <router-link
              :to="{
                name: 'CommunityArticleDetailView',
                params: { id: Communityarticle.id },
              }"
            >
              {{ Communityarticle.title }}
            </router-link>
          </td>
          <td>
            <span v-if="Communityarticle.board_type == 0">Talk</span>
            <span v-else-if="Communityarticle.board_type == 1">Review</span>
          </td>
          <td>
            {{ new Date(Communityarticle.created_at).toLocaleDateString() }}
          </td>
          <td>
            {{ new Date(Communityarticle.updated_at).toLocaleDateString() }}
          </td>
        </tr>
      </tbody>
    </table>
    </div>
    <div class="create-article-thing d-flex justify-content-end">
    <router-link :to="{ name: 'CreateView' }">[게시글 작성]</router-link>
  </div>
  </div>
</template>
<script>
import axios from "axios";
const API_URL = "http://127.0.0.1:8000";

// import { mapGetters } from 'vuex';
export default {
  name: "CommunityView",
  data() {
    return {
      Communityarticles: [],
    };
  },
  computed: {
    isLogin() {
      return this.$store.getters.isLogin; // 로그인 여부
    },
  },
  created() {
    this.getArticles();
    axios({
      method: "get",
      url: `${API_URL}/api/v1/community/boards/`,
    })
      .then((res) => {
        this.Communityarticles = res.data;
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

      // 로그인이 되어 있으면 getArticles action 실행
      // 로그인 X라면 login 페이지로 이동
    },
  },
};
</script>

<style scoped>
.community-board-container {
  display: flex;
  flex-direction:column;
  justify-content: center;
  align-items: center;
  width: 80%;
  height: 80%;
  margin: auto;
  background-color: #333; /* replace this with the color you want */
  border: 2px solid #ddd; /* replace this with the color you want */
  border-radius: 5px;
  color: #f5f5f5; /* a color close to white */
}
.community-board-container tr, 
.community-board-container th, 
.community-board-container td {
  color: #f5f5f5; /* a color close to white */
}
a{
  color: #f5f5f5; /* a color close to white */
}
</style>

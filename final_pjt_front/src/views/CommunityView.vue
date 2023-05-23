<template>
  <div>
    <h1>Community Board</h1>
    <hr />
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
    <router-link :to="{ name: 'CreateView' }">[게시글 작성]</router-link>
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
  created() {
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
  // computed: {
  //     ...mapGetters(['isLogin']),
  // },
  // beforeCreate(){
  //     if(!this.isLogin){
  //         this.$router.push({name: 'LogInView' });
  //     }
  // },
};
</script>

<style>
/* 작성 시 에러코드 403 해결, 따로 연결하기, 작성글 id 발급하기 등등 해결할 게 많음 */
</style>
<template>
  <div class="profile">
    <h1>{{ profileInfo.username }}님의 사용자 프로필</h1>
    <button v-if="isLogin && !isFollowing" @click="followUser">팔로우</button>
    <button v-if="isLogin && isFollowing" @click="unfollowUser">
      언팔로우
    </button>
    <hr />

    <p>
      {{ profileInfo.username }}님의 팔로잉 수:
      {{ profileInfo.followings.length }}명
    </p>
    <hr />
    <p>
      {{ profileInfo.username }}님의 팔로워 수:
      {{ profileInfo.followers.length }}명
    </p>
    <hr />
    <p>
      {{ profileInfo.username }}님의 좋아요 수: {{ profileInfo.like_boards }}
    </p>
    <hr />
    <p>{{ profileInfo.username }}님의 게시물 수: {{ profileInfo.boards }}</p>
    <hr />
    <p>
      {{ profileInfo.username }}님의 좋아요 댓글 수:
      {{ profileInfo.like_comments }}
    </p>
    <hr />
    <p>{{ profileInfo.username }}님의 댓글 수: {{ profileInfo.comments }}</p>
    <hr />
    <p>
      {{ profileInfo.username }}님의 좋아요 영화 수:
      {{ profileInfo.like_movies }}
    </p>
  </div>
</template>

<script>
import { mapState } from "vuex";

export default {
  props: {
    username: {
      type: String,
      required: true,
    },
  },
  computed: {
    isLogin() {
      return this.$store.getters.isLogin;
    },
    isFollowing() {
      return this.profileInfo && this.profileInfo.following;
    },
    ...mapState(["profileInfo"]),
  },
  created() {
    this.$store.dispatch("getUserProfile", this.username);
  },
  methods: {
    followUser() {
      this.$store
        .dispatch("followUser", this.username)
        .then(() => {
          console.log("유저를 팔로우했습니다.");
          this.$store.commit("SET_FOLLOWING", true); // 팔로우 상태 변경
        })
        .catch((error) => {
          console.error("유저 팔로우 중 오류가 발생했습니다.", error);
        });
    },
    unfollowUser() {
      this.$store
        .dispatch("unfollowUser", this.username)
        .then(() => {
          console.log("유저를 언팔로우했습니다.");
          this.$store.commit("SET_FOLLOWING", false); // 팔로우 상태 변경
        })
        .catch((error) => {
          console.error("유저 언팔로우 중 오류가 발생했습니다.", error);
        });
    },
  },
};
</script>

<style>
</style>

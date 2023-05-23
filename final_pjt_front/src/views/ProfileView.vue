<!-- 프로필 뷰에 필요한 것 -->
<template>
  <div class="profile">
    <h1>{{ userinfo?.username }}'s USER PROFILE</h1>
    <hr />
    <p>{{ userinfo?.username }}'s Followings : {{ userinfo?.followings }}</p>
    <hr />
    <p>{{ userinfo?.username }}'s Followers : {{ userinfo?.followers }}</p>
    <hr />
    <p>{{ userinfo?.username }}'s likes : {{ userinfo?.like_boards }}</p>
    <hr />
    <p>{{ userinfo?.username }}'s Board : {{ userinfo?.boards }}</p>
    <hr />
    <p>
      {{ userinfo?.username }}'s Like Comments : {{ userinfo?.like_comments }}
    </p>
    <hr />
    <p>{{ userinfo?.username }}'s Comments : {{ userinfo?.comments }}</p>
    <hr />
    <p>{{ userinfo?.username }}'s like_movies : {{ userinfo?.like_movies }}</p>
  </div>
</template>

<script>
import { mapState } from "vuex";
export default {
  computed: {
    ...mapState(["userinfo"]),
  },
  created() {
    // if(!this.userinfo){
    this.$store.dispatch("getMyProfile");
    // }
  },
};
</script>

<style>
</style>
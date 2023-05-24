<template>
  <div>
    <h1>회원가입 페이지</h1>
    <form @submit.prevent="signUp">
      <label for="username">사용자명:</label>
      <input type="text" id="username" v-model="username" />
      <button
        @click="checkUsernameAvailability"
        :disabled="usernameCheckInProgress"
      >
        중복 확인</button
      ><br />

      <!-- <label for="email">이메일:</label>
      <input type="email" id="email" v-model="email" /><br /> -->

      <label for="password1">비밀번호:</label>
      <input type="password" id="password1" v-model="password1" /><br />

      <label for="password2">비밀번호 확인:</label>
      <input type="password" id="password2" v-model="password2" /><br />

      <input
        type="submit"
        value="가입하기"
        :disabled="!isUsernameAvailable || usernameCheckInProgress"
      />
      <!-- <p v-if="!isUsernameAvailable">중복 확인을 통과해야 가입할 수 있습니다.</p> -->
    </form>
  </div>
</template>

<script>
export default {
  name: "SignUpView",
  data() {
    return {
      username: null,
      password1: null,
      password2: null,
      usernameCheckInProgress: false, // username 중복 확인 진행 여부를 나타내는 플래그 변수
      isUsernameAvailable: false, // username 사용 가능 여부를 나타내는 변수
    };
  },
  methods: {
    signUp() {
      const username = this.username;
      const password1 = this.password1;
      const password2 = this.password2;
      // const email = this.email;

      const payload = {
        username,
        password1,
        password2,
      };
      if (this.password1 !== this.password2) {
        alert("비밀번호가 일치하지 않습니다.");
        return;
      }
      console.log(payload);
      this.$store.dispatch("signUp", payload);
    },
    checkUsernameAvailability() {
      const username = this.username;
      console.log(username);

      this.usernameCheckInProgress = true; // username 중복 확인이 진행 중임을 표시하는 플래그를 설정합니다.

      fetch(`http://127.0.0.1:8000/profile/check/${username}/`)
        .then((response) => response.json())
        .then((data) => {
          if (data.isAvailable) {
            alert("사용 가능한 사용자명입니다.");
            this.isUsernameAvailable = true; // username이 사용 가능하면 플래그를 설정합니다.
          } else {
            alert("이미 사용 중인 사용자명입니다.");
            this.username = null;
            this.isUsernameAvailable = false; // username이 사용 불가능하면 플래그를 해제합니다.
          }
          this.usernameCheckInProgress = false; // username 중복 확인이 완료되면 플래그를 재설정합니다.
        })
        .catch((error) => {
          console.error("사용자명 중복 확인 오류:", error);
          this.usernameCheckInProgress = false; // 오류 발생 시에도 플래그를 재설정합니다.
        });
    },
  },
};
</script>

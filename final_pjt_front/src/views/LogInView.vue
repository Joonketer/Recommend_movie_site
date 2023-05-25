<template>
  <b-container fluid class="d-flex align-items-center justify-content-center vh-100 bg-#333 text-white">
    <b-card border-variant=light class="text-white bg-dark" style="width: 30rem;">
      <h1 class="text-center">LogIn Page</h1>
      <b-card-body>
        <form @submit.prevent="login">
          <b-form-group label="username : " label-for="username" label-class="text-white">
            <b-form-input id="username" v-model="username"></b-form-input>
          </b-form-group>

          <b-form-group label="password : " label-for="password" label-class="text-white">
            <b-form-input type="password" id="password" v-model="password"></b-form-input>
          </b-form-group>
          <p>회원이 아니라면,
            <router-link  to="/signup">
              회원가입
            </router-link>
          </p>
          <div class="d-flex justify-content-center">
            <b-button type="submit" variant="light">logIn</b-button>
          </div>
        </form>
      </b-card-body>
    </b-card>
  </b-container>
</template>

<script>
  // Keep your script as it is.
export default {
  name: 'LogInView',
  data() {
    return {
      username: null,
      password: null,
    }
  },
  methods: {
    login() {
      const username = this.username
      const password = this.password

      const payload = {
        username, password
      }

      this.$store.dispatch('login', payload)

    }
  }
}
</script>

<!-- views/UpdateView.vue -->

<template>
    <div>
      <h1>게시글 수정</h1>
      <form @submit.prevent="updateArticle">
        <label for="title">제목 : </label>
        <input type="text" id="title" v-model.trim="title"><br>
        <label for="content">내용 : </label>
        <textarea id="content" cols="30" rows="10" v-model="content"></textarea><br>
        <input type="submit" id="submit">
      </form>
    </div>
  </template>
  
  <script>
  import axios from 'axios'
  import { mapState } from "vuex";
  const API_URL = 'http://127.0.0.1:8000'
  
  export default {
    name: 'UpdateView',
    data() {
      return {
        title: null,
        content: null,
      }
    },
    computed: {
      ...mapState(["token"]),
    },
    created() {
      const id = this.$route.params.id
      axios({
        method: 'get',
        url: `${API_URL}/api/v1/articles/${id}/`,
      })
        .then((res) => {
          this.title = res.data.title
          this.content = res.data.content
        })
        .catch((err) => {
          console.log(err)
        })
    },
    methods: {
      updateArticle() {
        const id = this.$route.params.id
        axios({
          method: 'put',
          url: `${API_URL}/api/v1/articles/${id}/`,
          data: { title: this.title, content: this.content },
          headers: { Authorization: `Token ${this.token}` },
        })
        .then(() => {
          this.$router.push({ name: 'DetailView', params: { id: id } })
        })
        .catch((err) => {
          console.log(err)
        })
      },
    },
  }
  </script>
  
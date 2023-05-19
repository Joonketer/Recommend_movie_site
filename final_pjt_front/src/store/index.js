import Vue from 'vue'
import Vuex from 'vuex'

import axios from 'axios'
import createPersistedState from 'vuex-persistedstate'
import router from '../router'

const API_URL = 'http://127.0.0.1:8000'

Vue.use(Vuex)


export default new Vuex.Store({
  plugins: [
    createPersistedState(),
  ],
  state: {
    articles: [
    ],
    photos: [],

    token: null,
    username: null,
    user_pk: null,
  },
  getters: {
    isLogin(state) {

      return state.token ? true : false
    }
  },
  mutations: {
    GET_ARTICLES(state, articles) {
      state.articles = articles
    },
    GET_PHOTOS(state, photos) {
      state.photos = photos
    },
    // signup & login -> 완료하면 토큰 발급
    SAVE_TOKEN(state, token) {
      state.token = token

      router.push({ name: 'ArticleView' }) // store/index.js $router 접근 불가 -> import를 해야함
    },
    SAVE_USRE_INFO(state, info) {
      state.username = info.username
      state.user_pk = info.pk
    }
  },
  actions: {
    getPhotos(context) {
      axios({
        method: 'get',
        url: `${API_URL}/api/v1/recent_moives/`,
        headers: {
          Authorization: `Token ${context.state.token}`
        }
      })
        .then((res) => {
          console.log(res, context)
          context.commit('GET_PHOTOS', res.data)
        })
        .catch((err) => {
          console.log(err)
        })
    },

    getArticles(context) {
      axios({
        method: 'get',
        url: `${API_URL}/api/v1/movies/`,
      })
        .then((res) => {
          // console.log(res, context)
          context.commit('GET_ARTICLES', res.data)
        })
        .catch((err) => {
          console.log(err)
        })
    },
    signUp(context, payload) {
      const username = payload.username
      const password1 = payload.password1
      const password2 = payload.password2

      axios({
        method: 'post',
        url: `${API_URL}/accounts/signup/`,
        data: {
          username, password1, password2
        }
      })
        .then((res) => {
          // console.log(res)
          // context.commit('SIGN_UP', res.data.key)
          context.commit('SAVE_TOKEN', res.data.key)
        })
        .catch((err) => {
          console.log(err)
        })
    },
    login(context, payload) {
      axios({
        method: 'post',
        url: `${API_URL}/accounts/login/`,
        data: {
          username: payload.username,
          password: payload.password,
        }
      })
        .then((res) => {
          context.commit('SAVE_TOKEN', res.data.key)
        })
    },
    saveUserInfo(context, payload) {
      axios({
        method: 'get',
        url: `${API_URL}/accounts/user/`,
        headers: {
          Authorization: `Token ${payload}`
        }
      })
        .then((res) => {
          console.log(res.data)
          context.commit('SAVE_USRE_INFO', res.data)
        })
    },
    // fetchCurrentUser(context) {
    //   if (this.getters.isLoggedIn) {
    //     axios({
    //       method: 'get',
    //       url: `${API_URL}/accounts/user/`,
    //       headers: {
    //         Authorization: `Token ${context.state.token}`
    //       }
    //     })
    //       .then((res) => {
    //         context.commit("SET_CURRENT_USER", res.data)
    //       })
    //       .catch((err) => {
    //         console.error(err)
    //       })
    //   }
    // },
  },
  modules: {
  }
})

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
    articles: [],
    photos: [],
    token: null,
    username: null,
    user_pk: null,
    userinfo: null,
    popularMovies: [],
    popularPage: 1,
    topRatedMovies: [],
    topRatedPage: 1,
    movies: [],
    page: 1,
    itemsperpage: 10,
    topRatedStartIndex: 50,
    likedMovies: [],
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
    SAVE_USER_INFO(state, info) {
      state.userinfo = info;
      // state.username = info.username;
    },
    SET_ALL_MOVIES(state, movies) {
      state.movies = movies;
    },
    SET_POPULAR_MOVIES(state) {
      const start = (state.popularPage - 1) * 5;

      state.popularMovies = state.movies.sort((a, b) => b.popularity - a.popularity).slice(start, start + 5)
      // state.popularMovies = movies.slice(0,5)
    },
    SET_TOP_RATED_MOVIES(state) {
      // const start = (state.topRatedPage - 1) * 5;
      const start = state.topRatedStartIndex;
      const end = start + 5
      state.topRatedMovies = state.movies.sort((a, b) => b.vote_average - a.vote_average).slice(start, end);
      // state.topRatedMovies = state.movies.sort((a,b) => b.vote_average - a.vote_average).slice(start,start+5);
      // state.topRatedMovies = movies.slice(0,5)
    },
    INCREMENT_POPULAR_PAGE(state) {
      state.popularPage += 1;
    },
    DECREMENT_POPULAR_PAGE(state) {
      if (state.popularPage > 1) {
        state.popularPage -= 1;
      }
    },
    INCREMENT_TOP_RATED_PAGE(state) {
      state.topRatedPage += 1;
    },
    DECREMENT_TOP_RATED_PAGE(state) {
      if (state.topRatedPage > 1) {
        state.topRatedPage -= 1;
      }
    },
  },
  actions: {

    nextPopularPage(context) {
      context.commit('INCREMENT_POPULAR_PAGE');
      context.dispatch('getMovies');
    },
    previousPopularPage(context) {
      context.commit('DECREMENT_POPULAR_PAGE');
      context.dispatch('getMovies');
    },
    nextTopRatedPage(context) {
      context.commit('INCREMENT_TOP_RATED_PAGE');
      context.dispatch('getMovies');
    },
    previousTopRatedPage(context) {
      context.commit('DECREMENT_TOP_RATED_PAGE');
      context.dispatch('getMovies');
    },
    getMovies(context) {
      axios({
        method: 'get',
        url: `${API_URL}/api/v1/movies/`,
      })
        .then((res) => {

          const movies = Array.isArray(res.data) ? res.data : [];
          context.commit('SET_ALL_MOVIES', movies)
          context.commit('SET_POPULAR_MOVIES');
          context.commit('SET_TOP_RATED_MOVIES');
          context.commit('RESET_PAGE');
        })
        .catch((err) => {
          console.log(err)
        })
    },
    getMyProfile(context) {
      console.log('이름', context.state.userinfo.username)
      axios({
        method: 'get',
        url: `${API_URL}/profile/${context.state.userinfo.username}/`,
        headers: {
          Authorization: `Token ${context.state.token}`
        }
      })
        .then((res) => {
          console.log('유저', res)
          context.commit('SAVE_USER_INFO', res.data)
          // res.data 인지 확인 하기, userprofile 만들기
          // action만들고, action커밋하고, 
        })
    },
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
          context.dispatch('saveUserInfo', res.data.key);
        })
    },
    logout(context) {
      context.commit('SAVE_TOKEN', null);
      // context.commit('SAVE_USER_INFO', { username: null, pk: null });
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
          console.log('유저프로픽', res.data)
          context.commit('SAVE_USER_INFO', res.data)
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

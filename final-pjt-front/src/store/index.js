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
    following: null,
    profileInfo: null,
  },
  getters: {
    isLogin(state) {

      return state.token ? true : false
    },
    profileInfo: state => state.profileInfo,
  },
  mutations: {
    SET_LOGIN(state, isLogin) {
      state.isLogin = isLogin;
    },
    SET_PROFILE_INFO(state, profileInfo) {
      const updatedProfileInfo = {
        ...profileInfo,
        following: profileInfo.following // 초기값 설정
      };
      state.profileInfo = updatedProfileInfo;
    },
    SET_FOLLOWING(state, isFollowing) {
      if (state.profileInfo) {
        state.profileInfo.following = isFollowing;
      }
    },
    CLEAR_TOKEN(state) {
      state.token = null;
    },
    CLEAR_USER_INFO(state) {
      state.userinfo = null;
    },
    GET_ARTICLES(state, articles) {
      state.articles = articles
    },
    GET_PHOTOS(state, photos) {
      state.photos = photos
    },
    // signup & login -> 완료하면 토큰 발급
    SAVE_TOKEN(state, token) {
      state.token = token;

      if (token) {
        router.push('/');
      } else {
        router.push('/logout'); // 로그아웃 시 이동할 페이지 설정 (예: '/logout')
      }
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

      state.popularMovies = state.movies.sort((a, b) => b.popularity - a.popularity).slice(start, start + 10)
      // state.popularMovies = movies.slice(0,5)
    },
    SET_TOP_RATED_MOVIES(state) {
      // const start = (state.topRatedPage - 1) * 5;
      const start = state.topRatedStartIndex;
      const end = start + 10
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
    getUserProfile({ commit }, username) {
      // 사용자의 프로필 정보를 가져오기 위한 API 호출 코드를 여기에 작성합니다.
      // 예시:
      axios.get(`http://127.0.0.1:8000/profile/${username}/`)
        .then(response => {
          console.log('다른사람', response.data)
          commit('SET_PROFILE_INFO', response.data);
        })
        .catch(error => {
          console.error('사용자 프로필을 가져오는 중 오류가 발생했습니다:', error);
        });
    },
    // 유저를 팔로우하는 액션
    followUser({ commit, state }, username) {
      return new Promise((resolve, reject) => {
        axios
          .post(`${API_URL}/profile/${username}/follow/`, null, {
            headers: {
              Authorization: `Token ${state.token}`,
            },
          })
          .then((response) => {
            // 팔로우 성공 시
            // 상태 변경 및 추가 작업 수행
            commit('SET_FOLLOWING', true); // 팔로우 상태 변경
            commit('SET_PROFILE_INFO', response.data); // 프로필 정보 업데이트
            resolve(response.data);
          })
          .catch((error) => {
            // 팔로우 실패 시
            reject(error);
          });
      });
    },

    unfollowUser({ commit, state }, username) {
      return new Promise((resolve, reject) => {
        axios
          .post(`${API_URL}/profile/${username}/follow/`, null, {
            headers: {
              Authorization: `Token ${state.token}`,
            },
          })
          .then((response) => {
            // 팔로우 성공 시
            // 상태 변경 및 추가 작업 수행
            commit('SET_FOLLOWING', false); // 팔로우 상태 변경
            commit('SET_PROFILE_INFO', response.data); // 프로필 정보 업데이트
            resolve(response.data);
          })
          .catch((error) => {
            // 언팔로우 실패 시
            reject(error);
          });
      });
    },
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
      // const email = payload.email

      console.log('인덱스', payload)
      axios({
        method: 'post',
        url: `${API_URL}/accounts/signup/`,
        data: {
          username, password1, password2,
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
        .catch((err) => {
          if (err.response && err.response.status === 400) {
            // Display alert message for invalid credentials
            alert('Invalid username or password. Please try again.')
          } else {
            console.log(err)
          }
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

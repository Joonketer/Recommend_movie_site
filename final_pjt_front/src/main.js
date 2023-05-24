import Vue from 'vue'
import App from './App.vue'
import store from './store'
import router from './router'
import BootstrapVue from 'bootstrap-vue';
import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap-vue/dist/bootstrap-vue.css';

Vue.use(BootstrapVue);
Vue.config.productionTip = false

// // main.js 또는 메인 Vue 컴포넌트
// window.addEventListener('beforeunload', function () {
//   localStorage.removeItem('vuex'); // localStorage에서 전체 Vuex 상태를 삭제합니다.
//   store.commit('CLEAR_TOKEN'); // Vuex 상태에서 토큰을 삭제합니다.
//   store.commit('CLEAR_USER_INFO'); // Vuex 상태에서 userinfo를 삭제합니다.
// });

new Vue({
  store,
  router,
  render: h => h(App)
}).$mount('#app')

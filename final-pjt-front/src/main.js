import Vue from 'vue'
import App from './App.vue'
import store from './store'
import router from './router'
import BootstrapVue from 'bootstrap-vue';
import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap-vue/dist/bootstrap-vue.css';

Vue.use(BootstrapVue);
Vue.config.productionTip = false

// main.js 또는 메인 Vue 컴포넌트
window.addEventListener('beforeunload', function () {
  localStorage.setItem('vuex', JSON.stringify(store.state)); // Vuex 상태를 localStorage에 저장합니다.
});

// 페이지가 로드될 때 localStorage에서 저장된 상태를 불러와서 Vuex에 복원합니다.
const savedState = JSON.parse(localStorage.getItem('vuex'));
if (savedState) {
  store.replaceState(savedState);
}

new Vue({
  store,
  router,
  render: h => h(App)
}).$mount('#app')

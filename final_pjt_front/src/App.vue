<template>
  <div id="app">
    <nav>
      <router-link :to="{ name: 'HomeView' }">HomeView</router-link> |
      <router-link :to="{ name: 'ArticleView' }">Articles</router-link> |
      <router-link :to="{ name: 'SignUpView' }">SignUpPage</router-link> |
      <router-link :to="{ name: 'LogInView' }">LogInPage</router-link> |
      <router-link :to="{ name: 'RecommendView' }">추천영화</router-link> |
      <router-link
        :to="{
          name: 'ProfileView',
          params: { username: currentUser.username || '' },
        }"
        >내 프로필</router-link
      >
      | <router-link :to="{ name: 'BoxOfficeView' }">박스오피스</router-link> |
      <router-link :to="{ name: 'TagSearchView' }">태그검색</router-link> |
      <router-link :to="{ name: 'CommunityView' }">커뮤니티</router-link> |
      <button @click="logout" to="#">Logout</button>
    </nav>
    <div>
      <input
        type="text"
        v-model="searchQuery"
        placeholder="영화 검색어를 입력하세요"
        @keyup.enter="searchMovies"
      />
      <button @click="searchMovies">검색</button>
    </div>

    <router-view :search-results="searchResults" :search-query="searchQuery" />
  </div>
</template>

<script>
export default {
  data() {
    return {
      searchQuery: "",
      searchResults: [],
    };
  },
  computed: {
    currentUser() {
      return this.$store.state.userinfo; // 현재 로그인된 회원의 정보를 가져옴
    },
  },
  watch: {
    $route(to, from) {
      if (to.name === from.name && to.fullPath === from.fullPath) {
        // 동일한 페이지로 중첩 라우팅된 경우
        this.navigateToSearchView();
      }
    },
  },
  methods: {
    logout() {
      this.$store
        .dispatch("logout")
        .then(() => {
          // 로그아웃 성공 시 처리할 내용을 작성합니다.
          // 예: 로그인 페이지로 이동
          if (this.$route.name !== "LogInView") {
            this.$router.push({ name: "LogInView" });
          }
        })
        .catch((error) => {
          console.error("로그아웃 중 오류 발생:", error);
        });
    },
    navigateToSearchView() {
      const currentRoute = this.$route; // 현재 경로 가져오기
      const searchResultsRoute = {
        name: "SearchView",
        query: { searchResults: this.searchResults },
      };

      // 현재 경로와 목표 경로가 동일한지 확인
      const isSameRoute =
        this.$router.resolve(searchResultsRoute).resolved.fullPath ===
        currentRoute.fullPath;

      if (!isSameRoute) {
        this.$router.push(searchResultsRoute);
      }
    },
    searchMovies() {
      if (this.searchQuery && !this.searchInProgress) {
        this.searchInProgress = true; // 검색 버튼 비활성화
        const query = this.searchQuery;
        const url = `https://api.themoviedb.org/3/search/movie?query=${query}&include_adult=false&language=ko-KOR&page=1`;
        const headers = new Headers();
        headers.append("Authorization", "Bearer YOUR_API_TOKEN");

        fetch(url, { headers })
          .then((response) => response.json())
          .then((data) => {
            this.searchResults = data.results;
          })
          .catch((error) => {
            console.error("검색 중 오류 발생:", error);
          })
          .finally(() => {
            this.searchInProgress = false; // 검색 버튼 활성화
            this.navigateToSearchView(); // fetch 요청이 완료된 후에 navigateToSearchView 호출
          });
      }
    },
  },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

nav {
  padding: 30px;
}

nav a {
  font-weight: bold;
  color: #2c3e50;
}

nav a.router-link-exact-active {
  color: #42b983;
}
</style>



<template>
  <div id="app">
    <div class="container">
      <b-navbar toggleable="lg" type="dark" variant="#333"
      v-if="!isLoginPage && !isSignupPage">
        <b-navbar-brand @click="navigateHome">
          <img class="logo" src="@/assets/Cinemayologo.png" alt="minilogo" />
        </b-navbar-brand>

        <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

        <b-collapse id="nav-collapse" is-nav>
          <b-navbar-nav>
            <b-nav-item
              v-if="isLogin" :to="{name: 'ProfileView', params: { username: currentUser.username || '' },}">내 프로필</b-nav-item>
            <b-nav-item :to="{ name: 'ArticleView' }">All Movies</b-nav-item>
            <b-nav-item :to="{ name: 'RecommendView' }">추천영화</b-nav-item>
            <b-nav-item :to="{ name: 'BoxOfficeView' }">박스오피스</b-nav-item>
            <b-nav-item :to="{ name: 'TagSearchView' }">태그검색</b-nav-item>
            <b-nav-item :to="{ name: 'CommunityView' }">커뮤니티</b-nav-item>
            <b-nav-item v-if="!isLogin" :to="{ name: 'SignUpView' }"
              >SignUpPage</b-nav-item
            >
            <b-nav-item v-if="isLogin" @click="logout">Logout</b-nav-item>
            <div class="search-container" v-if="isLogin">
              <b-form-input
                v-model="searchQuery"
                placeholder="영화 검색어를 입력하세요"
                @keyup.enter="searchMovies"
              />
              <b-button
                size="sm"
                class="my-2 my-sm-0"
                type="submit"
                @click="searchMovies"
                >검색</b-button
              >
            </div>
          </b-navbar-nav>
        </b-collapse>
      </b-navbar>
      <div class="content">
        <router-view
          :search-results="searchResults"
          :search-query="searchQuery"
        />
      </div>
    </div>
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
      return this.$store.state.userinfo || {}; // 현재 로그인된 회원의 정보를 가져옴
    },
    isLogin() {
      return this.$store.getters.isLogin;
    },
    isSignupPage() {
      return this.$route.path === '/signup'; 
    },
    isLoginPage() {
      return this.$route.path === '/login';  // adjust this path to your login page route
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
    navigateHome() {
      // 현재 경로가 이미 "HomeView"인 경우 중복 호출로 간주하고 더 이상의 처리를 하지 않습니다.
      if (this.$route.name === "HomeView") {
        return;
      }
      // "HomeView"로 이동합니다.
      this.$router.push({ name: "HomeView" });
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

      if (!isSameRoute && this.$route.name !== "LogInView") {
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
@import url("https://fonts.googleapis.com/css2?family=Roboto:wght@300&display=swap");

@font-face {
  font-family: "Nanum Gothic";
  src: url("@/assets/fonts/NanumGothicCoding-Bold.ttf") format("truetype");
  font-weight: normal;
  font-style: normal;
}
html,
body,
#app {
  margin: 0;
  padding: 0;
  background-color: #333; /* 원하는 색상 코드로 변경 */
  /* color: #fff; */
  font-family: "Nanum Gothic", sans-serif;
  font-weight: 400;
  color: white;
}
.app {
  display: flex;
  font-family: "Roboto", sans-serif;
}
#sidebar {
  display: fixed;
  position: fixed; /* fixed positioning */
  top: 0; /* stick to top */
  left: 0; /* stick to left */
  height: 100%; /* full height */
  z-index: 2; /* Ensure sidebar is on top of content */
}
.container {
  padding-left: 220px; /* Make sure your sidebar width and this padding match */
}

.sidebar {
  width: 220px;
  background-color: darkgrey;
}

.content {
  width: 100%;
}
@media screen and (max-width: 768px) {
  #sidebar {
    width: 100%;
    height: auto;
  }

  .container {
    padding-left: 0;
  }
}
.navbar.navitem {
  color: lightgray;
  font-size: 25px;
}
.navbar.navitem.router-link-exact-active {
  color: orange;
}
.navbar.navitem:hover {
  color: skyblue;
}
.search-container {
  display: flex;
  justify-content: space-evenly;
  align-items: center;
  margin: 10px 0;
}
hr {
  border-color: white;
}
a.router-link-active {
  color: #f5f5f5; /* a color close to white */
}
</style>




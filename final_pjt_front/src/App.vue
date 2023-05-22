<template>
  <div id="app">
    <nav>
      <router-link :to="{ name: 'ArticleView' }">Articles</router-link> |
      <router-link :to="{ name: 'SignUpView' }">SignUpPage</router-link> |
      <router-link :to="{ name: 'LogInView' }">LogInPage</router-link> |
      <router-link :to="{ name: 'RecommendView' }">추천영화</router-link>
    </nav>
    <div>
      <input
        type="text"
        v-model="searchQuery"
        placeholder="영화 검색어를 입력하세요"
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
  methods: {
    navigateToSearchView() {
      console.log("app", this.searchResults);
      this.$router.push({
        name: "SearchView",
        query: { searchResults: this.searchResults },
      });
    },
    searchMovies() {
      const query = this.searchQuery; // 검색어를 별도의 변수에 저장

      const url = `https://api.themoviedb.org/3/search/movie?query=${query}&include_adult=false&language=ko-KOR&page=1`;

      const headers = new Headers();
      headers.append(
        "Authorization",
        "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIzYTRmODVmMDA1ZDExODVkNjg3Y2Q1ZjE3NTRjY2MyZCIsInN1YiI6IjYzZDIyZDFiY2I3MWI4MDA3YzFiOGNlYyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.zwYescz-jNoCc_X2jDOxOz90oofdYLmxwwkH5XuDmGs"
      );

      const navigateToSearchView = () => {
        console.log("app", this.searchResults);
        this.$router.push({
          name: "SearchView",
          query: { searchResults: this.searchResults },
        });
      };

      fetch(url, { headers })
        .then((response) => response.json())
        .then((data) => {
          this.searchResults = data.results;
          navigateToSearchView();
        })
        .catch((error) => {
          console.error("검색 중 오류 발생:", error);
        });
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

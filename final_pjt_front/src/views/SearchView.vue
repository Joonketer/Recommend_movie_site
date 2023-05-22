<template>
  <div>
    <h2>검색 결과</h2>

    <div v-for="movie in filteredSearchResults" :key="movie.id">
      <p>{{ movie.title }}</p>
      <p>
        포스터:
        <img :src="getBackdropUrl(movie?.backdrop_path)" alt="Backdrop Image" />
      </p>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      searchResults: [], // 검색 결과를 상태로 관리하기 위한 데이터
    };
  },
  props: {
    searchQuery: {
      type: String,
      default: "",
    },
  },
  computed: {
    filteredSearchResults() {
      return this.searchResults.filter((movie) =>
        movie.title.includes(this.searchQuery)
      );
    },
  },
  mounted() {
    // 페이지가 로드될 때 이전에 저장된 검색 결과 데이터를 로드
    const savedSearchResults = localStorage.getItem("searchResults");
    if (savedSearchResults) {
      this.searchResults = JSON.parse(savedSearchResults);
    }

    // 검색을 수행
    this.searchMovies();
  },
  watch: {
    searchQuery() {
      // searchQuery 값이 변경되면 검색을 다시 수행
      this.searchMovies();
    },
  },
  methods: {
    searchMovies() {
      const url = `https://api.themoviedb.org/3/search/movie?query=${this.searchQuery}&include_adult=false&language=ko-KOR&page=1`;

      const headers = new Headers();
      headers.append(
        "Authorization",
        "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIzYTRmODVmMDA1ZDExODVkNjg3Y2Q1ZjE3NTRjY2MyZCIsInN1YiI6IjYzZDIyZDFiY2I3MWI4MDA3YzFiOGNlYyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.zwYescz-jNoCc_X2jDOxOz90oofdYLmxwwkH5XuDmGs"
      );

      fetch(url, { headers })
        .then((response) => response.json())
        .then((data) => {
          this.searchResults = data.results;

          // 검색 결과 데이터를 로컬 스토리지에 저장
          localStorage.setItem(
            "searchResults",
            JSON.stringify(this.searchResults)
          );
        })
        .catch((error) => {
          console.error("검색 중 오류 발생:", error);
        });
    },
    getBackdropUrl(backdropPath) {
      const baseUrl = "https://image.tmdb.org/t/p/original";
      return `${baseUrl}${backdropPath}`;
    },
  },
};
</script>

<style scoped>
ul {
  margin-left: 1rem;
}
img {
  width: 100px;
  height: 100px;
}
</style>

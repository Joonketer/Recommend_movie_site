<template>
    <div class="article-list">
      <h3>마지막 클릭한 것과 관련된 영화</h3>
      <div v-if="isLoading">
        Loading...
      </div>
      <div v-else>
        <div v-if="lastClickedData">
          <p>{{ lastClickedData }}</p>
        </div>
        <!-- <div v-for="movie in recommendedMovies" :key="movie.id">
          {{ movie.movie }}
          <img :src="getBackdropUrl(movie.poster_path)" alt="Backdrop Image" />
        </div> -->
      </div>
    </div>
  </template>
  
  <script>
  import axios from "axios";
  
  export default {
    name: "ClickedList",
    data() {
      return {
        recommendedMovies: [],
        isLoading: true,
        lastClickedData: "",
      };
    },
    mounted() {
      this.fetchLastClickedData();
    },
    methods: {
      fetchLastClickedData() {
        // Make an API request to fetch the last clicked data
        const API_URL = "http://127.0.0.1:8000/api/v1/recent_movies/";
  
        axios.post(API_URL,{headers: {
          Authorization: `Token ${this.token}`,
        },})
          .then((response) => {
            this.lastClickedData = response.data;
            console.log(this.lastClickedData)
            this.fetchMoviesByMovie(this.lastClickedData.movie);
          })
          .catch((error) => {
            console.error("Error fetching last clicked data:", error);
            this.isLoading = false;
          });
      },
      fetchMoviesByMovie(title) {
        // API 요청을 통해 타이틀에 해당하는 영화 목록을 가져옵니다.
        const API_URL = `https://api.themoviedb.org/3/search/movie?query=${title}&include_adult=false&language=ko-KR&page=1`;
  
        axios.get(API_URL, {
          headers: {
            "accept": "application/json",
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIzYTRmODVmMDA1ZDExODVkNjg3Y2Q1ZjE3NTRjY2MyZCIsInN1YiI6IjYzZDIyZDFiY2I3MWI4MDA3YzFiOGNlYyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.zwYescz-jNoCc_X2jDOxOz90oofdYLmxwwkH5XuDmGs"
          },
        })
          .then((response) => {
            const movies = response.data.results;
            this.recommendedMovies = movies;
            this.isLoading = false;
          })
          .catch((error) => {
            console.error("Error fetching recommended movies:", error);
            this.isLoading = false;
          });
      },
      getBackdropUrl(backdropPath) {
        const baseUrl = "https://image.tmdb.org/t/p/original";
        return `${baseUrl}${backdropPath}`;
      },
    },
  };
  </script>
  
  <style>
  /* 필요한 스타일링 작성 */
  </style>
  
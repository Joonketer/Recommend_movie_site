<template>
    <div class="movie-list-item">
      <img :src="getImageUrl(movie.poster_path)" alt="Movie poster" @click="toDetail">
      <h3>{{ movie.title }}</h3>
      <p>{{ movie.overview }}</p>
    </div>
  </template>
  
  <script>
  export default {
    name: 'MovieListItem',
    props: {
      movie: Object,
    },
    methods: {
      getImageUrl(path) {
        return "https://image.tmdb.org/t/p/w500" + path;
      },
      toDetail() {
        this.$router.push({name: 'DetailView', params:{id:this.movie.movie_id}});
      }
    },
  };
  </script>
  
  <style>
  /* CSS styles for your component */
  </style>
  
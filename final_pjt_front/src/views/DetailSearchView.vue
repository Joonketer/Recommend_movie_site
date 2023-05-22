<template>
  <div>
    <h1>Detail</h1>
    <p>글 번호 : {{ movieDetail?.id }}</p>
    <p>제목 : {{ movieDetail?.title }}</p>
    <p>내용 : {{ movieDetail?.overview }}</p>
    <p>개봉일 : {{ movieDetail?.release_date }}</p>
    <p>장르 : {{ movieDetail?.genres }}</p>
    <p>
      포스터 :
      <img
        :src="getBackdropUrl(movieDetail?.backdrop_path)"
        alt="Backdrop Image"
      />
    </p>
  </div>
</template>

<script>
export default {
  name: "DetailSearchView",
  data() {
    return {
      movieDetail: null,
    };
  },
  created() {
    const movieDetailParam = this.$route.query.movieDetail;
    if (movieDetailParam) {
      this.movieDetail = JSON.parse(movieDetailParam);
    }
  },
  methods: {
    getBackdropUrl(backdropPath) {
      const baseUrl = "https://image.tmdb.org/t/p/original";
      return `${baseUrl}${backdropPath}`;
    },
  },
};
</script>
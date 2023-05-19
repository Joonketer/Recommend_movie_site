<template>
  <div class="article-list">
    <h3>10번 클릭한 것들 중 가장 많은 장르</h3>
    <!-- <GenreItem v-for="photo in photos" :key="photo.id" :photo="photo" /> -->
    <ul>
      <li v-for="genre in sortedGenres" :key="genre.id">
        {{ genre.id }}: {{ genre.count }}
      </li>
    </ul>
    <h3>날씨 api</h3>
  </div>
</template>

<script>
export default {
  name: "ArticleList",
  computed: {
    photos() {
      return this.$store.state.photos;
    },
    sortedGenres() {
      // Count the occurrence of each genre ID
      const genreCountMap = {};
      this.photos.forEach((photo) => {
        if (photo.genre_ids && Array.isArray(photo.genre_ids)) {
          photo.genre_ids.forEach((id) => {
            if (typeof id === "number") {
              if (genreCountMap[id]) {
                genreCountMap[id]++;
              } else {
                genreCountMap[id] = 1;
              }
            }
          });
        }
      });

      // Convert genreCountMap to an array of objects
      const genreCountArray = Object.keys(genreCountMap).map((id) => ({
        id: parseInt(id),
        count: genreCountMap[id],
      }));

      // Sort the array in descending order based on count
      genreCountArray.sort((a, b) => b.count - a.count);

      // Return the top 3 genres
      return genreCountArray.slice(0, 3);
    },
  },
};
</script>

<style>
.article-list {
  text-align: start;
}
</style>

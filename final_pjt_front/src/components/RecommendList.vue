<template>
  <div class="article-list">
    <h3>photo List</h3>
    <GenreItem v-for="photo in photos" :key="photo.id" :photo="photo" />
    <ul>
      <li v-for="photo in photos" :key="photo.id" :photo="photo">
        {{ photo.genre_ids }}
      </li>
    </ul>
  </div>
</template>

<script>
import GenreItem from "@/components/GenreItem";

export default {
  name: "ArticleList",
  components: {
    GenreItem,
  },
  computed: {
    photos() {
      return this.$store.state.photos;
    },
  },
};
</script>

<style>
.article-list {
  text-align: start;
}
</style>

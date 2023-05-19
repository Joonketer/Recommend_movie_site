<template>
  <div>
    <h5>{{ photo.id }}</h5>
    <p>{{ photo.user }}</p>
    <p>{{ photo.genre_ids }}</p>
    <p>{{ photo.movie }}</p>
    <p>{{ photo.clicked_at }}</p>

    <hr />
  </div>
</template>

<script>
export default {
  name: "GenreItem",
  props: {
    photo: Object,
  },
};
</script>

<style>
</style>

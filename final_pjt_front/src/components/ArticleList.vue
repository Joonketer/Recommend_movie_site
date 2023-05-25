<template>
  <div class="article-list">
    <ArticleListItem
      v-for="article in articles"
      :key="article.id"
      :article="article"
    />
  </div>
</template>

<script>
import ArticleListItem from "@/components/ArticleListItem";

export default {
  name: "ArticleList",
  components: {
    ArticleListItem,
  },
  computed: {
    articles() {
      return this.$store.state.articles;
    },
  },
  methods: {
    loadMoreArticles() {
      this.page += 1;
      this.$store.dispatch("getArticles", this.page);
    },
  },
  created() {
    window.addEventListener("scroll", () => {
      let bottomOfWindow =
        Math.max(
          window.pageYOffset,
          document.documentElement.scrollTop,
          document.body.scrollTop
        ) +
          window.innerHeight ===
        document.documentElement.offsetHeight;
      if (bottomOfWindow) {
        this.loadMoreArticles();
      }
    });
  },
};
</script>

<style>
.article-list {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
}
.article-list > * {
  flex-basis: calc(33.3333% - 1em);
}
</style>

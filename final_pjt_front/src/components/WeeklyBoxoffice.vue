<template>
  <b-container>
    <div class="Boxoffice-title d-flex justify-content-center">
      <h5>주말 박스오피스 순위</h5>
    </div>

    <b-row>
      <b-col
        md="4"
        v-for="box2movie in weeklyBoxOfficeList"
        :key="box2movie.movieCd"
      >
        <b-card
          bg-variant="dark"
          text-variant="white"
          class="mb-4 custom-card"
          style="width: 18rem"
          @click="searchMovie(box2movie.movieNm)"
        >
          <h4>Rank: {{ box2movie.rank }}</h4>
          <b-card-text>
            <h5>{{ box2movie.movieNm }}</h5>
            <p>관객동원수: {{ box2movie.audiCnt }}</p>
          </b-card-text>
        </b-card>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
import axios from "axios";
export default {
  data() {
    return {
      weeklyBoxOfficeList: [],
    };
  },
  mounted() {
    this.fetchWeeklyBoxOffice();
  },
  methods: {
    searchMovie(movieName) {
      const searchQuery = encodeURIComponent(movieName);
      const googleSearchURL = `https://www.google.com/search?q=영화%20${searchQuery}`;
      window.open(googleSearchURL, "_blank");
    },
    fetchWeeklyBoxOffice() {
      const apiKey = "f5eef3421c602c6cb7ea224104795888";
      const WEEKLY_BOXOFFICE_API_URL = `http://kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchWeeklyBoxOfficeList.json`;
      let today = new Date();
      let targetDate = new Date(today.getTime() - 7 * 24 * 60 * 60 * 1000);
      let todayYear = targetDate.getFullYear();
      let todayMonth = targetDate.getMonth() + 1;
      let todayDate = targetDate.getDate();
      let targetDt = `${todayYear}${todayMonth
        .toString()
        .padStart(2, "0")}${todayDate.toString().padStart(2, "0")}`;
      axios({
        method: "get",
        url: `${WEEKLY_BOXOFFICE_API_URL}?key=${apiKey}&targetDt=${targetDt}`,
      })
        .then((res) => {
          console.log(res);
          if (res.data.boxOfficeResult.weeklyBoxOfficeList) {
            this.weeklyBoxOfficeList =
              res.data.boxOfficeResult.weeklyBoxOfficeList;
          }
        })
        .catch((error) => {
          console.error("Error fetching weekly box office", error);
        });
    },
  },
};
</script>

<style scoped>
.custom-card .card-body {
  padding: 3rem; /* adjust this as per your requirement */
}
</style>

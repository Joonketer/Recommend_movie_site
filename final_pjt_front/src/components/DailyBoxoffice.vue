<template>
  <b-container>
    <div class="Daily-Boxoffice-title d-flex justify-content-center">
      <h5>일간 박스오피스 순위</h5>
    </div>
    <b-row>
      <b-col
        md="4"
        v-for="boxmovie in dailyBoxOfficeList"
        :key="boxmovie.boxmovieCd"
      >
        <b-card
          @click="searchMovie(boxmovie.movieNm)"
          bg-variant="dark"
          text-variant="white"
          class="mb-4 custom-card"
          style="width: 18rem"
        >
          <h4>Rank: {{ boxmovie.rank }}</h4>
          <b-card-text>
            <h5>{{ boxmovie.movieNm }}</h5>
            <p>관객동원수: {{ boxmovie.audiCnt }}</p>
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
      dailyBoxOfficeList: [],
    };
  },
  mounted() {
    this.fetchDailyBoxOffice();
  },
  methods: {
    searchMovie(movieName) {
      const searchQuery = encodeURIComponent(movieName);
      const googleSearchURL = `https://www.google.com/search?q=영화%20${searchQuery}`;
      window.open(googleSearchURL, "_blank");
    },
    fetchDailyBoxOffice() {
      const DAILY_BOXOFFICE_API_URL =
        "http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.json";
      const apiKey = "f5eef3421c602c6cb7ea224104795888";
      let today = new Date();
      let targetDate = new Date(today.getTime() - 1 * 24 * 60 * 60 * 1000);
      let todayYear = targetDate.getFullYear();
      let todayMonth = targetDate.getMonth() + 1;
      let todayDate = targetDate.getDate();
      let targetDt = `${todayYear}${todayMonth
        .toString()
        .padStart(2, "0")}${todayDate.toString().padStart(2, "0")}`;
      // let targetDt = todayYear + todayMonth + todayDate
      // const targetDt = '20120101'; // Replace with the desired date in yyyymmdd format
      // const targetDt = today;
      axios({
        method: "get",
        url: `${DAILY_BOXOFFICE_API_URL}?key=${apiKey}&targetDt=${targetDt}`,
      })
        .then((res) => {
          console.log(res);
          if (res.data.boxOfficeResult.dailyBoxOfficeList) {
            this.dailyBoxOfficeList =
              res.data.boxOfficeResult.dailyBoxOfficeList;
          }
          // if (data.boxOfficeResult.dailyBoxOfficeList){
          //   this.dailyBoxOfficeList = data.boxOfficeResult.dailyBoxOfficeList
          // }
        })
        .catch((error) => {
          console.error("Error fetching daily box office", error);
        });
    },
  },
};
</script>
  
<style scoped>
.custom-card .card-body {
  padding: 2rem; /* adjust this as per your requirement */
}
</style>
  
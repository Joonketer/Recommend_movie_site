<template>
    <div>
      <h1>Daily Box Office</h1>
      <ul>
        <li v-for="boxmovie in dailyBoxOfficeList" :key="boxmovie.boxmovieCd">
          <h2>{{ boxmovie.movieNm }}</h2>
          <p>Rank: {{ boxmovie.rank }}</p>
          <p>Sales: {{ boxmovie.salesAmt }}</p>
          <p>Audience: {{ boxmovie.audiCnt }}</p>
        </li>
      </ul>
    </div>
  </template>
  
  <script>
  import axios from 'axios'
  export default {
    data() {
      return {
        dailyBoxOfficeList: []
      };
    },
    mounted() {
      this.fetchDailyBoxOffice();
    },
    methods: {
      fetchDailyBoxOffice() {
        const DAILY_BOXOFFICE_API_URL = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.json';
        const apiKey = 'f5eef3421c602c6cb7ea224104795888';
        let today = new Date();
        var todayYear = today.getFullYear();
        var todayMonth = today.getMonth() + 1;
        var todayDate = today.getDate() - 1 ;
        let targetDt = `${todayYear}${todayMonth.toString().padStart(2, '0')}${todayDate.toString().padStart(2, '0')}`
        // let targetDt = todayYear + todayMonth + todayDate
        // const targetDt = '20120101'; // Replace with the desired date in yyyymmdd format
        // const targetDt = today;       
        axios({
          method:'get',
          url : `${DAILY_BOXOFFICE_API_URL}?key=${apiKey}&targetDt=${targetDt}`,
        })
        .then((res)=>{
          console.log(res)
          if (res.data.boxOfficeResult.dailyBoxOfficeList){
            this.dailyBoxOfficeList = res.data.boxOfficeResult.dailyBoxOfficeList
          }
          // if (data.boxOfficeResult.dailyBoxOfficeList){
          //   this.dailyBoxOfficeList = data.boxOfficeResult.dailyBoxOfficeList
          // }
        })
        .catch(error => {
          console.error('Error fetching daily box office', error)
        })
        }
    }
  };
  </script>
  
  <style scoped>
  /* Add your custom styles here */
  </style>
  
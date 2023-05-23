<!-- <template>
    <div>
      <h1>Weekly Box Office</h1>
      <ul>
        <li v-for="box2movie in WeeklyBoxOfficeList" :key="box2movie.movieCd">
          <h2>{{ box2movie.movieNm }}</h2>
          <p>Rank: {{ box2movie.rank }}</p>
          <p>Sales: {{ box2movie.salesAmt }}</p>
          <p>Audience: {{ box2movie.audiCnt }}</p>
        </li>
      </ul>
    </div>
  </template>
  
  <script>
  import axios from 'axios'
  export default {
    data() {
      return {
        WeeklyBoxOfficeList: [],
      };
    },
    mounted() {
      this.fetchWeeklyBoxOffice();
    },
    methods: {
      fetchWeeklyBoxOffice() {
        const apiKey = 'f5eef3421c602c6cb7ea224104795888';
        const WEEKLY_BOXOFFICE_API_URL = `http://kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchWeeklyBoxOfficeList.json`;
        let today = new Date();
        var todayYear = today.getFullYear();
        var todayMonth = today.getMonth() + 1;
        var todayDate = today.getDate() - 3 ;
        let targetDt = `${todayYear}${todayMonth.toString().padStart(2, '0')}${todayDate.toString().padStart(2, '0')}`
        axios({
          method:'get',
          url:`${WEEKLY_BOXOFFICE_API_URL}?key=${apiKey}&targetDt=${targetDt}`,
        })
        .then((res) => {
          console.log(res)
          if (res.data.boxOfficeResult.WeeklyBoxOfficeList){
            this.WeeklyBoxOfficeList = res.data.boxOfficeResult.WeeklyBoxOfficeList
          }
        })
        .catch(error => {
        console.error('Error fetching Weekly box office', error)
        })
      }
    }
  };
  </script>
  
  <style scoped>
  /* Add your custom styles here */
  </style>
   -->

   <template>
    <div>
      <h1>Weekly Box Office</h1>
      <ul>
        <li v-for="box2movie in weeklyBoxOfficeList" :key="box2movie.movieCd">
          <h2>{{ box2movie.movieNm }}</h2>
          <p>Rank: {{ box2movie.rank }}</p>
          <p>Sales: {{ box2movie.salesAmt }}</p>
          <p>Audience: {{ box2movie.audiCnt }}</p>
        </li>
      </ul>
    </div>
</template>

<script>
import axios from 'axios'
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
    fetchWeeklyBoxOffice() {
      const apiKey = 'f5eef3421c602c6cb7ea224104795888';
      const WEEKLY_BOXOFFICE_API_URL = `http://kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchWeeklyBoxOfficeList.json`;
      let today = new Date();
      var todayYear = today.getFullYear();
      var todayMonth = today.getMonth() + 1;
      var todayDate = today.getDate() - 3 ;
      let targetDt = `${todayYear}${todayMonth.toString().padStart(2, '0')}${todayDate.toString().padStart(2, '0')}`
      axios({
        method:'get',
        url:`${WEEKLY_BOXOFFICE_API_URL}?key=${apiKey}&targetDt=${targetDt}`,
      })
      .then((res) => {
        console.log(res)
        if (res.data.boxOfficeResult.weeklyBoxOfficeList){
          this.weeklyBoxOfficeList = res.data.boxOfficeResult.weeklyBoxOfficeList
        }
      })
      .catch(error => {
      console.error('Error fetching weekly box office', error)
      })
    }
  }
};
</script>

<style scoped>
/* Add your custom styles here */
</style>

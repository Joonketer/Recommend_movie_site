<template>
  <div>
    <h2>Current Weather: {{ weather }}</h2>
    <h3>Suggested Movie Genres:</h3>
    <ul>
      <li v-for="genre in movieGenres" :key="genre.id">
        {{ genre.name }}
      </li>
    </ul>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "WeatherMovieGenres",
  data() {
    return {
      weather: "",
      movieGenres: [],
    };
  },
  mounted() {
    this.fetchWeather();
  },
  methods: {
    fetchWeather() {
      // Make an API request to OpenWeatherMap to get the current weather
      const API_KEY = "da84d14f5b0aa15df43c26b699b795bf";
      const lat = "37.56667";
      const lon = "126.97806";
      const API_URL = `https://api.openweathermap.org/data/2.5/weather?lat=${lat}&lon=${lon}&appid=${API_KEY}`;
      console.log(API_URL);

      axios
        .get(API_URL)
        .then((response) => {
          const weather = response.data.weather[0].main;
          this.weather = weather;
          this.fetchMovieGenres(weather);
        })
        .catch((error) => {
          console.error("Error fetching weather:", error);
        });
    },
    fetchMovieGenres(weather) {
      // Define movie genres based on weather conditions
      const genreMap = {
        Clear: [28, 12, 16],
        Clouds: [18, 14, 36],
        Rain: [80, 18, 10749],
        Snow: [28, 16, 10751],
        Thunderstorm: [28, 27, 878],
        Drizzle: [18, 35, 9648],
        Mist: [18, 27, 53],
        Smoke: [53, 27, 9648],
        Haze: [28, 18, 10749],
        Dust: [28, 18, 9648],
        Fog: [18, 27, 53],
        Sand: [28, 18, 9648],
        Ash: [28, 18, 9648],
        Squall: [28, 18, 9648],
        Tornado: [28, 878, 53],
      };

      // Fetch movie genres based on the weather condition
      const movieGenres = genreMap[weather] || [];
      this.movieGenres = movieGenres.map((genreId) => {
        return {
          id: genreId,
          name: this.getGenreName(genreId),
        };
      });
    },
    getGenreName(genreId) {
      // Map genre IDs to genre names
      const genreMap = {
        28: "Action",
        12: "Adventure",
        16: "Animation",
        35: "Comedy",
        80: "Crime",
        18: "Drama",
        10751: "Family",
        14: "Fantasy",
        27: "Horror",
        9648: "Mystery",
        10749: "Romance",
        878: "Science Fiction",
        53: "Thriller",
      };

      return genreMap[genreId] || "Unknown";
    },
  },
};
</script>

<style scoped>
ul {
  margin-left: 1rem;
}
</style>
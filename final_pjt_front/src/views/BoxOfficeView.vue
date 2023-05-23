<template>
    <div>
      <h1>BoxOffice</h1>
      <br>
      <hr>
      <h2>DailyBoxOffice</h2>
      <DailyBoxoffice/>
      <hr>
      <h2>WeeklyBoxOffice</h2>
      <WeeklyBoxoffice/>
    </div>
  </template>
  
  <script>
  import DailyBoxoffice from '@/components/DailyBoxoffice.vue';
  import WeeklyBoxoffice from '@/components/WeeklyBoxoffice.vue';
  
  export default {
    components: {
      DailyBoxoffice,
      WeeklyBoxoffice
    }
  };
  </script>
  
  <style>
  /* Add your custom styles here */
  </style>
  
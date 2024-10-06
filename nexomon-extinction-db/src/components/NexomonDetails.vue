<template>
    <div>
      <h1>Nexomon Database</h1>
      <ul>
        <li v-for="nexomon in nexomons" :key="nexomon.Name">
          {{ nexomon.Name }}
          <img :src="nexomon.Sprites.Regular" alt="Sprite" />
        </li>
      </ul>
    </div>
  </template>
  
  <script>
  import data from '../../../Assets/nexomon_extinction_database.json';
  
  export default {
    data() {
      return {
        nexomons: data // Load your JSON data here
      };
    }
  };
  </script>
  
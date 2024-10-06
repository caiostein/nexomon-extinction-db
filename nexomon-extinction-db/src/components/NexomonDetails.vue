<template>
  <div>
    <h1>Nexomon Database</h1>
    <div class="nexomon-grid">
      <div class="nexomon-card" v-for="nexomon in nexomons" :key="nexomon.Name">
        <h3>{{ nexomon.Name }}</h3>
        <img :src="nexomon.Sprites.Thumbnail" alt="Sprite" />
      </div>
    </div>
  </div>
</template>

<script>
import data from '../../../python-scripts/assets/nexomon_extinction_database.json';

export default {
  data() {
    return {
      nexomons: data // Load your JSON data here
    };
  }
};
</script>

<style scoped>
.nexomon-grid {
  display: flex;
  flex-wrap: wrap; /* Allows the items to wrap to the next line */
  justify-content: space-between; /* Space between items */
}

.nexomon-card {
  width: calc(20% - 10px); /* 5 cards across, accounting for margins */
  margin-bottom: 20px; /* Space below each card */
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  text-align: center;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1); /* Optional: Adds a subtle shadow for depth */
}

.nexomon-card img {
  max-width: 30%; /* Make images responsive */
  height: auto;
}

/* On hover, darken the card and add a slight scale effect */
.nexomon-card:hover {
  background-color: rgba(0, 0, 0, 0.1); /* Slightly darken the background */
  transform: scale(1.02); /* Slightly increase the size for emphasis */
}
</style>

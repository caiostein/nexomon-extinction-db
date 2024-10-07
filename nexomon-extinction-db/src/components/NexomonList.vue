<template>
  <div>
    <h1>Nexomon Database</h1>
    
    <!-- Search Input -->
    <input
      type="text"
      v-model="searchQuery"
      placeholder="Search for a Nexomon"
      class="search-box"
    />

    <div class="nexomon-grid">
      <router-link
        v-for="nexomon in filteredNexomons"
        :key="nexomon.Number"
        :to="`/nexomon/${nexomon.Number}`"
        class="nexomon-card"
      >
        <h3>{{ nexomon.Name }}</h3>
        <img :src="nexomon.Sprites.Thumbnail" alt="Sprite" />
      </router-link>
    </div>

  </div>
</template>

<script>
import data from '../../../python-scripts/assets/nexomon_extinction_database.json';

export default {
  data() {
    return {
      nexomons: data,
      searchQuery: ''
    };
  },
  computed: {
    filteredNexomons() {
      return this.nexomons.filter(nexomon =>
        nexomon.Name.toLowerCase().includes(this.searchQuery.toLowerCase())
      );
    }
  }
};
</script>

<style scoped>
.nexomon-grid {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
}

.nexomon-card {
  width: calc(20% - 10px);
  margin-bottom: 20px;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  text-align: center;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  transition: background-color 0.3s ease, transform 0.3s ease;
  text-decoration: none; /* Remove underline from link */
  color: inherit; /* Keep the text color consistent with the rest of the app */
}

.nexomon-card img {
  max-width: 30%;
  height: auto;
}

.nexomon-card:hover {
  background-color: rgba(0, 0, 0, 0.1);
  transform: scale(1.02);
}

.search-box {
  width: 30%;
  padding: 10px;
  margin-bottom: 20px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 5px;
}
</style>

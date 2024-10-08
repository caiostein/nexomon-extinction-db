<template>
  <div>
    <!-- Search Input -->
    <input type="text" v-model="searchQuery" placeholder="Search for a Nexomon" class="search-box" />

    <div class="nexomon-grid">
      <router-link v-for="nexomon in filteredNexomons" :key="nexomon.Number" :to="`/nexomon/${nexomon.Number}`"
        class="nexomon-card">
        <h3>{{ nexomon.Number }} - {{ nexomon.Name }}</h3>
        <img :src="getThumbnail(nexomon.Name)" alt="Sprite" />
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
      const searchQueryLower = this.searchQuery.toLowerCase();

      return this.nexomons.filter(nexomon => {
        const nameMatches = nexomon.Name.toLowerCase().includes(searchQueryLower);

        // Check if the number matches, convert both to numbers for comparison
        const numberMatches = nexomon.Number.includes(searchQueryLower);

        // Return true if either name or number matches
        return nameMatches || numberMatches;
      }
      );
    }
  },
  methods: {
    getThumbnail(nexomonName) {

      try {
        return require(`@/assets/downloaded_images/${nexomonName}-menu.png`);
      } catch (error) {
        try {
          return require(`@/assets/downloaded_images/${nexomonName}_(Extinction)-menu.png`);
        } catch (error) {
          console.warn(`Neither ${nexomonName}-menu.png nor ${nexomonName}_(Extinction)-menu.png were found.`);
        }
      }
    },
  }
};
</script>

<style scoped>
.nexomon-grid {
  margin: 50px;
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
}

.nexomon-card {
  width: calc(25% - 10px);
  margin-bottom: 20px;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  text-align: center;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  transition: background-color 0.3s ease, transform 0.3s ease;
  text-decoration: none;
  color: inherit;
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
  margin-top: 40px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 5px;
}
</style>

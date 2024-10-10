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
      searchQuery: '',
    };
  },
  computed: {
    filteredNexomons() {
      const searchQueryLower = this.searchQuery.toLowerCase();

      return this.nexomons.filter(nexomon => {
        const nameMatches = nexomon.Name.toLowerCase().includes(searchQueryLower);
        const numberMatches = nexomon.Number.includes(searchQueryLower);

        return nameMatches || numberMatches;
      });
    },
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
  },
};
</script>

<style scoped>
.nexomon-grid {
  margin: 45px;
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  /* Center align cards */
  min-height: 10000px;
  /* Set a minimum height to prevent collapsing */
}

.nexomon-card {
  width: calc(14% - 14.8px);
  /* Default width for larger screens */
  margin: 30px;
  /* Space between cards */
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  text-align: center;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  transition: background-color 0.3s ease, transform 0.3s ease;
  text-decoration: none;
  color: inherit;
  max-height: 278px;
}

.nexomon-card img {
  max-width: 100%;
  /* Full width for images */
  height: auto;
  /* Maintain aspect ratio */
}

.nexomon-card h3 {
  font-size: 1.5em;
  /* Default font size */
  margin: 5px 0;
  /* Space around the heading */
}

.nexomon-card:hover {
  background-color: rgba(141, 140, 140, 0.068);
  transform: scale(1.02);
}

.search-box {
  width: 100%;
  /* Full width on smaller screens */
  max-width: 300px;
  /* Limit maximum width */
  padding: 10px;
  margin: 40px auto;
  /* Centered and space from the top */
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

/* Media Queries for Responsiveness */

@media (max-width: 3840px) {
  .nexomon-card {
    width: calc(14% - 14.8px);
    margin: 30px;
    max-height: 300px;
  }
}

@media (max-width: 1925px) {
  .nexomon-card {
    width: calc(14% - 14.8px);
    /* Default width for larger screens */
    margin: 30px;
    max-height: 278px;
  }
}


@media (max-width: 1280px) {
  .nexomon-card {
    width: calc(30% - 20px);
    /* Maintain three cards per row on small mobile devices */
    margin: 10px;
    /* Space between cards */
    flex-basis: 26.9%;
    max-height: 289px;
  }
}

@media (max-width: 480px) {
  .nexomon-card {
    width: calc(30% - 20px);
    /* Maintain three cards per row on small mobile devices */
    margin: 10px;
    /* Space between cards */
    flex-basis: 26.9%;
    max-height: 144px;
  }

  .nexomon-card h3 {
    font-size: 0.9em;
    /* Smaller font size for small devices */
  }

  .nexomon-grid {
    justify-content: space-between;
    /* Space out cards */
    margin: 20px;
    flex-flow: row wrap;
  }

}
</style>

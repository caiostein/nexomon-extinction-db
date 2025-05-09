<template>
  <div class="location-list-wrapper">
    <div class="filters-container">
      <input type="text" v-model="searchQuery" placeholder="Search for a Location" class="search-box" />
    </div>
    <div class="grid-scroll-container">
      <div class="location-grid">
        <router-link v-for="location in filteredLocations" :key="location" :to="`/location/${location}`" class="location-card">
          <h3>{{ location.replace(/ \(Extinction\)/i, '') }}</h3>
          <img :src="getRegionImage(location)" :alt="location" />
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
import data from '../../../python-scripts/assets/nexomon_extinction_database.json';

export default {
  data() {
    return {
      searchQuery: '',
      locations: this.getAllLocations(),
    };
  },
  methods: {
    getAllLocations() {
      const all = new Set();
      data.forEach(n => {
        if (n.Locations) {
          n.Locations.forEach(region => {
            if (region.Region && region.Region.text) {
              all.add(region.Region.text);
            }
          });
        }
      });
      return Array.from(all).sort();
    },
    getRegionImage(regionName) {
      let name = regionName;
      while (name.includes(' ')) {
        name = name.replace(' ', '_');
      }
      try {
        return require(`@/assets/downloaded_images/${name}Warp.png`);
      } catch {
        return '';
      }
    }
  },
  computed: {
    filteredLocations() {
      if (!this.searchQuery) return this.locations;
      return this.locations.filter(l => l.toLowerCase().includes(this.searchQuery.toLowerCase()));
    }
  }
};
</script>

<style scoped>
.location-list-wrapper {
  width: 100%;
}

.location-grid {
  display: grid;
  align-items: start;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 32px;
  justify-content: center;
  max-width: 1200px;
  margin: 0 auto;
}

.location-card {
  border: 2px solid #eee;
  border-radius: 12px;
  background: #fff;
  box-shadow: 0 4px 20px rgba(0,0,0,0.08);
  padding: 0 0 18px 0;
  margin: 0;
  text-align: center;
  transition: transform 0.3s, box-shadow 0.3s, background 0.3s, border-color 0.3s;
  cursor: pointer;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-decoration: none;
}

.location-card:hover {
  transform: scale(1.02);
  box-shadow: 0 8px 32px rgba(0,0,0,0.15);
  background: #f7f7f7;
  border-color: #b3e0f7;
}

.location-card img {
  width: 95%;
  height: 220px;
  object-fit: cover;
  border-radius: 8px 8px 0 0;
  margin: 18px 0 0 0;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
  background: #fff;
}

.location-card h3 {
  font-size: 2em;
  color: #222;
  margin: 18px 0 0 0;
  text-shadow: none;
}

.filters-container {
  display: flex;
  justify-content: center;
  align-items: center;
  margin: 30px 0 10px 0;
}

.search-box {
  width: 100%;
  max-width: 300px;
  padding: 10px;
  margin: 10px auto;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 5px;
  background-color: #fff;
  color: #333;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  transition: border-color 0.2s, box-shadow 0.2s, background 0.3s, color 0.3s;
}

.search-box:focus {
  border-color: #2b9fcc;
  box-shadow: 0 4px 16px rgba(43,159,204,0.15);
}

/* Dark mode styles for location list */
.dark-mode .location-list-wrapper {
  background: #212529;
}

.dark-mode .location-card {
  background: #23272b;
  border-color: #444;
}

.dark-mode .location-card:hover {
  background: #2c3136;
  border-color: #2b9fcc;
}

.dark-mode .location-card h3 {
  color: #fff;
  text-shadow: 2px 0 #000, -2px 0 #000, 0 2px #000, 0 -2px #000,
               1px 1px #000, -1px -1px #000, 1px -1px #000, -1px 1px #000;
  text-decoration: none;
}

.dark-mode .search-box {
  background-color: #333;
  color: #fff;
  border: 1px solid #555;
}

.dark-mode .search-box:focus {
  border-color: #1e7ca6;
  box-shadow: 0 4px 16px rgba(43,159,204,0.15);
}

@media (max-width: 900px) {
  .location-grid {
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    gap: 18px;
  }
  .location-card img {
    height: 120px;
  }
  .location-card h3 {
    font-size: 1.2em;
  }
}

@media (max-width: 480px) {
  .location-grid {
    grid-template-columns: 1fr;
    gap: 10px;
  }
  .location-card img {
    height: 90px;
  }
  .location-card h3 {
    font-size: 1em;
  }
}
</style>

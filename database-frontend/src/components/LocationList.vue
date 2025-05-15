<template>
  <div class="location-list-wrapper">
    <div class="filters-container">
      <div class="search-bar-container">
        <input type="text" v-model="searchQuery" placeholder="Search for a Location" class="search-box" />
      </div>
    </div>
    <div class="regions-container">
      <div class="location-grid">
        <router-link v-for="location in filteredLocations" :key="location" :to="`/location/${location}`" class="location-card">
          <div @click="clearRegionMapSelection(location)" style="width:100%;height:100%">
            <h3>{{ location.replace(/ \(Extinction\)/i, '') }}</h3>
            <img :src="getRegionImage(location)" :alt="location" />
          </div>
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
import data from '../../../python-scripts/assets/nexomon_extinction_database.json';
import locationExceptions from '../assets/location_exceptions.json';

export default {
  data() {
    return {
      searchQuery: '',
      locations: this.getAllLocations(),
      regionMaps: this.getRegionMapsLookup(),
      questLocations: locationExceptions.quest_locations || {}
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
    getRegionMapsLookup() {
      // Returns { regionName: Set of all map names (subareas) }
      const lookup = {};
      data.forEach(n => {
        if (n.Locations) {
          n.Locations.forEach(region => {
            if (region.Region && region.Region.text) {
              const regionName = region.Region.text;
              if (!lookup[regionName]) lookup[regionName] = new Set();
              if (typeof region.Maps === 'string') {
                region.Maps.split(', ').forEach(m => lookup[regionName].add(m));
              } else if (Array.isArray(region.Maps)) {
                region.Maps.forEach(m => lookup[regionName].add(m));
              }
            }
          });
        }
      });
      // Convert sets to arrays for easier use
      Object.keys(lookup).forEach(region => {
        lookup[region] = Array.from(lookup[region]);
      });
      return lookup;
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
    },
    clearRegionMapSelection(region) {
      localStorage.removeItem(`nexomondb_last_selected_map_${region}`);
    }
  },
  computed: {
    filteredLocations() {
      if (!this.searchQuery) return this.locations;
      const q = this.searchQuery.toLowerCase();
      return this.locations.filter(region => {
        if (region.toLowerCase().includes(q)) return true;
        const maps = this.regionMaps[region] || [];
        return maps.some(map => map && map.toLowerCase().includes(q));
      });
    }
  }
};
</script>

<style scoped>
.location-list-wrapper {
  width: 100%;
}

.filters-container {
  position: fixed;
  top: 60px;
  left: 0;
  width: 100%;
  padding: 20px 0;
  z-index: 10;
  display: flex;
  flex-direction: column;
  align-items: center;
  height: 90px;
  box-sizing: border-box;
  background: inherit;
}

.search-bar-container {
  width: 100%;
  display: flex;
  justify-content: center;
}

.regions-container {
  padding-top: 90px;
  height: calc(100vh - 90px - 60px);
  overflow-y: auto;
  box-sizing: border-box;
}

.grid-scroll-container {
  padding-top: 90px;
  box-sizing: border-box;
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
  width: 100%;
  max-width: 700px;
  border: 2px solid #eee;
  border-radius: 12px;
  background: #fff;
  box-shadow: 0 4px 20px rgba(0,0,0,0.08);
  padding: 0 0 32px 0;
  margin: 0;
  text-align: center;
  transition: transform 0.3s, box-shadow 0.3s, background 0.3s, border-color 0.3s;
  cursor: pointer;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-decoration: none;
  min-height: 340px;
}

.location-card:hover {
  transform: scale(1.02);
  box-shadow: 0 8px 32px rgba(0,0,0,0.15);
  background: #f7f7f7;
  border-color: #b3e0f7;
}

.location-card img {
  width: 100%;
  height: auto;
  max-height: 340px;
  object-fit: cover;
  border-radius: 8px 8px 0 0;
  margin: 18px 0 0 0;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
  background: #fff;
}

.location-card h3 {
  font-size: 2.2em;
  color: #222;
  margin: 28px 0 0 0;
  text-shadow: 2px 0 #fff, -2px 0 #fff, 0 2px #fff, 0 -2px #fff,
               1px 1px #fff, -1px -1px #fff, 1px -1px #fff, -1px 1px #fff;
  font-weight: 700;
  letter-spacing: 1px;
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
  .filters-container {
    margin-top: -10px;
    height: 120px;
    padding: 28px 0;
  }
  .regions-container {
    padding-top: 90px;
  }
  .location-grid {
    display: flex;
    flex-direction: column;
    gap: 18px;
    align-items: center;
    max-width: 100%;
    margin: 0 auto;
  }
  .location-card {
    max-width: 98vw;
    min-height: 220px;
    padding-bottom: 24px;
  }
  .location-card img {
    max-height: 180px;
  }
  .location-card h3 {
    font-size: 1.6em;
    margin-top: 18px;
  }
}

@media (max-width: 480px) {
  .location-grid {
    gap: 10px;
  }
  .location-card {
    max-width: 100vw;
    min-height: 160px;
    padding-bottom: 16px;
  }
  .location-card img {
    max-height: 120px;
  }
  .location-card h3 {
    font-size: 1.2em;
    margin-top: 12px;
  }
}
</style>

<style scoped src="../assets/styles/button-styles.css"></style>

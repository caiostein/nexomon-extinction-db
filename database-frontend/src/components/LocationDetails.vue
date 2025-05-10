<template>  <div class="location-details-wrapper">
    <h1>{{ locationName }}</h1>
    <img :src="getRegionImage(locationName)" :alt="locationName" class="region-image" />
    <div>
      <button class="btn btn-sm btn-outline-danger back-button" @click="goBack">Back to Locations</button>
    </div>
      <!-- Nexomon section - now displayed first -->
    <div v-if="nexomons.length" class="nexomon-section">
      <h2>Nexomon found here</h2>
      <div class="nexomon-grid">        <router-link 
          v-for="nexomon in nexomons" 
          :key="nexomon.Number" 
          :to="`/nexomon/${nexomon.Number}`"
          class="nexomon-item">
          <img :src="getThumbnail(nexomon.Name)" :alt="nexomon.Name" class="nexomon-thumb" />
          <div class="nexomon-info">
            <div class="nexomon-number">{{ nexomon.Number }}</div>
            <div class="nexomon-name">{{ nexomon.Name }}</div>
          </div>
        </router-link>
      </div>
    </div>
    
    <!-- Maps section - now displayed after Nexomon -->
    <div v-if="maps.length" class="maps-section">
      <h2>Maps</h2>
      <ul class="maps-list">
        <li v-for="map in maps" :key="map" class="map-item">
          <div class="map-name">{{ map }}</div>
          <img :src="getMapImage(map)" :alt="map" class="map-image" />
        </li>
      </ul>
    </div>
    <div v-else>
      <p>No maps found for this location.</p>
    </div>
  </div>
</template>

<script>
import data from '../../../python-scripts/assets/nexomon_extinction_database.json';
import locationExceptions from '../assets/location_exceptions.json';

export default {
  props: ['location'],
  data() {
    return {
      questLocations: locationExceptions.quest_locations || {}
    };
  },
  computed: {
    locationName() {
      return this.$route.params.location;
    },    maps() {
      // Find all maps for this region
      const maps = new Set();
      data.forEach(n => {
        if (n.Locations) {
          n.Locations.forEach(region => {
            if (region.Region && region.Region.text === this.locationName) {
              // Handle normal map strings (backward compatibility)
              if (typeof region.Maps === 'string') {
                if (!region.Maps.includes("Only during the Resurrect Bolzen quest:")) {
                  region.Maps.split(', ').forEach(m => maps.add(m));
                }
              } 
              // Handle new format with Maps as array
              else if (Array.isArray(region.Maps)) {                // Only display maps that don't have exceptions
                if (!region.Exception) {
                  region.Maps.forEach(map => {
                    maps.add(map);
                  });
                }
              }
            }
          });
        }
      });
      
      return Array.from(maps).sort();
    },    nexomons() {
      // Find all Nexomon found in this region
      return data.filter(n => {
        if (!n.Locations) return false;
        
        return n.Locations.some(region => {
          if (!region.Region || region.Region.text !== this.locationName) return false;
          
          // Don't show nexomon that only appear during quests
          if (region.Exception) return false;
          
          // Handle both string and array formats for backward compatibility
          if (typeof region.Maps === 'string') {
            return !region.Maps.includes("Only during the Resurrect Bolzen quest:");
          } else if (Array.isArray(region.Maps)) {
            return true;
          }
          
          return false;
        });
      });
    }
  },
  methods: {
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
    getMapImage(mapName) {
      const formattedMapName = mapName.replace(/\s+/g, '_');
      try {
        return require(`@/assets/downloaded_location_images/${formattedMapName}.png`);
      } catch {
        return '';
      }
    },    getThumbnail(nexomonName) {
      try {
        return require(`@/assets/downloaded_images/${nexomonName}-menu.png`);
      } catch (error) {
        try {
          return require(`@/assets/downloaded_images/${nexomonName}_(Extinction)-menu.png`);
        } catch (error) {
          // Fall back to regular image if menu icon doesn't exist
          try {
            nexomonName = nexomonName.replace(' (Extinction)', '');
            return require(`@/assets/downloaded_images/${nexomonName}.png`);
          } catch (error) {
            try {
              // Last resort - try alternate file naming
              return require(`@/assets/downloaded_images/${nexomonName}2.png`);
            } catch (error) {
              return '';
            }
          }
        }
      }
    },
    
    goBack() {
      this.$router.push({ path: '/locations' });
    }
  }
};
</script>

<style scoped>
.location-details-wrapper {
  max-width: 1200px;
  margin: 0 auto;
  padding: 24px;
  text-align: center;
  box-sizing: border-box;
}

.region-image {
  width: 180px;
  height: 180px;
  object-fit: contain;
  margin-bottom: 24px;
}

.back-button {
  margin: 5px 0 20px 0;
  padding: 4px 12px;
  font-size: 0.85rem;
  cursor: pointer;
  border-radius: 15px;
  transition: all 0.2s ease;
}

.back-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
}

.dark-mode .back-button {
  border-color: #dc3545;
  color: #dc3545;
}

.dark-mode .back-button:hover {
  background-color: rgba(220, 53, 69, 0.1);
  box-shadow: 0 2px 5px rgba(220, 53, 69, 0.2);
}

/* Nexomon section styling */
.nexomon-section {
  margin-bottom: 30px;
}

.nexomon-grid {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  padding: 0;
  margin: 0 auto;
  max-width: 1200px;
  gap: 5px;
}

.nexomon-item {
  width: calc(16.666% - 20px);
  margin: 10px;
  padding: 10px 6px 15px;
  border: 1px solid #ccc;
  border-radius: 8px;
  text-align: center;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  transition: background-color 0.3s ease, transform 0.3s ease;
  max-height: 290px;
  text-decoration: none;
  color: inherit;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: center;
}

.nexomon-item:hover {
  background-color: rgba(141, 140, 140, 0.068);
  transform: scale(1.02);
}

.dark-mode .nexomon-item {
  border-color: #444;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.3);
}

.dark-mode .nexomon-item:hover {
  background-color: rgba(255, 255, 255, 0.05);
}

.nexomon-thumb {
  width: 64px;
  height: 64px;
  object-fit: contain;
  margin-bottom: 8px;
  border-radius: 10px;
  background-color: rgba(0, 0, 0, 0.05);
  padding: 5px;
  transition: transform 0.2s ease-in-out;
}

.nexomon-thumb:hover {
  transform: scale(1.1);
}

.nexomon-info {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.nexomon-number {
  font-size: 0.8rem;
  color: #666;
  margin-bottom: 2px;
}

.dark-mode .nexomon-number {
  color: #aaa;
}

.nexomon-name {
  font-size: 0.9rem;
  text-align: center;
  width: 100%;
  min-height: 2.8em; /* Allow for two lines of text */
  line-height: 1.4em;
  word-wrap: break-word;
  hyphens: auto;
}

/* Maps section styling */
.maps-section {
  margin-top: 30px;
}

.maps-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 20px;
  list-style-type: none;
  padding: 0;
}

.map-item {
  border: 1px solid #444;
  border-radius: 8px;
  overflow: hidden;
  padding: 10px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.map-name {
  font-size: 1rem;
  margin-bottom: 10px;
  text-align: center;
}

.map-image {
  width: 150px;
  height: 150px;
  object-fit: contain;
}

/* Dark mode adjustments */
.dark-mode .map-item {
  border-color: #555;
  background-color: #2a2a2a;
}

/* Media Queries for Responsiveness */
@media (max-width: 3840px) {
  .nexomon-item {
    width: calc(16.666% - 20px);
    margin: 10px;
    max-height: 310px;
  }
}

@media (max-width: 1925px) {
  .nexomon-item {
    width: calc(16.666% - 20px);
    margin: 10px;
    max-height: 300px;
  }
}

@media (max-width: 1280px) {
  .nexomon-item {
    width: calc(20% - 20px);
    margin: 10px;
    max-height: 290px;
  }
}

@media (max-width: 1024px) {
  .nexomon-item {
    width: calc(25% - 20px);
    margin: 10px;
    max-height: 280px;
  }
}

@media (max-width: 768px) {
  .nexomon-item {
    width: calc(33.333% - 20px);
    margin: 10px;
    max-height: 260px;
  }
}

@media (max-width: 600px) {
  .nexomon-item {
    width: calc(50% - 20px);
    margin: 10px;
    max-height: 240px;
  }
}

@media (max-width: 480px) {
  .nexomon-item {
    width: calc(50% - 15px);
    margin: 7px;
    max-height: 220px;
  }

  .nexomon-name {
    font-size: 0.85em;
    min-height: 3.2em; /* More space for text on small screens */
    line-height: 1.3em;
  }
  
  .nexomon-number {
    font-size: 0.75em;
  }
  
  .nexomon-thumb {
    width: 48px;
    height: 48px;
  }
}
</style>

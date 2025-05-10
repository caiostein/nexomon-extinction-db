<template>  <div class="location-details-wrapper">
    <h1>{{ locationName }}</h1>
    <img :src="getRegionImage(locationName)" :alt="locationName" class="region-image" />
    <div>
      <button class="nexo-button nexo-button-danger" @click="goBack">Back to Locations</button>
    </div>

    <!-- Maps section - now displayed first and made collapsible -->
    <div v-if="maps.length" class="maps-section">
      <div class="section-header" @click="toggleMapsSection">
        <h2>Maps <span class="toggle-icon">{{ mapsCollapsed ? '▼' : '▲' }}</span></h2>
      </div>
        <transition name="collapse">
        <div v-show="!mapsCollapsed" class="section-content">          <p v-if="selectedMap" class="map-highlight-notice">
            Highlighting Nexomon from: {{ selectedMap }}
            <button class="nexo-button nexo-button-secondary" @click="selectedMap = null; highlightedNexomon.clear()">Clear</button>
          </p>
          <ul class="maps-list">
            <li 
              v-for="map in maps" 
              :key="map" 
              class="map-item" 
              :class="{ 'selected-map': selectedMap === map }"
              @click="toggleMapHighlight(map)">
              <div class="map-name">{{ map }}</div>
              <img :src="getMapImage(map)" :alt="map" class="map-image" />
            </li>
          </ul>
        </div>
      </transition>
    </div>
    
    <!-- Nexomon section - now displayed after Maps -->
    <div v-if="nexomons.length" class="nexomon-section">
      <h2>Nexomon found here</h2>
      <div class="nexomon-grid">
        <router-link 
          v-for="nexomon in nexomons" 
          :key="nexomon.Number" 
          :to="`/nexomon/${nexomon.Number}`"
          class="nexomon-item"
          :class="exceptionClass(nexomon)"
          @mouseenter="showTooltip($event, nexomon)"
          @mouseleave="hideTooltip"
        >
          <img :src="getThumbnail(nexomon.Name)" :alt="nexomon.Name" class="nexomon-thumb" />
          <div class="nexomon-info">
            <div class="nexomon-number">
              {{ nexomon.Number }}
              <span v-if="nexomon._regionException && selectedMap" class="exception-icon">
                ⚠️
              </span>
            </div>
            <div class="nexomon-name">{{ nexomon.Name }}</div>
          </div>
          <!-- Tooltip rendered inside the card, absolutely positioned -->
          <div
            v-if="tooltipNexomon === nexomon.Number && tooltipPos.visible"
            class="custom-tooltip"
            :style="{ position: 'absolute', left: '50%', top: '-44px', transform: 'translateX(-50%)', zIndex: 2147483647, pointerEvents: 'none' }"
          >
            {{ tooltipText }}
          </div>
        </router-link>
      </div>
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
  props: ['location'],  data() {
    return {
      questLocations: locationExceptions.quest_locations || {},
      selectedMap: null,
      highlightedNexomon: new Set(),
      mapsCollapsed: true,
      tooltipNexomon: null,
      tooltipText: '',
      tooltipPos: { left: 0, top: 0, visible: false },
    };
  },
  mounted() {
    // Restore last selected map for this location from localStorage
    const key = `nexomondb_last_selected_map_${this.locationName}`;
    const lastMap = localStorage.getItem(key);
    if (lastMap && this.maps.includes(lastMap)) {
      this.selectedMap = lastMap;
      this.highlightNexomonForMap(lastMap);
    }
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
                region.Maps.split(', ').forEach(m => maps.add(m));
              } 
              // Handle new format with Maps as array
              else if (Array.isArray(region.Maps)) {
                region.Maps.forEach(map => {
                  maps.add(map);
                });
              }
            }
          });
        }
      });
      return Array.from(maps).sort();
    },    nexomons() {
      // Find all Nexomon found in this region, including those with exceptions
      return data
        .map(n => {
          if (!n.Locations) return null;
          // Find the region object for this location
          const regionObj = n.Locations.find(region => region.Region && region.Region.text === this.locationName);
          if (!regionObj) return null;
          // Attach the exception (if any) to the nexomon object for use in the template
          return {
            ...n,
            _regionException: regionObj.Exception || null,
            _regionExceptionText: regionObj.Exception ? regionObj.Exception : null
          };
        })
        .filter(Boolean);
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
      localStorage.removeItem(`nexomondb_last_selected_map_${this.locationName}`);
      this.$router.push({ path: '/locations' });
    },
    
    toggleMapHighlight(map) {
      // If clicking the same map, toggle it off
      if (this.selectedMap === map) {
        this.selectedMap = null;
        this.highlightedNexomon.clear();
        // Remove from localStorage
        localStorage.removeItem(`nexomondb_last_selected_map_${this.locationName}`);
        return;
      }
      // Set the new selected map
      this.selectedMap = map;
      // Save to localStorage
      localStorage.setItem(`nexomondb_last_selected_map_${this.locationName}`, map);
      this.highlightNexomonForMap(map);
    },
    highlightNexomonForMap(map) {
      // Clear previous highlights
      this.highlightedNexomon.clear();
      // Find all nexomon that appear in this map
      data.forEach(nexomon => {
        if (!nexomon.Locations) return;
        nexomon.Locations.forEach(location => {
          if (location.Region && location.Region.text === this.locationName) {
            // Check if this nexomon appears in the selected map
            if (Array.isArray(location.Maps) && location.Maps.includes(map)) {
              this.highlightedNexomon.add(nexomon.Number);
            } else if (typeof location.Maps === 'string' && location.Maps.split(', ').includes(map)) {
              this.highlightedNexomon.add(nexomon.Number);
            }
          }
        });
      });
    },
      isNexomonHighlighted(nexomonNumber) {
      if (!this.selectedMap) return false;
      return this.highlightedNexomon.has(nexomonNumber);
    },
    
    toggleMapsSection() {
      this.mapsCollapsed = !this.mapsCollapsed;
    },
    exceptionClass(nexomon) {
      if (nexomon._regionException && this.selectedMap) {
        return 'exception-nexomon';
      } else if (this.isNexomonHighlighted(nexomon.Number)) {
        return 'highlighted-nexomon';
      } else {
        return '';
      }
    },
    showTooltip(event, nexomon) {
      if (nexomon._regionException && this.selectedMap) {
        this.tooltipNexomon = nexomon.Number;
        this.tooltipText = nexomon._regionExceptionText;
        this.tooltipPos.visible = true;
      }
    },
    hideTooltip() {
      this.tooltipNexomon = null;
      this.tooltipText = '';
      this.tooltipPos.visible = false;
    },
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
  width: 640px;
  height: 400px;
  object-fit: contain;
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
  margin: 20px 0 30px 0;
}

.nexomon-grid {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  padding: 0;
  margin: 0 auto;
  max-width: 1200px;
  gap: 2px; /* Tighter gap between grid items */
}

.nexomon-item {
  width: calc(16.666% - 8px); /* Reduced margin for tighter layout */
  margin: 4px;
  padding: 10px 6px 15px;
  border: 1px solid #ccc;
  border-radius: 8px;
  text-align: center;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  max-height: 290px;
  text-decoration: none;
  color: inherit;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: center;
  position: relative;
}

.nexomon-item:hover {
  background-color: rgba(141, 140, 140, 0.068);
  transform: scale(1.02);
}

@media (hover: none) {
  /* Special touch interactions for mobile devices */
  .nexomon-item:active {
    background-color: rgba(141, 140, 140, 0.12);
    transform: scale(0.98);
    transition: all 0.1s ease;
  }
}

.highlighted-nexomon {
  background-color: rgba(43, 159, 204, 0.15) !important;
  border-color: rgb(43, 159, 204) !important;
  box-shadow: 0 0 8px rgba(43, 159, 204, 0.4) !important;
  transform: scale(1.02);
}

.dark-mode .highlighted-nexomon {
  background-color: rgba(43, 159, 204, 0.25) !important;
  border-color: rgb(43, 159, 204) !important;
  box-shadow: 0 0 10px rgba(43, 159, 204, 0.6) !important;
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
  margin: 10px 0 30px 0;
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 0;
  overflow: hidden;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
  background-color: #f9f9f9;
}

.section-header {
  cursor: pointer;
  display: flex;
  justify-content: center;
  padding: 12px;
  transition: background-color 0.3s ease;
  border-radius: 0;
}

.section-header:hover {
  background-color: rgba(0, 0, 0, 0.03);
}

.section-header h2 {
  margin: 0;
  display: flex;
  align-items: center;
  font-size: 1.5rem;
}

.toggle-icon {
  margin-left: 10px;
  font-size: 0.8rem;
}

.section-content {
  padding: 10px 10px 15px;
  overflow: hidden;
  background-color: #f9f9f9; /* Consistent background to avoid white lines */
}

.dark-mode .section-content {
  background-color: #2a2a2a;
}

/* Collapse/expand transition effects */
.collapse-enter-active,
.collapse-leave-active {
  transition: all 0.4s cubic-bezier(0.4, 0.0, 0.2, 1);
  max-height: 2000px; /* Higher value to accommodate more content */
  opacity: 1;
  overflow: hidden;
  will-change: max-height, opacity;
}

.collapse-enter-from,
.collapse-leave-to {
  max-height: 0;
  opacity: 0;
  overflow: hidden;
  padding: 0;
}

.maps-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 20px;
  list-style-type: none;
  padding: 0;
  margin: 5px 0 0 0;
  border: none;
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

.map-item {
  cursor: pointer;
  transition: all 0.3s ease;
}

.map-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

@media (hover: none) {
  /* Touch interactions for mobile devices */
  .map-item:active {
    background-color: rgba(0, 0, 0, 0.05);
    transform: scale(0.98);
    transition: all 0.1s ease;
  }
  
  .dark-mode .map-item:active {
    background-color: rgba(255, 255, 255, 0.1);
  }
}

.selected-map {
  border-color: rgb(43, 159, 204);
  background-color: rgba(43, 159, 204, 0.1);
  box-shadow: 0 0 10px rgba(43, 159, 204, 0.3);
  transform: translateY(-3px);
}

.map-highlight-notice {
  background-color: rgba(43, 159, 204, 0.1);
  padding: 8px 15px;
  border-radius: 5px;
  margin: 10px 0 20px;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 1rem;
}

.clear-btn {
  margin-left: 10px;
  padding: 2px 8px;
  font-size: 0.8rem;
}

/* Dark mode adjustments */
.dark-mode .map-item {
  border-color: #555;
  background-color: #2a2a2a;
}

.dark-mode .selected-map {
  border-color: rgb(43, 159, 204);
  background-color: rgba(43, 159, 204, 0.2);
  box-shadow: 0 0 15px rgba(43, 159, 204, 0.4);
}

.dark-mode .map-highlight-notice {
  background-color: rgba(43, 159, 204, 0.2);
  color: #fff;
}

/* Dark mode styling for collapsible sections */
.dark-mode .maps-section {
  border-color: #444;
  background-color: #2a2a2a;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
}

.dark-mode .section-header:hover {
  background-color: rgba(255, 255, 255, 0.05);
}

/* Media Queries for Responsiveness */
@media (max-width: 3840px) {
  .nexomon-item {
    width: calc(16.666% - 8px);
    margin: 4px;
    max-height: 310px;
  }
}

@media (max-width: 1925px) {
  .nexomon-item {
    width: calc(16.666% - 8px);
    margin: 4px;
    max-height: 300px;
  }
}

@media (max-width: 1280px) {
  .nexomon-item {
    width: calc(20% - 6px);
    margin: 3px;
    max-height: 290px;
  }
}

@media (max-width: 1024px) {
  .nexomon-item {
    width: calc(25% - 6px);
    margin: 3px;
    max-height: 280px;
  }
}

@media (max-width: 768px) {
  .nexomon-grid {
    gap: 0;
    justify-content: space-evenly;
  }
  
  .nexomon-item {
    width: calc(33.333% - 4px);
    margin: 2px;
    max-height: 260px;
  }
}

@media (max-width: 600px) {
  .nexomon-grid {
    gap: 0;
    justify-content: space-evenly;
  }
  
  .nexomon-item {
    width: calc(33.333% - 4px); /* 3 per row with minimal spacing */
    margin: 2px;
    max-height: 220px;
  }
  
  .nexomon-thumb {
    width: 56px;
    height: 56px;
  }
  
  .nexomon-name {
    font-size: 0.85em;
  }
  
  .nexomon-number {
    font-size: 0.77em;
  }
}

@media (max-width: 480px) {
  .location-details-wrapper {
    padding: 15px 10px;
  }
  
  .region-image {
    width: 320px;
    height: 200px;
  }

  .nexomon-grid {
    gap: 0;
    justify-content: space-evenly;
  }

  .nexomon-item {
    width: calc(33.333% - 2px); /* 3 per row with minimal spacing */
    margin: 1px;
    max-height: 160px;
    padding: 6px 4px 8px;
  }

  .nexomon-name {
    font-size: 0.75em;
    min-height: 2.6em;
    line-height: 1.2em;
  }
  
  .nexomon-number {
    font-size: 0.7em;
  }
  
  .nexomon-thumb {
    width: 40px;
    height: 40px;
    margin-bottom: 4px;
  }

  h1 {
    font-size: 1.5rem;
    margin-bottom: 0.5rem;
  }

  h2 {
    font-size: 1.3rem;
    margin-bottom: 0.5rem;
  }
}

/* Maps section responsiveness */
@media (max-width: 768px) {
  .maps-list {
    grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
    gap: 15px;
  }
  
  .map-image {
    width: 120px;
    height: 120px;
  }

  .section-header {
    padding: 15px; /* Larger touch target */
  }
  
  .toggle-icon {
    font-size: 0.9rem;
    margin-left: 15px;
  }
}

@media (max-width: 480px) {
  .maps-list {
    grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
    gap: 10px;
  }
  
  .map-image {
    width: 100px;
    height: 100px;
  }
  
  .map-name {
    font-size: 0.9rem;
    margin-bottom: 8px;
  }

  .map-item {
    padding: 8px;
  }
  
  .section-header h2 {
    font-size: 1.3rem;
  }
  
  .map-highlight-notice {
    font-size: 0.9rem;
    padding: 6px 12px;
    margin: 8px 0 15px;
  }
  
  .clear-btn {
    padding: 1px 6px;
    font-size: 0.7rem;
  }
}

/* Extra small screens */
@media (max-width: 359px) {
  .location-details-wrapper {
    padding: 10px 6px;
  }

  .nexomon-grid {
    gap: 0;
    justify-content: space-evenly;
  }

  .nexomon-item {
    width: calc(33.333% - 1px); /* Maintain 3 per row with minimal spacing */
    margin: 0.5px;
    max-height: 140px;
    padding: 4px 1px 6px;
  }

  .nexomon-thumb {
    width: 36px;
    height: 36px;
  }
  
  .maps-list {
    grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
    gap: 8px;
  }
  
  .map-image {
    width: 80px;
    height: 80px;
  }
  
  .map-name {
    font-size: 0.8rem;
    margin-bottom: 6px;
  }

  h1 {
    font-size: 1.4rem;
    margin-bottom: 0.4rem;
  }

  h2 {
    font-size: 1.2rem;
    margin-bottom: 0.4rem;
  }

  .section-header h2 {
    font-size: 1.2rem;
  }
}

/* Very narrow screens */
@media (max-width: 320px) {
  .nexomon-item {
    width: calc(50% - 1px); /* Switch to 2 per row with minimal spacing */
    margin: 0.5px;
    padding: 4px 1px 6px;
  }

  .nexomon-name {
    font-size: 0.7em;
    min-height: 2.4em;
  }

  .nexomon-thumb {
    width: 32px;
    height: 32px;
  }
}

.exception-nexomon {
  border-color: #e6b800 !important;
  box-shadow: 0 0 8px rgba(230, 184, 0, 0.3) !important;
  background-color: rgba(255, 243, 205, 0.4) !important;
  position: relative;
}

.dark-mode .exception-nexomon {
  border-color: #ffd700 !important;
  background-color: rgba(80, 70, 0, 0.3) !important;
}

.exception-icon {
  margin-left: 6px;
  font-size: 1.1em;
  vertical-align: middle;
  cursor: pointer;
}

.custom-tooltip {
  position: absolute;
  left: 50%;
  top: -44px;
  transform: translateX(-50%);
  background: #fffbe6;
  color: #7a5a00;
  border: 1px solid #e6b800;
  border-radius: 8px;
  padding: 8px 14px;
  font-size: 0.95em;
  box-shadow: 0 2px 8px rgba(230, 184, 0, 0.15);
  white-space: pre-line;
  min-width: 180px;
  max-width: 260px;
  pointer-events: none;
  opacity: 1;
  transition: opacity 0.15s;
  z-index: 2147483647;
}
.dark-mode .custom-tooltip {
  background: #2a2300;
  color: #ffe066;
  border: 1px solid #ffd700;
  box-shadow: 0 2px 8px rgba(255, 215, 0, 0.18);
  z-index: 2147483647;
}
</style>

<style scoped src="../assets/styles/button-styles.css"></style>

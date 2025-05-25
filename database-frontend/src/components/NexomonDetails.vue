<!-- src/components/NexomonDetails.vue -->
<template>
  <div class="nexomon-details-wrapper"> <!-- Add this wrapping div -->
    <div class="nexomon-maininfo-container">
      <div v-if="isCaught(nexomon.Number)" class="caught-checkmark-overlay">
        <span class="caught-checkmark">✔</span>
      </div>
      <div class="main-infos">
        <!-- Consistent Nexomon name/number display -->
        <div class="nexomon-info">
          <div class="nexomon-number">{{ nexomon.Number }}</div>
          <div class="nexomon-name">{{ nexomon.Name }}</div>
        </div>
        <div class="sprite-container">
          <img class="nexomon-sprite" :src="getImage(nexomon.Name, showCosmic)" alt="Nexomon Sprite" />
          <div class="element-info">
            <h3 style="margin-top: 7px;">Element:</h3>
            <img :src="getImage(nexomon.Element + '_Type_Icon')" alt="Element Image" class="element-label" />            <span>{{ nexomon.Element }}</span>
            <button v-if="nexomon.Sprites && nexomon.Sprites.Cosmic" class="nexo-button nexo-button-toggle" @click="toggleSprite">
              {{ showCosmic ? 'Show Regular' : 'Show Cosmic' }}
            </button>
          </div>
          <div class="navigation-buttons">
            <button class="nexo-button nexo-button-primary" @click="goToPreviousNexomon" :disabled="!hasPrevious" aria-label="Previous Nexomon">Previous</button>
            <button class="nexo-button nexo-button-danger details-back-btn" @click="goBack">{{ backButtonText }}</button>
            <button class="nexo-button nexo-button-primary" @click="goToNextNexomon()" :disabled="!hasNext" aria-label="Next Nexomon">Next</button>
          </div>
          <div class="description-container">
            <p>{{ description.Description }}</p>
          </div>
          <div class="rarity-row">
            <h3 style="margin: 0; font-weight: 500;">Rarity:</h3>
            <span class="rarity-label" :style="{ backgroundColor: getRarityColor(nexomon.Rarity), color: 'white' }">{{ nexomon.Rarity }}</span>
          </div>
        </div>
      </div>
    </div>

      <div class="extra-info">
        <div class="extra-section" @click="toggleSection('battle-info')">
          <h3>&#x1F94A; Battle Info </h3>
          <div
            :class="{ 'extra-list': true, 'expanded': !collapsedSections['battle-info'], 'collapsed': collapsedSections['battle-info'] }"
            v-if="!collapsedSections['battle-info']">
            <table>
              <tbody>
                <tr>
                  <td>
                  <span>{{ nexomon.Name }}'s Type: <img :src="getImage(nexomon.Element + '_Type_Icon')" alt="Element Image" class="element-image" /></span>
                  </td>
                </tr>
                <tr v-if="effectiveVs.length > 0">
                  <td>
                    <strong><span style='color:green' class="battle-text">Effective</span> Against:</strong>
                    <ul>
                      <li v-for="type in effectiveVs" :key="type" class="extra-item">
                        <img :src="getImage(type + '_Type_Icon')" alt="Element Image" class="element-image" />{{ type }}
                      </li>
                    </ul>
                  </td>
                </tr>
                <tr v-if="vulnerableTo.length > 0">
                  <td>
                    <strong><span style='color:crimson' class="battle-text">Vulnerable</span> Against:</strong>
                    <ul>
                      <li v-for="type in vulnerableTo" :key="type" class="extra-item">
                        <img :src="getImage(type + '_Type_Icon')" alt="Element Image" class="element-image" />{{ type }}
                      </li>
                    </ul>
                  </td>
                </tr>
                <tr v-if="ineffectiveVs.length > 0">
                  <td>
                    <strong><span style='color:dodgerblue' class="battle-text">Ineffective</span> Against:</strong>
                    <ul>
                      <li v-for="type in ineffectiveVs" :key="type" class="extra-item">
                        <img :src="getImage(type + '_Type_Icon')" alt="Element Image" class="element-image" />{{ type }}
                      </li>
                    </ul>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <div class='extra-section' @click="toggleSection('loved-food')">
          <h3>&#x1F359; Loved Food</h3>
          <div
            :class="{ 'extra-list': true, 'expanded': !collapsedSections['loved-food'], 'collapsed': collapsedSections['loved-food'] }"
            v-if="!collapsedSections['loved-food']">
            <table>
              <tbody>
                <tr v-if="lovedFood.length > 0">
                  <td>
                    <ul>
                      <li v-for="food in lovedFood" :key="food" class="extra-item">
                        <img :src="getFoodImage(food)" alt="Food Image" class="food-image" />{{ food.name }}
                      </li>
                    </ul>
                  </td>
                </tr>
                <tr v-else>
                  <td>
                    <ul>
                      <li>
                        No food info to display
                      </li>
                    </ul>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <div class='extra-section' @click="toggleSection('base-stats')">
          <h3>&#x1F4C8; Base Stats</h3>
          <div
            :class="{ 'extra-list': true, 'expanded': !collapsedSections['base-stats'], 'collapsed': collapsedSections['base-stats'] }"
            v-if="!collapsedSections['base-stats']">
            <table>
              <tbody>
                <tr>
                  <td>
                    <ul>
                      <li v-for="(value, key) in baseStats" :key="key" class="extra-item">
                        <img :src="getStatImage(key)" alt="Stat image" class="element-image" />{{ key }} : {{ value }}
                      </li>
                      <li class="extra-item">
                        <span style="margin-right: 5%; font-size:24px">&#x1F4CB;</span> Stats Total: {{ nexomon.BST }}
                      </li>
                    </ul>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <!-- Standalone Skill Tree collapsible section -->
      <div class="skill-tree-section">
        <div class="section-header" @click="toggleSkillTreeSection">
          <h2>Skill Tree <span class="toggle-icon">{{ skillTreeCollapsed ? '▼' : '▲' }}</span></h2>
        </div>
        <transition name="collapse">
          <div v-show="!skillTreeCollapsed" class="section-content">
            <div>
              <template v-if="skillTree.length">
                <div class="skill-tree-table-container">
                  <table class="skill-tree-table">
                    <thead>
                      <tr>
                        <th>Level</th>
                        <th>Skill</th>
                        <th>Type</th>
                        <th>Power</th>
                        <th>Acc</th>
                        <th>STA</th>
                        <th>Speed</th>
                        <th>Crit %</th>
                        <th>Effect</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr v-for="(skill, idx) in skillTree" :key="idx" @click="goToSkill(skill._db?.Name)" style="cursor:pointer;">
                        <td>{{ skill.Level || skill.level || '-' }}</td>
                        <td style="text-align:left;">
                          <img v-if="skill._db && skill._db.Image" :src="require(`@/assets/${skill._db.Image}`)" :alt="skill._db.Name" style="height:28px;vertical-align:middle;margin-right:6px;" />
                          {{ skill._db?.Name || skill.Skill?.text || skill.Skill || '-' }}
                        </td>
                        <td>
                          <img v-if="skill._db && skill._db.Type && skill._db.Type.image" :src="require(`@/assets/${skill._db.Type.image}`)" :alt="skill._db.Type.text.replace(' Type', '')" class="skill-type-icon" />
                          <span>{{ skill._db?.Type?.text ? skill._db.Type.text.replace(' Type', '') : '-' }}</span>
                        </td>
                        <td>{{ skill._db?.Power || '-' }}</td>
                        <td>{{ skill._db?.Acc || '-' }}</td>
                        <td>{{ skill._db?.STA || '-' }}</td>
                        <td>{{ skill._db?.Speed || '-' }}</td>
                        <td>{{ skill._db?.['Crit %'] || '-' }}</td>
                        <td>
                          <span v-if="skill._db && skill._db.Effect && skill._db.Effect.image">
                            <img :src="require(`@/assets/${skill._db.Effect.image}`)" :alt="skill._db.Effect.text" style="height:22px;vertical-align:middle;margin-right:4px;" />
                          </span>
                          {{ skill._db?.Effect?.text ? skill._db.Effect.text.replace(' (Status)', '') : (skill._db?.Effect ? skill._db.Effect.replace(' (Status)', '') : '-') }}
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </template>
              <template v-else>
                <div>No skill tree data available.</div>
              </template>
            </div>
          </div>
        </transition>
      </div>

    </div>

    <div v-if="nexomon.Evolution && nexomon.Evolution.length" class="evolution-container">
      <h3>Evolution Line:</h3>
      <div>
        <router-link class="evolution-stage" v-for="(details, nexomonName) in nexomonEvolution" :key="nexomonName"
          :to="goToEvolution(nexomonName)">
          <img :src="getImage(nexomonName)" :alt="nexomonName" class="evolution-image" />
          <span>{{ nexomonName }} - {{ details.text }}</span>
        </router-link>
      </div>
    </div>

    <div class="location-info">
      <h3>Locations</h3>

      <p v-if="!hasLocations" class="location-exception">{{ locationException }}</p>

      <div class="regions-grid">

        <div class="region-card" v-for="(region, index) in nexomon.Locations" :key="index" @click="toggleRegion(index)">

          <img :src="getRegionImage(region.Region.text)" alt="Region Image" class="region-image" />          <div class="region-text">
            <h4>{{ region.Region.text }}</h4>
            <button class="nexo-button nexo-button-primary" @click.stop="goToLocation(region.Region.text)">
              View Region Details
            </button>
          </div>

          <!-- Only show maps when the card is expanded --><div
            :class="{ 'maps-list': true, 'expanded': expandedRegion === index, 'collapsed': expandedRegion !== index }">
            <ul @click.stop>
              <!-- Quest exception notice -->
              <div v-if="region.Exception" class="quest-exception">
                <strong>Quest Location:</strong> {{ region.Exception }}
              </div>
              
              <!-- Maps list -->
              <template v-if="Array.isArray(region.Maps)">
                <li v-for="map in region.Maps" :key="map" @mouseenter="hoverMap(map)"
                  @mouseleave="hoverMap(null)" @click="clickMap(map)" :class="{ 'highlighted-map': clickedMap === map }">
                  {{ map }} <br>
                  <img v-if="hoveredMap === map || clickedMap === map" :src="getMapImage(map)" alt="Map Image"
                    class="map-preview" />
                </li>
              </template>
              <!-- Legacy format support -->
              <template v-else-if="typeof region.Maps === 'string'">
                <!-- Check if this is a quest location (legacy format) -->
                <template v-if="isQuestLocation(region)">
                  <li v-for="map in getCleanMapsList(region.Maps)" :key="map" @mouseenter="hoverMap(map)"
                    @mouseleave="hoverMap(null)" @click="clickMap(map)" :class="{ 'highlighted-map': clickedMap === map }">
                    {{ map }} <br>
                    <img v-if="hoveredMap === map || clickedMap === map" :src="getMapImage(map)" alt="Map Image"
                      class="map-preview" />
                  </li>
                </template>
                <!-- Regular location (legacy format) -->
                <template v-else>
                  <li v-for="map in region.Maps.split(', ')" :key="map" @mouseenter="hoverMap(map)"
                    @mouseleave="hoverMap(null)" @click="clickMap(map)" :class="{ 'highlighted-map': clickedMap === map }">
                    {{ map }} <br>
                    <img v-if="hoveredMap === map || clickedMap === map" :src="getMapImage(map)" alt="Map Image"
                      class="map-preview" />
                  </li>
                </template>
              </template>
            </ul>
          </div>

        </div>
      </div>
    </div>

    <!-- Supa Zoom -->    <div v-if="showZoom" class="zoomed-map-overlay" @click="closeZoom">
      <div class="zoomed-map-container">
        <img :src="zoomedMap" alt="Zoomed Map" class="zoomed-map-image" />
        <button class="nexo-button nexo-button-secondary close-zoom-btn" @click.stop="closeZoom">Close</button>
      </div>
    </div>
</template>



<script>
import data from '../../../python-scripts/assets/nexomon_extinction_database.json';
import descriptionData from '../../../python-scripts/assets/nexomon_description_database.json'
import locationExceptions from '../assets/location_exceptions.json';
import typeChart from '../assets/type_chart.json'
import skillDatabase from '../assets/skill_database.json';
import { useCaughtMode } from './useCaughtMode.js';

export default {
  props: ['number'],
  setup() {
    const { caughtMode, toggleCaught, isCaught } = useCaughtMode();
    return { caughtMode, toggleCaught, isCaught };
  },
  data() {
      return {
        database: data,
        description_database: descriptionData,
        locationExceptions: locationExceptions,
        typeChart: typeChart,
        showCosmic: false,
        expandedRegion: null,
        hoveredMap: null,
        zoomedMap: null,
        showZoom: false,
        clickedMap: null,
        questLocations: locationExceptions.quest_locations || {},
        collapsedSections: {
          'battle-info': true,
          'loved-food': true,
          'base-stats': true,
        },
        skillTreeCollapsed: true, // Collapsed by default
      };
    },
  computed: {
    //Basic Info
    nexomon() {
      return this.database.find(n => parseInt(n.Number) === parseInt(this.number));
    },

    description() {
      return this.description_database.find(n => parseInt(n.Number) === parseInt(this.number))
    },

    //Evolution Info
    nexomonEvolution() {
      if (this.nexomon && this.nexomon.Evolution && this.nexomon.Evolution.length > 0) {
        return this.nexomon.Evolution[0];
      }
      return {};
    },

    //Navigation Info
    hasPrevious() {
      return this.nexomon && parseInt(this.nexomon.Number) > 1;
    },
    hasNext() {
      return this.nexomon && parseInt(this.nexomon.Number) < this.database.length;
    },

    //Habitat Info
    hasLocations() {
      return this.nexomon && this.nexomon.Locations && this.nexomon.Locations.length > 0;
    },
    locationException() {
      if (!this.hasLocations && this.nexomon) {
        // Check both locationExceptions and legendary_exceptions
        if (this.locationExceptions[this.nexomon.Name]) {
          return this.locationExceptions[this.nexomon.Name];
        }
        if (
          this.locationExceptions.legendary_exceptions &&
          this.locationExceptions.legendary_exceptions[this.nexomon.Name]
        ) {
          return this.locationExceptions.legendary_exceptions[this.nexomon.Name];
        }
        return "No specific habitat information.";
      }
      return null;
    },

    //Battle Info
    effectiveVs() {
      return this.typeChart.types[this.nexomon.Element]?.effective_vs || [];
    },
    vulnerableTo() {
      return this.typeChart.types[this.nexomon.Element]?.vulnerable_to || [];
    },
    ineffectiveVs() {
      return this.typeChart.types[this.nexomon.Element]?.ineffective_vs || [];
    },

    //Food Info
    lovedFood() {
      if (this.nexomon && this.nexomon['Loved Food'] && this.nexomon['Loved Food'].length > 0) {
        return this.nexomon['Loved Food'];
      }
      return { name: "This nexomon doesn't have any loved food" };
    },    //Stats Info
    baseStats() {
      if (this.nexomon) {
        return this.nexomon['Stats']
      }
      return {}
    },
    
    skillTree() {
      if (!this.nexomon || !this.nexomon['Skill Tree']) return [];
      // Map each skill in the tree to its full info from the skill database
      return this.nexomon['Skill Tree'].map(entry => {
        let skillName = entry.Skill?.text || entry.Skill?.name || entry.Skill || '';
        let dbSkill = skillDatabase.find(s => s.Name === skillName);
        return {
          ...entry,
          _db: dbSkill
        };
      });
    },
    
    //UI Text
    backButtonText() {
      // Check if we came from a location page
      const previousRouteString = localStorage.getItem('previousRoute');
      try {
        const previousRoute = JSON.parse(previousRouteString);
        if (previousRoute && previousRoute.name === 'Location Details') {
          return `Back to ${previousRoute.params.location}`;
        }
        if (previousRoute && previousRoute.name === 'My Collection') {
          return 'Back to Collection';
        }
      } catch (e) {
        // If there's an error parsing, fall back to default text
      }
      return 'Back';
    }
  },

  mounted() {
    this.preloadImages(); // Preload battle and food images on page load
    window.addEventListener('keydown', this.handleArrowNavigation);
    window.addEventListener('keydown', this.handleSpacebarCaught);
  },
  beforeUnmount() {
    window.removeEventListener('keydown', this.handleArrowNavigation);
    window.removeEventListener('keydown', this.handleSpacebarCaught);
  },
  methods: {
    // Quest location related methods
    isQuestLocation(region) {
      if (typeof region.Maps === 'string') {
        return region.Maps.includes("Only during the Resurrect Bolzen quest:");
      }
      return false;
    },

    getCleanMapsList(mapsString) {
      if (typeof mapsString !== 'string') return [];
      // Remove the quest text and split by comma
      return mapsString.replace("Only during the Resurrect Bolzen quest:", "").split(', ')
        .map(map => map.trim())
        .filter(map => map.length > 0);
    },

    // Existing methods
    toggleSection(section) {
      this.collapsedSections[section] = !this.collapsedSections[section];
    },    toggleRegion(index) {
      if (this.expandedRegion !== index) {
        this.expandedRegion = index;

        // Get the maps from the region
        const regionMaps = this.nexomon.Locations[index].Maps;
        
        // Preload all map images for the clicked region
        if (typeof regionMaps === 'string') {
          // Handle legacy string format
          this.preloadMapImages(regionMaps.split(', '));
        } else if (Array.isArray(regionMaps)) {
          // Handle new array format
          this.preloadMapImages(regionMaps);
        }
      } else {
        this.expandedRegion = null;
      }
    },

    getRarityColor(rarity) {
      switch (rarity) {
        case 'Common':
          return 'grey';
        case 'Uncommon':
          return 'green';
        case 'Rare':
          return 'aqua';
        case 'Mega Rare':
          return 'purple';
        case 'Ultra Rare':
          return 'brown';
        case 'Ultimate':
          return '#264BA3'
        case 'Legendary':
          return 'orange'; // or use a gradient if needed
        default:
          return 'transparent'; // default background color
      }
    },

    preloadMapImages(mapNames) {
      this.preloadedImages = mapNames.map(mapName => {
        const formattedMapName = mapName.replace(/\s+/g, '_'); // Format the map name as needed
        const img = new Image();
        img.src = this.getMapImage(formattedMapName);
        return img;
      });
    },

    hoverMap(map) {
      this.hoveredMap = map;
    },

    clickMap(map) {
      this.clickedMap = map;
      this.zoomedMap = this.getMapImage(map);
      this.showZoom = true;
    },    closeZoom() {
      this.clickedMap = null;
      this.showZoom = false;
    },    goBack() {
      // Check if we came from a location details page, skill details page, or collection page
      const previousRouteString = localStorage.getItem('previousRoute');
      let previousRoute = null;
      try {
        if (previousRouteString) {
          previousRoute = JSON.parse(previousRouteString);
        }
      } catch (e) {
        console.error('Error parsing previous route from localStorage', e);
      }
      if (previousRoute && previousRoute.name === 'Location Details' && previousRoute.params.location) {
        this.$router.push({ 
          name: 'Location Details', 
          params: { location: previousRoute.params.location }
        });
      } else if (previousRoute && previousRoute.name === 'Skill Details' && previousRoute.params.name) {
        this.$router.push(`/skill/${encodeURIComponent(previousRoute.params.name)}`);
      } else if (previousRoute && previousRoute.name === 'My Collection') {
        this.$router.push({ name: 'My Collection' });
      } else {
        this.$router.push({ name: 'Nexomon Database', params: {} });
      }
    },
    
    goToLocation(locationName) {
      // Navigate to the location details page
      this.$router.push({ 
        name: 'Location Details', 
        params: { location: locationName }
      });
    },goToNexomon(number) {
      this.showCosmic = false;
      this.expandedRegion = null;
      
      // When using Next/Previous buttons, we want to clear location context
      // Set a marker that we're navigating within the Nexomon list
      localStorage.setItem('previousRoute', JSON.stringify({
        name: 'Nexomon Database',
        path: '/',
        params: {}
      }));
      
      this.$router.push({ name: 'Nexomon Details', params: { number } });
    },

    goToEvolution(nexomonName) {
      let evolvedNexomon = this.database.find(n => n.Name == nexomonName);
      if (evolvedNexomon) {
        return `/nexomon/${evolvedNexomon.Number}`
      }
      return ''
    },

    getFoodImage(food) {
      const imageName = food.name.replace(' ', '-');
      return require(`@/assets/downloaded_images/${imageName}.png`);
    },

    getStatImage(stat) {
      return require(`@/assets/downloaded_images/${stat}_Stat_Icon.png`)
    },

    getImage(imageName, showCosmic) {
      if (showCosmic) {
        try {
          return require(`@/assets/downloaded_images/${imageName}_Cosmic.png`);
        } catch (error) {
          try {
            return require(`@/assets/downloaded_images/${imageName}2_Cosmic.png`);
          } catch (error) {
            console.warn(`Neither ${imageName}_Cosmic.png nor ${imageName}2_Cosmic.png were found.`);
          }
        }
      } else {

        imageName = imageName.replace(' (Extinction)', '');

        try {
          return require(`@/assets/downloaded_images/${imageName}.png`);
        } catch (error) {
          try {
            return require(`@/assets/downloaded_images/${imageName}2.png`);
          } catch (error) {
            console.warn(`Neither ${imageName}.png nor ${imageName}2.png were found.`);
          }
        }
      }
    },

    getRegionImage(regionName) {
      while (regionName.includes(' ')) {
        regionName = regionName.replace(" ", "_")
      }

      return require(`@/assets/downloaded_images/${regionName}Warp.png`);
    },

    toggleSprite() {
      this.showCosmic = !this.showCosmic;
    },

    getMapImage(mapName) {
      const formattedMapName = mapName.replace(/\s+/g, '_');
      try {
        return require(`@/assets/downloaded_location_images/${formattedMapName}.png`);
      } catch (error) {
        console.warn(`Map image for ${formattedMapName} not found.`);
        return null;
      }
    },

    preloadImages() {
      // Preload battle info images (element icons)
      const elementTypes = [...this.effectiveVs, ...this.vulnerableTo, ...this.ineffectiveVs];
      this.preloadImageSet(elementTypes, 'downloaded_images', 'Type_Icon');

      // Preload loved food images
      if (this.lovedFood && this.lovedFood.length > 0) {
        const foodImages = this.lovedFood.map(food => food.name);
        this.preloadImageSet(foodImages, 'downloaded_images');
      }
    },

    // Helper method to preload a set of images from a folder
    preloadImageSet(imageNames, folder, extra_params) {
      imageNames.forEach(name => {
        const img = new Image();
        let formattedName = name.replace(/\s+/g, '-'); // Replace spaces with hyphens
        img.src = this.getImagePath(formattedName, folder, extra_params);
      });
    },

    // Helper method to get the correct image path based on the folder
    getImagePath(name, folder, extra_params) {
      if (extra_params) {
        return require(`@/assets/${folder}/${name}_${extra_params}.png`);
      } else {
        return require(`@/assets/${folder}/${name}.png`);
      }
    },

    toggleSkillTreeSection() {
      this.skillTreeCollapsed = !this.skillTreeCollapsed;
    },

    goToSkill(skillName) {
      if (!skillName || typeof skillName !== 'string' || !skillName.trim()) return;
      // Save current route as previousRoute for back navigation
      localStorage.setItem('previousRoute', JSON.stringify({
        name: 'Skill Details',
        path: `/skill/${skillName}`,
        params: { name: skillName }
      }));
      this.$router.push(`/skill/${encodeURIComponent(skillName)}`);
    },

    goToPreviousNexomon() {
      if (this.hasPrevious) {
        this.goToNexomon(parseInt(this.nexomon.Number) - 1);
      }
    },

    goToNextNexomon() {
      console.log()
      if (this.hasNext) {
        this.goToNexomon(parseInt(this.nexomon.Number) + 1);
      }
    },

    handleArrowNavigation(e) {
      if (e.key === 'ArrowLeft') {
        this.goToPreviousNexomon();
      } else if (e.key === 'ArrowRight') {
        this.goToNextNexomon();
      }
    },

    handleSpacebarCaught(e) {
      if (e.code === 'Space') {
          this.toggleCaught(this.nexomon.Number);
        e.preventDefault();
      }
    },
  }
};
</script>

<style scoped>
.details-container {
  text-align: center;
}

.nexomon-info {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 0 !important;
}

.nexomon-number {
  font-size: 1.3rem;
  color: #666;
  margin-bottom: 4px;
  background-color: rgba(0, 0, 0, 0.05);
  padding: 4px 14px;
  border-radius: 10px;
  display: inline-block;
  font-weight: 600;
  margin-top: 20px
}

.dark-mode .nexomon-number {
  color: #aaa;
  background-color: rgba(255, 255, 255, 0.1);
}

.nexomon-name {
  font-size: 2rem;
  text-align: center;
  width: 100%;
  min-height: 2.8em;
  line-height: 1.4em;
  word-wrap: break-word;
  hyphens: auto;
  font-weight: 700;
  margin-bottom: -20px;
}

.navigation-buttons {
  margin: 20px 0;
  display: flex;
  justify-content: center;
  gap: 15px;
}

.nexomon-details-wrapper {
  width: 100%;
}

.close-zoom-btn {
  position: absolute;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
}

@media (max-width: 1024px) {
  .nexomon-number {
    font-size: 1.2rem;
    padding: 3px 10px;
  }
  .nexomon-name {
    font-size: 1.5rem;
  }
  html, body, .nexomon-details-wrapper, .regions-grid, .region-card, .skill-tree-section, .skill-tree-table {
    max-width: 100vw !important;
    overflow-x: hidden !important;
  }
}
@media (max-width: 600px) {
  .nexomon-number {
    font-size: 1.2rem;
    padding: 2px 8px;
  }
  .nexomon-name {
    font-size: 1.5rem;
  }
}

.location-exception {
  margin: 18px auto 18px auto;
  max-width: 600px;
  width: fit-content;
  min-width: 220px;
  background: #f8f9fa;
  color: #333;
  border: 1.5px solid #d1d5db;
  border-radius: 10px;
  padding: 18px 22px;
  text-align: center;
  font-size: 1.08rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.07);
  font-style: italic;
  display: block;
  margin-left: auto;
  margin-right: auto;
  max-width: 90vw;
}

.dark-mode .location-exception {
  background: #23272e;
  color: #e0e0e0;
  border: 1.5px solid #444b55;
  box-shadow: 0 2px 8px rgba(0,0,0,0.25);
}

.location-info {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.nexomon-maininfo-container {
  background: #fafdff;
  border-radius: 18px;
  box-shadow: 0 4px 24px rgba(0,0,0,0.10), 0 1.5px 6px rgba(0,0,0,0.04);
  padding: 32px 32px 24px 32px;
  margin: 0 auto 32px auto;
  max-width: 520px;
  min-width: 260px;
  display: flex;
  flex-direction: column;
  align-items: center;
  border: none;
  position: relative;
  z-index: 2;
  transition: background 0.3s, box-shadow 0.3s;
  margin-top: 20px;
}
.dark-mode .nexomon-maininfo-container {
  background: #23272b;
  border: none;
  box-shadow: 0 4px 24px rgba(0,0,0,0.18), 0 1.5px 6px rgba(0,0,0,0.18);
}
.details-back-btn {
  margin-top: 18px;
  align-self: flex-end;
}

/* Caught checkmark overlay */
.caught-checkmark-overlay {
  position: absolute;
  top: 10px;
  right: 10px;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(0, 128, 0, 0.8);
  border-radius: 50%;
  z-index: 3;
}

.caught-checkmark {
  color: white;
  font-size: 30px;
  line-height: 1;
}

</style>

<style scoped src="../assets/styles/basic-info.css"></style>
<style scoped src="../assets/styles/location-info.css"></style>
<style scoped src="../assets/styles/evolution-info.css"></style>
<style scoped src="../assets/styles/extra-info.css"></style>
<style scoped src="../assets/styles/button-styles.css"></style>
<style scoped src="../assets/styles/section-common.css"></style>
<style scoped src="../assets/styles/skill-tree.css"></style>

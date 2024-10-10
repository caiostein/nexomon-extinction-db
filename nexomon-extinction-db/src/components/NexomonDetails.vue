<!-- src/components/NexomonDetails.vue -->
<template>
  <div v-if="nexomon" class="details-container">
    <h1 class="h1" style="margin-top: 20px;">{{ nexomon.Number }} - {{ nexomon.Name }}</h1>

    <div class="sprite-container">
      <img class="nexomon-sprite" :src="getImage(nexomon.Name, showCosmic)" alt="Nexomon Sprite" />
    </div>

    <div class="element-info">
      <h3>Element:</h3>
      <img :src="getImage(nexomon.Element + '_Type_Icon')" alt="Element Image" class="element-image" />
      <span>{{ nexomon.Element }}</span>

      <button v-if="nexomon.Sprites && nexomon.Sprites.Cosmic" class="toggle-button" @click="toggleSprite">
        {{ showCosmic ? 'Show Regular' : 'Show Cosmic' }}
      </button>
    </div>

    <h3>Rarity: {{ nexomon.Rarity }}</h3>

    <div class="navigation-buttons">
      <button class="btn btn-outline-primary" @click="goToNexomon(parseInt(nexomon.Number) - 1)"
        :disabled="!hasPrevious">Previous</button>
      <button class="btn btn-outline-primary" @click="goToNexomon(parseInt(nexomon.Number) + 1)"
        :disabled="!hasNext">Next</button>
    </div>

    <button class="btn btn-outline-danger" @click="goBack">Back</button>

    <!-- Add more details as needed -->

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

  <div class="habitat-info">
    <h3>Habitats</h3>
    <div class="regions-grid">

      <div class="region-card" v-for="(region, index) in nexomon.Locations" :key="index" @click="toggleRegion(index)">

        <img :src="getRegionImage(region.Region.text)" alt="Region Image" class="region-image" />
        
        <div class="region-text">
        <h4>{{ region.Region.text }}</h4>
        </div>

        <!-- Only show maps when the card is expanded -->
        <div :class="{ 'maps-list': true, 'expanded': expandedRegion === index, 'collapsed': expandedRegion !== index }">
          <ul @click.stop>
            <li
                v-for="map in region.Maps.split(', ')"
                :key="map"
                @mouseenter="hoverMap(map)"
                @mouseleave="hoverMap(null)"
              >
              {{ map }} <br>
              <img v-if="hoveredMap === map" :src="getMapImage(map)" alt="Map Image" class="map-preview" />
            </li>
          </ul>
        </div>
        
      </div>
    </div>
  </div>

</template>



<script>
import data from '../../../python-scripts/assets/nexomon_extinction_database.json';

export default {
  props: ['number'],
  data() {
    return {
      nexomons: data,
      showCosmic: false,
      expandedRegion: null,
      hoveredMap: null
    };
  },
  computed: {
    nexomon() {
      return this.nexomons.find(n => parseInt(n.Number) === parseInt(this.number));
    },
    nexomonEvolution() {
      if (this.nexomon && this.nexomon.Evolution && this.nexomon.Evolution.length > 0) {
        return this.nexomon.Evolution[0];
      }
      return {};
    },
    hasPrevious() {
      return this.nexomon && parseInt(this.nexomon.Number) > 1;
    },
    hasNext() {
      return this.nexomon && parseInt(this.nexomon.Number) < this.nexomons.length;
    }
  },
  methods: {

    toggleRegion(index) {
      // Toggle the region between expanded and collapsed states
      this.expandedRegion = this.expandedRegion === index ? null : index;
    },

    hoverMap(map) {
      this.hoveredMap = map;
    },

    goBack() {
      this.$router.push({ name: 'dex', params: {} });
    },

    goToNexomon(number) {
      this.showCosmic = false;
      this.clickedRegion = null;
      this.$router.push({ name: 'NexomonDetails', params: { number } });
    },

    goToEvolution(nexomonName) {
      let evolvedNexomon = this.nexomons.find(n => n.Name == nexomonName);
      if (evolvedNexomon) {
        return `/nexomon/${evolvedNexomon.Number}`
      }
      return ''
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
    }
  }
};
</script>

<style scoped>
.details-container {
  text-align: center;
}

.sprite-container {
  position: relative;
  /* Make the sprite container the relative parent */
  display: inline-block;
  /* Inline block to respect content size */
}

.toggle-button {
  padding: 5px;
  background-color: #2b9fcc;
  color: #fff;
  border: none;
  font-size: 12px;
  cursor: pointer;
  border-radius: 5px;
  transition: background-color 0.3s ease;
}

.element-info {
  display: flex;
  justify-content: center;
  /* Center the elements horizontally */
  align-items: center;
  /* Align items vertically center */
  margin: 10px 0;
  /* Add some space above and below */
}

.element-image {
  width: 30px;
  height: 30px;
  margin-left: 10px;
  margin-right: 5px
}

.nexomon-sprite {
  max-width: 300px;
  height: auto;
  border: 1px solid #ccc;
  border-radius: 5px;
  text-align: center;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  transition: background-color 0.3s ease, transform 0.3s ease;
  text-decoration: none;
  color: inherit;
}

.nexomon-card {
  width: calc(25% - 10px);
  margin-bottom: 20px;
  padding: 10px;

}

.navigation-buttons {
  margin: 20px 0;
}

button {
  margin: 0 10px;
  padding: 10px;
  font-size: 16px;
}

.evolution-container {
  margin-top: 20px;
  text-align: center;
}

.evolution-stage {
  display: inline-block;
  margin: 10px;
  text-align: center;
  border: 1px solid #ccc;
  border-radius: 5px;
  text-align: center;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  transition: background-color 0.3s ease, transform 0.3s ease;
  text-decoration: none;
  color: inherit;
}

.evolution-stage:hover {
  background-color: rgba(0, 0, 0, 0.1);
  transform: scale(1.02);
}

.evolution-image {
  width: 140px;
  height: auto;
  display: block;
  margin: 0 auto;
}

.habitat-info {
  margin: 20px 0;
}

.regions-grid {
  display: grid;
  align-items: start;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 20px;
  justify-content: center;
  /* This will center the grid */
  max-width: 1000px;
  /* Optional: restrict the grid's width if needed */
  margin: 0 auto;
  /* Center the grid container itself */
}

@keyframes expand {
  from {
    max-height: 0;
    opacity: 0;
  }

  to {
    max-height: 500px;
    /* Adjust based on content height */
    opacity: 1;
  }
}

@keyframes collapse {
  from {
    max-height: 500px;
    /* Same as above, must match content */
    opacity: 1;
  }

  to {
    max-height: 0;
    opacity: 0;
  }
}

.region-card {
  border: 1px solid #ccc;
  border-radius: 8px;
  padding: 10px;
  text-align: center;
  transition: transform 0.3s ease;
  cursor: pointer;
  overflow: hidden;
}

.region-card:hover {
  transform: scale(1.01);
}

.region-image {
  width: 100%;
  height: auto;
  border-radius: 4px;
}

.maps-list {
  padding: 10px;
  border-top: 1px solid #ccc;
  margin-top: 10px;
  max-height: 0;
  opacity: 0;
  overflow: hidden;
  /* Ensure the collapsed content is hidden */
}

.map-preview {
  margin-left: 10px;
  height: 130px;
  display: inline-block;
  overflow: visible;
  vertical-align: middle;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.maps-list ul {
  list-style-type: none; /* Remove bullet points */
  padding-left: 0; /* Remove default padding */
  margin-left: 0; /* Remove default margin */
  margin-bottom: 0;
}

.maps-list li {
  transition: background-color 0.3s ease, color 0.3s ease;
  list-style-type: none;
  padding-bottom: 3%;
  padding-top: 3%;
  background-clip: padding-box;
}

.maps-list li:hover {
  background-color: #e0e0e0; /* Change to your preferred highlight color */
  color: #000; /* Optional: Change the text color on hover */
  cursor: pointer; /* Optional: Change the cursor to indicate interactivity */
}

.maps-list.expanded {
  animation: expand 0.3s forwards;
}

.maps-list.collapsed {
  animation: collapse 0.3s forwards;
  position: absolute;
}

.region-text {
  padding-top: 15px;
}
</style>

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

    <div class="location-container" v-if="nexomon.Locations && nexomon.Locations.length">
      <h3>Locations:</h3>
      <div>
        <div v-for="(location, index) in nexomon.Locations" :key="index"
          :class="{ 'location-stage': true, 'location-stage-active': clickedRegion === index }">
          
          <!-- Region Image and Name -->
          <img @click="toggleRegion(index)" :src="getRegionImage(location.Region.text)" :alt="location.Region.text"
            class="location-image" />
          <span>{{ location.Region.text }}</span>

          <!-- Maps (shown when clicked) -->
          <div v-if="clickedRegion === index" class="maps-container">
            <ul>
              <li v-for="(map, mapIndex) in splitMaps(location.Maps)" :key="mapIndex"
                @mouseenter="showMapImage(map, $event)" @mouseleave="hideMapImage">
                {{ map }}
              </li>
            </ul>
          </div>

        </div>
      </div>
    </div>
    <!-- Image display area -->
    <div v-if="hoveredMapImage" class="map-image-container" :style="{ top: mouseY + 'px', left: mouseX + 'px' }">
      <img :src="hoveredMapImage" alt="Map Image" class="map-image" />
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
      clickedRegion: null,
      hoveredMapImage: null,
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
    // Toggle the region to show or hide maps
    toggleRegion(index) {
      this.clickedRegion = this.clickedRegion === index ? null : index;
    },
    // Split maps string into an array
    splitMaps(maps) {
      return maps.split(", ").map(map => map.trim());
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

    // Method to split and clean up the Maps field into an array
    parseMaps(mapsString) {
      return mapsString.split(',').map(map => map.trim());
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

    showMapImage(map, event) {
    this.hoveredMapImage = this.getMapImage(map);

    // Get the bounding box of the hovered element
    const hoveredElement = event.currentTarget.getBoundingClientRect();

    const imageWidth = 300; // Adjust based on your image size
    const imageHeight = 300; // Adjust based on your image size
    const padding = 20; // Padding from the hovered element

    // Get available window width and height
    const windowWidth = window.innerWidth;
    const windowHeight = window.innerHeight;

    // Determine the X position (to the right of the hovered element)
    let newXPosition = hoveredElement.right + padding;
    if (newXPosition + imageWidth > windowWidth) {
      // If it overflows, place it to the left
      newXPosition = hoveredElement.left - imageWidth - padding;
    }

    // Determine the Y position (centered on the hovered element)
    let newYPosition = hoveredElement.top + (hoveredElement.height / 2) - (imageHeight / 2);
    if (newYPosition + imageHeight > windowHeight) {
      // If it overflows at the bottom, adjust it upward
      newYPosition = windowHeight - imageHeight - padding;
    } else if (newYPosition < 0) {
      // If it overflows at the top, adjust it downward
      newYPosition = padding;
    }

    // Update the position based on the calculated values
    this.mouseX = newXPosition;
    this.mouseY = newYPosition;
  },

  hideMapImage() {
    this.hoveredMapImage = null;
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

.location-container {
  margin-top: 20px;
  text-align: center;
}

.location-stage {
  display: inline-block;
  margin: 10px;
  margin-bottom: 40px;
  text-align: center;
  border: 1px solid #ccc;
  border-radius: 5px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  transition: background-color 0.3s ease, transform 0.3s ease;
  cursor: pointer;
  position: relative;
  /* Allows positioning of the maps-container relative to location-stage */
}

.location-stage-active {
  background-color: rgba(0, 0, 0, 0.1);
  /* Set a new background color when active */
  transform: scale(1.02);
  /* Optional: slightly scale the card for a visual cue */
}

.location-image {
  width: 300px;
  height: auto;
  display: block;
  margin: 0 auto;
}

.maps-container {
  margin-top: 10px;
  text-align: center;
  display: block;
  /* Block level to take up the full width inside location-stage */
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
  /* Center the maps-container horizontally */
}

.maps-container ul {
  list-style-type: none;
  padding-left: 0;
  margin: 0;
  text-align: left;
}

.maps-container li {
  margin: 5px 0;
  padding: 5px;
  border-radius: 5px;
  width: 200px;
  display: block;
  text-align: center;
}

.maps-container li:hover {
  background: #f0f0f0;
}

.map-image-container {
  position: fixed;
  /* Fixed positioning to keep it on top */
  pointer-events: none;
  /* Allow clicks to pass through */
}

.map-image {
  width: 500px;
  /* Adjust the size of the image as necessary */
  height: auto;
  border: 1px solid #ccc;
  /* Optional: Add border for better visibility */
  border-radius: 5px;
  /* Optional: Round corners */
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  /* Optional: Add shadow */
}
</style>

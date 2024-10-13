<!-- src/components/NexomonDetails.vue -->
<template>
  <div v-if="nexomon" class="details-container">

    <div class="main-infos">
      <h1 class="h1" style="margin-top: 20px;">{{ nexomon.Number }} - {{ nexomon.Name }}</h1>

      <div class="sprite-container">
        <img class="nexomon-sprite" :src="getImage(nexomon.Name, showCosmic)" alt="Nexomon Sprite" />
        <div class="element-info">
          <h3 style="margin-top: 10px;">Element:</h3>
          <img :src="getImage(nexomon.Element + '_Type_Icon')" alt="Element Image" class="element-label" />
          <span>{{ nexomon.Element }}</span>
          <button v-if="nexomon.Sprites && nexomon.Sprites.Cosmic" class="toggle-button" @click="toggleSprite">
            {{ showCosmic ? 'Show Regular' : 'Show Cosmic' }}
          </button>
        </div>
        <div class="description-container">
          <p>{{ description.Description }}</p>
        </div>
      </div>

        <h3 >
          Rarity: <span :style="{ backgroundColor: getRarityColor(nexomon.Rarity), color: 'white', borderRadius: '5px', padding: '3px'}" >{{ nexomon.Rarity }}</span>
        </h3>

      <div class="navigation-buttons">
        <button class="btn btn-outline-primary" @click="goToNexomon(parseInt(nexomon.Number) - 1)"
          :disabled="!hasPrevious">Previous</button>
        <button class="btn btn-outline-primary" @click="goToNexomon(parseInt(nexomon.Number) + 1)"
          :disabled="!hasNext">Next</button>
      </div>
    </div>

    <button class="btn btn-outline-danger" @click="goBack">Back</button>

    <div class="extra-info">
      <div class="extra-section" @click="toggleSection('battle-info')">
        <h3>&#x1F94A; Battle Info </h3>
        <div
          :class="{ 'extra-list': true, 'expanded': !collapsedSections['battle-info'], 'collapsed': collapsedSections['battle-info'] }"
          v-if="!collapsedSections['battle-info']">
          <table>
            <tbody>
              <tr v-if="strongAgainst.length > 0">
                <td>
                  <strong><span style='color:green' class="battle-text">Strong</span> Against:</strong>
                  <ul>
                    <li v-for="type in strongAgainst" :key="type" class="extra-item">
                      <img :src="getImage(type + '_Type_Icon')" alt="Element Image" class="element-image" />{{ type }}
                    </li>
                  </ul>
                </td>
              </tr>
              <tr v-if="weakAgainst.length > 0">
                <td>
                  <strong><span style='color:crimson' class="battle-text">Weak</span> Against:</strong>
                  <ul>
                    <li v-for="type in weakAgainst" :key="type" class="extra-item">
                      <img :src="getImage(type + '_Type_Icon')" alt="Element Image" class="element-image" />{{ type }}
                    </li>
                  </ul>
                </td>
              </tr>
              <tr v-if="neutralAgainst.length > 0">
                <td>
                  <strong><span style='color:dodgerblue' class="battle-text">Neutral</span> Against:</strong>
                  <ul>
                    <li v-for="type in neutralAgainst" :key="type" class="extra-item">
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

        <img :src="getRegionImage(region.Region.text)" alt="Region Image" class="region-image" />

        <div class="region-text">
          <h4>{{ region.Region.text }}</h4>
        </div>

        <!-- Only show maps when the card is expanded -->
        <div
          :class="{ 'maps-list': true, 'expanded': expandedRegion === index, 'collapsed': expandedRegion !== index }">
          <ul @click.stop>
            <li v-for="map in region.Maps.split(', ')" :key="map" @mouseenter="hoverMap(map)"
              @mouseleave="hoverMap(null)" @click="clickMap(map)" :class="{ 'highlighted-map': clickedMap === map }">
              {{ map }} <br>
              <img v-if="hoveredMap === map || clickedMap === map" :src="getMapImage(map)" alt="Map Image"
                class="map-preview" />
            </li>
          </ul>
        </div>

      </div>
    </div>
  </div>

  <!-- Supa Zoom -->
  <div v-if="showZoom" class="zoomed-map-overlay" @click="closeZoom">
    <div class="zoomed-map-container">
      <img :src="zoomedMap" alt="Zoomed Map" class="zoomed-map-image" />
    </div>
  </div>

</template>



<script>
import data from '../../../python-scripts/assets/nexomon_extinction_database.json';
import descriptionData from '../../../python-scripts/assets/nexomon_description_database.json'
import locationExceptions from '../assets/location_exceptions.json';
import typeChart from '../assets/type_chart.json'

export default {
  props: ['number'],
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
      collapsedSections: {
        'battle-info': true,
        'loved-food': true,
        'base-stats': true,
      }
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
        return this.locationExceptions[this.nexomon.Name] || "No specific habitat information.";
      }
      return null;
    },

    //Battle Info
    strongAgainst() {
      return this.typeChart.types[this.nexomon.Element]?.strong_against || [];
    },
    weakAgainst() {
      return this.typeChart.types[this.nexomon.Element]?.weak_against || [];
    },
    neutralAgainst() {
      return this.typeChart.types[this.nexomon.Element]?.neutral_against || [];
    },

    //Food Info
    lovedFood() {
      if (this.nexomon && this.nexomon['Loved Food'] && this.nexomon['Loved Food'].length > 0) {
        return this.nexomon['Loved Food'];
      }
      return { name: "This nexomon doesn't have any loved food" };
    },

    //Stats Info
    baseStats() {
      if (this.nexomon) {
        return this.nexomon['Stats']
      }
      return {}
    }
  },

  mounted() {
    this.preloadImages(); // Preload battle and food images on page load
  },

  methods: {

    toggleSection(section) {
      this.collapsedSections[section] = !this.collapsedSections[section];
    },

    toggleRegion(index) {
      if (this.expandedRegion !== index) {
        this.expandedRegion = index;

        // Preload all map images for the clicked region
        this.preloadMapImages(this.nexomon.Locations[index].Maps.split(', '));
      } else {
        this.expandedRegion = null; // Collapse the region if it's already expanded
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
    },

    closeZoom() {
      this.clickedMap = null;
      this.showZoom = false;
    },

    goBack() {
      this.$router.push({ name: 'dex', params: {} });
    },

    goToNexomon(number) {
      this.showCosmic = false;
      this.expandedRegion = null;
      this.$router.push({ name: 'NexomonDetails', params: { number } });
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
      const elementTypes = [...this.strongAgainst, ...this.weakAgainst, ...this.neutralAgainst];
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
    }
  }
};
</script>

<style scoped>
.details-container {
  text-align: center;
}

.navigation-buttons {
  margin: 20px 0;
}

button {
  margin: 0 10px;
  padding: 10px;
  font-size: 16px;
}
</style>

<style scoped src="../assets/styles/basic-info.css"></style>
<style scoped src="../assets/styles/location-info.css"></style>
<style scoped src="../assets/styles/evolution-info.css"></style>
<style scoped src="../assets/styles/extra-info.css"></style>

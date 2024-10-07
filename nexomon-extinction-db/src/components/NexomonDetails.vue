<!-- src/components/NexomonDetails.vue -->
<template>
  <div v-if="nexomon" class="details-container">
    <h1 class="h1" style="margin-top: 20px;">{{ nexomon.Number }} - {{ nexomon.Name }}</h1>
    
    <div class="sprite-container">
      <img
        class="nexomon-sprite"
        :src="getImage(nexomon.Name, showCosmic)"
        alt="Nexomon Sprite"
      />
    </div>

    <div class="element-info">
      <h3>Element:</h3>
      <img :src="getImage(nexomon.Element + '_Type_Icon')" alt="Element Image" class="element-image" />
      <span>{{ nexomon.Element }}</span>

      <button
        v-if="nexomon.Sprites && nexomon.Sprites.Cosmic"
        class="toggle-button"
        @click="toggleSprite"
      >
        {{ showCosmic ? 'Show Regular' : 'Show Cosmic' }}
      </button>
    </div>

    <h3>Rarity: {{ nexomon.Rarity }}</h3>

    <!-- Add more details as needed -->

    <div v-if="nexomon.Evolution && nexomon.Evolution.length" class="evolution-container">
      <h3>Evolution Line:</h3>
      <div>
        <router-link class="evolution-stage" v-for="(details, nexomonName) in nexomonEvolution" :key="nexomonName" :to="goToEvolution(nexomonName)"
        >
        <img :src="getImage(nexomonName)" :alt="nexomonName" class="evolution-image" />
        <span>{{ nexomonName }} - {{ details.text }}</span>
        </router-link>
      </div>
    </div>


    <div class="navigation-buttons">
      <button class="btn btn-outline-primary" @click="goToNexomon(parseInt(nexomon.Number) - 1)" :disabled="!hasPrevious">Previous</button>
      <button class="btn btn-outline-primary" @click="goToNexomon(parseInt(nexomon.Number) + 1)" :disabled="!hasNext">Next</button>
    </div>

    <button class="btn btn-outline-danger" @click="goBack">Back</button>
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
      return this.nexomon && parseInt(this.nexomon.Number) < this.nexomons.length; // Adjust this if needed
    }
  },
  methods: {
    goBack() {
      this.$router.push({ name: 'dex', params: {} });
    },

    goToNexomon(number) {
      this.$router.push({ name: 'NexomonDetails', params: { number } });
    },

    goToEvolution(nexomonName) {
      let evolvedNexomon = this.nexomons.find(n => n.Name == nexomonName);
      return `/nexomon/${evolvedNexomon.Number}`
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

    toggleSprite() {
      this.showCosmic = !this.showCosmic; // Toggle between cosmic and regular sprite
    }
  }
};
</script>

<style scoped>
.details-container {
  text-align: center;
  /* Center-align all text in the container */
}

.sprite-container {
  position: relative; /* Make the sprite container the relative parent */
  display: inline-block; /* Inline block to respect content size */
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

.evolution-stage:hover{
  background-color: rgba(0, 0, 0, 0.1);
  transform: scale(1.02);
}

.evolution-image {
  width: 140px;
  height: auto;
  display: block;
  margin: 0 auto;
}
</style>

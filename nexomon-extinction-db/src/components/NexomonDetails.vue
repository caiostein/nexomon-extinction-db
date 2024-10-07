<!-- src/components/NexomonDetails.vue -->
<template>
  <div v-if="nexomon" class="details-container">
    <h1>{{nexomon.Number}} - {{ nexomon.Name }}</h1>
    <img class="nexomon-sprite" :src="getImage(nexomon.Name, false)" />
    <img class="nexomon-sprite" v-if="nexomon.Sprites.Cosmic" :src="getImage(nexomon.Name, true)" alt="Cosmic Sprite" />

    <div class="element-info">
      <h3>Element:</h3>
      <img :src="getImage(nexomon.Element + '_Type_Icon')" alt="Element Image" class="element-image" />
      <span>{{ nexomon.Element }}</span>
    </div>

    <h3>Rarity: {{ nexomon.Rarity }}</h3>

    <!-- Add more details as needed -->

    <div class="navigation-buttons">
      <button @click="goToNexomon(parseInt(nexomon.Number) - 1)" :disabled="!hasPrevious">Previous</button>
      <button @click="goToNexomon(parseInt(nexomon.Number) + 1)" :disabled="!hasNext">Next</button>
    </div>

    <button @click="goBack">Back</button>
  </div>
</template>



<script>
import data from '../../../python-scripts/assets/nexomon_extinction_database.json';

export default {
  props: ['number'],
  data() {
    return {
      nexomons: data,
    };
  },
  computed: {
  nexomon() {      
    return this.nexomons.find(n => parseInt(n.Number) === parseInt(this.number));
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
      this.$router.push({ name: 'dex', params: { } });
    },
    
    goToNexomon(number) {
    this.$router.push({ name: 'NexomonDetails', params: { number } });
    },

    getImage(imageName, isCosmic) {
      if (isCosmic) {
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
    }
  }
};
</script>

<style scoped>
.details-container {
  text-align: center;
  /* Center-align all text in the container */
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
  width: 18%;
  height: auto;
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

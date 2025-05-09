<template>
  <div class="location-details-wrapper">
    <h1>{{ locationName }}</h1>
    <img :src="getRegionImage(locationName)" :alt="locationName" class="region-image" />
    <div v-if="maps.length">
      <h2>Maps</h2>
      <ul>
        <li v-for="map in maps" :key="map">
          {{ map }}
          <img :src="getMapImage(map)" :alt="map" class="map-image" />
        </li>
      </ul>
    </div>
    <div v-else>
      <p>No maps found for this location.</p>
    </div>
    <div v-if="nexomons.length">
      <h2>Nexomon found here</h2>
      <ul>
        <li v-for="nexomon in nexomons" :key="nexomon.Number">
          <router-link :to="`/nexomon/${nexomon.Number}`">
            <img :src="getThumbnail(nexomon.Name)" :alt="nexomon.Name" class="nexomon-thumb" />
            {{ nexomon.Name }}
          </router-link>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
import data from '../../../python-scripts/assets/nexomon_extinction_database.json';

export default {
  props: ['location'],
  computed: {
    locationName() {
      return this.$route.params.location;
    },
    maps() {
      // Find all maps for this region
      const maps = new Set();
      data.forEach(n => {
        if (n.Locations) {
          n.Locations.forEach(region => {
            if (region.Region && region.Region.text === this.locationName) {
              region.Maps.split(', ').forEach(m => maps.add(m));
            }
          });
        }
      });
      return Array.from(maps).sort();
    },
    nexomons() {
      // Find all Nexomon found in this region
      return data.filter(n => n.Locations && n.Locations.some(region => region.Region && region.Region.text === this.locationName));
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
    },
    getThumbnail(name) {
      name = name.replace(' (Extinction)', '');
      try {
        return require(`@/assets/downloaded_images/${name}.png`);
      } catch {
        try {
          return require(`@/assets/downloaded_images/${name}2.png`);
        } catch {
          return '';
        }
      }
    }
  }
};
</script>

<style scoped>
.location-details-wrapper {
  max-width: 700px;
  margin: 0 auto;
  padding: 24px;
}
.region-image {
  width: 180px;
  height: 180px;
  object-fit: contain;
  margin-bottom: 16px;
}
.map-image {
  width: 120px;
  height: 120px;
  object-fit: contain;
  margin-left: 8px;
}
.nexomon-thumb {
  width: 40px;
  height: 40px;
  object-fit: contain;
  margin-right: 8px;
}
</style>

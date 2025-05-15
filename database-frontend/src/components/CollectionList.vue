<template>
  <div class="collection-wrapper">
    <div class="filters-container collection-header-row">
      <div class="collection-title-row">
        <h1 class="collection-title">My Nexomon Collection</h1>
      </div>
      <div class="collection-search-row">
        <input
          type="text"
          v-model="searchQuery"
          placeholder="Search by name or number..."
          class="collection-search-box"
        />
        <button 
          class="caught-toggle-btn" 
          :class="{ active: caughtMode }" 
          @click="toggleCaughtMode"
          title="Toggle Caught Mode"
          aria-label="Toggle Caught Mode"
          style="margin-left: 1rem;"
        >
          <span class="switch-slider"></span>
        </button>
      </div>
    </div>
    <div class="collection-grid-scroll-container">
      <div v-if="filteredNexomonList.length" class="nexomon-grid">
        <template v-for="nexomon in filteredNexomonList" :key="nexomon.Number">
          <router-link
            v-if="!caughtMode"
            :to="`/nexomon/${nexomon.Number}`"
            class="nexomon-item"
            style="cursor: pointer;"
            tabindex="0"
          >
            <img :src="getThumbnail(nexomon.Name)" :alt="nexomon.Name" class="nexomon-thumb" />
            <div class="nexomon-info">
              <div class="nexomon-number">{{ nexomon.Number }}</div>
              <div class="nexomon-name">{{ nexomon.Name }}</div>
            </div>
          </router-link>
          <div
            v-else
            class="nexomon-item remove-glow"
            style="cursor: pointer;"
            tabindex="0"
            @click="removeFromCollection(nexomon.Number)"
          >
            <img :src="getThumbnail(nexomon.Name)" :alt="nexomon.Name" class="nexomon-thumb" />
            <div class="nexomon-info">
              <div class="nexomon-number">{{ nexomon.Number }}</div>
              <div class="nexomon-name">{{ nexomon.Name }}</div>
            </div>
          </div>
        </template>
      </div>
    </div>
    <button
      v-if="caughtNexomonList.length"
      class="nexo-button nexo-button-danger clear-collection-btn"
      :disabled="!caughtMode"
      :aria-disabled="!caughtMode"
      @click="caughtMode && clearCollection()"
      style="position: static; margin: 2rem auto 0 auto; display: block; left: unset; bottom: unset; transform: none;"
    >
      Clear Collection
    </button>
    <div v-if="!caughtNexomonList.length">
      <p>You haven't caught any Nexomon yet!</p>
    </div>
  </div>
</template>

<script>
import data from '../../../python-scripts/assets/nexomon_extinction_database.json';
import { useCaughtMode } from './useCaughtMode.js';
import { computed } from 'vue';

export default {
  name: 'CollectionList',
  data() {
    return {
      searchQuery: '',
    };
  },
  setup() {
    const { caughtNexomons, caughtMode, toggleCaughtMode } = useCaughtMode();
    // Make caughtNexomonList reactive to caughtNexomons
    const caughtNexomonList = computed(() => data.filter(n => caughtNexomons.value.includes(n.Number)));
    function getThumbnail(nexomonName) {
      try {
        return require(`../assets/downloaded_images/${nexomonName}-menu.png`);
      } catch (error) {
        try {
          return require(`../assets/downloaded_images/${nexomonName}_(Extinction)-menu.png`);
        } catch (error) {
          try {
            nexomonName = nexomonName.replace(' (Extinction)', '');
            return require(`../assets/downloaded_images/${nexomonName}.png`);
          } catch (error) {
            try {
              return require(`../assets/downloaded_images/${nexomonName}2.png`);
            } catch (error) {
              return '';
            }
          }
        }
      }
    }
    function clearCollection() {
      localStorage.removeItem('caughtNexomons');
      // Instead of reload, update the array
      caughtNexomons.value = [];
    }
    function removeFromCollection(nexomonNumber) {
      const index = caughtNexomons.value.indexOf(nexomonNumber);
      console.log('Removing Nexomon:', nexomonNumber);
      console.log('Current caughtNexomons:', caughtNexomons.value);
      if (index > -1) {
        caughtNexomons.value.splice(index, 1);
        localStorage.setItem('caughtNexomons', JSON.stringify(caughtNexomons.value));
      }
    }
    return {
      caughtNexomonList,
      getThumbnail,
      caughtMode,
      toggleCaughtMode,
      clearCollection,
      removeFromCollection
    };
  },
  computed: {
    filteredNexomonList() {
      const q = this.searchQuery.trim().toLowerCase();
      if (!q) return this.caughtNexomonList;
      return this.caughtNexomonList.filter(n =>
        n.Name.toLowerCase().includes(q) || n.Number.toLowerCase().includes(q)
      );
    },
  },
};
</script>

<style scoped>
.collection-wrapper {
  --header-height: 120px;
  padding: 0 1rem;
  display: block;
  min-height: 100vh;
  max-width: 1200px;
  margin: 0 auto;
}
.collection-grid-scroll-container {
  margin-top: var(--header-height, 120px);
  height: calc(100vh - var(--header-height, 120px));
  overflow-y: auto;
  box-sizing: border-box;
}

.nexomon-grid {
  display: flex;
  flex-wrap: wrap;
  flex-direction: row;
  align-content: flex-start;
  gap: 2px;
  justify-content: center;
  width: 100%;
  margin: 0;
}
.filters-container.collection-header-row {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  z-index: 20;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 16px;
  padding: 20px 0;
  background: var(--header-bg, #fff);
}
.dark-mode .filters-container.collection-header-row {
  background: #212529;
}
.collection-title-row {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 24px;
  width: 100%;
}
.collection-title {
  font-size: 2rem;
  font-weight: 700;
  margin: 0;
  text-align: center;
}
.caught-toggle-btn {
  margin-left: 0;
  align-self: flex-start;
  margin-top: 10px;
}
.collection-search-row {
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 0.5rem;
  margin-bottom: 0.5rem;
  gap: 1rem;
}
.collection-search-box {
  width: 320px;
  padding: 10px 16px;
  border: 1px solid #ccc;
  border-radius: 5px;
  font-size: 1.1rem;
  margin-bottom: 12px;
  outline: none;
  transition: border 0.2s, box-shadow 0.2s;
  background: #fff;
  color: #333;
  box-shadow: 0 1px 3px rgba(0,0,0,0.08);
  margin-right: 0;
  margin-left: 0;
  display: block;
}
.dark-mode .collection-search-box {
  background-color: #333;
  color: #fff;
  border: 1px solid #555;
}
.nexomon-grid {
  display: flex;
  flex-wrap: wrap;
  flex-direction: row;
  align-content: flex-start;
  gap: 2px;
  justify-content: center;
  width: 100%;
}
.nexomon-item {
  width: calc(16.666% - 8px);
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
  background: #fff;
}
.nexomon-item:hover {
  background-color: rgba(141, 140, 140, 0.068);
  box-shadow: 0 4px 12px rgba(43,159,204,0.18);
  transform: scale(1.02);
}
.dark-mode .nexomon-item {
  background: #212529;
  border-color: #444;
  color: #fff;
  box-shadow: 0 2px 5px rgba(0,0,0,0.30);
}
.dark-mode .nexomon-item:hover {
  background-color: rgba(255,255,255,0.05);
}
.nexomon-thumb {
  width: 64px;
  height: 64px;
  object-fit: contain;
  margin-bottom: 8px;
  border-radius: 10px;
  background-color: rgba(0, 0, 0, 0.05);
  padding: 5px;
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
.nexomon-name {
  font-size: 0.9rem;
  text-align: center;
  width: 100%;
  min-height: 2.8em;
  line-height: 1.4em;
  word-wrap: break-word;
  hyphens: auto;
}
.clear-collection-btn {
  /* Remove all positioning so it flows naturally below the grid */
  position: relative !important;
  margin: 2rem auto 6rem auto !important;
  display: block;
  padding: 0.75rem 2.5rem;
  font-size: 1.1rem;
  font-weight: 600;
  color: #fff;
  background: #e53935;
  border: none;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(229,57,53,0.08);
  cursor: pointer;
  transition: background 0.2s, box-shadow 0.2s, opacity 0.2s;
  opacity: 1;
  z-index: 1;
}
.clear-collection-btn:disabled,
.clear-collection-btn[aria-disabled="true"] {
  background: #aaa !important;
  cursor: not-allowed;
  opacity: 0.6;
}
.clear-collection-btn:hover {
  background: #b71c1c;
  box-shadow: 0 4px 16px rgba(229,57,53,0.18);
}
.dark-mode .clear-collection-btn {
  background: #b71c1c;
  color: #fff;
}
.dark-mode .clear-collection-btn:hover {
  background: #e53935;
}
@media (min-width: 0px) {
  .filters-container.collection-header-row {
    position: static;
  }
  .collection-grid-scroll-container {
    margin-top: 0;
    height: auto;
    overflow-y: visible;
  }
}

@media (max-width: 900px) {
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
</style>
<style scoped src="../assets/styles/button-styles.css"></style>
<style scoped src="../assets/styles/caught-mode.css"></style>

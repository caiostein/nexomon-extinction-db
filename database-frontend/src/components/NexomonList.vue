<template>
  <div class="nexomon-list-wrapper"
    :class="{ 'filters-collapsed': filtersCollapsed }"
>
    <!-- Removed the extra inner div -->
    <div class="filters-container" :class="{ collapsed: filtersCollapsed }">      

        <input type="text" v-model="searchQuery" placeholder="Search for a Nexomon" class="search-box" />
      
      <!-- Custom Element Filter Dropdown -->
      <div class="custom-select">        <div @click.stop="toggleDropdown" class="selected-option">
          <span v-if="selectedElement">
            <img :src="getElementIcon(selectedElement)" alt="Icon" class="element-icon" />
            {{ selectedElement }}
          </span>
          <span v-else>
            <span class="element-icon" style="font-size: 1.2em;">🌈</span>
            All Elements
          </span>
          <span class="dropdown-arrow">▼</span>
        </div>        <div class="dropdown-menu" v-if="dropdownOpen">
          <div class="dropdown-item" @click.stop="selectElement('')">
            <span class="element-icon" style="font-size: 1.2em; margin-left: -4px; margin-right: 8px;">🌈</span>
            All Elements
          </div>
          <div 
            v-for="element in uniqueElements" 
            :key="element" 
            class="dropdown-item"
            @click.stop="selectElement(element)"
          >
            <img :src="getElementIcon(element)" alt="Icon" class="element-icon" />
            {{ element }}
          </div>
        </div>
      </div>
      <div class="custom-select">
        <div @click.stop="toggleRarityDropdown" class="selected-option">
          <span v-if="selectedRarity">
            <span class="rarity-label" :style="{ backgroundColor: getRarityColor(selectedRarity), color: 'white' }">{{ selectedRarity }}</span>
          </span>
          <span v-else>
            <span class="element-icon" style="font-size: 1.2em; margin-left: -4px; margin-right: 8px;">✨</span>
            All Rarities
          </span>
          <span class="dropdown-arrow">▼</span>
        </div>
        <div class="dropdown-menu" v-if="showRarityDropdown">
          <div class="dropdown-item" @click.stop="selectRarity('')">
            <span class="element-icon" style="font-size: 1.2em; margin-left: -4px; margin-right: 8px;">✨</span>
            All Rarities
          </div>
          <div class="dropdown-item" v-for="rarity in rarities" :key="rarity" @click.stop="selectRarity(rarity)">
            <span class="rarity-label" :style="{ backgroundColor: getRarityColor(rarity), color: 'white' }">{{ rarity }}</span>
          </div>
        </div>
      </div>
        <button 
          class="caught-toggle-btn" 
          :class="{ active: caughtMode }" 
          @click="toggleCaughtMode"
          title="Toggle Caught Mode"
          aria-label="Toggle Caught Mode"
        >
          <span class="switch-slider"></span>
        </button>
        <button class="collapse-arrow" aria-label="Collapse Filters" @click="toggleFiltersCollapse" :aria-expanded="!filtersCollapsed">
          <svg :style="filtersCollapsed ? 'transform: rotate(180deg);' : ''" viewBox="0 0 24 24"><path d="M7.41 15.59L12 11l4.59 4.59L18 14.17l-6-6-6 6z"/></svg>
        </button>
    </div>

    <div class="grid-scroll-container"> <!-- Container for scrolling -->
      <div class="nexomon-grid">
        <template v-for="nexomon in filteredNexomons" :key="nexomon.Number">
          <div
            v-if="caughtMode"
            class="nexomon-card"
            :class="{ 'caught-glow': isCaught(nexomon.Number) }"
            @click="toggleCaught(nexomon.Number, $event)"
            :style="{ cursor: 'pointer' }"
          >
            <!-- Caught Checkbox (only in caught mode) -->
            <div class="caught-checkbox" @click.stop="toggleCaught(nexomon.Number, $event)">
              <input type="checkbox" :checked="isCaught(nexomon.Number)" readonly />
              <span class="checkmark" :class="{ checked: isCaught(nexomon.Number) }"></span>
            </div>
            <div class="nexomon-info">
              <div class="nexomon-number">{{ nexomon.Number }}</div>
              <div class="nexomon-name">{{ nexomon.Name }}</div>
            </div>
            <img :src="getThumbnail(nexomon.Name)" alt="Sprite" class="nexomon-thumb" />
          </div>
          <router-link
            v-else
            :to="`/nexomon/${nexomon.Number}`"
            class="nexomon-card"
          >
            <div class="nexomon-info">
              <div class="nexomon-number">{{ nexomon.Number }}</div>
              <div class="nexomon-name">{{ nexomon.Name }}</div>
            </div>
            <img :src="getThumbnail(nexomon.Name)" alt="Sprite" class="nexomon-thumb" />
          </router-link>
        </template>
      </div>
    </div>
  </div>
</template>

<script>
import data from '../../../python-scripts/assets/nexomon_extinction_database.json';
import typeChart from '../assets/type_chart.json';
import { useCaughtMode } from './useCaughtMode.js';''

const RARITY_ORDER = [
  'Common',
  'Uncommon',
  'Rare',
  'Mega Rare',
  'Ultra Rare',
  'Legendary',
  'Ultimate',
];

export default {
  setup() {
    const {
      caughtMode,
      caughtNexomons,
      toggleCaughtMode,
      isCaught,
      toggleCaught,
    } = useCaughtMode();
    return {
      caughtMode,
      caughtNexomons,
      toggleCaughtMode,
      isCaught,
      toggleCaught,
    };
  },
  data() {
    return {
      nexomons: data,
      searchQuery: '',
      selectedElement: '',
      dropdownOpen: false,
      elementIcons: {},
      selectedRarity: '',
      showRarityDropdown: false,
      filtersCollapsed: false, // NEW: collapsed state
    };
  },
  computed: {
    uniqueElements() {
      return Object.keys(typeChart.types);
    },
    rarities() {
      // Only include rarities present in the data, in the custom order
      const set = new Set();
      this.nexomons.forEach(n => {
        if (n.Rarity) set.add(n.Rarity);
      });
      return RARITY_ORDER.filter(r => set.has(r));
    },
    filteredNexomons() {
      const searchQueryLower = this.searchQuery.toLowerCase();

      let filtered = this.nexomons.filter(nexomon => {
        const nameMatches = nexomon.Name.toLowerCase().includes(searchQueryLower);
        const numberMatches = nexomon.Number.includes(searchQueryLower);
        const elementMatches = this.selectedElement === '' || nexomon.Element === this.selectedElement;

        return (nameMatches || numberMatches) && elementMatches;
      });

      if (this.selectedRarity) {
        filtered = filtered.filter(n => n.Rarity === this.selectedRarity);
      }

      return filtered;
    },
  },
  mounted() {
    // Load caught Nexomons from localStorage
    const saved = localStorage.getItem('caughtNexomons');
    if (saved) {
      try {
        this.caughtNexomons = JSON.parse(saved);
      } catch (e) {
        this.caughtNexomons = [];
      }
    }
    
    window.addEventListener('resize', this.handleResizeExpandFilters);

  },
  methods: {
    getThumbnail(nexomonName) {
      try {
        return require(`@/assets/downloaded_images/${nexomonName}-menu.png`);
      } catch (error) {
        try {
          return require(`@/assets/downloaded_images/${nexomonName}_(Extinction)-menu.png`);
        } catch (error) {
          console.warn(`Neither ${nexomonName}-menu.png nor ${nexomonName}_(Extinction)-menu.png were found.`);
        }
      }
    },
    getElementIcon(element) {
      try {
        return require(`@/assets/downloaded_images/${element}_Type_Icon.png`);
      } catch (error) {
        console.warn(`Element icon for ${element} not found.`);
        return '';
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
          return '#264BA3';
        case 'Legendary':
          return 'orange';
        default:
          return 'transparent';
      }
    },
    toggleDropdown() {
      this.dropdownOpen = !this.dropdownOpen;      
      // Add click outside listener when dropdown is opened
      if (this.dropdownOpen) {
        // Ensure this runs after the current event loop completes
        setTimeout(() => {
          document.addEventListener('click', this.closeDropdownOutside);
        }, 10);
      }
    },
    closeDropdownOutside(e) {
      if (!e.target.closest('.custom-select')) {
        this.dropdownOpen = false;
        document.removeEventListener('click', this.closeDropdownOutside);
      }
    },
    selectElement(element) {
      this.selectedElement = element;
      this.dropdownOpen = false;
      // Remove the event listener when an option is selected
      document.removeEventListener('click', this.closeDropdownOutside);
    },
    toggleRarityDropdown() {
      this.showRarityDropdown = !this.showRarityDropdown;
      if (this.showRarityDropdown) {
        setTimeout(() => {
          document.addEventListener('click', this.closeRarityDropdownOutside);
        }, 10);
      }
    },
    closeRarityDropdownOutside(e) {
      if (!e.target.closest('.custom-select')) {
        this.showRarityDropdown = false;
        document.removeEventListener('click', this.closeRarityDropdownOutside);
      }
    },
    selectRarity(rarity) {
      this.selectedRarity = rarity;
      this.showRarityDropdown = false;
      document.removeEventListener('click', this.closeRarityDropdownOutside);
    },
    goToNexomon(number) {
      this.$router.push(`/nexomon/${number}`);
    },
    toggleFiltersCollapse() {
      // Only allow collapse on mobile (≤480px)
      if (window.innerWidth <= 480) {
        this.filtersCollapsed = !this.filtersCollapsed;
      }
    },
    handleResizeExpandFilters() {
      if (this.filtersCollapsed && window.innerWidth > 480) {
        this.filtersCollapsed = false;
      }
    },
  },
  beforeUnmount() {
    // Clean up event listener when component is unmounted
    document.removeEventListener('click', this.closeDropdownOutside);
    document.removeEventListener('click', this.closeRarityDropdownOutside);
    window.removeEventListener('resize', this.handleResizeExpandFilters);

  },
};
</script>

<style scoped>
.nexomon-list-wrapper {
  --header-height: 60px; /* Adjust to your actual header height */
  --filter-container-height: 92px; /* Adjust based on actual filter height */
}

.filters-container {
  position: fixed;
  top: var(--header-height);
  left: 0;
  width: 100%;
  max-width: 100vw;
  background: var(--filter-bg, #f8f9fb);
  color: var(--filter-fg, #222);
  box-shadow: 0 4px 18px rgba(0,0,0,0.08), 0 1.5px 0 #e0e0e0;
  border-radius: 0 0 18px 18px;
  padding: 18px 18px 10px 18px;
  display: flex;
  flex-wrap: wrap;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  gap: 18px 24px;
  z-index: 10;
  transition: box-shadow 0.25s, background 0.25s;
  transition: max-height 0.35s cubic-bezier(.4,0,.2,1), opacity 0.25s;
  overflow: visible; /* Allow dropdowns to overflow. If you use a collapsed animation, apply overflow: hidden; only when collapsed. */
}

.filters-container.collapsed {
  max-height: 0 !important;
  opacity: 0;
  pointer-events: none;
  overflow: hidden !important;
  padding-top: 0 !important;
  padding-bottom: 0 !important;
  transition: max-height 0.35s cubic-bezier(.4,0,.2,1), opacity 0.25s, padding 0.25s;
}

.dark-mode .filters-container {
  background: var(--filter-bg-dark, #23242a);
  color: var(--filter-fg-dark, #f3f3f3);
  box-shadow: 0 4px 18px rgba(0,0,0,0.22), 0 1.5px 0 #23242a;
}

.filters-container .search-box,
.filters-container .custom-select {
  margin: 0;
  box-sizing: border-box;
}

.filters-container .search-box {
  flex: 1 1 220px;
  min-width: 140px;
  max-width: 320px;
  padding: 6px 10px;
  border-radius: 8px;
  border: 1.5px solid #d0d0d0;
  font-size: 0.98rem;
  background: #fff;
  color: #222;
  box-shadow: 0 1px 3px rgba(0,0,0,0.04);
  transition: border 0.2s, box-shadow 0.2s;
}
.dark-mode .filters-container .search-box {
  background: #23242a;
  color: #f3f3f3;
  border: 1.5px solid #444b55;
}

.filters-container .custom-select {
  flex: 1 1 180px;
  min-width: 140px;
  max-width: 220px;
  margin: 0;
}

/* Card effect for filter controls */
.filters-container .search-box,
.filters-container .custom-select {
  background: rgba(255,255,255,0.92);
  box-shadow: 0 1.5px 6px rgba(0,0,0,0.06);
  border-radius: 8px;
}
.dark-mode .filters-container .search-box,
.dark-mode .filters-container .custom-select {
  background: rgba(35,36,42,0.98);
  box-shadow: 0 1.5px 6px rgba(0,0,0,0.18);
}

/* Responsive stacking for mobile */
@media (max-width: 900px) {
  .filters-container {
    display: flex;
    align-items: center;
    gap: 12px 0;
    padding: 10px 2vw 8px 2vw;
    border-radius: 0 0 12px 12px;
  }
  .filters-container .search-box,
  .filters-container .custom-select {
    justify-self: center;
    max-width: 42%;
    margin: 0 10px 10px 10px;
    box-shadow: 0 1.5px 6px rgba(0,0,0,0.08);
  }
  .filters-container .search-box {
    padding: 5px 9px;
    font-size: 0.93rem;
    min-width: 100px;
    max-width: 100vw;
    height: 36px;
  }

  .filters-container .caught-toggle-btn {
    margin-bottom: 5px;
  }
}

/* Make sure dropdowns and toggle are visually unified */
.filters-container .custom-select .selected-option,
.filters-container .custom-select .dropdown-menu {
  border-radius: 7px;
  font-size: 1rem;
}

/* Accessibility: focus states */
.filters-container .search-box:focus,
.filters-container .custom-select .selected-option:focus,
.filters-container .caught-toggle-btn:focus {
  outline: 2px solid #6c63ff;
  outline-offset: 2px;
}

.grid-scroll-container {
  padding-top: 10px;
  height: calc(100vh - var(--filter-container-height) - var(--header-height));
  overflow-y: auto;
  box-sizing: border-box;
}

.nexomon-grid {
  margin: 0 60px 45px 45px;
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 5px;
}

.nexomon-card {
  width: calc(16.666% - 8px);
  margin: 4px;
  padding: 10px 6px 15px;
  border: 1px solid #ccc;
  border-radius: 8px;
  text-align: center;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  text-decoration: none;
  color: inherit;
  max-height: 290px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: space-between;
  z-index: 0;
  position: relative; /* For potential positioning of elements */
}

.nexomon-card img.nexomon-thumb {
  width: 100px;
  height: 100px;
  object-fit: contain;
  margin: -10px 0 0 0 !important;
  border-radius: 10px;
  background-color: rgba(0, 0, 0, 0.05);
  padding: 5px;
  transition: transform 0.2s ease-in-out;
}

.nexomon-info {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 0 !important; /* Remove extra space below number/name for all screens */
}

.nexomon-number {
  font-size: 0.8rem;
  color: #666;
  margin-bottom: 2px;
  background-color: rgba(0, 0, 0, 0.05);
  padding: 2px 8px;
  border-radius: 10px;
  display: inline-block;
}

.dark-mode .nexomon-number {
  color: #aaa;
  background-color: rgba(255, 255, 255, 0.1);
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

.nexomon-card:hover {
  background-color: rgba(141, 140, 140, 0.068);
  transform: scale(1.02);
}

@media (hover: none) {
  /* Touch interactions for mobile devices */
  .nexomon-card:active {
    background-color: rgba(141, 140, 140, 0.12);
    transform: scale(0.98);
    transition: all 0.1s ease;
  }
}

.search-box {
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

/* Dark mode styles for search box */
.dark-mode .search-box {
  background-color: #333;
  color: #fff;
  border: 1px solid #555;
}

/* Dark mode adjustments for nexomon cards */
.dark-mode .nexomon-card {
  border-color: #444;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.3);
}

.dark-mode .nexomon-card:hover {
  background-color: rgba(255, 255, 255, 0.05);
}

.filters-container .collapse-arrow {
  display: none;
}

.dark-mode .filters-container .collapse-arrow svg {
  fill: #969191;
  filter: drop-shadow(0 2px 6px rgba(0,0,0,0.55));
}

/* Media Queries for Responsiveness */
@media (max-width: 3840px) {
  .nexomon-card {
    width: calc(16.666% - 8px);
    margin: 4px;
    max-height: 350px;
  }
  
  .nexomon-thumb {
    width: 120px !important;
    height: 120px !important;
  }
  
  .nexomon-name {
    font-size: 1.1rem !important;
  }
  
  .nexomon-number {
    font-size: 1rem !important;
    font-weight: 500;
  }
}

@media (max-width: 1925px) {
  .nexomon-card {
    width: calc(16.666% - 8px);
    margin: 4px;
    max-height: 320px;
  }
  
  .nexomon-thumb {
    width: 100px !important;
    height: 100px !important;
  }
  
  .nexomon-name {
    font-size: 1rem !important;
  }
  
  .nexomon-number {
    font-size: 0.9rem !important;
    font-weight: 500;
  }
}

@media (max-width: 1280px) {
  .nexomon-card {
    width: calc(20% - 6px);
    margin: 3px;
    max-height: 290px;
  }
  
  .nexomon-thumb {
    width: 90px !important;
    height: 90px !important;
  }
}

@media (max-width: 1024px) {
  .nexomon-card {
    width: calc(25% - 6px);
    margin: 3px;
    max-height: 280px;
  }
  
  .nexomon-thumb {
    width: 80px !important;
    height: 80px !important;
  }
}

@media (max-width: 768px) {
  .nexomon-grid {
    gap: 0;
    justify-content: space-evenly;
  }
  
  .nexomon-card {
    width: calc(33.333% - 4px);
    margin: 2px;
    max-height: 260px;
  }
  
  .nexomon-thumb {
    width: 70px !important;
    height: 70px !important;
  }
}

@media (max-width: 600px) {
  .nexomon-grid {
    gap: 0;
    justify-content: space-evenly;
  }
  
  .nexomon-card {
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

  .nexomon-grid {
    gap: 0;
    justify-content: space-evenly;
    margin: -90px 20px 20px;
  }

  .nexomon-card {
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

  .nexomon-list-wrapper {
  --filter-container-height: 145px; /* Adjust based on actual filter height */
  --total-height: calc(var(--header-height) + var(--filter-container-height));
  }

  .nexomon-list-wrapper.filters-collapsed {
  --filter-container-height: 75px;
}

  .grid-scroll-container {
     padding-top: var(--total-height); /* Ensure padding is applied */
     height: calc(100vh - var(--total-height)); /* Ensure height is calculated */
  }
  .filters-container .collapse-arrow {
    display: block;
    position: absolute;
    right: 12px;
    bottom: 8px;
    width: 32px;
    height: 32px;
    background: none;
    border: none;
    z-index: 20;
    cursor: pointer;
    padding: 0;
    transition: transform 0.25s;
  }

    .filters-container {
    transition: max-height 0.35s cubic-bezier(.4,0,.2,1), opacity 0.25s, padding 0.25s;
    will-change: max-height, opacity, padding;
  }

  .filters-container.collapsed {
    max-height: 0 !important;
    opacity: 0;
    padding-top: 0 !important;
    padding-bottom: 0 !important;
    padding-left: 0 !important;
    padding-right: 0 !important;
    overflow: hidden !important;
    pointer-events: none;
  }
  .filters-container .collapse-arrow svg {
    transition: transform 0.35s cubic-bezier(.4,0,.2,1);
  }
  .filters-container.collapsed {
    max-height: 38px !important; /* Show just enough for the arrow */
    min-height: 38px !important;
    opacity: 1;
    padding-top: 0 !important;
    padding-bottom: 0 !important;
    padding-left: 0 !important;
    padding-right: 0 !important;
    overflow: hidden !important;
    pointer-events: auto;
    background: #23242a; /* Ensure background is visible */
  }
  .filters-container.collapsed > *:not(.collapse-arrow) {
    display: none !important;
  }
  .filters-container .collapse-arrow {
    display: block;
    position: absolute;
    right: 12px;
    bottom: 4px;
    width: 32px;
    height: 32px;
    background: none;
    border: none;
    z-index: 20;
    cursor: pointer;
    padding: 0;
    transition: transform 0.25s;
  }
  .filters-container .collapse-arrow svg {
    transition: transform 0.35s cubic-bezier(.4,0,.2,1);
  }
}

/* Extra small screens */
@media (max-width: 359px) {
  .nexomon-card {
    width: calc(33.333% - 1px); /* Maintain 3 per row with minimal spacing */
    margin: 0.5px;
    max-height: 140px;
    padding: 4px 1px 6px;
  }

  .nexomon-thumb {
    width: 36px;
    height: 36px;
  }
}

/* Very narrow screens */
@media (max-width: 320px) {
  .nexomon-card {
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

.element-icon {
  width: 20px;
  height: 20px;
  margin-right: 5px;
  vertical-align: middle;
}

.custom-select {
  position: relative;
  min-width: 180px;
  margin: 0 8px 12px 8px;
  user-select: none;
  font-size: 1.05rem;
}

.selected-option {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  background-color: #fff;
  color: #333;
  font-size: 16px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

/* Dark mode styles for selected option */
.dark-mode .selected-option {
  background-color: #333;
  color: #fff;
  border: 1px solid #555;
}

.dropdown-arrow {
  font-size: 12px;
  margin-left: 10px;
}

.dropdown-menu {
  position: absolute;
  top: 100%;
  left: 0;
  width: 100%;
  max-height: 300px;
  overflow-y: auto;
  background-color: #fff;
  color: #333;
  border: 1px solid #ccc;
  border-radius: 0 0 5px 5px;
  z-index: 30;
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
  /* Ensure the dropdown is visible when displayed */
  display: block !important;
  margin-top: 2px;
}

/* Dark mode styles for dropdown menu */
.dark-mode .dropdown-menu {
  background-color: #333;
  color: #fff;
  border: 1px solid #555;
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.3);
}

.dropdown-item {
  display: flex;
  align-items: center;
  padding: 10px;
  transition: background-color 0.2s ease;
  color: #333;
}

.dropdown-item:hover {
  background-color: #f5f5f5;
}

/* Dark mode styles for dropdown items */
.dark-mode .dropdown-item {
  color: #fff;
}

.dark-mode .dropdown-item:hover {
  background-color: #444;
}

/* Enhanced hover effects for desktop */
@media (min-width: 1024px) {
  .nexomon-card:hover {
    transform: translateY(-5px) scale(1.03);
    box-shadow: 0 8px 15px rgba(0, 0, 0, 0.15);
  }
  
  .dark-mode .nexomon-card:hover {
    box-shadow: 0 8px 15px rgba(0, 0, 0, 0.4);
  }
  
  .nexomon-card:hover .nexomon-thumb {
    transform: scale(1.15);
  }
}

.rarity-label {
  min-width: 0;
  padding: 2px 8px;
  border-radius: 10px;
  font-weight: 600;
  font-size: 0.8rem;
  letter-spacing: 0.5px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.10);
  border: 1.5px solid #ddd;
  margin-left: 8px;
  vertical-align: middle;
  text-align: left;
  transition: background 0.2s, color 0.2s;
  display: inline-block;
}

.dark-mode .rarity-label {
  border: 1.5px solid #444b55;
  box-shadow: 0 2px 8px rgba(0,0,0,0.18);
}
</style>

<style scoped src="../assets/styles/button-styles.css"></style>
<style scoped src="../assets/styles/caught-mode.css"></style>

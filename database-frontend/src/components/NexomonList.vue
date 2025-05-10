<template>
  <div class="nexomon-list-wrapper">
    <!-- Removed the extra inner div -->
    <div class="filters-container">      <!-- Search Input -->
      <input type="text" v-model="searchQuery" placeholder="Search for a Nexomon" class="search-box" />
      
      <!-- Custom Element Filter Dropdown -->
      <div class="custom-select">        <div @click.stop="toggleDropdown" class="selected-option">
          <span v-if="selectedElement">
            <img :src="getElementIcon(selectedElement)" alt="Icon" class="element-icon" />
            {{ selectedElement }}
          </span>
          <span v-else>All Elements</span>
          <span class="dropdown-arrow">▼</span>
        </div>        <div class="dropdown-menu" v-if="dropdownOpen">
          <div class="dropdown-item" @click.stop="selectElement('')">
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
    </div>

    <div class="grid-scroll-container"> <!-- Container for scrolling -->
      <div class="nexomon-grid">
        <router-link v-for="nexomon in filteredNexomons" :key="nexomon.Number" :to="`/nexomon/${nexomon.Number}`"
          class="nexomon-card">
          <div class="nexomon-info">
            <div class="nexomon-number">{{ nexomon.Number }}</div>
            <div class="nexomon-name">{{ nexomon.Name }}</div>
          </div>
          <img :src="getThumbnail(nexomon.Name)" alt="Sprite" class="nexomon-thumb" />
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
import data from '../../../python-scripts/assets/nexomon_extinction_database.json';
import typeChart from '../assets/type_chart.json';

export default {
  data() {
    return {
      nexomons: data,
      searchQuery: '',
      selectedElement: '',
      dropdownOpen: false,
      elementIcons: {}
    };
  },
  computed: {
    uniqueElements() {
      return Object.keys(typeChart.types);
    },
    filteredNexomons() {
      const searchQueryLower = this.searchQuery.toLowerCase();

      return this.nexomons.filter(nexomon => {
        const nameMatches = nexomon.Name.toLowerCase().includes(searchQueryLower);
        const numberMatches = nexomon.Number.includes(searchQueryLower);
        const elementMatches = this.selectedElement === '' || nexomon.Element === this.selectedElement;

        return (nameMatches || numberMatches) && elementMatches;
      });
    },  },
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
    },    toggleDropdown() {
      this.dropdownOpen = !this.dropdownOpen;      
      // Add click outside listener when dropdown is opened
      if (this.dropdownOpen) {
        // Ensure this runs after the current event loop completes
        setTimeout(() => {
          document.addEventListener('click', this.closeDropdownOutside);
        }, 10);
      }
    },    closeDropdownOutside(e) {
      if (!e.target.closest('.custom-select')) {
        this.dropdownOpen = false;
        document.removeEventListener('click', this.closeDropdownOutside);
      }
    },    selectElement(element) {
      this.selectedElement = element;
      this.dropdownOpen = false;
      // Remove the event listener when an option is selected
      document.removeEventListener('click', this.closeDropdownOutside);
    }
  },
  beforeUnmount() {
    // Clean up event listener when component is unmounted
    document.removeEventListener('click', this.closeDropdownOutside);
  },
};
</script>

<style scoped>
.nexomon-list-wrapper {
  --header-height: 60px; /* Adjust to your actual header height */
  --filter-container-height: 150px; /* Adjust based on actual filter height */
}

.filters-container {
  position: fixed;
  top: var(--header-height);
  left: 0;
  width: 100%;
  padding: 20px 0;
  z-index: 10;
  display: flex;
  flex-direction: column;
  align-items: center;
  height: var(--filter-container-height);
  box-sizing: border-box;
}

.grid-scroll-container {
  padding-top: var(--filter-container-height);
  height: calc(100vh - var(--filter-container-height) - var(--header-height));
  overflow-y: auto;
  box-sizing: border-box;
}

.nexomon-grid {
  margin: -100px 45px 45px; /* Adjust top margin */
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 5px; /* Consistent with LocationDetails */
}

.nexomon-card {
  width: calc(16.666% - 8px); /* Match LocationDetails sizing */
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

.nexomon-card img.nexomon-thumb:hover {
  transform: scale(1.1);
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
  width: 100%;
  /* Full width on smaller screens */
  max-width: 300px;
  /* Limit maximum width */
  padding: 10px;
  margin: 10px auto; /* Adjust margin for flex container */
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 5px;
  background-color: #fff;
  color: #333;
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
    margin: -150px 20px 20px;
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

  .grid-scroll-container {
     padding-top: var(--filter-container-height); /* Ensure padding is applied */
     height: calc(100vh - 300px); /* Ensure height is calculated */
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

/* Custom dropdown styles */
.custom-select {
  position: relative;
  width: 100%;
  max-width: 300px;
  margin: 10px auto;
  cursor: pointer;
  user-select: none;
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
  z-index: 1000;
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
</style>

<style scoped src="../assets/styles/button-styles.css"></style>

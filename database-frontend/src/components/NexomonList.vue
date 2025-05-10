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
          <h3>{{ nexomon.Number }} - {{ nexomon.Name }}</h3>
          <img :src="getThumbnail(nexomon.Name)" alt="Sprite" />
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
  justify-content: flex-start;
}

.nexomon-card {
  width: calc(14% - 14.8px);
  /* Default width for larger screens */
  margin: 30px;
  /* Space between cards */
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  text-align: center;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  transition: background-color 0.3s ease, transform 0.3s ease;
  text-decoration: none;
  color: inherit;
  max-height: 278px;
}

.nexomon-card img {
  max-width: 100%;
  /* Full width for images */
  height: auto;
  /* Maintain aspect ratio */
}

.nexomon-card h3 {
  font-size: 1.5em;
  /* Default font size */
  margin: 5px 0;
  /* Space around the heading */
}

.nexomon-card:hover {
  background-color: rgba(141, 140, 140, 0.068);
  transform: scale(1.02);
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

/* Media Queries for Responsiveness */

@media (max-width: 3840px) {
  .nexomon-card {
    width: calc(14% - 14.8px);
    margin: 30px;
    max-height: 300px;
  }
}

@media (max-width: 1925px) {
  .nexomon-card {
    width: calc(14% - 14.8px);
    /* Default width for larger screens */
    margin: 30px;
    max-height: 278px;
  }
}


@media (max-width: 1280px) {
  .nexomon-card {
    width: calc(30% - 20px);
    /* Maintain three cards per row on small mobile devices */
    margin: 10px;
    /* Space between cards */
    flex-basis: 26.9%;
    max-height: 289px;
  }
}

@media (max-width: 480px) {
  .nexomon-card {
    width: calc(30% - 20px);
    /* Maintain three cards per row on small mobile devices */
    margin: 10px;
    /* Space between cards */
    flex-basis: 26.9%;
    max-height: 144px;
  }

  .nexomon-card h3 {
    font-size: 0.9em;
    /* Smaller font size for small devices */
  }

  .nexomon-grid {
    justify-content: space-between;
    /*which one is the top margin?
     */
    margin: -150px 20px 20px;
    flex-flow: row wrap;
  }

  .grid-scroll-container {
     padding-top: var(--filter-container-height); /* Ensure padding is applied */
     height: calc(100vh - 300px); /* Ensure height is calculated */
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
</style>

<style scoped src="../assets/styles/button-styles.css"></style>

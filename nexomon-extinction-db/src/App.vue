<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
    <a class="navbar-brand" href="#" style="margin-left: 15px;">Nexomon Extinction Database</a>
    <button ref="navbarToggler" class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNavDropdown" aria-controls="navbarNavDropdown" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarNavDropdown">
      <ul class="navbar-nav">
        <li class="nav-item active">
          <router-link class="nav-link" to="/" @click="handleNavClick">Home</router-link>
        </li>
        <li class="nav-item">
          <router-link class="nav-link" to="/dex" @click="handleNavClick">Database</router-link>
        </li>
      </ul>
    </div>
  </nav>
  <div id="app" :class="{ 'dark-mode': isDarkMode }">
    <router-view v-slot="{ Component }">
      <transition name="fade">
        <component :is="Component" />
      </transition>
    </router-view>
  </div>
</template>

<script>
import { Collapse } from 'bootstrap';
export default {
  data() {
    return {
      isDarkMode: false,
    };
  },
  methods: {
    toggleDarkMode() {
      this.isDarkMode = !this.isDarkMode;
      
      // Apply to documentElement instead of body to match index.html
      if (this.isDarkMode) {
        document.documentElement.classList.add('dark-mode');
      } else {
        document.documentElement.classList.remove('dark-mode');
      }
      
      // Also apply to body to maintain backward compatibility
      if (this.isDarkMode) {
        document.body.classList.add('dark-mode');
      } else {
        document.body.classList.remove('dark-mode');
      }
      
      // Save preference to localStorage
      localStorage.setItem('dark-mode', this.isDarkMode);
    },
    loadUserPreference() {
      const savedMode = localStorage.getItem('dark-mode') === 'true';
      this.isDarkMode = savedMode;
      
      // Apply to documentElement to match index.html
      if (savedMode) {
        document.documentElement.classList.add('dark-mode');
      } else {
        document.documentElement.classList.remove('dark-mode');
      }
      
      // Also apply to body to maintain backward compatibility
      if (savedMode) {
        document.body.classList.add('dark-mode');
      } else {
        document.body.classList.remove('dark-mode');
      }
    },
    handleNavClick() {
      const toggler = this.$refs.navbarToggler;
      const collapseElement = document.getElementById('navbarNavDropdown');

      if (toggler && toggler.offsetParent !== null && collapseElement && collapseElement.classList.contains('show')) {
        const bsCollapse = Collapse.getInstance(collapseElement);
        if (bsCollapse) {
          bsCollapse.hide();
        }
      }
    },
  },
  mounted() {
    this.loadUserPreference(); // Load user dark mode preference on app mount
  }
};
</script>

<style>
#app {
  min-height: 100%; /* Ensure the app fills at least the viewport */
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  background-color: #ffffff;
  height: fit-content;
  color: #000000;
  position: relative; /* Needed for absolute positioning of children if used */
}

html, body {
  margin: 0; /* Remove default margin */
  padding: 0; /* Remove default padding */
  height: 100%; /* Ensure full height for body and app */
}

.navbar {
  padding: 15px 30px; /* Adjust padding for better layout */
  width: 100%; /* Ensure navbar takes full width */
  position: relative; /* Needed for z-index */
  z-index: 20; /* Higher than filters-container (10) */
}

.navbar a {
  font-weight: bold;
  color: #e0e0e0;
}

.navbar a.router-link-exact-active {
  color: #e2e79e;
}

.navbar-toggler{
  margin-right: 10px;
}

.maps-list {
  background-color: #f0f0f0;
}

#app {
  min-height: 100%; /* Ensure the app fills at least the viewport */
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

/* Style the expanded dropdown menu background - Updated to fix desktop view */
.navbar-collapse {
  background-color: #343a40;
  padding: 0.5rem 1rem;
  border-radius: 0.25rem;
  margin-top: 5px;
}

/* Add styles specifically for large screens */
@media (min-width: 992px) {
  .navbar-collapse {
    background-color: transparent; /* Remove background on desktop */
    padding: 0; /* Remove padding on desktop */
    margin-top: 0; /* Remove margin on desktop */
  }
}

/* Dark mode for body, app, and html */
.dark-mode html ,
.dark-mode body,
.dark-mode #app {
  background-color: #212529;
  color: #e0e0e0;
  text-shadow: 2px 0 #000000, -2px 0 #000000, 0 2px #000000, 0 -2px #000000,
               1px 1px #000000, -1px -1px #000000, 1px -1px #000000, -1px 1px #000000;
}

/* Maps list and other sections */
.maps-list {
  background-color: #f0f0f0;
}

/* Dark mode specific styles */
.dark-mode .maps-list {
  background-color: #313131;
  border-top: 1px solid #ccc;
}

/* Page Transition Styles */
.fade-enter-active { /* Only apply transition to entering element */
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to { /* Start transparent (enter) or end transparent (leave) */
  opacity: 0;
}

.fade-enter-to,
.fade-leave-from { /* End opaque (enter) or start opaque (leave) */
  opacity: 1;
}

</style>

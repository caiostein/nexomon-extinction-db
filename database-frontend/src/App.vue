<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
    <div class="container-fluid">
      <a class="navbar-brand" href="#/nexomons">Nexomon Extinction Database</a>
      <button ref="navbarToggler" class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNavDropdown" aria-controls="navbarNavDropdown" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarNavDropdown">        <ul class="navbar-nav me-auto">
          <li class="nav-item">
            <router-link class="nav-link" to="/nexomons" @click="handleNavClick">Nexomon Database</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/locations" @click="handleNavClick">Location Database</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/collection" @click="handleNavClick">Collection</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/skills" @click="handleNavClick">Skill Database</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/about" @click="handleNavClick">About</router-link>
          </li>
        </ul>
          <!-- Dark mode toggle in navbar -->
        <button class="nexo-button nexo-button-toggle" @click="toggleDarkMode">
          {{ isDarkMode ? 'Light Mode' : 'Dark Mode' }}
        </button>
      </div>
    </div>
  </nav>
  <div id="app" :class="{ 'dark-mode': isDarkMode }">
    <router-view v-slot="{ Component }">
      <transition name="fade">
        <div>
          <component :is="Component" />
        </div>
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
  min-height: 100%;
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  background-color: #ffffff;
  height: fit-content;
  color: #000000;
  position: relative;
}

html, body {
  margin: 0;
  padding: 0;
  height: 100%;
}

.navbar {
  padding: 0.5rem 1rem;
  width: 100%;
  position: fixed;
  top: 0;
  left: 0;
  z-index: 100;
  background-color: #212529;
}

.navbar-brand {
  margin-left: 0 !important; /* Remove any inline margin that could cause shifting */
  padding-left: 0;
}

.navbar-toggler {
  margin-right: 0 !important; /* Ensure no right margin on the toggle button */
  padding: 0.25rem 0.75rem; /* Bootstrap's default padding for navbar-toggler */
}

.navbar a {
  font-weight: bold;
  color: #e0e0e0;
}

.navbar a.router-link-active {
  color: #e2e79e;
}

.navbar a.router-link-exact-active {
  color: #e2e79e;
}

.maps-list {
  background-color: #f0f0f0;
}

#app {
  min-height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

/* Style the expanded dropdown menu background */
.navbar-collapse {
  background-color: #343a40;
  padding: 0.5rem 1rem;
  border-radius: 0.25rem;
  margin-top: 5px;
}

/* Add styles specifically for large screens */
@media (min-width: 992px) {
  .navbar-collapse {
    background-color: transparent;
    padding: 0;
    margin-top: 0;
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
.fade-enter-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.fade-enter-to,
.fade-leave-from {
  opacity: 1;
}

/* Dark mode toggle button in navbar */
.toggle-button {
  padding: 8px 15px;
  background-color: #3aa9bd;
  color: #ffffff;
  border: none;
  cursor: pointer;
  border-radius: 5px;
  margin-right: 15px;
  font-size: 0.9rem;
  transition: background-color 0.3s ease;
}

.dark-mode .toggle-button {
  background-color: #555555;
  color: #f0f0f0;
}

@media (max-width: 991.98px) {
  .toggle-button {
    margin: 10px 0;
    width: 150px;
  }
  
  .navbar-collapse {
    padding-top: 0.5rem;
    padding-bottom: 0.5rem;
  }
}
</style>

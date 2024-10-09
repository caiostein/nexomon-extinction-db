<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
    <a class="navbar-brand" href="#" style="margin-left: 15px;">Nexomon Extinction Database</a>
    <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNavDropdown"
      aria-controls="navbarNavDropdown" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarNavDropdown">
      <ul class="navbar-nav">
        <li class="nav-item active">
          <router-link class="nav-link" to="/">Home</router-link>
        </li>
        <li class="nav-item">
          <router-link class="nav-link" to="/dex">Database</router-link>
        </li>
      </ul>
    </div>
  </nav>
  <div id="app" :class="{ 'dark-mode': isDarkMode }">
    <router-view />
  </div>
</template>

<script>
export default {
  data() {
    return {
      isDarkMode: false,
    };
  },
  methods: {
    toggleDarkMode() {
      this.isDarkMode = !this.isDarkMode;
      document.body.classList.toggle('dark-mode', this.isDarkMode);
      localStorage.setItem('dark-mode', this.isDarkMode);
    },
    loadUserPreference() {
      const savedMode = localStorage.getItem('dark-mode') === 'true';
      this.isDarkMode = savedMode;
      if (savedMode) {
        document.body.classList.add('dark-mode');
      } else {
        document.body.classList.remove('dark-mode');
      }
    }
  },
  mounted() {
    this.loadUserPreference(); // Load user dark mode preference on app mount
  }
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  background-color: #ffffff;
  color: #000000;
}

html, body {
  background-color: #ffffff;
  color: #000000;
}

nav {
  padding: 30px;
}

nav a {
  font-weight: bold;
  color: #2c3e50;
}

nav a.router-link-exact-active {
  color: #3aa9bd;
}

.maps-list {
  background-color: #f0f0f0;
}

#app {
  height: fit-content; /* Ensure full height for body and app */
}

body, html {
  height: 100%; /* Ensure full height for body and app */
}

#app {
  min-height: 100%; /* Ensure the app fills at least the viewport */
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

/* Dark mode for body, app, and html */
.dark-mode html,
.dark-mode body,
.dark-mode #app {
  background-color: #212529;
  color: #e0e0e0;
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
</style>

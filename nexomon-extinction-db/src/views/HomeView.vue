<template>
  <div class="home">
    <img alt="Nexomon Extinction logo" class="logo" src="../assets/logo.png">
    <button class="toggle-button" @click="toggleDarkMode">
      {{ isDarkMode ? 'Switch to Light Mode' : 'Switch to Dark Mode' }}
    </button>
  </div>
</template>

<script>
export default {
  name: 'HomeView',
  computed: {
    isDarkMode() {
      return this.$root.isDarkMode; // Access dark mode state from App.vue
    }
  },
  methods: {
    toggleDarkMode() {
      this.$root.toggleDarkMode(); // Call the global toggle method
    }
  }
};
</script>

<style scoped>
.home {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
}

.logo {
  margin: 50px;
}

.toggle-button {
  margin-top: 20px;
  padding: 10px 20px;
  background-color: #3aa9bd;
  color: #ffffff;
  border: none;
  cursor: pointer;
  border-radius: 5px;
}

/* Dark mode styles */
.dark-mode .toggle-button {
  background-color: #555555;
  color: #f0f0f0;
}
</style>

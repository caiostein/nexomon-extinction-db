<template>
  <div class="about-container">
    <h1>About Nexomon Extinction Database</h1>
    
    <div class="about-card">
      <h2>Project Information</h2>
      <p>
        This Nexomon Extinction Database is a comprehensive resource for players of Nexomon: Extinction.
        It provides detailed information about all Nexomon species, their locations, evolution paths, and more.
      </p>
      <p>
        This project was built using Vue.js and includes features such as:
      </p>
      <ul>
        <li>Complete Nexomon database with searchable entries</li>
        <li>Detailed information for each Nexomon including stats, elemental type, and habitat</li>
        <li>Evolution chains</li>
        <li>Location maps</li>
        <li>Dark/Light mode toggle</li>
      </ul>
    </div>
    
    <div class="about-card">
      <h2>Credits</h2>
      <p>
        Data for this project was compiled from various sources including:
      </p>
      <ul>
        <li>Nexomon: Extinction game</li>
        <li>Community resources and wikis</li>
      </ul>
      <p>
        All Nexomon images, data, and related content are property of VEWO Interactive Inc. 
        This is a fan-made project and is not affiliated with or endorsed by the official game developers.
      </p>
    </div>
    
    <div class="about-card">
      <h2>Contact</h2>
      <p>
        Found an issue or have suggestions for improvement? Please let me know!
      </p>
      <div class="links">
        <a href="https://github.com/caiostein/nexomon-extinction-db" target="_blank" rel="noopener noreferrer">
          <i class="fab fa-github"></i> GitHub Repository
        </a>
      </div>
    </div>
  </div>
</template>

<style scoped>
.about-container {
  max-width: 800px;
  margin: auto auto 100px auto;
  padding: 10px 20px;
  text-align: left;
}

h1 {
  text-align: center;
  margin-bottom: 50px;
  color: #333;
  padding-top: 15px;
}

.about-card {
  background-color: #f8f9fa;
  border: 1px solid #dee2e6;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 30px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

h2 {
  color: #3aa9bd;
  margin-bottom: 15px;
}

ul {
  padding-left: 20px;
  margin-bottom: 15px;
}

li {
  margin-bottom: 5px;
}

.links {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}

.links a {
  display: inline-flex;
  align-items: center;
  padding: 10px 20px;
  background-color: #3aa9bd;
  color: white;
  text-decoration: none;
  border-radius: 5px;
  transition: background-color 0.3s ease;
}

.links a:hover {
  background-color: #2d8a9e;
}

.links i {
  margin-right: 8px;
  font-size: 1.2em;
}

.dark-mode h1 {
  color: white;
  text-shadow: 2px 0 #000000, -2px 0 #000000, 0 2px #000000, 0 -2px #000000,
               1px 1px #000000, -1px -1px #000000, 1px -1px #000000, -1px 1px #000000;
}

.dark-mode .about-card,
.dark-mode .about-card p,
.dark-mode .about-card li,
.dark-mode .about-card h2 {
  text-shadow: none;
  color: #333;
}
</style>

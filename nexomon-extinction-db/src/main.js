import { createApp } from 'vue';
import App from './App.vue';
import router from './router';

// Import Bootstrap CSS and JavaScript
import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap';

// Import BootstrapVue3 CSS
import 'bootstrap-vue-3/dist/bootstrap-vue-3.css';

import BootstrapVue3 from 'bootstrap-vue-3';

// Import global styles
import './assets/styles/global.css';

const app = createApp(App);

app.use(router);
app.use(BootstrapVue3);

app.mount('#app');

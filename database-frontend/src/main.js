import { createApp } from 'vue';
import App from './App.vue';
import router from './router';

import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap';
import 'bootstrap-vue-3/dist/bootstrap-vue-3.css';
import BootstrapVue3 from 'bootstrap-vue-3';
import '@fortawesome/fontawesome-free/css/all.css';
import './assets/styles/global.css';
import './assets/styles/button-styles.css';
import './assets/styles/caught-mode.css';
import './assets/styles/section-common.css';
import './assets/styles/basic-info.css';
import './assets/styles/location-info.css';
import './assets/styles/evolution-info.css';
import './assets/styles/extra-info.css';
import './assets/styles/skill-tree.css';
import './assets/styles/maps-section.css';

const app = createApp(App);

app.use(router);
app.use(BootstrapVue3);

app.mount('#app');

<template>
  <div class="collection-wrapper">
    <div class="filters-container collection-header-row">
      <div class="collection-title-row">
        <h1 class="collection-title">My Nexomon Collection</h1>
      </div>
      <div class="collection-search-row">
        <input type="text" v-model="searchQuery" placeholder="Search by name or number..."
          class="collection-search-box" />
        <button class="caught-toggle-btn" :class="{ active: caughtMode }" @click="toggleCaughtMode"
          title="Toggle Caught Mode" aria-label="Toggle Caught Mode" style="margin-left: 1rem;">
          <span class="switch-slider"></span>
        </button>
      </div>
    </div>
    <div class="collection-grid-scroll-container">
      <div v-if="filteredNexomonList.length" class="nexomon-grid">
        <template v-for="nexomon in filteredNexomonList" :key="nexomon.Number">
          <router-link v-if="!caughtMode" :to="`/nexomon/${nexomon.Number}`" class="nexomon-item"
            style="cursor: pointer;" tabindex="0">
            <img :src="getThumbnail(nexomon.Name)" :alt="nexomon.Name" class="nexomon-thumb" />
            <div class="nexomon-info">
              <div class="nexomon-number">{{ nexomon.Number }}</div>
              <div class="nexomon-name">{{ nexomon.Name }}</div>
            </div>
          </router-link>
          <div v-else class="nexomon-item remove-glow" style="cursor: pointer;" tabindex="0"
            @click="removeFromCollection(nexomon.Number)">
            <img :src="getThumbnail(nexomon.Name)" :alt="nexomon.Name" class="nexomon-thumb" />
            <div class="nexomon-info">
              <div class="nexomon-number">{{ nexomon.Number }}</div>
              <div class="nexomon-name">{{ nexomon.Name }}</div>
            </div>
          </div>
        </template>
      </div>
    </div>
    <div v-if="!caughtNexomonList.length">
      <p>You haven't caught any Nexomon yet!</p>
    </div>
    <div style="text-align: center; margin-top: 0.5rem;">
      <button class="nexo-button wrench-toggle-btn" :disabled="!caughtMode" :aria-disabled="!caughtMode" @click="handleWrenchToggle" title="Show import/export tools" aria-label="Show import/export tools">
        <img src="@/assets/wrench-icon.svg" alt="Wrench" class="wrench-svg-icon" />
      </button>
      <transition name="dropdown-fade">
        <div v-if="showTools" class="collection-tools-stack">
          <button class="nexo-button nexo-button-danger clear-collection-btn"
            :disabled="!caughtMode || !caughtNexomonList.length" @click="caughtMode && clearCollection()">
            Clear Collection
          </button>
          <button class="nexo-button nexo-button-info" :disabled="!caughtNexomonList.length" @click="toggleExportJson">Export Collection</button>
          <button class="nexo-button nexo-button-confirm" @click="toggleImportJson">Import Collection</button>
          <transition name="dropdown-fade">
            <div v-if="showExportJson" class="json-modal">
              <textarea readonly class="json-textarea" :value="exportedJson"></textarea>
              <button class="nexo-button nexo-button-confirm" @click="copyExportedJson">Copy</button>
              <button class="nexo-button nexo-button-secondary" @click="showExportJson = false">Close</button>
            </div>
          </transition>
          <transition name="dropdown-fade">
            <div v-if="showImportJson" class="json-modal">
              <textarea class="json-textarea" v-model="importJsonText" placeholder="Paste your collection JSON here"></textarea>
              <button class="nexo-button nexo-button-confirm" @click="confirmImportJson">Confirm Import</button>
              <button class="nexo-button nexo-button-secondary" @click="showImportJson = false">Cancel</button>
            </div>
          </transition>
        </div>
      </transition>
    </div>
    <!-- Toast notification -->
    <transition name="dropdown-fade">
      <div v-if="toast.show" :class="['nexo-toast', toast.type]">
        {{ toast.message }}
      </div>
    </transition>
  </div>
</template>

<script>
import data from '../../../python-scripts/assets/nexomon_extinction_database.json';
import { useCaughtMode } from './useCaughtMode.js';
import { computed, ref } from 'vue';

export default {
  name: 'CollectionList',
  data() {
    return {
      searchQuery: ''
    };
  },
  setup() {
    const { caughtNexomons, caughtMode, toggleCaughtMode } = useCaughtMode();
    // Make caughtNexomonList reactive to caughtNexomons
    const caughtNexomonList = computed(() => data.filter(n => caughtNexomons.value.includes(n.Number)));
    function getThumbnail(nexomonName) {
      try {
        return require(`../assets/downloaded_images/${nexomonName}-menu.png`);
      } catch (error) {
        try {
          return require(`../assets/downloaded_images/${nexomonName}_(Extinction)-menu.png`);
        } catch (error) {
          try {
            nexomonName = nexomonName.replace(' (Extinction)', '');
            return require(`../assets/downloaded_images/${nexomonName}.png`);
          } catch (error) {
            try {
              return require(`../assets/downloaded_images/${nexomonName}2.png`);
            } catch (error) {
              return '';
            }
          }
        }
      }
    }
    function clearCollection() {
      localStorage.removeItem('caughtNexomons');
      caughtNexomons.value = [];
      showImportJson.value = false;
      showExportJson.value = false;
    }
    function removeFromCollection(nexomonNumber) {
      const index = caughtNexomons.value.indexOf(nexomonNumber);
      console.log('Removing Nexomon:', nexomonNumber);
      console.log('Current caughtNexomons:', caughtNexomons.value);
      if (index > -1) {
        caughtNexomons.value.splice(index, 1);
        localStorage.setItem('caughtNexomons', JSON.stringify(caughtNexomons.value));
      }
    }
    function scrollToBottomIfMobile() {
      if (window.innerWidth < 600) {
        window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' });
      }
    }
    function handleWrenchToggle() {
      showTools.value = !showTools.value;
      if (showTools.value) {
        setTimeout(scrollToBottomIfMobile, 200);
      }
    }
    const showTools = ref(false);
    const showExportJson = ref(false);
    const showImportJson = ref(false);
    const importJsonText = ref('');
    const exportedJson = computed(() => JSON.stringify(caughtNexomons.value, null, 2));

    // Toast state
    const toast = ref({ show: false, message: '', type: 'success' });
    let toastTimeout = null;
    function showToast(message, type = 'success') {
      toast.value = { show: true, message, type };
      if (toastTimeout) clearTimeout(toastTimeout);
      toastTimeout = setTimeout(() => {
        toast.value.show = false;
      }, 2500);
    }

    function handleToggleCaughtMode() {
      toggleCaughtMode();
      showTools.value = false;
      showExportJson.value = false;
      showImportJson.value = false;
    }
    function toggleExportJson() {
      showExportJson.value = !showExportJson.value;
      showImportJson.value = false;
      if (showExportJson.value) {
        setTimeout(scrollToBottomIfMobile, 200);
      }
    }
    function toggleImportJson() {
      showImportJson.value = !showImportJson.value;
      showExportJson.value = false;
      if (showImportJson.value) {
        setTimeout(scrollToBottomIfMobile, 200);
      }
    }
    function copyExportedJson() {
      // Try Clipboard API first
      if (navigator.clipboard && typeof navigator.clipboard.writeText === 'function') {
        navigator.clipboard.writeText(exportedJson.value)
          .then(() => {
            showToast('Collection copied to clipboard!', 'success');
          })
          .catch(() => {
            fallbackCopy();
          });
      } else {
        fallbackCopy();
      }
      function fallbackCopy() {
        // Find the textarea in the DOM
        const textarea = document.querySelector('.json-modal .json-textarea');
        if (textarea) {
          textarea.removeAttribute('readonly');
          textarea.select();
          textarea.setSelectionRange(0, 99999); // For mobile
          try {
            const successful = document.execCommand('copy');
            if (successful) {
              showToast('Collection copied to clipboard!', 'success');
            } else {
              showToast('Copy failed. Please copy manually.', 'error');
            }
          } catch (err) {
            showToast('Copy failed. Please copy manually.', 'error');
          }
          textarea.setAttribute('readonly', 'readonly');
          window.getSelection().removeAllRanges();
        } else {
          showToast('Copy failed. Please copy manually.', 'error');
        }
      }
    }
    function confirmImportJson() {
      try {
        const imported = JSON.parse(importJsonText.value);
        if (Array.isArray(imported)) {
          caughtNexomons.value = imported;
          localStorage.setItem('caughtNexomons', JSON.stringify(imported));
          showToast('Collection imported successfully!', 'success');
          showImportJson.value = false;
          importJsonText.value = '';
        } else {
          showToast('Invalid file format.', 'error');
        }
      } catch (err) {
        showToast('Failed to import collection.', 'error');
      }
    }
    return {
      caughtNexomonList,
      getThumbnail,
      caughtMode,
      toggleCaughtMode: handleToggleCaughtMode,
      clearCollection,
      removeFromCollection,
      exportCollection: () => {}, // no-op, replaced by export textarea
      importCollection: () => {}, // no-op, replaced by import textarea
      showTools,
      showExportJson,
      showImportJson,
      toggleExportJson,
      toggleImportJson,
      exportedJson,
      copyExportedJson,
      importJsonText,
      confirmImportJson,
      toast,
      handleWrenchToggle,
    };
  },
  computed: {
    filteredNexomonList() {
      const q = this.searchQuery.trim().toLowerCase();
      if (!q) return this.caughtNexomonList;
      return this.caughtNexomonList.filter(n =>
        n.Name.toLowerCase().includes(q) || n.Number.toLowerCase().includes(q)
      );
    },
  },
};
</script>

<style scoped>
.collection-wrapper {
  --header-height: 120px;
  padding: 0 1rem;
  display: block;
  min-height: 100vh;
  max-width: 1200px;
  margin: 0 auto;
}

.collection-grid-scroll-container {
  margin-top: var(--header-height, 120px);
  height: calc(100vh - var(--header-height, 120px));
  overflow-y: auto;
  box-sizing: border-box;
}

.nexomon-grid {
  display: flex;
  flex-wrap: wrap;
  flex-direction: row;
  align-content: flex-start;
  gap: 2px;
  justify-content: center;
  width: 100%;
  margin: 0;
}

.filters-container.collection-header-row {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  z-index: 20;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 16px;
  padding: 20px 0;
  background: var(--header-bg, #fff);
}

.dark-mode .filters-container.collection-header-row {
  background: #212529;
}

.collection-title-row {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 24px;
  width: 100%;
}

.collection-title {
  font-size: 2rem;
  font-weight: 700;
  margin: 0;
  text-align: center;
}

.caught-toggle-btn {
  margin-left: 0;
  align-self: flex-start;
  margin-top: 10px;
}

.collection-search-row {
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 0.5rem;
  margin-bottom: 0.5rem;
  gap: 1rem;
}

.collection-search-box {
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
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
  margin-right: 0;
  margin-left: 0;
  display: block;
}

.dark-mode .collection-search-box {
  background-color: #333;
  color: #fff;
  border: 1px solid #555;
}

.nexomon-grid {
  display: flex;
  flex-wrap: wrap;
  flex-direction: row;
  align-content: flex-start;
  gap: 2px;
  justify-content: center;
  width: 100%;
}

.nexomon-item {
  width: calc(16.666% - 8px);
  margin: 4px;
  padding: 10px 6px 15px;
  border: 1px solid #ccc;
  border-radius: 8px;
  text-align: center;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  max-height: 290px;
  text-decoration: none;
  color: inherit;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: center;
  position: relative;
  background: #fff;
}

.nexomon-item:hover {
  background-color: rgba(141, 140, 140, 0.068);
  box-shadow: 0 4px 12px rgba(43, 159, 204, 0.18);
  transform: scale(1.02);
}

.dark-mode .nexomon-item {
  background: #212529;
  border-color: #444;
  color: #fff;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.30);
}

.dark-mode .nexomon-item:hover {
  background-color: rgba(255, 255, 255, 0.05);
}

.nexomon-thumb {
  width: 64px;
  height: 64px;
  object-fit: contain;
  margin-bottom: 8px;
  border-radius: 10px;
  background-color: rgba(0, 0, 0, 0.05);
  padding: 5px;
}

.nexomon-info {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.nexomon-number {
  font-size: 0.8rem;
  color: #666;
  margin-bottom: 2px;
}

.nexomon-name {
  font-size: 0.9rem;
  text-align: center;
  width: 100%;
  min-height: 2.8em;
  line-height: 1.4em;
  word-wrap: break-word;
  hyphens: auto;
}

.clear-collection-btn {
  position: relative !important;
  display: block;
  padding: 0.75rem 2.5rem;
  font-size: 1.1rem;
  font-weight: 600;
  color: #fff;
  background: #e53935;
  border: none;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(229, 57, 53, 0.08);
  cursor: pointer;
  transition: background 0.2s, box-shadow 0.2s, opacity 0.2s;
  opacity: 1;
  z-index: 1;
}

.clear-collection-btn:disabled,
.clear-collection-btn[aria-disabled="true"] {
  background: #aaa !important;
  cursor: not-allowed;
  opacity: 0.6;
}

.clear-collection-btn:hover {
  background: #b71c1c;
  box-shadow: 0 4px 16px rgba(229, 57, 53, 0.18);
}

.dark-mode .clear-collection-btn {
  background: #b71c1c;
  color: #fff;
}

.dark-mode .clear-collection-btn:hover {
  background: #e53935;
}

.wrench-toggle-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 50%;
  border: 1.5px solid #b0b8c1;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  color: #444;
  font-size: 1.4rem;
  box-shadow: 0 2px 8px rgba(43, 159, 204, 0.10), 0 1.5px 4px rgba(0, 0, 0, 0.08);
  transition: background 0.2s, color 0.2s, box-shadow 0.2s, transform 0.1s;
  cursor: pointer;
  outline: none;
  margin-bottom: 0.5rem;
}

.wrench-toggle-btn:hover,
.wrench-toggle-btn:focus {
  background: linear-gradient(135deg, #e3ecfa 0%, #b6c6e2 100%);
  color: #1976d2;
  box-shadow: 0 4px 16px rgba(43, 159, 204, 0.18), 0 2px 8px rgba(0, 0, 0, 0.10);
  transform: scale(1.08);
}

.wrench-toggle-btn:active {
  background: linear-gradient(135deg, #d1e0fa 0%, #a3b6d2 100%);
  color: #0d47a1;
  box-shadow: 0 2px 8px rgba(43, 159, 204, 0.18);
  transform: scale(0.97);
}

.dark-mode .wrench-toggle-btn {
  background: linear-gradient(135deg, #23272f 0%, #3a4250 100%);
  color: #e0e6f0;
  border: 1.5px solid #444b5a;
}

.dark-mode .wrench-toggle-btn:hover,
.dark-mode .wrench-toggle-btn:focus {
  background: linear-gradient(135deg, #2d3440 0%, #4a5670 100%);
  color: #90caf9;
}

.dark-mode .wrench-toggle-btn:active {
  background: linear-gradient(135deg, #23272f 0%, #3a4250 100%);
  color: #42a5f5;
}

.wrench-svg-icon {
  width: 1.5rem;
  height: 1.5rem;
  display: block;
  margin: 0 auto;
  filter: invert(20%) sepia(0%) saturate(0%) hue-rotate(180deg) brightness(90%) contrast(90%);
}
.wrench-toggle-btn:hover .wrench-svg-icon,
.wrench-toggle-btn:focus .wrench-svg-icon {
  filter: invert(34%) sepia(99%) saturate(748%) hue-rotate(181deg) brightness(95%) contrast(92%);
}
.dark-mode .wrench-svg-icon {
  filter: invert(90%) sepia(6%) saturate(0%) hue-rotate(180deg) brightness(90%) contrast(90%);
}
.dark-mode .wrench-toggle-btn:hover .wrench-svg-icon,
.dark-mode .wrench-toggle-btn:focus .wrench-svg-icon {
  filter: invert(70%) sepia(60%) saturate(400%) hue-rotate(181deg) brightness(110%) contrast(110%);
}

.collection-tools-stack {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
  margin-top: 0.2rem;
}

.dropdown-fade-enter-active, .dropdown-fade-leave-active {
  transition: all 0.25s cubic-bezier(.4,0,.2,1);
}
.dropdown-fade-enter-from, .dropdown-fade-leave-to {
  opacity: 0;
  transform: translateY(-16px) scaleY(0.95);
  pointer-events: none;
}
.dropdown-fade-enter-to, .dropdown-fade-leave-from {
  opacity: 1;
  transform: translateY(0) scaleY(1);
}

.json-modal {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
  margin-top: 0.5rem;
  width: 100%;
}
.json-textarea {
  width: 320px;
  min-height: 120px;
  font-family: monospace;
  font-size: 0.95rem;
  padding: 8px;
  border-radius: 8px;
  border: 1px solid #bbb;
  resize: vertical;
  background: #f8f9fa;
  color: #222;
}
.dark-mode .json-textarea {
  background: #23272f;
  color: #e0e6f0;
  border: 1px solid #444b5a;
}

.toast {
  position: fixed;
  left: 50%;
  bottom: 2.5rem;
  transform: translateX(-50%);
  min-width: 220px;
  max-width: 90vw;
  background: #323232;
  color: #fff;
  padding: 0.85rem 1.5rem;
  border-radius: 8px;
  font-size: 1.08rem;
  font-weight: 500;
  box-shadow: 0 4px 24px rgba(0,0,0,0.18);
  z-index: 1000;
  opacity: 0.97;
  pointer-events: none;
  text-align: center;
  transition: background 0.2s, color 0.2s;
}
.toast.success {
  background: #388e3c;
  color: #fff;
}
.toast.error {
  background: #d32f2f;
  color: #fff;
}
.dark-mode .toast {
  background: #23272f;
  color: #e0e6f0;
}
.dark-mode .toast.success {
  background: #2e7d32;
}
.dark-mode .toast.error {
  background: #b71c1c;
}
.toast-fade-enter-active, .toast-fade-leave-active {
  transition: opacity 0.35s cubic-bezier(.4,0,.2,1), transform 0.35s cubic-bezier(.4,0,.2,1);
}
.toast-fade-enter-from, .toast-fade-leave-to {
  opacity: 0;
  transform: translateX(-50%) translateY(30px) scale(0.98);
}
.toast-fade-enter-to, .toast-fade-leave-from {
  opacity: 0.97;
  transform: translateX(-50%) translateY(0) scale(1);
}

.nexo-toast {
  position: fixed;
  left: 50%;
  bottom: 2.5rem;
  transform: translateX(-50%);
  min-width: 220px;
  max-width: 90vw;
  background: #f0fdf4;
  color: #1b5e20;
  border: 1.5px solid #a5d6a7;
  border-radius: 8px;
  padding: 0.85rem 1.5rem;
  font-size: 1.1rem;
  font-weight: 500;
  box-shadow: 0 2px 12px rgba(43, 159, 204, 0.10);
  z-index: 1000;
  opacity: 0.98;
  transition: all 0.25s cubic-bezier(.4,0,.2,1);
  pointer-events: none;
}
.nexo-toast.error {
  background: #fff0f0;
  color: #b71c1c;
  border-color: #ef9a9a;
}
.nexo-toast.success {
  background: #f0fdf4;
  color: #1b5e20;
  border-color: #a5d6a7;
}
.dark-mode .nexo-toast {
  background: #23272f;
  color: #a5d6a7;
  border-color: #444b5a;
}
.dark-mode .nexo-toast.error {
  background: #2d1c1c;
  color: #ef9a9a;
  border-color: #b71c1c;
}
.dark-mode .nexo-toast.success {
  background: #1b2d1c;
  color: #a5d6a7;
  border-color: #388e3c;
}

@media (min-width: 0px) {
  .filters-container.collection-header-row {
    position: static;
  }

  .collection-grid-scroll-container {
    margin-top: 0;
    height: auto;
    overflow-y: visible;
  }
}

@media (max-width: 900px) {
  .nexomon-grid {
    gap: 0;
    justify-content: space-evenly;
  }

  .nexomon-item {
    width: calc(33.333% - 4px);
    margin: 2px;
    max-height: 260px;
  }
}
</style>
<style scoped src="../assets/styles/button-styles.css"></style>
<style scoped src="../assets/styles/caught-mode.css"></style>

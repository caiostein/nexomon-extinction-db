import { ref, watch } from 'vue';

export function useCaughtMode(storageKey = 'caughtNexomons') {
  const caughtMode = ref(false);
  const caughtNexomons = ref([]);

  // Load caught Nexomons from localStorage
  const saved = localStorage.getItem(storageKey);
  if (saved) {
    try {
      caughtNexomons.value = JSON.parse(saved);
    } catch (e) {
      caughtNexomons.value = [];
    }
  }

  // Load caughtMode from localStorage
  const savedMode = localStorage.getItem('caughtMode');
  if (savedMode !== null) {
    caughtMode.value = savedMode === 'true';
  }

  // Watch for changes and persist caughtMode to localStorage
  watch(
    caughtMode,
    (val) => {
      localStorage.setItem('caughtMode', val ? 'true' : 'false');
    },
    { immediate: true }
  );

  function toggleCaughtMode() {
    caughtMode.value = !caughtMode.value;
  }

  function isCaught(number) {
    return caughtNexomons.value.includes(number);
  }

  function toggleCaught(number) {
    const idx = caughtNexomons.value.indexOf(number);
    if (idx === -1) {
      caughtNexomons.value.push(number);
    } else {
      caughtNexomons.value.splice(idx, 1);
    }
    localStorage.setItem(storageKey, JSON.stringify(caughtNexomons.value));
  }

  return {
    caughtMode,
    caughtNexomons,
    toggleCaughtMode,
    isCaught,
    toggleCaught,
  };
}

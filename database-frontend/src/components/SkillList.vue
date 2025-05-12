<template>
    <div class="skill-list-wrapper">
        <div class="filters-container">
            <input type="text" v-model="searchQuery" placeholder="Search for a Skill" class="search-box" />

            <!-- Type Filter Dropdown -->
            <div class="custom-select">
                <div @click.stop="toggleDropdown('type')" class="selected-option">
                    <span v-if="selectedType">
                        <img :src="getTypeIcon(selectedType)" alt="Icon" class="type-icon" />
                        {{ selectedType }}
                    </span>
                    <span v-else><span class="type-icon emoji-icon">🌈</span> All Types</span>
                    <span class="dropdown-arrow">▼</span>
                </div>
                <div class="dropdown-menu" v-show="dropdownOpen && filterType === 'type'">
                    <div class="dropdown-item" @mousedown.stop="selectDropdown('type', '')">
                        <span class="type-icon emoji-icon">🌈</span> All Types
                    </div>
                    <div v-for="type in uniqueTypes" :key="type" class="dropdown-item"
                        @mousedown.stop="selectDropdown('type', type)">
                        <img :src="getTypeIcon(type)" alt="Icon" class="type-icon" />
                        {{ type }}
                    </div>
                </div>
            </div>
            <!-- Effect Filter Dropdown -->
            <div class="custom-select" v-show="!(dropdownOpen && filterType === 'type' && isMobile)">
                <div @click.stop="toggleDropdown('effect')" class="selected-option">
                    <div class="selected-content">
                        <template v-if="selectedEffect === 'No Effect'">
                            <span class="selected-flex"><span class="type-icon emoji-icon">🚫</span> No Effect</span>
                        </template>
                        <template v-else-if="selectedEffect">
                            <span class="selected-flex"><img :src="getEffectIcon(selectedEffect)" alt="Icon" class="effect-icon" />
                            {{ selectedEffect }}</span>
                        </template>
                        <template v-else>
                            <span class="selected-flex"><span class="type-icon emoji-icon">✨</span> All Effects</span>
                        </template>
                    </div>
                    <span class="dropdown-arrow">▼</span>
                </div>
                <div class="dropdown-menu" v-show="dropdownOpen && filterType === 'effect'">
                    <div class="dropdown-item" @mousedown.stop="selectDropdown('effect', '')">
                        <span class="type-icon emoji-icon">✨</span> All Effects
                    </div>
                    <div class="dropdown-item" @mousedown.stop="selectDropdown('effect', 'No Effect')">
                        <span class="type-icon emoji-icon">🚫</span> No Effect
                    </div>
                    <div v-for="effect in uniqueEffects" :key="effect" class="dropdown-item"
                        @mousedown.stop="selectDropdown('effect', effect)">
                        <img :src="getEffectIcon(effect)" alt="Icon" class="type-icon" />
                        {{ effect }}
                    </div>
                </div>
            </div>
        </div>
        <div class="grid-scroll-container">
            <div class="skill-grid">
                <div v-for="skill in filteredSkills" :key="skill.Name" class="skill-card">
                    <router-link :to="`/skill/${encodeURIComponent(skill.Name)}`" class="skill-link">
                        <div class="skill-info">
                            <div class="skill-name">
                                <img v-if="skill.Image" :src="require(`@/assets/${skill.Image}`)" :alt="skill.Name"
                                    class="skill-icon" />
                                {{ skill.Name }}
                            </div>
                            <div class="skill-type"
                                :class="{ 'single-row': !skill.Effect || (typeof skill.Effect === 'string' && skill.Effect === '-') }">
                                <img v-if="skill.Type && skill.Type.image" :src="require(`@/assets/${skill.Type.image}`)"
                                    :alt="skill.Type.text" class="type-icon" />
                                {{ skill.Type && skill.Type.text }}
                            </div>
                            <div v-if="skill.Effect && !(typeof skill.Effect === 'string' && skill.Effect === '-')"
                                class="skill-effect">
                                <img v-if="skill.Effect && skill.Effect.image"
                                    :src="require(`@/assets/${skill.Effect.image}`)" :alt="skill.Effect.text"
                                    class="effect-icon" />
                                <span v-if="skill.Effect && skill.Effect.text">{{
                                    skill.Effect.text.replace(/\s*\(status\)$/i, '') }}</span>
                                <span v-else-if="typeof skill.Effect === 'string'">{{
                                    skill.Effect.replace(/\s*\(status\)$/i, '') }}</span>
                            </div>
                        </div>
                    </router-link>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import skills from '../assets/skill_database.json';

export default {
    data() {
        return {
            skills,
            searchQuery: '',
            selectedType: '',
            selectedEffect: '',
            dropdownOpen: false,
            filterType: '', // 'type' or 'effect'
            isMobile: window.innerWidth <= 900,
        };
    },
    computed: {
        uniqueTypes() {
            const types = new Set();
            this.skills.forEach(skill => {
                if (skill.Type && typeof skill.Type === 'object' && skill.Type.text) {
                    const typeText = skill.Type.text.replace('Type', '').trim();
                    types.add(typeText);
                }
            });
            return Array.from(types).sort();
        },
        uniqueEffects() {
            const effects = new Set();
            this.skills.forEach(skill => {
                if (skill.Effect && typeof skill.Effect === 'object' && skill.Effect.text) {
                    // Remove (status) from dropdown
                    effects.add(skill.Effect.text.replace(/\s*\(status\)$/i, ''));
                } else if (typeof skill.Effect === 'string' && skill.Effect !== '-') {
                    effects.add(skill.Effect.replace(/\s*\(status\)$/i, ''));
                }
            });
            return Array.from(effects).sort();
        },
        filteredSkills() {
            const query = this.searchQuery.toLowerCase();
            return this.skills.filter(skill => {
                const nameMatch = skill.Name.toLowerCase().includes(query);
                let typeMatch = true;
                let effectMatch = true;
                if (this.selectedType) {
                    const skillType = skill.Type && skill.Type.text ? skill.Type.text.replace('Type', '').trim() : '';
                    typeMatch = skillType === this.selectedType;
                }
                if (this.selectedEffect === 'No Effect') {
                    effectMatch = !skill.Effect || (typeof skill.Effect === 'string' && skill.Effect === '-');
                } else if (this.selectedEffect) {
                    let skillEffect = '';
                    if (skill.Effect && typeof skill.Effect === 'object' && skill.Effect.text) {
                        skillEffect = skill.Effect.text.replace(/\s*\(status\)$/i, '');
                    } else if (typeof skill.Effect === 'string') {
                        skillEffect = skill.Effect.replace(/\s*\(status\)$/i, '');
                    }
                    effectMatch = skillEffect === this.selectedEffect;
                }
                return nameMatch && typeMatch && effectMatch;
            });
        }
    },
    mounted() {
        window.addEventListener('resize', this.handleResize);
    },
    beforeUnmount() {
        window.removeEventListener('resize', this.handleResize);
        document.removeEventListener('click', this.closeDropdownOutside);
    },
    methods: {
        getTypeIcon(type) {
            if (!type) return '';
            try {
                return require(`@/assets/downloaded_images/${type}_Type_Icon.png`);
            } catch {
                console.log(`Icon for type ${type} not found.`);
                return '';
            }
        },
        getEffectIcon(effect) {
            if (!effect) return ''; 
            try {
                return require(`@/assets/downloaded_images/${effect}_Status_Icon.png`);
            } catch {
                console.log(`Icon for effect ${effect} not found.`);
                return '';
            }
        },
        toggleDropdown(type) {
            if (!this.dropdownOpen || this.filterType !== type) {
                this.dropdownOpen = true;
                this.filterType = type;
                setTimeout(() => document.addEventListener('click', this.closeDropdownOutside), 10);
            } else {
                this.dropdownOpen = false;
                this.filterType = '';
                document.removeEventListener('click', this.closeDropdownOutside);
            }
        },
        closeDropdownOutside(e) {
            if (!e.target.closest('.custom-select')) {
                this.dropdownOpen = false;
                this.filterType = '';
                document.removeEventListener('click', this.closeDropdownOutside);
            }
        },
        selectDropdown(type, value) {
            if (type === 'type') {
                this.selectedType = value;
            } else if (type === 'effect') {
                this.selectedEffect = value;
            }
            this.dropdownOpen = false;
            this.filterType = '';
            document.removeEventListener('click', this.closeDropdownOutside);
        },
        handleResize() {
            this.isMobile = window.innerWidth <= 900;
        },
    },
};
</script>

<style scoped>
.skill-list-wrapper {
    --header-height: 60px;
    --filter-container-height: 150px;
}

.filters-container {
    position: fixed;
    top: var(--header-height);
    left: 0;
    width: 100%;
    padding: 20px 0;
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;
    align-items: center;
    justify-content: center;
    height: var(--filter-container-height);
    box-sizing: border-box;
    gap: 16px;
}

.grid-scroll-container {
    padding-top: var(--filter-container-height);
    height: calc(100vh - var(--filter-container-height) - var(--header-height));
    overflow-y: auto;
    box-sizing: border-box;
}

.skill-grid {
    margin: -100px 45px 45px;
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 5px;
}

.skill-card {
  background: var(--card-bg, #fafdff);
  border-radius: 16px;
  border: 2px solid #e3e8f0;
  box-shadow: 0 2px 8px rgba(0,0,0,0.10), 0 1.5px 6px rgba(0,0,0,0.08);
  padding: 18px 16px 14px 16px;
  margin: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  transition: box-shadow 0.18s, border-color 0.18s, background 0.18s;
  cursor: pointer;
  position: relative;
  border-bottom: 3.5px solid #414652;
  min-width: 220px;
  max-width: 260px;
  min-height: 170px;
  max-height: 210px;
}
.skill-card:hover {
  box-shadow: 0 4px 18px rgba(0,0,0,0.18), 0 2px 8px rgba(0,0,0,0.10);
  border-color: #264ba3;
  background: #f0f6ff;
  z-index: 2;
}
.dark-mode .skill-card {
  background: #23272b;
  border: 2px solid #353a40;
  box-shadow: 0 2px 8px rgba(0,0,0,0.22), 0 1.5px 6px rgba(0,0,0,0.18);
  border-bottom: 3.5px solid #4f545f;
}
.dark-mode .skill-card:hover {
  background: #232c3a;
  border-color: #264ba3;
  box-shadow: 0 4px 18px rgba(0,0,0,0.28), 0 2px 8px rgba(0,0,0,0.18);
}

.skill-info {
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-bottom: 0;
}

.skill-name {
    font-size: 1.1rem;
    font-weight: bold;
    margin-bottom: 10px;
    display: flex;
    align-items: center;
    gap: 4px;
    background: rgba(0, 0, 0, 0.05);
    border-radius: 10px;
    padding: 4px 12px;
    min-width: 0;
    min-height: 2.8em;
    line-height: 1.4em;
    /* Prevent text from breaking out of the card */
    max-width: 95%;
    overflow: visible;
    text-overflow: unset;
    white-space: normal;
    word-break: normal;
    hyphens: none;
    justify-content: center;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
}

.dark-mode .skill-name {
    background: rgba(255, 255, 255, 0.08);
}

.skill-type,
.skill-effect {
    font-size: 0.95rem;
    margin-bottom: 2px;
    display: flex;
    align-items: center;
    gap: 4px;
    max-width: 100%;
    overflow: visible;
    text-overflow: unset;
    white-space: normal;
}

.skill-type.single-row {
    align-items: flex-end;
    min-height: 28px;
    height: 28px;
    margin-bottom: 0;
    margin-top: auto;
    display: flex;
    justify-content: center;
}

.skill-icon {
    width: 28px;
    height: 28px;
    object-fit: contain;
    vertical-align: middle;
    margin-right: 4px;
}

.type-icon,
.effect-icon {
    width: 20px;
    height: 20px;
    object-fit: contain;
    vertical-align: middle;
    margin-right: 4px;
}

.skill-stats {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    justify-content: center;
    font-size: 0.9rem;
    color: #555;
}

.search-box {
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
}

.search-box:focus {
    border-color: #3aa9bd;
    box-shadow: 0 0 0 2px rgba(58, 169, 189, 0.15);
}

.dark-mode .search-box {
    background-color: #333;
    color: #fff;
    border: 1px solid #555;
}

.custom-select {
    position: relative;
    min-width: 180px;
    margin: 0 8px 12px 8px;
    user-select: none;
    font-size: 1.05rem;
    z-index: 30;
}

.selected-option {
    background: #fff;
    color: #333;
    border: 1px solid #ccc;
    border-radius: 5px;
    padding: 10px 14px;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: space-between;
    min-width: 140px;
    transition: border 0.2s, background 0.2s, box-shadow 0.2s;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
}

.selected-option:hover {
    border-color: #3aa9bd;
    background: #e6f7fa;
}

.dark-mode .selected-option {
    background-color: #333;
    color: #fff;
    border: 1px solid #555;
}

.dropdown-arrow {
    margin-left: 10px;
    font-size: 0.9em;
}

.dropdown-menu {
    position: absolute;
    top: 110%;
    left: 0;
    right: 0;
    background: #fff;
    border: 1px solid #ccc;
    border-radius: 5px;
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
    z-index: 60;
    padding: 4px 0;
    max-height: 220px;
    overflow-y: auto;
    display: block;
}

.dark-mode .dropdown-menu {
    background-color: #333;
    color: #fff;
    border: 1px solid #555;
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.3);
}

.dropdown-item {
    padding: 10px 16px;
    cursor: pointer;
    display: flex;
    align-items: center;
    transition: background 0.2s, color 0.2s;
    color: #333;
}

.dropdown-item:hover {
    background-color: #f5f5f5;
}

.dark-mode .dropdown-item {
    color: #fff;
}

.dark-mode .dropdown-item:hover {
    background-color: #444;
}

.filters-container {
    flex-direction: row;
    gap: 16px;
    z-index: 30;
}

@media (max-width: 900px) {
    .skill-grid {
        gap: 12px 16px;
        /* Increase horizontal gap for better separation */
        justify-content: space-evenly;
    }

    .skill-card {
        width: calc(90% - 16px);
        /* Nearly full width on small screens */
        min-width: 0;
        max-width: 100vw;
        margin: 8px auto;
        max-height: 220px;
    }
}

@media (max-width: 600px) {
    .skill-grid {
        gap: 8px 4px;
        /* Reduce horizontal and vertical gap for more width */
        justify-content: space-between;
    }

    .skill-card {
        width: calc(50% - 6px);
        /* Slightly wider cards with smaller gap */
        min-width: 0;
        max-width: 100vw;
        margin: 8px 0;
        max-height: 160px;
        padding: 6px 4px 8px;
    }
}

@media (max-width: 400px) {
    .skill-card {
        width: calc(100% - 16px);
        margin: 8px 0;
        max-height: 140px;
        padding: 4px 1px 6px;
    }
}

@media (max-width: 900px) {

    .grid-scroll-container {
        padding-top: var(--filter-container-height);
        /* Ensure padding is applied */
        height: calc(100vh - 320px);
        /* Ensure height is calculated */
    }

    .filters-container {
        flex-direction: column;
        height: auto;
        gap: 0;
        align-items: center;
        justify-content: center;
    }

    .search-box {
        width: 90vw;
        max-width: 320px;
        margin: 0 auto 10px auto;
        display: block;
    }

    .custom-select {
        width: 90vw;
        max-width: 320px;
        margin: 0 auto 10px auto;
        display: block;

    }
}

@media (max-width: 447px) {
    .skill-name {
        font-size: 1rem;
        padding: 4px 6px;
        min-width: 0;
        max-width: 90vw;
    }
}

.emoji-icon {
    display: inline-block;
    width: 20px;
    height: 20px;
    text-align: center;
    font-size: 20px;
    line-height: 1;
    vertical-align: middle;
    margin-right: 8px;
    margin-left: -4px;
    object-fit: contain;
}

.selected-flex {
    display: flex;
    align-items: center;
    justify-content: flex-start;
    gap: 4px;
}

.skill-link {
    display: block;
    color: inherit;
    text-decoration: none;
    width: 100%;
    height: 100%;
}
.skill-link:focus {
  outline: none;
  box-shadow: none;
}
</style>

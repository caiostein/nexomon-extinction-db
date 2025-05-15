<template>
  <div class="skill-details-wrapper" v-if="skill">
    <div class="skill-details-container">
      <div class="skill-header">
        <img v-if="skill.Image" :src="require(`@/assets/${skill.Image}`)" :alt="skill.Name" class="skill-icon-large" />
        <h1 class="skill-title">{{ skill.Name }}</h1>
      </div>
      <div class="skill-info-grid">
        <div class="skill-info-row"><span class="label">Type:</span>
          <img v-if="skill.Type && skill.Type.image" :src="require(`@/assets/${skill.Type.image}`)" :alt="skill.Type.text" class="type-icon" />
          <span>{{ skill.Type && skill.Type.text }}</span>
        </div>
        <div class="skill-info-row"><span class="label">Power:</span> <span>{{ skill.Power }}</span></div>
        <div class="skill-info-row"><span class="label">Accuracy:</span> <span>{{ skill.Acc }}</span></div>
        <div class="skill-info-row"><span class="label">Stamina:</span> <span>{{ skill.STA }}</span></div>
        <div class="skill-info-row"><span class="label">Speed:</span> <span>{{ skill.Speed }}</span></div>
        <div class="skill-info-row"><span class="label">Crit %:</span> <span>{{ skill['Crit %'] }}</span></div>
        <div class="skill-info-row" v-if="skill.Effect && skill.Effect !== '-'">
          <span class="label">Effect:</span>
          <template v-if="typeof skill.Effect === 'object' && skill.Effect.image">
            <img :src="require(`@/assets/${skill.Effect.image}`)" :alt="skill.Effect.text" class="effect-icon" />
            <span>{{ skill.Effect.text.replace(/\s*\(status\)$/i, '') }}</span>
          </template>
          <template v-else>
            <span>{{ skill.Effect.replace(/\s*\(status\)$/i, '') }}</span>
          </template>
        </div>
      </div>
      <button class="nexo-button nexo-button-danger details-back-btn" @click="$router.back()">Back</button>
    </div>
    <h2 class="learned-by-title">Learned By</h2>
    <div class="nexomon-learners-grid">
      <router-link v-for="nexomon in learners" :key="nexomon.Number" :to="`/nexomon/${nexomon.Number}`" class="nexomon-learner-card">
        <img :src="getThumbnail(nexomon.Name)" :alt="nexomon.Name" class="nexomon-thumb" />
        <div class="nexomon-info">
          <div class="nexomon-number">{{ nexomon.Number }}</div>
          <div class="nexomon-name">{{ nexomon.Name }}</div>
          <div class="nexomon-learn-level">
            Lv. {{ getLearnLevel(nexomon) }}
          </div>
        </div>
      </router-link>
      <div v-if="learners.length === 0" class="no-learners">No Nexomon can learn this skill.</div>
    </div>
  </div>
  <div v-else class="not-found">Skill not found.</div>
</template>

<script>
import skills from '../assets/skill_database.json';
import nexomonData from '../../../python-scripts/assets/nexomon_extinction_database.json';

export default {
  name: 'SkillDetails',
  data() {
    return {
      skill: null,
      learners: [],
    };
  },
  created() {
    const skillName = decodeURIComponent(this.$route.params.skillName);
    this.skill = skills.find(s => s.Name === skillName);
    if (this.skill) {
      // Find all Nexomon that can learn this skill (by Skill Tree)
      this.learners = nexomonData.filter(n =>
        Array.isArray(n['Skill Tree']) &&
        n['Skill Tree'].some(
          entry => entry.Skill && entry.Skill.text === this.skill.Name
        )
      );
    }
  },
  methods: {
    getThumbnail(name) {
      try {
        return require(`@/assets/downloaded_images/${name}-menu.png`);
      } catch {
        try {
          return require(`@/assets/downloaded_images/${name}_(Extinction)-menu.png`);
        } catch {
          try {
            name = name.replace(' (Extinction)', '');
            return require(`@/assets/downloaded_images/${name}.png`);
          } catch {
            try {
              return require(`@/assets/downloaded_images/${name}2.png`);
            } catch {
              return '';
            }
          }
        }
      }
    },
    getLearnLevel(nexomon) {
      if (!this.skill) return '';
      const entry = Array.isArray(nexomon['Skill Tree'])
        ? nexomon['Skill Tree'].find(e => e.Skill && e.Skill.text === this.skill.Name)
        : null;
      return entry && entry.Level ? entry.Level : '?';
    },
  },
};
</script>

<style scoped>
.skill-details-wrapper {
  max-width: 1200px;
  margin: 0 auto;
  padding: 24px;
  text-align: center;
  box-sizing: border-box;
}
.skill-details-container {
  background: #fafdff;
  border-radius: 18px;
  box-shadow: 0 4px 24px rgba(0,0,0,0.10), 0 1.5px 6px rgba(0,0,0,0.04);
  padding: 32px 32px 24px 32px;
  margin: 0 auto 32px auto;
  max-width: 520px;
  min-width: 260px;
  display: flex;
  flex-direction: column;
  align-items: center;
  border: none;
  position: relative;
  z-index: 2;
  transition: background 0.3s, box-shadow 0.3s;
}
.dark-mode .skill-details-container {
  background: #23272b;
  border: none;
  box-shadow: 0 4px 4px rgba(0, 0, 0, 0.10), 0 1.5px 6px rgba(0,0,0,0.04);
}
.skill-header {
  display: flex;
  align-items: center;
  gap: 18px;
  justify-content: center;
  margin-bottom: 18px;
  width: 100%;
}
.skill-icon-large {
  width: 64px;
  height: 64px;
  object-fit: contain;
  border-radius: 12px;
  background: rgba(0,0,0,0.04);
  box-shadow: 0 1px 4px rgba(0,0,0,0.08);
}
.skill-title {
  font-size: 2.1rem;
  font-weight: bold;
  margin: 0;
  padding: 0.2em 0.7em;
  border-radius: 12px;
  background: rgba(0, 0, 0, 0.05);
  color: #2b3a4a;
  box-shadow: 0 1px 4px rgba(0,0,0,0.08);
  letter-spacing: 0.01em;
  transition: background 0.3s, color 0.3s;
}
.dark-mode .skill-title {
  background: rgba(255,255,255,0.04);
  color: #e3f0fa;
  box-shadow: 0 1px 4px rgba(0,0,0,0.08);
}
.skill-info-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px 24px;
  margin-bottom: 28px;
  justify-items: start;
  width: 100%;
}
.skill-info-row {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 1.1rem;
}
.label {
  font-weight: bold;
  min-width: 70px;
}
.type-icon, .effect-icon {
  width: 24px;
  height: 24px;
  object-fit: contain;
  vertical-align: middle;
}
.details-back-btn {
  margin-top: 18px;
  align-self: flex-end;
}
.learned-by-title {
  margin: 30px 0 10px 0;
  font-size: 1.3rem;
  font-weight: bold;
}
.nexomon-learners-grid {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  padding: 0;
  margin: 0 auto;
  max-width: 1200px;
  gap: 2px;
}
.nexomon-learner-card {
  width: calc(16.666% - 8px); /* Reduced margin for tighter layout */
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
}
.nexomon-learner-card:hover {
  background-color: rgba(141, 140, 140, 0.068);
  box-shadow: 0 4px 12px rgba(43,159,204,0.18);
  transform: scale(1.02);
}
.dark-mode .nexomon-learner-card {
  background: #212529;
  border-color: #444;
  color: #fff;
  box-shadow: 0 2px 5px rgba(0,0,0,0.30);
}
.dark-mode .nexomon-learner-card:hover {
  background-color: rgba(255,255,255,0.05);
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
.dark-mode .nexomon-thumb {
  background-color: rgba(255,255,255,0.04);
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
.dark-mode .nexomon-number {
  color: #aaa;
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
.nexomon-learn-level {
  font-size: 0.85em;
  color: #3aa9bd;
  margin-top: 2px;
  font-weight: 500;
}
.dark-mode .nexomon-learn-level {
  color: #7fd6ff;
}
.no-learners {
  width: 100%;
  text-align: center;
  color: #888;
  font-size: 1.1rem;
  margin: 20px 0;
}
.not-found {
  text-align: center;
  color: #c00;
  font-size: 1.3rem;
  margin: 40px 0;
}

@media (max-width: 3840px) {
  .nexomon-learner-card {
    width: calc(16.666% - 8px);
    margin: 4px;
    max-height: 310px;
  }
}

@media (max-width: 1925px) {
  .nexomon-learner-card {
    width: calc(16.666% - 8px);
    margin: 4px;
    max-height: 300px;
  }
}

@media (max-width: 1280px) {
  .nexomon-learner-card {
    width: calc(20% - 6px);
    margin: 3px;
    max-height: 290px;
  }
}

@media (max-width: 1024px) {
  .nexomon-learner-card {
    width: calc(25% - 6px);
    margin: 3px;
    max-height: 280px;
  }
}

@media (max-width: 768px) {
  .nexomon-learners-grid {
    gap: 0;
    justify-content: space-evenly;
  }
  
  .nexomon-learner-card {
    width: calc(33.333% - 4px);
    margin: 2px;
    max-height: 260px;
  }
}

@media (max-width: 600px) {
  .nexomon-learners-grid {
    gap: 0;
    justify-content: space-evenly;
  }
  
  .nexomon-learner-card {
    width: calc(33.333% - 4px); /* 3 per row with minimal spacing */
    margin: 2px;
    max-height: 220px;
  }
  
  .nexomon-thumb {
    width: 56px;
    height: 56px;
  }
  
  .nexomon-name {
    font-size: 0.85em;
  }
  
  .nexomon-number {
    font-size: 0.77em;
  }
}
</style>

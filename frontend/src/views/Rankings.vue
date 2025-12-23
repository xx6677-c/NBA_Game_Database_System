<template>
  <div class="rankings-container">
    <div class="page-header">
      <div class="header-content">
        <h1>数据榜单</h1>
        <p class="subtitle">查看球队战绩排名和球员各项数据榜单</p>
      </div>
    </div>

    <!-- 球队战绩榜 -->
    <div class="section-title">
      <el-icon><Trophy /></el-icon>
      <h2>球队战绩榜</h2>
    </div>

    <div class="standings-grid">
      <!-- 西部排名 -->
      <div class="glass-card standing-card">
        <div class="card-header west-header">
          <h3>西部联盟</h3>
        </div>
        <div class="table-container">
          <table class="glass-table">
            <thead>
              <tr>
                <th>排名</th>
                <th>球队</th>
                <th>胜</th>
                <th>负</th>
                <th>胜率</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="team in westTeams" :key="team.team_id">
                <td class="rank-cell">
                  <span :class="['rank-badge', getRankClass(team.rank)]">{{ team.rank }}</span>
                </td>
                <td class="team-cell">
                  <div class="team-info">
                    <img v-if="team.logo_url" :src="team.logo_url" class="team-logo-sm" alt="Team Logo" @error="handleImageError" />
                    <div v-else class="team-logo-placeholder-sm">{{ team.name ? team.name[0] : '?' }}</div>
                    <span class="team-name">{{ team.name }}</span>
                  </div>
                </td>
                <td>{{ team.wins }}</td>
                <td>{{ team.losses }}</td>
                <td class="win-rate">{{ team.win_rate }}%</td>
              </tr>
              <tr v-if="westTeams.length === 0">
                <td colspan="5" class="empty-cell">暂无数据</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- 东部排名 -->
      <div class="glass-card standing-card">
        <div class="card-header east-header">
          <h3>东部联盟</h3>
        </div>
        <div class="table-container">
          <table class="glass-table">
            <thead>
              <tr>
                <th>排名</th>
                <th>球队</th>
                <th>胜</th>
                <th>负</th>
                <th>胜率</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="team in eastTeams" :key="team.team_id">
                <td class="rank-cell">
                  <span :class="['rank-badge', getRankClass(team.rank)]">{{ team.rank }}</span>
                </td>
                <td class="team-cell">
                  <div class="team-info">
                    <img v-if="team.logo_url" :src="team.logo_url" class="team-logo-sm" alt="Team Logo" @error="handleImageError" />
                    <div v-else class="team-logo-placeholder-sm">{{ team.name ? team.name[0] : '?' }}</div>
                    <span class="team-name">{{ team.name }}</span>
                  </div>
                </td>
                <td>{{ team.wins }}</td>
                <td>{{ team.losses }}</td>
                <td class="win-rate">{{ team.win_rate }}%</td>
              </tr>
              <tr v-if="eastTeams.length === 0">
                <td colspan="5" class="empty-cell">暂无数据</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- 球员数据榜 -->
    <div class="section-title mt-large">
      <el-icon><DataLine /></el-icon>
      <h2>球员数据榜</h2>
      <div class="stat-tabs">
        <button 
          v-for="tab in statTabs" 
          :key="tab.key"
          :class="['glass-btn', { active: currentStat === tab.key }]"
          @click="changeStatTab(tab.key)"
        >
          {{ tab.label }}
        </button>
      </div>
    </div>

    <div class="glass-card player-rankings-card">
      <div class="table-container">
        <table class="glass-table">
          <thead>
            <tr>
              <th>排名</th>
              <th>球员</th>
              <th>球队</th>
              <th>位置</th>
              <th>出场数</th>
              <th>{{ getCurrentStatLabel() }}</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="player in playerRankings" :key="player.player_id">
              <td class="rank-cell">
                <span :class="['rank-badge', getRankClass(player.rank)]">{{ player.rank }}</span>
              </td>
              <td class="player-cell">
                <div class="player-info">
                  <img v-if="player.photo_url" :src="player.photo_url" class="player-avatar-sm" alt="Player Photo" @error="handleImageError" />
                  <div v-else class="player-avatar-placeholder-sm">{{ player.name ? player.name[0] : '?' }}</div>
                  <span class="player-name">{{ player.name }}</span>
                </div>
              </td>
              <td>{{ player.team_name }}</td>
              <td>{{ player.position }}</td>
              <td>{{ player.games_played }}</td>
              <td class="stat-value">{{ getStatValue(player) }}</td>
            </tr>
            <tr v-if="playerRankings.length === 0">
              <td colspan="6" class="empty-cell">暂无数据</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <div v-if="loading" class="loading-overlay">
      <el-icon class="is-loading"><Loading /></el-icon>
    </div>
  </div>
</template>

<script>
import api from '../services/api'
import { Trophy, DataLine, Loading } from '@element-plus/icons-vue'

export default {
  name: 'Rankings',
  components: {
    Trophy,
    DataLine,
    Loading
  },
  data() {
    return {
      loading: false,
      westTeams: [],
      eastTeams: [],
      playerRankings: [],
      currentStat: 'points',
      statTabs: [
        { key: 'points', label: '得分' },
        { key: 'rebounds', label: '篮板' },
        { key: 'assists', label: '助攻' },
        { key: 'steals', label: '抢断' },
        { key: 'blocks', label: '盖帽' },
        { key: 'minutes', label: '上场时间' }
      ]
    }
  },
  mounted() {
    this.fetchTeamStandings()
    this.fetchPlayerRankings()
  },
  methods: {
    async fetchTeamStandings() {
      this.loading = true
      try {
        const response = await api.get('/rankings/teams')
        this.westTeams = response.west
        this.eastTeams = response.east
      } catch (error) {
        console.error('获取球队战绩失败:', error)
      } finally {
        this.loading = false
      }
    },
    async fetchPlayerRankings() {
      this.loading = true
      try {
        const response = await api.get(`/rankings/players?stat=${this.currentStat}&limit=20`)
        this.playerRankings = response.players
      } catch (error) {
        console.error('获取球员榜单失败:', error)
      } finally {
        this.loading = false
      }
    },
    changeStatTab(stat) {
      this.currentStat = stat
      this.fetchPlayerRankings()
    },
    getRankClass(rank) {
      if (rank === 1) return 'rank-1'
      if (rank === 2) return 'rank-2'
      if (rank === 3) return 'rank-3'
      return ''
    },
    getCurrentStatLabel() {
      const tab = this.statTabs.find(t => t.key === this.currentStat)
      return tab ? `场均${tab.label}` : '数据'
    },
    getStatValue(player) {
      const map = {
        'points': 'avg_points',
        'rebounds': 'avg_rebounds',
        'assists': 'avg_assists',
        'steals': 'avg_steals',
        'blocks': 'avg_blocks',
        'minutes': 'avg_minutes'
      }
      const val = player[map[this.currentStat]]
      return val !== undefined && val !== null ? val : 0
    },
    handleImageError(e) {
      e.target.style.display = 'none'
    }
  }
}
</script>

<style scoped>
.rankings-container {
  padding: 80px 24px 40px;
  max-width: 1200px;
  margin: 0 auto;
  min-height: 100vh;
}

.page-header {
  margin-bottom: 32px;
}

.header-content h1 {
  font-size: 2.5rem;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: var(--spacing-xs);
}

.subtitle {
  color: var(--color-text-secondary);
  margin: 0;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 24px;
  color: var(--color-text-primary);
}

.section-title h2 {
  margin: 0;
  font-size: 24px;
}

.mt-large {
  margin-top: 48px;
}

.standings-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
}

@media (max-width: 768px) {
  .standings-grid {
    grid-template-columns: 1fr;
  }
}

.standing-card {
  padding: 0;
  overflow: hidden;
}

.card-header {
  padding: 16px 24px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.card-header h3 {
  margin: 0;
  font-size: 18px;
}

.west-header {
  background: linear-gradient(90deg, rgba(237, 23, 76, 0.2), transparent);
  border-left: 4px solid #ed174c;
}

.east-header {
  background: linear-gradient(90deg, rgba(0, 107, 182, 0.2), transparent);
  border-left: 4px solid #006bb6;
}

.table-container {
  overflow-x: auto;
}

.glass-table {
  width: 100%;
  border-collapse: collapse;
  color: var(--color-text-primary);
}

.glass-table th,
.glass-table td {
  padding: 12px 16px;
  text-align: left;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}

.glass-table th {
  font-weight: 600;
  color: var(--color-text-secondary);
  font-size: 14px;
}

.rank-cell {
  width: 60px;
  text-align: center;
}

.rank-badge {
  display: inline-block;
  width: 24px;
  height: 24px;
  line-height: 24px;
  text-align: center;
  border-radius: 50%;
  font-size: 12px;
  font-weight: bold;
  background: rgba(255, 255, 255, 0.1);
}

.rank-1 {
  background: linear-gradient(135deg, #ffd700, #ffa500);
  color: #000;
  box-shadow: 0 0 10px rgba(255, 215, 0, 0.5);
}

.rank-2 {
  background: linear-gradient(135deg, #e0e0e0, #bdbdbd);
  color: #000;
}

.rank-3 {
  background: linear-gradient(135deg, #cd7f32, #a0522d);
  color: #000;
}

.team-cell {
  font-weight: 500;
}

.team-info {
  display: flex;
  align-items: center;
  gap: 10px;
}

.team-logo-sm {
  width: 28px;
  height: 28px;
  object-fit: contain;
  border-radius: 4px;
}

.team-logo-placeholder-sm {
  width: 28px;
  height: 28px;
  border-radius: 4px;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.15), rgba(255, 255, 255, 0.05));
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 14px;
  color: var(--color-text-secondary);
}

.team-name {
  font-weight: 500;
}

.player-cell {
  font-weight: 500;
}

.player-info {
  display: flex;
  align-items: center;
  gap: 10px;
}

.player-avatar-sm {
  width: 32px;
  height: 32px;
  object-fit: cover;
  border-radius: 50%;
  border: 2px solid rgba(255, 255, 255, 0.1);
}

.player-avatar-placeholder-sm {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.15), rgba(255, 255, 255, 0.05));
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 14px;
  color: var(--color-text-secondary);
  border: 2px solid rgba(255, 255, 255, 0.1);
}

.player-name {
  font-weight: 600;
  color: var(--color-text-primary);
}

.win-rate {
  font-family: monospace;
  color: var(--color-accent);
}

.stat-tabs {
  margin-left: auto;
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.stat-tabs .glass-btn {
  padding: 6px 16px;
  font-size: 14px;
  border-radius: 20px;
}

.stat-tabs .glass-btn.active {
  background: var(--color-accent);
  color: #000;
  border-color: var(--color-accent);
}

.player-rankings-card {
  padding: 0;
}

.stat-value {
  font-weight: 700;
  color: var(--color-accent);
  font-size: 16px;
}

.empty-cell {
  text-align: center;
  padding: 32px;
  color: var(--color-text-secondary);
}

.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 2000;
  color: var(--color-accent);
  font-size: 32px;
}
</style>

<template>
  <div class="games-container">
    <div class="page-header">
      <div class="header-content">
        <h1>比赛管理</h1>
        <p class="subtitle">查看和管理NBA比赛数据</p>
      </div>
      
      <div class="header-actions">
        <div class="compact-filters glass-card">
          <div class="filter-item">
            <input v-model="filters.date_from" type="date" class="glass-input sm-input" placeholder="开始">
          </div>
          <div class="filter-item">
            <input v-model="filters.date_to" type="date" class="glass-input sm-input" placeholder="结束">
          </div>
          <div class="filter-item">
            <el-icon><Trophy /></el-icon>
            <select v-model="filters.team_id" class="glass-select sm-select">
              <option value="">所有球队</option>
              <option v-for="team in teams" :key="team.team_id" :value="team.team_id">
                {{ team.name }}
              </option>
            </select>
          </div>
          <button @click="applyFilters" class="glass-btn sm-btn primary-btn icon-only" title="筛选">
            <el-icon><Search /></el-icon>
          </button>
          <button @click="resetFilters" class="glass-btn sm-btn icon-only" title="重置">
            <el-icon><Refresh /></el-icon>
          </button>
        </div>

        <button v-if="isAdmin" @click="openCreateModal" class="glass-btn primary-btn">
          <el-icon><Plus /></el-icon> 新建比赛
        </button>
      </div>
    </div>

    <div class="games-list">
      <div v-for="game in games" :key="game.game_id" class="glass-card game-card">
        <div class="card-header">
          <div class="season-badge">{{ game.season }} 赛季</div>
          <span class="status-badge" :class="game.status === '已结束' ? 'finished' : 'upcoming'">
            <el-icon><Timer /></el-icon>
            {{ game.status === '已结束' ? '已结束' : '未开始' }}
          </span>
        </div>
        
        <div class="game-matchup">
          <div class="team home">
            <img v-if="game.home_logo_url" :src="game.home_logo_url" class="team-logo-sm" alt="Home Logo" />
            <span class="team-name">{{ game.home_team }}</span>
            <span class="score">{{ game.home_score !== null ? game.home_score : '-' }}</span>
          </div>
          <div class="vs-divider">VS</div>
          <div class="team away">
            <span class="score">{{ game.away_score !== null ? game.away_score : '-' }}</span>
            <span class="team-name">{{ game.away_team }}</span>
            <img v-if="game.away_logo_url" :src="game.away_logo_url" class="team-logo-sm" alt="Away Logo" />
          </div>
        </div>
        
        <div class="game-meta">
          <div class="meta-item">
            <el-icon><Calendar /></el-icon>
            <span>{{ game.date }}</span>
          </div>
          <div class="meta-item">
            <el-icon><Location /></el-icon>
            <span>{{ game.venue }}</span>
          </div>
          <div class="meta-item" v-if="game.winner_team">
            <el-icon><Trophy /></el-icon>
            <span>胜者: {{ game.winner_team }}</span>
          </div>
        </div>

        <div class="card-actions">
          <router-link :to="`/posts?game_id=${game.game_id}`" class="glass-btn sm-btn">
            <el-icon><ChatDotRound /></el-icon> 讨论
          </router-link>
          <button @click="viewGameDetails(game)" class="glass-btn sm-btn secondary">
            <el-icon><View /></el-icon> 详情
          </button>
          <div v-if="isAdmin" class="admin-actions">
            <button @click="openEditModal(game)" class="glass-btn icon-only warning">
              <el-icon><Edit /></el-icon>
            </button>
            <button @click="deleteGame(game.game_id)" class="glass-btn icon-only danger">
              <el-icon><Delete /></el-icon>
            </button>
          </div>
        </div>
      </div>
    </div>

    <div v-if="loading" class="loading-state">
      <el-icon class="is-loading"><Loading /></el-icon>
      <p>加载中...</p>
    </div>

    <div v-if="!loading && games.length === 0" class="empty-state">
      <el-icon><Basketball /></el-icon>
      <p>暂无比赛数据</p>
    </div>

    <!-- Modal -->
    <div v-if="showModal" class="modal-overlay glass-overlay">
      <div class="glass-card modal-content">
        <div class="modal-header">
          <h2>{{ isEditing ? '编辑比赛' : '新建比赛' }}</h2>
          <button @click="closeModal" class="close-btn"><el-icon><Close /></el-icon></button>
        </div>
        
        <form @submit.prevent="saveGame" class="glass-form">
          <div class="form-row">
            <div class="form-group">
              <label>赛季</label>
              <div class="input-wrapper">
                <el-icon><Trophy /></el-icon>
                <input v-model="gameForm.season" type="text" class="glass-input" required placeholder="例如: 2023-2024" readonly>
              </div>
            </div>
            <div class="form-group">
              <label>比赛时间</label>
              <div class="input-wrapper">
                <el-icon><Calendar /></el-icon>
                <input v-model="gameForm.date" type="datetime-local" class="glass-input" required>
              </div>
            </div>
          </div>
          
          <div class="form-row">
            <div class="form-group">
              <label>主队</label>
              <div class="input-wrapper">
                <el-icon><House /></el-icon>
                <input v-if="isEditing" :value="gameForm.home_team" type="text" class="glass-input" readonly>
                <select v-else v-model="gameForm.home_team_id" class="glass-select" required @change="onHomeTeamChange">
                  <option value="">选择主队</option>
                  <option v-for="team in teams" :key="team.team_id" :value="team.team_id">
                    {{ team.name }}
                  </option>
                </select>
              </div>
            </div>
            <div class="form-group">
              <label>客队</label>
              <div class="input-wrapper">
                <el-icon><Guide /></el-icon>
                <input v-if="isEditing" :value="gameForm.away_team" type="text" class="glass-input" readonly>
                <select v-else v-model="gameForm.away_team_id" class="glass-select" required>
                  <option value="">选择客队</option>
                  <option v-for="team in teams" :key="team.team_id" :value="team.team_id">
                    {{ team.name }}
                  </option>
                </select>
              </div>
            </div>
          </div>
          
          <div class="form-row">
            <div class="form-group">
              <label>状态</label>
              <div class="input-wrapper">
                <el-icon><Timer /></el-icon>
                <select v-model="gameForm.status" class="glass-select" @change="onStatusChange">
                  <option value="未开始">未开始</option>
                  <option value="已结束">已结束</option>
                </select>
              </div>
            </div>
            <div class="form-group">
              <label>场馆</label>
              <div class="input-wrapper">
                <el-icon><Location /></el-icon>
                <input v-model="gameForm.venue" type="text" class="glass-input" placeholder="比赛场馆" readonly>
              </div>
            </div>
          </div>
          
          <div v-if="gameForm.status === '已结束'" class="score-section glass-card inner-card">
            <h3>比赛比分</h3>
            <div class="form-row">
              <div class="form-group">
                <label>主队得分</label>
                <input v-model.number="gameForm.home_score" type="number" min="0" step="1" class="glass-input" required>
              </div>
              <div class="form-group">
                <label>客队得分</label>
                <input v-model.number="gameForm.away_score" type="number" min="0" step="1" class="glass-input" required>
              </div>
            </div>
            
            <div class="player-stats-section">
              <div class="section-header">
                <h3>球员比赛数据</h3>
                <button type="button" @click="loadPlayerTemplate" class="glass-btn sm-btn">
                  <el-icon><Download /></el-icon> 加载模板
                </button>
              </div>
              
              <div v-if="playerTemplate.length > 0" class="player-template custom-scrollbar">
                <div v-for="player in playerTemplate" :key="player.player_id" class="player-stat-row">
                  <div class="player-info">
                    <strong>{{ player.name }}</strong>
                    <span class="player-sub-info">({{ player.team_name }} #{{ player.jersey_number }})</span>
                  </div>
                  <div class="stat-inputs">
                    <div class="stat-field">
                      <label>时间</label>
                      <input v-model.number="playerStats[player.player_id].上场时间" type="number" min="0" step="1" placeholder="0" class="glass-input sm-input">
                    </div>
                    <div class="stat-field">
                      <label>得分</label>
                      <input v-model.number="playerStats[player.player_id].得分" type="number" min="0" step="1" placeholder="0" class="glass-input sm-input">
                    </div>
                    <div class="stat-field">
                      <label>篮板</label>
                      <input v-model.number="playerStats[player.player_id].篮板" type="number" min="0" step="1" placeholder="0" class="glass-input sm-input">
                    </div>
                    <div class="stat-field">
                      <label>助攻</label>
                      <input v-model.number="playerStats[player.player_id].助攻" type="number" min="0" step="1" placeholder="0" class="glass-input sm-input">
                    </div>
                    <div class="stat-field">
                      <label>抢断</label>
                      <input v-model.number="playerStats[player.player_id].抢断" type="number" min="0" step="1" placeholder="0" class="glass-input sm-input">
                    </div>
                    <div class="stat-field">
                      <label>盖帽</label>
                      <input v-model.number="playerStats[player.player_id].盖帽" type="number" min="0" step="1" placeholder="0" class="glass-input sm-input">
                    </div>
                    <div class="stat-field">
                      <label>失误</label>
                      <input v-model.number="playerStats[player.player_id].失误" type="number" min="0" step="1" placeholder="0" class="glass-input sm-input">
                    </div>
                    <div class="stat-field">
                      <label>犯规</label>
                      <input v-model.number="playerStats[player.player_id].犯规" type="number" min="0" step="1" placeholder="0" class="glass-input sm-input">
                    </div>
                    <div class="stat-field">
                      <label>正负值</label>
                      <input v-model.number="playerStats[player.player_id].正负值" type="number" step="1" placeholder="0" class="glass-input sm-input">
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <div class="form-actions">
            <button type="button" @click="closeModal" class="glass-btn">取消</button>
            <button type="submit" class="glass-btn primary-btn" :disabled="submitting">
              {{ submitting ? '保存中...' : (isEditing ? '更新' : '创建') }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import api from '../services/api'
import { 
  Calendar, Location, Trophy, ChatDotRound, View, Edit, Delete, 
  Plus, Search, Refresh, Timer, Close, Download, House, Guide, Loading, Basketball 
} from '@element-plus/icons-vue'

export default {
  name: 'Games',
  components: {
    Calendar, Location, Trophy, ChatDotRound, View, Edit, Delete, 
    Plus, Search, Refresh, Timer, Close, Download, House, Guide, Loading, Basketball
  },
  data() {
    return {
      games: [],
      teams: [],
      filters: {
        date_from: '',
        date_to: '',
        team_id: ''
      },
      loading: false,
      showModal: false,
      isEditing: false,
      submitting: false,
      playerTemplate: [],
      playerStats: {},
      gameForm: {
        season: '',
        date: '',
        home_team_id: '',
        away_team_id: '',
        status: '未开始',
        home_score: null,
        away_score: null,
        venue: '',
        player_data: []
      },
      currentUser: null
    }
  },
  computed: {
    isAdmin() {
      return this.currentUser && this.currentUser.role === 'admin'
    }
  },
  async mounted() {
    await this.getCurrentUser()
    
    // 从URL参数获取team_id
    const teamId = this.$route.query.team_id
    if (teamId) {
      this.filters.team_id = parseInt(teamId)
    }
    
    await Promise.all([this.loadTeams(), this.loadGames()])
  },
  methods: {
    async getCurrentUser() {
      try {
        this.currentUser = JSON.parse(localStorage.getItem('user') || '{}')
      } catch (error) {
        console.error('获取用户信息失败:', error)
      }
    },
    async loadTeams() {
      try {
        this.teams = await api.getTeams()
      } catch (error) {
        console.error('加载球队数据失败:', error)
      }
    },
    async loadGames() {
      this.loading = true
      try {
        // 构建查询参数
        const queryParams = {}
        if (this.filters.date_from) queryParams.date_from = this.filters.date_from
        if (this.filters.date_to) queryParams.date_to = this.filters.date_to
        if (this.filters.team_id) queryParams.team_id = this.filters.team_id
        
        this.games = await api.getGames(queryParams)
      } catch (error) {
        console.error('加载比赛数据失败:', error)
        // alert('加载比赛数据失败')
      } finally {
        this.loading = false
      }
    },
    applyFilters() {
      this.loadGames()
    },
    resetFilters() {
      this.filters = {
        date_from: '',
        date_to: '',
        team_id: ''
      }
      this.loadGames()
    },
    viewGameDetails(game) {
      this.$router.push(`/games/${game.game_id}`)
    },
    openCreateModal() {
      this.isEditing = false
      this.resetForm()
      this.showModal = true
    },
    openEditModal(game) {
      this.isEditing = true
      this.gameForm = {
        ...game,
        date: game.date.replace(' ', 'T'), // 转换为datetime-local格式
        player_data: []
      }
      this.showModal = true
    },
    closeModal() {
      this.showModal = false
      this.resetForm()
    },
    resetForm() {
      this.gameForm = {
        season: '2025-2026',
        date: '',
        home_team_id: '',
        away_team_id: '',
        status: '未开始',
        home_score: null,
        away_score: null,
        venue: '',
        player_data: []
      }
      this.playerTemplate = []
      this.playerStats = {}
    },
    onStatusChange() {
      if (this.gameForm.status === '未开始') {
        this.gameForm.home_score = null
        this.gameForm.away_score = null
        this.playerTemplate = []
        this.playerStats = {}
      }
    },
    onHomeTeamChange() {
      const homeTeam = this.teams.find(t => t.team_id === this.gameForm.home_team_id)
      if (homeTeam) {
        this.gameForm.venue = homeTeam.arena
      }
    },
    async loadPlayerTemplate() {
      if (!this.gameForm.home_team_id || !this.gameForm.away_team_id) {
        alert('请先选择主队和客队')
        return
      }
      
      try {
        // 对于新建比赛，我们直接根据球队ID获取球员
        const allPlayers = await api.getPlayers()
        const gamePlayers = allPlayers.filter(player => 
          player.current_team_id === this.gameForm.home_team_id || 
          player.current_team_id === this.gameForm.away_team_id
        )
        
        this.playerTemplate = gamePlayers.map(player => ({
          ...player,
          default_stats: {
            上场时间: 0,
            得分: 0,
            篮板: 0,
            助攻: 0,
            抢断: 0,
            盖帽: 0,
            失误: 0,
            犯规: 0,
            正负值: 0
          }
        }))
        
        // 初始化球员统计数据
        this.playerStats = {}
        this.playerTemplate.forEach(player => {
          this.playerStats[player.player_id] = { ...player.default_stats }
        })
        
      } catch (error) {
        console.error('加载球员模板失败:', error)
        alert('加载球员模板失败')
      }
    },
    async saveGame() {
      if (this.gameForm.home_team_id === this.gameForm.away_team_id) {
        alert('主队和客队不能相同')
        return
      }
      
      this.submitting = true
      
      try {
        // 转换日期格式为MySQL格式
        let date = this.gameForm.date
        if (date && date.includes('T')) {
          date = date.replace('T', ' ')
        }
        
        const gameData = {
          ...this.gameForm,
          date: date
        }
        
        // 处理球员数据
        if (this.gameForm.status === '已结束' && Object.keys(this.playerStats).length > 0) {
          gameData.player_data = Object.entries(this.playerStats).map(([playerId, stats]) => ({
            player_id: parseInt(playerId),
            ...stats
          }))
        }
        
        // 如果比赛未开始，移除比分和球员数据
        if (this.gameForm.status === '未开始') {
          delete gameData.player_data
        }
        
        console.log('发送的比赛数据:', gameData)
        
        if (this.isEditing) {
          await api.updateGame(this.gameForm.game_id, gameData)
          // alert('比赛更新成功')
        } else {
          await api.createGame(gameData)
          // alert('比赛创建成功')
        }
        
        this.closeModal()
        this.loadGames()
        
      } catch (error) {
        console.error('保存比赛失败:', error)
        alert('保存比赛失败: ' + (error.message || '未知错误'))
      } finally {
        this.submitting = false
      }
    },
    async deleteGame(gameId) {
      if (!confirm('确定要删除这场比赛吗？此操作不可恢复。')) {
        return
      }
      
      try {
        await api.deleteGame(gameId)
        // alert('比赛删除成功')
        this.loadGames()
      } catch (error) {
        console.error('删除比赛失败:', error)
        alert('删除比赛失败: ' + (error.message || '未知错误'))
      }
    }
  }
}
</script>

<style scoped>
.games-container {
  padding: var(--spacing-lg);
  max-width: 1400px;
  margin: 0 auto;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-xl);
}

.header-content h1 {
  font-size: 2.5rem;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: var(--spacing-xs);
  text-shadow: none;
}

.subtitle {
  color: var(--text-secondary);
  font-size: 1.1rem;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: var(--spacing-lg);
}

.compact-filters {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  padding: 6px 12px;
  border-radius: 8px;
}

.filter-item {
  position: relative;
  display: flex;
  align-items: center;
}

.filter-item .el-icon {
  position: absolute;
  left: 8px;
  color: var(--text-secondary);
  font-size: 0.9rem;
  z-index: 1;
}

.sm-input, .sm-select {
  padding: 0 8px 0 32px;
  font-size: 0.9rem;
  height: 38px;
  line-height: 38px;
  width: 160px;
}

.sm-select {
  width: auto;
  min-width: 140px;
}

.games-list {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
}

.game-card {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
  transition: all 0.3s ease;
  padding: var(--spacing-sm) var(--spacing-md);
  gap: var(--spacing-md);
}

.card-header {
  margin-bottom: 0;
  padding-bottom: 0;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  min-width: 120px;
}

.game-matchup {
  margin-bottom: 0;
  padding: 0;
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: var(--spacing-md);
}

.team {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  flex: 1;
}

.team.home {
  justify-content: flex-end;
  text-align: right;
}

.team.away {
  justify-content: flex-start;
  text-align: left;
}

.team-name {
  font-size: 1.1rem;
  font-weight: 600;
}

.team-logo-sm {
  width: 32px;
  height: 32px;
  object-fit: contain;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.score {
  font-size: 1.5rem;
  min-width: 40px;
  text-align: center;
  font-weight: 700;
  color: var(--accent-color);
}

.vs-divider {
  margin: 0 var(--spacing-sm);
  font-size: 0.9rem;
  color: var(--text-secondary);
  font-weight: bold;
}

.game-meta {
  margin-bottom: 0;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 4px;
  min-width: 160px;
  font-size: 0.85rem;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 6px;
  color: var(--text-secondary);
}

.card-actions {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
}

.glass-btn.sm-btn {
  padding: 0.3rem 0.8rem;
  font-size: 0.85rem;
}

.glass-btn.icon-only {
  padding: 0.4rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.glass-btn.warning {
  color: #f59e0b;
  border-color: rgba(245, 158, 11, 0.3);
}

.glass-btn.warning:hover {
  background: rgba(245, 158, 11, 0.1);
}

.glass-btn.danger {
  color: #ef4444;
  border-color: rgba(239, 68, 68, 0.3);
}

.glass-btn.danger:hover {
  background: rgba(239, 68, 68, 0.1);
}

/* Loading & Empty States */
.loading-state, .empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem;
  color: var(--text-secondary);
  gap: var(--spacing-md);
}

.loading-state .el-icon, .empty-state .el-icon {
  font-size: 3rem;
  color: var(--accent-color);
  opacity: 0.8;
}

/* Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  width: 95%;
  max-width: 900px;
  max-height: 90vh;
  overflow-y: auto;
  padding: var(--spacing-xl);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-xl);
  padding-bottom: var(--spacing-md);
  border-bottom: 1px solid var(--glass-border);
}

.modal-header h2 {
  font-size: 1.5rem;
  color: var(--text-primary);
  margin: 0;
}

.close-btn {
  background: none;
  border: none;
  cursor: pointer;
  color: var(--text-secondary);
  font-size: 1.2rem;
  padding: 4px;
  border-radius: 50%;
  transition: all 0.3s ease;
}

.close-btn:hover {
  background: rgba(0,0,0,0.05);
  color: var(--text-primary);
}

.glass-form .form-group {
  margin-bottom: var(--spacing-lg);
}

.glass-form .form-row {
  display: flex;
  gap: var(--spacing-lg);
  margin-bottom: var(--spacing-lg);
}

.glass-form .form-group {
  flex: 1;
}

.glass-form label {
  display: block;
  margin-bottom: var(--spacing-xs);
  color: var(--text-primary);
  font-weight: 500;
}

.input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.input-wrapper .el-icon {
  position: absolute;
  left: 12px;
  color: var(--text-secondary);
  z-index: 1;
}

.glass-input, .glass-select {
  width: 100%;
  padding: 10px 12px 10px 36px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid var(--glass-border);
  border-radius: 8px;
  font-size: 1rem;
  color: var(--text-primary);
  transition: all 0.3s ease;
}

.glass-input:focus, .glass-select:focus {
  outline: none;
  background: rgba(255, 255, 255, 0.1);
  border-color: var(--accent-color);
  box-shadow: 0 0 0 3px rgba(212, 175, 55, 0.1);
}

.score-section {
  margin-top: var(--spacing-xl);
  padding: var(--spacing-lg);
}

.score-section h3 {
  margin-bottom: var(--spacing-lg);
  color: var(--text-primary);
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-md);
}

.player-template {
  max-height: 400px;
  overflow-y: auto;
  padding-right: var(--spacing-sm);
}

.player-stat-row {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-sm);
  padding: var(--spacing-md);
  border-bottom: 1px solid var(--glass-border);
}

.player-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.player-sub-info {
  color: var(--text-secondary);
  font-size: 0.9rem;
}

.stat-inputs {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(80px, 1fr));
  gap: var(--spacing-sm);
}

.stat-field {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.stat-field label {
  font-size: 0.85rem;
  color: var(--text-primary);
  margin: 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.glass-input.sm-input {
  padding: 6px 8px;
  font-size: 0.9rem;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: var(--spacing-md);
  margin-top: var(--spacing-xl);
}

@media (max-width: 768px) {
  .page-header {
    flex-direction: column;
    gap: var(--spacing-md);
    text-align: center;
  }
  
  .compact-filters {
    flex-direction: column;
    align-items: stretch;
    width: 100%;
  }

  .game-card {
    flex-direction: column;
    align-items: stretch;
  }
  
  .game-matchup {
    flex-direction: column;
    gap: var(--spacing-md);
  }
  
  .vs-divider {
    margin: var(--spacing-sm) 0;
  }
  
  .game-meta {
    flex-direction: column;
    align-items: center;
    gap: var(--spacing-sm);
    width: 100%;
  }
  
  .card-actions {
    flex-wrap: wrap;
    justify-content: center;
    width: 100%;
  }
  
  .glass-form .form-row {
    flex-direction: column;
    gap: var(--spacing-md);
  }
}
</style>

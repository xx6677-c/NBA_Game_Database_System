<template>
  <div class="teams-container">
    <div class="page-header">
      <div class="header-content">
        <h1>球队管理</h1>
        <p class="subtitle">查看和管理NBA球队信息</p>
      </div>
      <button v-if="userRole === 'admin'" @click="showCreateTeam = true" class="glass-btn primary-btn">
        <el-icon><Plus /></el-icon> 新建球队
      </button>
    </div>

    <div class="teams-grid">
      <div v-for="team in teams" :key="team.team_id" class="glass-card team-card">
        <div class="card-header">
          <div class="team-title">
            <h3>{{ team.name }}</h3>
            <span class="conference-badge" :class="team.conference === '东部' ? 'east' : 'west'">
              {{ team.conference }}
            </span>
          </div>
        </div>
        
        <div class="card-content">
          <div class="info-item">
            <el-icon><Location /></el-icon>
            <span>{{ team.city }}</span>
          </div>
          <div class="info-item">
            <el-icon><House /></el-icon>
            <span>{{ team.arena }}</span>
          </div>
          <div class="info-item">
            <el-icon><Calendar /></el-icon>
            <span>{{ team.founded_year }}</span>
          </div>
        </div>

        <div class="card-actions">
          <router-link :to="`/players?team_id=${team.team_id}`" class="glass-btn sm-btn">
            <el-icon><User /></el-icon> 球员
          </router-link>
          <router-link :to="`/games?team_id=${team.team_id}`" class="glass-btn sm-btn">
            <el-icon><Trophy /></el-icon> 比赛
          </router-link>
          <div v-if="userRole === 'admin'" class="admin-actions">
            <button @click="editTeam(team)" class="glass-btn icon-only warning">
              <el-icon><Edit /></el-icon>
            </button>
            <button @click="deleteTeam(team.team_id)" class="glass-btn icon-only danger">
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

    <div v-if="!loading && teams.length === 0" class="empty-state">
      <el-icon><Basketball /></el-icon>
      <p>暂无球队数据</p>
    </div>

    <!-- Modals -->
    <div v-if="showCreateTeam || showEditTeam" class="modal-overlay glass-overlay">
      <div class="glass-card modal-content">
        <div class="modal-header">
          <h3>{{ showCreateTeam ? '新建球队' : '编辑球队' }}</h3>
          <button @click="closeModal" class="close-btn"><el-icon><Close /></el-icon></button>
        </div>
        <form @submit.prevent="showCreateTeam ? handleCreateTeam() : handleUpdateTeam()" class="glass-form">
          <div class="form-group">
            <label>球队名称</label>
            <div class="input-wrapper">
              <el-icon><Trophy /></el-icon>
              <input v-model="teamForm.name" type="text" required class="glass-input" placeholder="输入球队名称">
            </div>
          </div>
          <div class="form-group">
            <label>所在城市</label>
            <div class="input-wrapper">
              <el-icon><Location /></el-icon>
              <input v-model="teamForm.city" type="text" required class="glass-input" placeholder="输入城市">
            </div>
          </div>
          <div class="form-group">
            <label>主场场馆</label>
            <div class="input-wrapper">
              <el-icon><House /></el-icon>
              <input v-model="teamForm.arena" type="text" required class="glass-input" placeholder="输入场馆">
            </div>
          </div>
          <div class="form-group">
            <label>分区</label>
            <div class="input-wrapper">
              <el-icon><Guide /></el-icon>
              <select v-model="teamForm.conference" required class="glass-select">
                <option value="">请选择分区</option>
                <option value="东部">东部</option>
                <option value="西部">西部</option>
              </select>
            </div>
          </div>
          <div class="form-group">
            <label>成立年份</label>
            <div class="input-wrapper">
              <el-icon><Calendar /></el-icon>
              <input v-model="teamForm.founded_year" type="number" min="1900" :max="new Date().getFullYear()" required class="glass-input">
            </div>
          </div>
          <div class="form-actions">
            <button type="button" @click="closeModal" class="glass-btn">取消</button>
            <button type="submit" :disabled="teamLoading" class="glass-btn primary-btn">
              {{ teamLoading ? '处理中...' : (showCreateTeam ? '创建' : '保存') }}
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
  Plus, Edit, Delete, User, Trophy, Location, 
  House, Calendar, Loading, Basketball, Close, Guide 
} from '@element-plus/icons-vue'

export default {
  name: 'Teams',
  components: {
    Plus, Edit, Delete, User, Trophy, Location, 
    House, Calendar, Loading, Basketball, Close, Guide
  },
  data() {
    return {
      teams: [],
      loading: false,
      teamLoading: false,
      showCreateTeam: false,
      showEditTeam: false,
      teamForm: {
        team_id: null,
        name: '',
        city: '',
        arena: '',
        conference: '',
        founded_year: new Date().getFullYear()
      },
      userRole: 'user'
    }
  },
  async mounted() {
    await this.loadTeams()
    await this.getUserRole()
  },
  methods: {
    async loadTeams() {
      this.loading = true
      try {
        this.teams = await api.getTeams()
      } catch (error) {
        console.error('加载球队数据失败:', error)
      } finally {
        this.loading = false
      }
    },
    
    async getUserRole() {
      try {
        const userData = JSON.parse(localStorage.getItem('user') || '{}')
        this.userRole = userData.role || 'user'
      } catch (error) {
        console.error('获取用户角色失败:', error)
        this.userRole = 'user'
      }
    },
    
    editTeam(team) {
      this.teamForm = {
        team_id: team.team_id,
        name: team.name,
        city: team.city,
        arena: team.arena,
        conference: team.conference,
        founded_year: team.founded_year
      }
      this.showEditTeam = true
    },
    
    async deleteTeam(teamId) {
      if (!confirm('确定要删除这个球队吗？此操作不可撤销！')) {
        return
      }
      
      try {
        await api.deleteTeam(teamId)
        await this.loadTeams()
      } catch (error) {
        console.error('删除球队失败:', error)
        alert('删除球队失败: ' + error.message)
      }
    },
    
    async handleCreateTeam() {
      this.teamLoading = true
      try {
        await api.createTeam(this.teamForm)
        this.closeModal()
        await this.loadTeams()
      } catch (error) {
        console.error('创建球队失败:', error)
        alert('创建球队失败: ' + error.message)
      } finally {
        this.teamLoading = false
      }
    },
    
    async handleUpdateTeam() {
      this.teamLoading = true
      try {
        await api.updateTeam(this.teamForm.team_id, this.teamForm)
        this.closeModal()
        await this.loadTeams()
      } catch (error) {
        console.error('更新球队失败:', error)
        alert('更新球队失败: ' + error.message)
      } finally {
        this.teamLoading = false
      }
    },
    
    closeModal() {
      this.showCreateTeam = false
      this.showEditTeam = false
      this.teamForm = {
        team_id: null,
        name: '',
        city: '',
        arena: '',
        conference: '',
        founded_year: new Date().getFullYear()
      }
    }
  }
}
</script>

<style scoped>
.teams-container {
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

.teams-grid {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
}

.team-card {
  display: flex;
  flex-direction: row;
  align-items: center;
  padding: var(--spacing-md) var(--spacing-lg);
  gap: var(--spacing-lg);
  transition: all 0.3s ease;
}

.team-card:hover {
  transform: translateX(5px);
  box-shadow: var(--glass-shadow-hover);
  background: rgba(255, 255, 255, 0.08);
}

.card-header {
  border-bottom: none;
  padding-bottom: 0;
  margin-bottom: 0;
  flex: 0 0 250px; /* Fixed width for alignment */
  display: flex;
  align-items: center;
}

.team-title {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
}

.team-title h3 {
  font-size: 1.6rem;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0;
  white-space: nowrap;
}

.conference-badge {
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 0.95rem;
  font-weight: 600;
}

.conference-badge.east {
  background: rgba(25, 118, 210, 0.1);
  color: #1976d2;
  border: 1px solid rgba(25, 118, 210, 0.2);
}

.conference-badge.west {
  background: rgba(194, 24, 91, 0.1);
  color: #c2185b;
  border: 1px solid rgba(194, 24, 91, 0.2);
}

.card-content {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: flex-start;
  gap: var(--spacing-xl);
  margin-bottom: 0;
}

.info-item {
  display: flex;
  align-items: center;
  gap: 8px;
  color: var(--text-secondary);
  font-size: 1.1rem;
  flex: 0 0 180px; /* Fixed width for alignment */
}

.info-item .el-icon {
  color: var(--accent-color);
  font-size: 1.2rem;
}

.card-actions {
  display: flex;
  gap: var(--spacing-sm);
  margin-top: 0;
  margin-left: var(--spacing-xl);
}

.admin-actions {
  display: flex;
  gap: var(--spacing-sm);
  margin-left: auto;
}

.glass-btn.sm-btn {
  padding: 0.4rem 1rem;
  font-size: 0.9rem;
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
  width: 90%;
  max-width: 500px;
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

.modal-header h3 {
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

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: var(--spacing-md);
  margin-top: var(--spacing-xl);
}

@media (max-width: 768px) {
  .team-card {
    flex-direction: column;
    align-items: flex-start;
  }

  .card-header {
    width: 100%;
    border-bottom: 1px solid var(--glass-border);
    padding-bottom: var(--spacing-sm);
    margin-bottom: var(--spacing-sm);
  }

  .card-content {
    width: 100%;
    flex-direction: column;
    align-items: flex-start;
    gap: var(--spacing-sm);
  }

  .card-actions {
    width: 100%;
    margin-top: var(--spacing-md);
    justify-content: space-between;
  }
  
  .page-header {
    flex-direction: column;
    gap: var(--spacing-md);
    text-align: center;
  }
  
  .card-actions {
    flex-wrap: wrap;
  }
  
  .glass-btn {
    flex: 1;
    justify-content: center;
  }
}
</style>

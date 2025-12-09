<template>
  <div class="players-container">
    <div class="page-header">
      <div class="header-content">
        <h1>球员管理</h1>
        <p class="subtitle">查看和管理NBA球员信息</p>
      </div>
      <div class="header-actions">
        <div class="search-wrapper glass-input-wrapper">
          <el-icon class="search-icon"><Search /></el-icon>
          <select v-model="selectedTeam" @change="loadPlayers" class="glass-select filter-select">
            <option value="">所有球队</option>
            <option v-for="team in teams" :key="team.team_id" :value="team.team_id">
              {{ team.name }}
            </option>
          </select>
        </div>
        <button v-if="isAdmin" @click="showPlayerModal('create')" class="glass-btn primary-btn">
          <el-icon><Plus /></el-icon> 新建球员
        </button>
      </div>
    </div>

    <div class="players-grid">
      <div v-for="player in players" :key="player.player_id" class="glass-card player-card">
        <div class="card-header">
          <div class="player-title">
            <h3>{{ player.name }}</h3>
          </div>
        </div>

        <div class="card-content">
          <div class="info-item jersey-item">
            <span class="jersey-number">#{{ player.jersey_number }}</span>
          </div>
          <div class="info-item position-item">
            <div class="player-position-badge">
              {{ player.position }}
            </div>
          </div>
          <div class="info-item team-item">
            <el-icon><Trophy /></el-icon>
            <span>{{ player.team_name || '自由球员' }}</span>
          </div>
          <div class="info-item nationality-item">
            <el-icon><Flag /></el-icon>
            <span>{{ player.nationality }}</span>
          </div>
        </div>

        <div class="card-actions">
          <button @click="showPlayerModal('view', player)" class="glass-btn sm-btn">
            <el-icon><User /></el-icon> 查看
          </button>
          <router-link :to="player.current_team_id ? `/games?team_id=${player.current_team_id}` : '/games'" class="glass-btn sm-btn">
            <el-icon><Basketball /></el-icon> 比赛
          </router-link>
          <div v-if="isAdmin" class="admin-actions">
            <button @click="showPlayerModal('edit', player)" class="glass-btn icon-only warning">
              <el-icon><Edit /></el-icon>
            </button>
            <button @click="deletePlayer(player)" class="glass-btn icon-only danger">
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

    <div v-if="!loading && players.length === 0" class="empty-state">
      <el-icon><User /></el-icon>
      <p>暂无球员数据</p>
    </div>

    <!-- Modal -->
    <div v-if="showModal" class="modal-overlay glass-overlay">
      <div class="glass-card modal-content">
        <div class="modal-header">
          <h3>{{ getModalTitle() }}</h3>
          <button @click="closeModal" class="close-btn"><el-icon><Close /></el-icon></button>
        </div>
        
        <form @submit.prevent="handleSubmit" class="glass-form">
          <div class="form-group">
            <label>姓名 *</label>
            <div class="input-wrapper">
              <el-icon><User /></el-icon>
              <input v-model="formData.name" type="text" required class="glass-input" :disabled="modalMode === 'view'">
            </div>
          </div>
          
          <div class="form-row">
            <div class="form-group half">
              <label>位置 *</label>
              <div class="input-wrapper">
                <el-icon><Coordinate /></el-icon>
                <select v-model="formData.position" required class="glass-select" :disabled="modalMode === 'view'">
                  <option value="">请选择位置</option>
                  <option value="控球后卫">控球后卫</option>
                  <option value="得分后卫">得分后卫</option>
                  <option value="小前锋">小前锋</option>
                  <option value="大前锋">大前锋</option>
                  <option value="中锋">中锋</option>
                </select>
              </div>
            </div>
            <div class="form-group half">
              <label>球衣号 *</label>
              <div class="input-wrapper">
                <el-icon><PriceTag /></el-icon>
                <input v-model="formData.jersey_number" type="number" min="0" max="99" required class="glass-input" :disabled="modalMode === 'view'">
              </div>
            </div>
          </div>
          
           <div class="form-row">
            <div class="form-group half">
              <label>身高 (m)</label>
              <div class="input-wrapper">
                <el-icon><Top /></el-icon>
                <input v-model="formData.height" type="number" step="0.01" min="1.5" max="2.5" class="glass-input" :disabled="modalMode === 'view'">
              </div>
            </div>
            <div class="form-group half">
              <label>体重 (kg)</label>
              <div class="input-wrapper">
                <el-icon><Odometer /></el-icon>
                <input v-model="formData.weight" type="number" step="0.01" min="50" max="200" class="glass-input" :disabled="modalMode === 'view'">
              </div>
            </div>
          </div>

          <div class="form-row">
             <div class="form-group half">
              <label>国籍</label>
              <div class="input-wrapper">
                <el-icon><Flag /></el-icon>
                <input v-model="formData.nationality" type="text" class="glass-input" :disabled="modalMode === 'view'">
              </div>
            </div>
             <div class="form-group half">
              <label>出生日期</label>
              <div class="input-wrapper">
                <el-icon><Calendar /></el-icon>
                <input v-model="formData.birth_date" type="date" class="glass-input" :disabled="modalMode === 'view'">
              </div>
            </div>
          </div>

          <div class="form-group">
            <label>所属球队</label>
            <div class="input-wrapper">
              <el-icon><Trophy /></el-icon>
              <select v-model="formData.current_team_id" class="glass-select" :disabled="modalMode === 'view'">
                <option value="">无球队</option>
                <option v-for="team in teams" :key="team.team_id" :value="team.team_id">
                  {{ team.name }}
                </option>
              </select>
            </div>
          </div>

          <div class="form-actions">
            <button type="button" @click="closeModal" class="glass-btn">
              {{ modalMode === 'view' ? '关闭' : '取消' }}
            </button>
            <button v-if="modalMode !== 'view'" type="submit" class="glass-btn primary-btn">
              {{ modalMode === 'create' ? '创建' : '更新' }}
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
  Search, Plus, User, Trophy, Flag, Top, Odometer, 
  Calendar, Basketball, Edit, Delete, Loading, 
  Close, Coordinate, PriceTag 
} from '@element-plus/icons-vue'

export default {
  name: 'Players',
  components: {
    Search, Plus, User, Trophy, Flag, Top, Odometer, 
    Calendar, Basketball, Edit, Delete, Loading, 
    Close, Coordinate, PriceTag
  },
  data() {
    return {
      players: [],
      teams: [],
      selectedTeam: '',
      loading: false,
      showModal: false,
      modalMode: 'create', // 'create' or 'edit'
      formData: {
        player_id: null,
        name: '',
        position: '',
        jersey_number: '',
        height: '',
        weight: '',
        birth_date: '',
        nationality: '',
        current_team_id: '',
        contract_expiry: '',
        salary: ''
      }
    }
  },
  computed: {
    isAdmin() {
      const user = JSON.parse(localStorage.getItem('user') || '{}')
      return user.role === 'admin'
    }
  },
  async mounted() {
    // 从URL参数获取team_id
    const teamId = this.$route.query.team_id
    if (teamId) {
      this.selectedTeam = parseInt(teamId)
    }
    await Promise.all([this.loadTeams(), this.loadPlayers()])
  },
  methods: {
    async loadTeams() {
      try {
        this.teams = await api.getTeams()
      } catch (error) {
        console.error('加载球队数据失败:', error)
      }
    },
    async loadPlayers() {
      this.loading = true
      try {
        this.players = await api.getPlayers(this.selectedTeam || null)
      } catch (error) {
        console.error('加载球员数据失败:', error)
        // alert('加载球员数据失败')
      } finally {
        this.loading = false
      }
    },
    
    showPlayerModal(mode, player = null) {
      this.modalMode = mode
      this.showModal = true
      
      if (mode === 'create') {
        this.resetForm()
      } else if ((mode === 'edit' || mode === 'view') && player) {
        this.formData = {
          player_id: player.player_id,
          name: player.name || '',
          position: player.position || '',
          jersey_number: player.jersey_number !== undefined ? player.jersey_number : '',
          height: player.height || '',
          weight: player.weight || '',
          birth_date: player.birth_date || '',
          nationality: player.nationality || '',
          current_team_id: player.current_team_id || '',
          contract_expiry: player.contract_expiry || '',
          salary: player.salary || ''
        }
      }
    },

    getModalTitle() {
      switch (this.modalMode) {
        case 'create': return '新建球员'
        case 'edit': return '编辑球员'
        case 'view': return '球员详情'
        default: return '球员信息'
      }
    },
    
    closeModal() {
      this.showModal = false
      this.resetForm()
    },
    
    resetForm() {
      this.formData = {
        player_id: null,
        name: '',
        position: '',
        jersey_number: '',
        height: '',
        weight: '',
        birth_date: '',
        nationality: '',
        current_team_id: '',
        contract_expiry: '',
        salary: ''
      }
    },
    
    async handleSubmit() {
      try {
        if (this.modalMode === 'create') {
          await api.createPlayer(this.formData)
          alert('球员创建成功')
        } else {
          await api.updatePlayer(this.formData.player_id, this.formData)
          alert('球员更新成功')
        }
        
        this.closeModal()
        await this.loadPlayers() // 重新加载球员列表
      } catch (error) {
        console.error('操作失败:', error)
        alert(error.message || '操作失败')
      }
    },
    
    async deletePlayer(player) {
      if (!confirm(`确定要删除球员 ${player.name} 吗？此操作不可撤销。`)) {
        return
      }
      
      try {
        await api.deletePlayer(player.player_id)
        alert('球员删除成功')
        await this.loadPlayers() // 重新加载球员列表
      } catch (error) {
        console.error('删除失败:', error)
        alert(error.message || '删除失败')
      }
    }
  }
}
</script>

<style scoped>
.players-container {
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
  gap: var(--spacing-md);
  align-items: center;
}

.glass-input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.search-icon {
  position: absolute;
  left: 12px;
  color: var(--text-secondary);
  z-index: 1;
}

.filter-select {
  padding-left: 36px;
  min-width: 200px;
}

.players-grid {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
}

.player-card {
  display: flex;
  flex-direction: row;
  align-items: center;
  padding: var(--spacing-md) var(--spacing-lg);
  gap: var(--spacing-lg);
  transition: all 0.3s ease;
}

.player-card:hover {
  transform: translateX(5px);
  box-shadow: var(--glass-shadow-hover);
  background: rgba(255, 255, 255, 0.08);
}

.card-header {
  display: flex;
  flex-direction: row;
  align-items: center;
  padding-bottom: 0;
  border-bottom: none;
  margin-bottom: 0;
  flex: 0 0 200px; /* Reduced width since jersey number moved */
  gap: var(--spacing-md);
}

.player-title {
  display: flex;
  align-items: center;
  gap: 8px;
}

.player-title h3 {
  font-size: 1.4rem;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0;
  white-space: nowrap;
}

.jersey-number {
  font-size: 1.2rem;
  color: var(--accent-color);
  font-weight: 700;
}

.player-position-badge {
  background: rgba(255, 255, 255, 0.1);
  padding: 4px 10px;
  border-radius: 12px;
  font-size: 0.9rem;
  color: var(--color-accent);
  border: 1px solid rgba(212, 175, 55, 0.3);
  font-weight: 600;
  white-space: nowrap;
  display: inline-block;
}

.card-content {
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: var(--spacing-lg);
  margin-bottom: 0;
}

.info-item {
  display: flex;
  align-items: center;
  gap: 8px;
  color: var(--text-secondary);
  font-size: 1.1rem;
}

.jersey-item {
  flex: 0 0 80px;
  justify-content: center;
}

.position-item {
  flex: 0 0 120px;
}

.team-item {
  flex: 0 0 180px;
}

.nationality-item {
  flex: 0 0 140px;
}

.card-actions {
  display: flex;
  gap: var(--spacing-sm);
  margin-top: 0;
  margin-left: var(--spacing-xl);
}

.info-item.full-width {
  width: auto;
}

.info-item .el-icon {
  color: var(--accent-color);
  opacity: 0.8;
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
  padding: 0.4rem 0.8rem;
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
  width: 90%;
  max-width: 600px;
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

.glass-form .form-row {
  display: flex;
  gap: var(--spacing-lg);
  margin-bottom: var(--spacing-lg);
}

.glass-form .form-group.half {
  flex: 1;
  margin-bottom: 0;
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
  .player-card {
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

  .info-row {
    width: 100%;
    justify-content: space-between;
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
  
  .header-actions {
    flex-direction: column;
    width: 100%;
  }
  
  .search-wrapper {
    width: 100%;
  }
  
  .filter-select {
    width: 100%;
  }
  
  .glass-form .form-row {
    flex-direction: column;
    gap: var(--spacing-lg);
  }
}
</style>

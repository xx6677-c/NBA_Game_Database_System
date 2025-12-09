<template>
  <div class="profile-container">
    <div class="page-header">
      <div class="header-content">
        <h1>个人中心</h1>
        <p class="subtitle">管理您的个人信息和活动记录</p>
      </div>
    </div>

    <div class="profile-content">
      <!-- 个人信息卡片 -->
      <div class="glass-card profile-card">
        <div class="card-header">
          <h3><el-icon><User /></el-icon> 基本信息</h3>
          <button @click="editMode = !editMode" class="glass-btn sm-btn">
            <el-icon><Edit /></el-icon> {{ editMode ? '取消编辑' : '编辑信息' }}
          </button>
        </div>
        
        <div class="user-info">
          <div class="info-item">
            <label>用户名</label>
            <div class="info-value">{{ userInfo.username }}</div>
          </div>
          <div class="info-item">
            <label>角色</label>
            <div class="info-value">
              <span class="role-badge">{{ userInfo.role }}</span>
            </div>
          </div>
          <div class="info-item">
            <label>注册时间</label>
            <div class="info-value">{{ userInfo.register_time }}</div>
          </div>
          <div class="info-item">
            <label>最后登录</label>
            <div class="info-value">{{ userInfo.last_login || '首次登录' }}</div>
          </div>
          
          <!-- 可编辑信息 -->
          <div class="info-item">
            <label>邮箱</label>
            <div class="info-value">
              <input v-if="editMode" v-model="editForm.email" type="email" class="glass-input sm-input">
              <span v-else>{{ userInfo.email || '未设置' }}</span>
            </div>
          </div>
          <div class="info-item">
            <label>手机号</label>
            <div class="info-value">
              <input v-if="editMode" v-model="editForm.phone" type="tel" class="glass-input sm-input">
              <span v-else>{{ userInfo.phone || '未设置' }}</span>
            </div>
          </div>
          
          <div v-if="editMode" class="edit-actions">
            <button @click="saveProfile" class="glass-btn primary-btn">保存修改</button>
            <button @click="cancelEdit" class="glass-btn">取消</button>
          </div>
        </div>
      </div>

      <!-- 统计信息 -->
      <div class="stats-grid">
        <div class="glass-card stat-card">
          <div class="stat-icon"><el-icon><Document /></el-icon></div>
          <div class="stat-content">
            <h3>发帖数量</h3>
            <p class="stat-number">{{ userPosts.length }}</p>
          </div>
        </div>
        <div class="glass-card stat-card">
          <div class="stat-icon"><el-icon><Star /></el-icon></div>
          <div class="stat-content">
            <h3>评分数量</h3>
            <p class="stat-number">{{ userRatings.length }}</p>
          </div>
        </div>
        <div class="glass-card stat-card">
          <div class="stat-icon"><el-icon><View /></el-icon></div>
          <div class="stat-content">
            <h3>总浏览量</h3>
            <p class="stat-number">{{ totalViews }}</p>
          </div>
        </div>
        <div class="glass-card stat-card">
          <div class="stat-icon"><el-icon><Pointer /></el-icon></div>
          <div class="stat-content">
            <h3>总点赞数</h3>
            <p class="stat-number">{{ totalLikes }}</p>
          </div>
        </div>
      </div>

      <!-- 我的帖子 -->
      <div class="glass-card profile-card">
        <div class="card-header">
          <h3><el-icon><Document /></el-icon> 我的帖子 ({{ userPosts.length }})</h3>
        </div>
        <div v-if="userPosts.length === 0" class="empty-state">
          <el-icon><DocumentRemove /></el-icon>
          <p>您还没有发布过任何帖子</p>
        </div>
        <div v-else class="posts-list custom-scrollbar">
          <div v-for="post in userPosts" :key="post.post_id" class="post-item glass-card inner-card">
            <div class="post-header">
              <h4>{{ post.title }}</h4>
              <span class="post-time">{{ post.create_time }}</span>
            </div>
            <div class="post-content">
              <p>{{ post.content.substring(0, 100) }}{{ post.content.length > 100 ? '...' : '' }}</p>
            </div>
            <div class="post-meta">
              <span v-if="post.season" class="game-info">
                {{ post.season }} | {{ post.home_team }} vs {{ post.away_team }}
              </span>
              <div class="post-stats">
                <span><el-icon><View /></el-icon> {{ post.views }}</span>
                <span><el-icon><Pointer /></el-icon> {{ post.likes }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 我的评分 -->
      <div class="glass-card profile-card">
        <div class="card-header">
          <h3><el-icon><Star /></el-icon> 我的评分 ({{ userRatings.length }})</h3>
        </div>
        <div v-if="userRatings.length === 0" class="empty-state">
          <el-icon><StarFilled /></el-icon>
          <p>您还没有对任何球员进行评分</p>
        </div>
        <div v-else class="ratings-list custom-scrollbar">
          <div v-for="rating in userRatings" :key="`${rating.user_id}-${rating.player_id}-${rating.game_id}`" class="rating-item glass-card inner-card">
            <div class="rating-header">
              <div class="player-info">
                <h4>{{ rating.player_name }}</h4>
                <span class="player-details">{{ rating.position }} | {{ rating.team_name }}</span>
              </div>
              <div class="rating-score">
                <span class="score">{{ rating.rating }}</span>/10
              </div>
            </div>

            <div class="rating-time">
              <span>{{ rating.create_time }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 操作区域 -->
      <div class="action-section">
        <button @click="handleLogout" class="glass-btn secondary-btn logout-btn">
          <el-icon><SwitchButton /></el-icon> 退出登录
        </button>
        <button @click="showLogoutDialog" class="glass-btn danger logout-btn">
          <el-icon><Delete /></el-icon> 注销账户
        </button>
      </div>

      <!-- 注销确认对话框 -->
      <div v-if="showLogoutModal" class="modal-overlay glass-overlay" @click="closeLogoutDialog">
        <div class="glass-card modal-content" @click.stop>
          <!-- 警告图标 -->
          <div class="modal-icon">
            <div class="warning-icon"><el-icon><Warning /></el-icon></div>
          </div>
          
          <!-- 标题和描述 -->
          <div class="modal-header">
            <h3 class="modal-title">确认注销账户</h3>
            <p class="modal-description">
              此操作将永久删除您的账户和所有相关数据
            </p>
          </div>
          
          <!-- 警告信息 -->
          <div class="warning-section">
            <div class="warning-item">
              <span class="warning-dot">•</span>
              <span>所有帖子将被删除</span>
            </div>
            <div class="warning-item">
              <span class="warning-dot">•</span>
              <span>所有评分将被清除</span>
            </div>
            <div class="warning-item">
              <span class="warning-dot">•</span>
              <span>账户信息将无法恢复</span>
            </div>
            <div class="warning-highlight">
              <strong>此操作不可撤销！</strong>
            </div>
          </div>
          
          <!-- 验证区域 -->
          <div class="verification-section">
            <div class="input-group">
              <label for="password">
                <span class="label-icon"><el-icon><Lock /></el-icon></span>
                请输入密码确认
              </label>
              <input 
                v-model="logoutPassword" 
                type="password" 
                id="password"
                placeholder="输入您的登录密码"
                class="glass-input password-input"
                @keyup.enter="confirmLogout"
              >
            </div>
            
            <div class="confirmation-check">
              <label class="checkbox-container">
                <input 
                  v-model="logoutConfirmed" 
                  type="checkbox" 
                  class="confirm-checkbox"
                >
                <span class="checkmark"></span>
                <span class="checkbox-label">
                  我理解此操作不可撤销，确认要永久注销账户
                </span>
              </label>
            </div>
          </div>
          
          <!-- 操作按钮 -->
          <div class="modal-actions">
            <button 
              @click="closeLogoutDialog" 
              class="glass-btn"
            >
              取消操作
            </button>
            <button 
              @click="confirmLogout" 
              :disabled="!canLogout"
              class="glass-btn danger"
              :class="{ 'btn-disabled': !canLogout }"
            >
              {{ isLoggingOut ? '处理中...' : '确认注销' }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from '../services/api'
import { 
  User, Edit, Document, Star, View, Pointer, DocumentRemove, StarFilled, 
  SwitchButton, Delete, Warning, Lock 
} from '@element-plus/icons-vue'

export default {
  name: 'Profile',
  components: {
    User, Edit, Document, Star, View, Pointer, DocumentRemove, StarFilled, 
    SwitchButton, Delete, Warning, Lock
  },
  data() {
    return {
      userInfo: {},
      userPosts: [],
      userRatings: [],
      editMode: false,
      editForm: {
        email: '',
        phone: ''
      },
      showLogoutModal: false,
      logoutPassword: '',
      logoutConfirmed: false,
      isLoggingOut: false
    }
  },
  computed: {
    totalViews() {
      return this.userPosts.reduce((sum, post) => sum + (post.views || 0), 0)
    },
    totalLikes() {
      return this.userPosts.reduce((sum, post) => sum + (post.likes || 0), 0)
    },
    canLogout() {
      return this.logoutPassword.trim() && this.logoutConfirmed && !this.isLoggingOut
    }
  },
  async mounted() {
    await this.loadUserData()
  },
  methods: {
    async loadUserData() {
      try {
        // 加载用户信息
        const userData = await api.getCurrentUser()
        this.userInfo = userData
        this.editForm.email = userData.email || ''
        this.editForm.phone = userData.phone || ''

        // 加载用户帖子
        const postsData = await api.getUserPosts()
        this.userPosts = postsData

        // 加载用户评分
        const ratingsData = await api.getUserRatings()
        this.userRatings = ratingsData

      } catch (error) {
        console.error('加载用户数据失败:', error)
        alert('加载用户数据失败')
      }
    },

    async saveProfile() {
      try {
        await api.updateUserProfile(this.editForm)
        this.editMode = false
        await this.loadUserData() // 重新加载数据
        alert('个人信息更新成功')
      } catch (error) {
        console.error('更新个人信息失败:', error)
        alert('更新个人信息失败')
      }
    },

    cancelEdit() {
      this.editMode = false
      this.editForm.email = this.userInfo.email || ''
      this.editForm.phone = this.userInfo.phone || ''
    },

    async handleLogout() {
      try {
        await api.logout()
        this.$router.push('/login')
      } catch (error) {
        console.error('登出失败:', error)
      }
    },

    showLogoutDialog() {
      this.showLogoutModal = true
      this.logoutPassword = ''
      this.logoutConfirmed = false
      this.isLoggingOut = false
    },

    closeLogoutDialog() {
      this.showLogoutModal = false
      this.logoutPassword = ''
      this.logoutConfirmed = false
      this.isLoggingOut = false
    },

    async confirmLogout() {
      if (!this.canLogout) return

      this.isLoggingOut = true
      
      try {
        // 先验证密码
        const passwordValid = await this.verifyPassword()
        
        if (!passwordValid) {
          alert('密码验证失败，请检查密码是否正确')
          this.isLoggingOut = false
          return
        }

        // 执行注销操作
        const success = await api.deleteAccount(this.logoutPassword)
        
        if (success) {
          alert('账户注销成功！感谢您使用我们的服务。')
          await api.logout()
          this.$router.push('/login')
        } else {
          alert('注销失败，请稍后重试')
        }
        
      } catch (error) {
        console.error('注销失败:', error)
        alert('注销过程中发生错误，请稍后重试')
      } finally {
        this.isLoggingOut = false
      }
    },

    async verifyPassword() {
      try {
        // 这里需要调用后端API验证密码
        // 暂时模拟验证，实际应该调用后端API
        const response = await api.verifyPassword(this.logoutPassword)
        return response.success
      } catch (error) {
        console.error('密码验证失败:', error)
        return false
      }
    }
  }
}
</script>

<style scoped>
.profile-container {
  padding: var(--spacing-lg);
  max-width: 1200px;
  margin: 0 auto;
}

.page-header {
  text-align: center;
  margin-bottom: var(--spacing-xl);
}

.header-content h1 {
  font-size: 2.5rem;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: var(--spacing-xs);
}

.subtitle {
  color: var(--text-secondary);
  font-size: 1.1rem;
}

.profile-content {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-lg);
}

.profile-card {
  padding: var(--spacing-lg);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-md);
  padding-bottom: var(--spacing-sm);
  border-bottom: 1px solid var(--glass-border);
}

.card-header h3 {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 1.2rem;
  color: var(--text-primary);
  margin: 0;
}

.user-info {
  display: grid;
  gap: var(--spacing-md);
}

.info-item {
  display: flex;
  align-items: center;
  padding: var(--spacing-sm) 0;
  border-bottom: 1px solid rgba(0,0,0,0.05);
}

.info-item label {
  font-weight: 600;
  color: var(--text-secondary);
  width: 120px;
  flex-shrink: 0;
}

.info-value {
  color: var(--text-primary);
  flex: 1;
}

.role-badge {
  background: var(--accent-color);
  color: white;
  padding: 2px 10px;
  border-radius: 12px;
  font-size: 0.85rem;
}

.sm-input {
  padding: 4px 8px;
  width: 200px;
}

.edit-actions {
  display: flex;
  gap: var(--spacing-sm);
  margin-top: var(--spacing-md);
  justify-content: flex-end;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: var(--spacing-md);
}

.stat-card {
  padding: var(--spacing-lg);
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
}

.stat-icon {
  font-size: 2.5rem;
  color: var(--primary-color);
  background: rgba(201, 8, 42, 0.1);
  width: 60px;
  height: 60px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.stat-content h3 {
  margin: 0 0 4px 0;
  color: var(--text-secondary);
  font-size: 0.9rem;
  font-weight: normal;
}

.stat-number {
  font-size: 1.8rem;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--spacing-sm);
  padding: var(--spacing-xl);
  color: var(--text-secondary);
}

.empty-state .el-icon {
  font-size: 3rem;
  opacity: 0.5;
}

.posts-list, .ratings-list {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
  max-height: 500px;
  overflow-y: auto;
  padding-right: var(--spacing-sm);
}

.post-item, .rating-item {
  padding: var(--spacing-md);
}

.post-header, .rating-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: var(--spacing-sm);
}

.post-header h4, .rating-header h4 {
  margin: 0;
  color: var(--text-primary);
  font-size: 1.1rem;
}

.post-time, .rating-time {
  color: var(--text-secondary);
  font-size: 0.85rem;
  white-space: nowrap;
  margin-left: var(--spacing-md);
}

.post-content {
  color: var(--text-secondary);
  font-size: 0.95rem;
  margin-bottom: var(--spacing-sm);
  line-height: 1.5;
}

.post-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.85rem;
}

.game-info {
  background: rgba(0,0,0,0.05);
  padding: 2px 8px;
  border-radius: 4px;
  color: var(--text-secondary);
}

.post-stats {
  display: flex;
  gap: var(--spacing-md);
  color: var(--text-secondary);
}

.post-stats span {
  display: flex;
  align-items: center;
  gap: 4px;
}

.player-details {
  color: var(--text-secondary);
  font-size: 0.9rem;
  display: block;
  margin-top: 4px;
}

.rating-score {
  display: flex;
  align-items: baseline;
  gap: 2px;
  color: var(--text-secondary);
}

.rating-score .score {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--accent-color);
}

.action-section {
  display: flex;
  justify-content: center;
  gap: var(--spacing-md);
  margin-top: var(--spacing-lg);
}

.logout-btn {
  padding: 0.8rem 2rem;
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 1rem;
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
  padding: var(--spacing-xl);
  border: 1px solid rgba(255, 255, 255, 0.5);
}

.modal-icon {
  display: flex;
  justify-content: center;
  margin-bottom: var(--spacing-lg);
}

.warning-icon {
  font-size: 3rem;
  color: #f59e0b;
  background: #fef3c7;
  width: 80px;
  height: 80px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 4px solid #fffbeb;
}

.modal-header {
  text-align: center;
  margin-bottom: var(--spacing-lg);
}

.modal-title {
  color: #dc2626;
  font-size: 1.5rem;
  margin: 0 0 var(--spacing-xs) 0;
}

.modal-description {
  color: var(--text-secondary);
  margin: 0;
}

.warning-section {
  background: rgba(251, 191, 36, 0.1);
  border: 1px solid rgba(251, 191, 36, 0.3);
  border-radius: 8px;
  padding: var(--spacing-md);
  margin-bottom: var(--spacing-lg);
}

.warning-item {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
  color: #fcd34d;
  font-size: 0.95rem;
}

.warning-dot {
  color: #f59e0b;
  font-weight: bold;
}

.warning-highlight {
  text-align: center;
  margin-top: var(--spacing-sm);
  padding-top: var(--spacing-sm);
  border-top: 1px solid rgba(251, 191, 36, 0.3);
  color: #ef4444;
  font-weight: 600;
}

.verification-section {
  margin-bottom: var(--spacing-lg);
}

.input-group {
  margin-bottom: var(--spacing-md);
}

.input-group label {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: var(--spacing-sm);
}

.password-input {
  width: 100%;
}

.checkbox-container {
  display: flex;
  align-items: flex-start;
  cursor: pointer;
  font-size: 0.9rem;
  color: var(--text-secondary);
  line-height: 1.4;
  position: relative;
  padding-left: 30px;
}

.confirm-checkbox {
  position: absolute;
  opacity: 0;
  cursor: pointer;
  height: 0;
  width: 0;
}

.checkmark {
  position: absolute;
  top: 0;
  left: 0;
  height: 20px;
  width: 20px;
  background-color: rgba(255, 255, 255, 0.5);
  border: 1px solid var(--glass-border);
  border-radius: 4px;
  transition: all 0.2s;
}

.checkbox-container:hover .checkmark {
  background-color: rgba(255, 255, 255, 0.8);
}

.confirm-checkbox:checked ~ .checkmark {
  background-color: var(--primary-color);
  border-color: var(--primary-color);
}

.checkmark:after {
  content: "";
  position: absolute;
  display: none;
}

.confirm-checkbox:checked ~ .checkmark:after {
  display: block;
}

.checkbox-container .checkmark:after {
  left: 6px;
  top: 2px;
  width: 5px;
  height: 10px;
  border: solid white;
  border-width: 0 2px 2px 0;
  transform: rotate(45deg);
}

.modal-actions {
  display: flex;
  gap: var(--spacing-md);
  justify-content: flex-end;
}

.modal-actions button {
  min-width: 100px;
}

@media (max-width: 768px) {
  .info-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 4px;
  }
  
  .info-item label {
    width: auto;
  }
  
  .modal-actions {
    flex-direction: column;
  }
  
  .modal-actions button {
    width: 100%;
  }
}
</style>

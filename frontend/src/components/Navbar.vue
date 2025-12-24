<template>
  <nav class="navbar glass-nav">
    <div class="navbar-container">
      <div class="navbar-brand">
        <el-icon class="brand-icon" :size="24"><Basketball /></el-icon>
        <h2>NBA DB</h2>
      </div>
      
      <div class="navbar-menu">
        <router-link to="/dashboard" class="nav-link">
          <el-icon><HomeFilled /></el-icon>
          <span>首页</span>
        </router-link>
        
        <router-link to="/teams" class="nav-link">
          <el-icon><Trophy /></el-icon>
          <span>球队</span>
        </router-link>
        
        <router-link to="/players" class="nav-link">
          <el-icon><User /></el-icon>
          <span>球员</span>
        </router-link>

        <router-link to="/comparison" class="nav-link">
          <el-icon><DataLine /></el-icon>
          <span>对比</span>
        </router-link>
        
        <router-link to="/games" class="nav-link">
          <el-icon><VideoPlay /></el-icon>
          <span>比赛</span>
        </router-link>
        
        <router-link to="/rankings" class="nav-link">
          <el-icon><TrendCharts /></el-icon>
          <span>榜单</span>
        </router-link>

        <router-link to="/posts" class="nav-link">
          <el-icon><ChatDotRound /></el-icon>
          <span>社区</span>
        </router-link>
        
        <router-link v-if="user.role === 'analyst' || user.role === 'admin'" to="/query" class="nav-link">
          <el-icon><DataAnalysis /></el-icon>
          <span>分析</span>
        </router-link>
      </div>

      <div class="navbar-end">
        <router-link to="/profile" class="user-profile-link">
          <div class="avatar-placeholder">
            {{ user.username ? user.username.charAt(0).toUpperCase() : 'U' }}
          </div>
          <span class="username">{{ user.username }}</span>
        </router-link>
      </div>
    </div>
  </nav>
</template>

<script>
import api from '../services/api'

export default {
  name: 'Navbar',
  data() {
    return {
      user: {}
    }
  },
  mounted() {
    this.loadUserInfo()
    window.addEventListener('storage', this.handleStorageChange)
    window.addEventListener('userInfoChanged', this.handleUserInfoChanged)
  },
  beforeUnmount() {
    window.removeEventListener('storage', this.handleStorageChange)
    window.removeEventListener('userInfoChanged', this.handleUserInfoChanged)
  },
  methods: {
    loadUserInfo() {
      const userData = localStorage.getItem('user')
      if (userData) {
        this.user = JSON.parse(userData)
      } else {
        this.user = {}
      }
    },
    handleStorageChange(event) {
      if (event.key === 'user') {
        this.loadUserInfo()
      }
    },
    handleUserInfoChanged() {
      this.loadUserInfo()
    },
    logout() {
      api.logout()
      this.$router.push('/login')
    }
  }
}
</script>

<style scoped>
.navbar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 64px;
  z-index: 1000;
  transition: all 0.3s ease;
}

.glass-nav {
  background: rgba(10, 14, 23, 0.8);
  border-bottom: 1px solid rgba(212, 175, 55, 0.3);
  backdrop-filter: blur(10px);
  box-shadow: 0 4px 20px rgba(0,0,0,0.5);
}

.navbar-container {
  max-width: 1200px;
  margin: 0 auto;
  height: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 24px;
}

.navbar-brand {
  display: flex;
  align-items: center;
  gap: 12px;
  color: var(--color-text-primary);
}

.brand-icon {
  color: var(--color-accent);
}

.navbar-brand h2 {
  margin: 0;
  font-size: 18px;
  font-weight: 700;
  letter-spacing: -0.5px;
}

.navbar-menu {
  display: flex;
  align-items: center;
  gap: 8px;
  height: 100%;
}

.nav-link {
  display: flex;
  align-items: center;
  gap: 8px;
  text-decoration: none;
  color: var(--color-text-secondary);
  font-size: 14px;
  font-weight: 500;
  padding: 8px 16px;
  border-radius: 20px;
  transition: all 0.2s ease;
  height: 36px;
}

.nav-link:hover {
  color: var(--color-text-primary);
  background: rgba(255, 255, 255, 0.1);
}

.nav-link.router-link-active {
  color: var(--color-accent);
  background: rgba(212, 175, 55, 0.15);
  border: 1px solid rgba(212, 175, 55, 0.3);
}

.navbar-end {
  display: flex;
  align-items: center;
}

.user-profile-link {
  display: flex;
  align-items: center;
  gap: 10px;
  text-decoration: none;
  color: var(--color-text-primary);
  padding: 4px 12px 4px 4px;
  border-radius: 30px;
  transition: background 0.2s;
}

.user-profile-link:hover {
  background: rgba(255, 255, 255, 0.1);
}

.avatar-placeholder {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: linear-gradient(135deg, #e0e0e0 0%, #f5f5f5 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 14px;
  color: #666;
  border: 1px solid rgba(0,0,0,0.05);
}

.username {
  font-size: 14px;
  font-weight: 500;
}
</style>
<template>
  <div class="login-container">
    <!-- 全屏背景 -->
    <div class="background-image"></div>
    
    <!-- 中央磨砂玻璃卡片 -->
    <div class="glass-card login-card">
      <div class="card-header">
        <h1><el-icon class="logo-icon"><Basketball /></el-icon> NBA比赛数据库</h1>
        <p class="subtitle">欢迎回来，登录进入篮球世界</p>
      </div>
      
      <form @submit.prevent="handleLogin" class="login-form">
        <div class="form-group">
          <label><el-icon><User /></el-icon> 用户名</label>
          <input v-model="form.username" type="text" required placeholder="请输入用户名" class="glass-input">
        </div>
        <div class="form-group">
          <label><el-icon><Lock /></el-icon> 密码</label>
          <input v-model="form.password" type="password" required placeholder="请输入密码" class="glass-input">
        </div>

        <button type="submit" :disabled="loading" class="glass-btn primary-btn login-btn">
          <el-icon v-if="loading" class="is-loading"><Loading /></el-icon>
          <span class="btn-text">{{ loading ? '登录中...' : '立即登录' }}</span>
          <el-icon v-if="!loading"><Right /></el-icon>
        </button>
      </form>
      
      <div class="register-link">
        <span>没有账号？</span>
        <button @click="showRegister = true" class="link-btn">立即注册</button>
      </div>
    </div>

    <!-- 注册弹窗 -->
    <div v-if="showRegister" class="modal-overlay glass-overlay">
      <div class="glass-card modal-content">
        <div class="modal-header">
          <h3>用户注册</h3>
          <button @click="showRegister = false" class="close-btn"><el-icon><Close /></el-icon></button>
        </div>
        
        <form @submit.prevent="handleRegister" class="register-form">
          <div class="form-group">
            <label>用户名</label>
            <input v-model="registerForm.username" type="text" required class="glass-input">
          </div>
          <div class="form-group">
            <label>密码</label>
            <input v-model="registerForm.password" type="password" required class="glass-input">
          </div>
          <div class="form-group">
            <label>确认密码</label>
            <input v-model="registerForm.confirmPassword" type="password" required class="glass-input">
          </div>
          <div class="form-group">
            <label>角色</label>
            <div class="select-wrapper">
              <select v-model="registerForm.role" @change="handleRoleChange" class="glass-input glass-select">
                <option value="user">普通用户</option>
                <option value="admin">管理员</option>
                <option value="analyst">数据分析师</option>
              </select>
              <el-icon class="select-icon"><ArrowDown /></el-icon>
            </div>
          </div>
          <div v-if="registerForm.role === 'admin' || registerForm.role === 'analyst'" class="form-group">
            <label>{{ registerForm.role === 'admin' ? '管理员密钥' : '数据分析师密钥' }}</label>
            <input 
              v-model="registerForm.secretKey" 
              type="password" 
              required 
              :placeholder="registerForm.role === 'admin' ? '请输入管理员密钥' : '请输入数据分析师密钥'"
              class="glass-input"
            >
            <small class="hint-text">
              <el-icon><InfoFilled /></el-icon>
              {{ registerForm.role === 'admin' ? '请联系系统管理员获取管理员密钥' : '请联系系统管理员获取数据分析师密钥' }}
            </small>
          </div>
          <div class="form-actions">
            <button type="button" @click="showRegister = false" class="glass-btn">取消</button>
            <button type="submit" :disabled="registerLoading" class="glass-btn primary-btn">
              <el-icon v-if="registerLoading" class="is-loading"><Loading /></el-icon>
              {{ registerLoading ? '注册中...' : '注册' }}
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
  Basketball, User, Lock, Loading, Right, Close, ArrowDown, InfoFilled 
} from '@element-plus/icons-vue'

export default {
  name: 'Login',
  components: {
    Basketball, User, Lock, Loading, Right, Close, ArrowDown, InfoFilled
  },
  data() {
    return {
      form: {
        username: '',
        password: ''
      },
      registerForm: {
        username: '',
        password: '',
        confirmPassword: '',
        role: 'user',
        secretKey: ''
      },
      loading: false,
      registerLoading: false,
      showRegister: false
    }
  },
  methods: {
    async handleLogin() {
      this.loading = true
      try {
        await api.login(this.form.username, this.form.password)
        this.$router.push('/dashboard')
      } catch (error) {
        alert(error.message || '登录失败')
      } finally {
        this.loading = false
      }
    },
    
    handleRoleChange() {
      // 当角色改变时，清空密钥字段
      this.registerForm.secretKey = ''
    },
    
    async handleRegister() {
      if (this.registerForm.password !== this.registerForm.confirmPassword) {
        alert('两次输入的密码不一致')
        return
      }
      
      // 验证管理员和数据分析师角色的密钥
      if (this.registerForm.role === 'admin' || this.registerForm.role === 'analyst') {
        if (!this.registerForm.secretKey) {
          alert(`${this.registerForm.role === 'admin' ? '管理员' : '数据分析师'}注册需要提供密钥`)
          return
        }
      }
      
      this.registerLoading = true
      try {
        await api.register(
          this.registerForm.username, 
          this.registerForm.password, 
          this.registerForm.role,
          this.registerForm.secretKey
        )
        alert('注册成功，请登录')
        this.showRegister = false
        this.registerForm = {
          username: '',
          password: '',
          confirmPassword: '',
          role: 'user',
          secretKey: ''
        }
      } catch (error) {
        alert(error.message || '注册失败')
      } finally {
        this.registerLoading = false
      }
    }
  }
}
</script>

<style scoped>
/* 全屏背景图片 */
.login-container {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  overflow: hidden;
  background: linear-gradient(135deg, #1a1c2c 0%, #4a192c 100%);
  z-index: 9999;
}

.background-image {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: url('../assets/background.png');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  z-index: 1;
  opacity: 0.4;
}

/* 中央磨砂玻璃卡片 - 黑色毛玻璃风格 */
.login-card {
  width: 420px;
  padding: 2.5rem;
  position: relative;
  z-index: 3;
  background: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 16px;
  box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
  animation: cardFloat 6s ease-in-out infinite;
}

@keyframes cardFloat {
  0%, 100% { transform: translateY(0px); }
  50% { transform: translateY(-10px); }
}

/* 卡片头部 */
.card-header {
  text-align: center;
  margin-bottom: 2rem;
}

.card-header h1 {
  font-size: 1.8rem;
  font-weight: 700;
  color: #ffffff;
  margin-bottom: 0.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  text-shadow: 0 2px 4px rgba(0,0,0,0.5);
}

.logo-icon {
  color: var(--color-orange);
  font-size: 2rem;
}

.subtitle {
  color: rgba(255, 255, 255, 0.7);
  font-size: 0.95rem;
  margin: 0;
}

/* 表单样式 */
.login-form {
  text-align: left;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: flex;
  align-items: center;
  gap: 6px;
  margin-bottom: 0.5rem;
  font-weight: 600;
  color: #ffffff;
  font-size: 0.95rem;
}

.glass-input {
  width: 100%;
  padding: 0.8rem 1rem;
  font-size: 1rem;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 8px;
  color: white;
  transition: all 0.3s ease;
}

.glass-input::placeholder {
  color: rgba(255, 255, 255, 0.5);
}

.glass-input:focus {
  outline: none;
  background: rgba(255, 255, 255, 0.15);
  border-color: var(--color-orange);
  box-shadow: 0 0 10px rgba(250, 131, 32, 0.3);
}

.select-wrapper {
  position: relative;
}

.glass-select {
  appearance: none;
  cursor: pointer;
}

.glass-select option {
  background: #1e1e1e;
  color: white;
}

.select-icon {
  position: absolute;
  right: 12px;
  top: 50%;
  transform: translateY(-50%);
  color: rgba(255, 255, 255, 0.7);
  pointer-events: none;
}

/* 登录按钮 */
.login-btn {
  width: 100%;
  padding: 0.8rem;
  font-size: 1.1rem;
  margin-top: 1rem;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  background: linear-gradient(135deg, var(--color-accent) 0%, #8a051d 100%);
  border: none;
  color: white;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.login-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(201, 8, 42, 0.4);
}

/* 注册链接 */
.register-link {
  margin-top: 1.5rem;
  text-align: center;
  color: rgba(255, 255, 255, 0.7);
  font-size: 0.9rem;
}

.link-btn {
  background: none;
  border: none;
  color: var(--color-orange);
  cursor: pointer;
  font-weight: 600;
  padding: 0 4px;
  transition: color 0.3s ease;
}

.link-btn:hover {
  color: #ff9f43;
  text-decoration: underline;
}

/* 注册弹窗样式 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.8);
  backdrop-filter: blur(5px);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  width: 90%;
  max-width: 450px;
  padding: 2rem;
  max-height: 90vh;
  overflow-y: auto;
  background: rgba(30, 30, 30, 0.9);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 16px;
  box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.5);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.modal-header h3 {
  margin: 0;
  color: #ffffff;
  font-size: 1.4rem;
}

.close-btn {
  background: none;
  border: none;
  color: rgba(255, 255, 255, 0.7);
  cursor: pointer;
  font-size: 1.2rem;
  padding: 4px;
  border-radius: 50%;
  transition: all 0.3s ease;
}

.close-btn:hover {
  background: rgba(255, 255, 255, 0.1);
  color: #ffffff;
}

.form-actions {
  display: flex;
  gap: 1rem;
  margin-top: 2rem;
}

.form-actions button {
  flex: 1;
}

.glass-btn {
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: white;
  padding: 0.8rem;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.glass-btn:hover {
  background: rgba(255, 255, 255, 0.2);
}

.glass-btn.primary-btn {
  background: var(--color-accent);
  border: none;
}

.glass-btn.primary-btn:hover {
  background: var(--color-accent-hover);
}

.hint-text {
  display: flex;
  align-items: center;
  gap: 4px;
  margin-top: 0.5rem;
  font-size: 0.8rem;
  color: rgba(255, 255, 255, 0.6);
}

/* 响应式设计 */
@media (max-width: 480px) {
  .login-card {
    width: 90%;
    padding: 2rem 1.5rem;
  }
  
  .card-header h1 {
    font-size: 1.5rem;
  }
}
</style>

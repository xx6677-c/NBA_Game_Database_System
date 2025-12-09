<template>
  <div id="app">
    <Navbar v-if="isAuthenticated" />
    <div class="app-content" :class="{ 'with-navbar': isAuthenticated }">
      <router-view />
    </div>
  </div>
</template>

<script>
import Navbar from './components/Navbar.vue'

export default {
  name: 'App',
  components: {
    Navbar
  },
  data() {
    return {
      isAuthenticated: false
    }
  },
  mounted() {
    this.checkAuth()
    // 监听登录状态变化
    window.addEventListener('storage', this.checkAuth)
    window.addEventListener('userInfoChanged', this.checkAuth)
    window.addEventListener('userLogout', this.checkAuth)
  },
  beforeUnmount() {
    window.removeEventListener('storage', this.checkAuth)
    window.removeEventListener('userInfoChanged', this.checkAuth)
    window.removeEventListener('userLogout', this.checkAuth)
  },
  methods: {
    checkAuth() {
      this.isAuthenticated = localStorage.getItem('token') !== null
    }
  }
}
</script>

<style>
#app {
  height: 100vh;
  overflow: hidden;
  /* Premium Dark Theme Background - Slightly Lighter Overlay */
  background-image: linear-gradient(rgba(10, 14, 23, 0.65), rgba(10, 14, 23, 0.5)), url('./assets/background.png');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
}

.app-content {
  height: 100vh;
  overflow-y: auto;
}

.app-content.with-navbar {
  height: calc(100vh - 70px);
  margin-top: 70px;
}
</style>

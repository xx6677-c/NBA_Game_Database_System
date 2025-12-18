<template>
  <div class="dashboard">
    <!-- 页面标题 -->
    <div class="dashboard-header">
      <h1>NBA 赛事中心</h1>
      <p>实时掌握赛事动态，分享精彩瞬间</p>
    </div>

    <!-- 主要内容区域 -->
    <div class="main-content">
      <!-- 左侧区域 -->
      <div class="left-section">
        <!-- 快速导航按钮 -->
        <div class="navigation-section">
          <div class="nav-buttons">
            <router-link to="/games" class="nav-btn glass-card">
              <div class="nav-icon-wrapper">
                <el-icon><Calendar /></el-icon>
              </div>
              <span>赛程表</span>
            </router-link>
            <router-link to="/rankings" class="nav-btn glass-card">
              <div class="nav-icon-wrapper">
                <el-icon><TrendCharts /></el-icon>
              </div>
              <span>数据榜</span>
            </router-link>
            <router-link to="/teams" class="nav-btn glass-card">
              <div class="nav-icon-wrapper">
                <el-icon><Basketball /></el-icon>
              </div>
              <span>球队库</span>
            </router-link>
          </div>
        </div>

        <!-- 比赛信息区域 -->
        <div class="games-section glass-card">
          <div class="section-header">
            <div class="header-title">
              <el-icon class="header-icon"><Trophy /></el-icon>
              <h2>赛事精选</h2>
            </div>
          </div>
          
          <div class="games-grid">
            <!-- 最近已结束的比赛 -->
            <div class="game-category">
              <div class="category-header">
                <el-icon><Timer /></el-icon>
                <h3>最近结束</h3>
              </div>
              <div v-if="finishedGames.length === 0" class="empty-state">
                <p>暂无已结束比赛</p>
              </div>
              <div v-else class="games-list">
                <div 
                  v-for="game in finishedGames" 
                  :key="game.game_id" 
                  class="game-card finished"
                >
                  <div class="game-layout">
                    <div class="team-logo-side">
                      <img v-if="game.home_logo_url" :src="game.home_logo_url" class="team-logo" alt="Home Logo" />
                      <div v-else class="team-logo-placeholder">
                        <el-icon><Basketball /></el-icon>
                      </div>
                    </div>
                    
                    <div class="game-center">
                      <div class="teams-row">
                        <span class="team-name home">{{ game.home_team }}</span>
                        <span class="vs-badge">VS</span>
                        <span class="team-name away">{{ game.away_team }}</span>
                      </div>
                      <div class="score-row">
                        <span class="score">{{ game.home_score || 0 }}</span>
                        <span class="score-divider">:</span>
                        <span class="score">{{ game.away_score || 0 }}</span>
                      </div>
                    </div>

                    <div class="team-logo-side">
                      <img v-if="game.away_logo_url" :src="game.away_logo_url" class="team-logo" alt="Away Logo" />
                      <div v-else class="team-logo-placeholder">
                        <el-icon><Basketball /></el-icon>
                      </div>
                    </div>
                  </div>
                  
                  <div class="game-info">
                    <span class="date">{{ formatDate(game.date) }}</span>
                    <span class="winner" v-if="game.winner_team">
                      <el-icon><Medal /></el-icon> {{ game.winner_team }}
                    </span>
                  </div>
                </div>
              </div>
            </div>

            <!-- 即将开始的比赛 -->
            <div class="game-category">
              <div class="category-header">
                <el-icon><AlarmClock /></el-icon>
                <h3>即将开赛</h3>
              </div>
              <div v-if="upcomingGames.length === 0" class="empty-state">
                <p>暂无即将开始的比赛</p>
              </div>
              <div v-else class="games-list">
                <div 
                  v-for="game in upcomingGames" 
                  :key="game.game_id" 
                  class="game-card upcoming"
                >
                  <div class="game-layout">
                    <div class="team-logo-side">
                      <img v-if="game.home_logo_url" :src="game.home_logo_url" class="team-logo" alt="Home Logo" />
                      <div v-else class="team-logo-placeholder">
                        <el-icon><Basketball /></el-icon>
                      </div>
                    </div>
                    
                    <div class="game-center">
                      <div class="teams-row">
                        <span class="team-name home">{{ game.home_team }}</span>
                        <span class="vs-badge">VS</span>
                        <span class="team-name away">{{ game.away_team }}</span>
                      </div>
                      <div class="time-row">
                        <span class="time">未开始</span>
                      </div>
                    </div>

                    <div class="team-logo-side">
                      <img v-if="game.away_logo_url" :src="game.away_logo_url" class="team-logo" alt="Away Logo" />
                      <div v-else class="team-logo-placeholder">
                        <el-icon><Basketball /></el-icon>
                      </div>
                    </div>
                  </div>

                  <div class="game-info">
                    <span class="date">{{ formatDate(game.date) }}</span>
                    <span class="venue" v-if="game.venue">
                      <el-icon><Location /></el-icon> {{ game.venue }}
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 右侧帖子区域 -->
      <div class="right-section">
        <div class="posts-section glass-card">
          <div class="section-header">
            <div class="header-title">
              <el-icon class="header-icon"><ChatDotRound /></el-icon>
              <h2>社区动态</h2>
            </div>
            <router-link to="/posts" class="view-all-link">
              查看全部 <el-icon><ArrowRight /></el-icon>
            </router-link>
          </div>
          
          <div v-if="recentPosts.length === 0" class="empty-state">
            <p>暂无帖子，快来发表第一条帖子吧！</p>
          </div>
          <div v-else class="posts-list">
            <div 
              v-for="post in recentPosts" 
              :key="post.post_id" 
              class="post-card-item"
              @click="goToPost(post.post_id)"
            >
              <div class="post-main-content">
                <div class="post-header">
                  <h4 class="post-title">{{ post.title }}</h4>
                  <div class="post-meta">
                    <span class="author">{{ post.username }}</span>
                    <span class="time">{{ formatRelativeTime(post.create_time) }}</span>
                  </div>
                </div>
                <!-- 首页只显示标题和图片，隐藏内容摘要 -->
                <!-- <div class="post-content">
                  <p>{{ truncateContent(post.content) }}</p>
                </div> -->
                <div class="post-stats">
                  <span class="stat"><el-icon><View /></el-icon> {{ post.view_count || 0 }}</span>
                  <span class="stat"><el-icon><Star /></el-icon> {{ post.like_count || 0 }}</span>
                  <span class="stat" v-if="post.comment_count"><el-icon><ChatLineSquare /></el-icon> {{ post.comment_count }}</span>
                </div>
              </div>
              <div class="post-image-placeholder">
                <img v-if="post.image_url" :src="post.image_url" class="post-image-thumb" alt="Post Image">
                <el-icon v-else><Picture /></el-icon>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 功能提示弹窗 -->
    <div v-if="showComingSoonModal" class="modal-overlay" @click="closeComingSoon">
      <div class="modal glass-card" @click.stop>
        <div class="modal-icon">
          <el-icon><Warning /></el-icon>
        </div>
        <h3>功能开发中</h3>
        <p>{{ comingSoonFeature }} 功能即将推出，敬请期待！</p>
        <button @click="closeComingSoon" class="btn btn-primary">知道了</button>
      </div>
    </div>
  </div>
</template>

<script>
import api from '../services/api'

export default {
  name: 'Dashboard',
  data() {
    return {
      finishedGames: [],
      upcomingGames: [],
      recentPosts: [],
      showComingSoonModal: false,
      comingSoonFeature: ''
    }
  },
  async created() {
    await this.loadData()
  },
  methods: {
    async loadData() {
      try {
        // 并行加载数据
        const [games, posts] = await Promise.all([
          api.getGames(),
          api.getPosts()
        ])
        
        // 处理比赛数据
        const now = new Date()
        const sortedGames = games.sort((a, b) => new Date(b.date) - new Date(a.date))
        
        this.finishedGames = sortedGames
          .filter(g => new Date(g.date) < now)
          .slice(0, 4)
          
        this.upcomingGames = sortedGames
          .filter(g => new Date(g.date) >= now)
          .sort((a, b) => new Date(a.date) - new Date(b.date))
          .slice(0, 4)
          
        // 处理帖子数据
        this.recentPosts = posts.slice(0, 5)
      } catch (error) {
        console.error('加载数据失败:', error)
      }
    },
    formatDate(dateStr) {
      const date = new Date(dateStr)
      return `${date.getMonth() + 1}月${date.getDate()}日`
    },
    formatRelativeTime(dateStr) {
      const date = new Date(dateStr)
      const now = new Date()
      const diff = now - date
      
      const minutes = Math.floor(diff / 60000)
      const hours = Math.floor(diff / 3600000)
      const days = Math.floor(diff / 86400000)
      
      if (minutes < 1) return '刚刚'
      if (minutes < 60) return `${minutes}分钟前`
      if (hours < 24) return `${hours}小时前`
      if (days < 30) return `${days}天前`
      return `${date.getMonth() + 1}月${date.getDate()}日`
    },
    truncateContent(content) {
      if (!content) return ''
      return content.length > 60 ? content.substring(0, 60) + '...' : content
    },
    goToPost(postId) {
      this.$router.push(`/posts?id=${postId}`)
    },
    showComingSoon(feature) {
      this.comingSoonFeature = feature
      this.showComingSoonModal = true
    },
    closeComingSoon() {
      this.showComingSoonModal = false
    }
  }
}
</script>

<style scoped>
.dashboard {
  max-width: 1200px;
  margin: 0 auto;
  padding: 1rem;
}

/* 页面标题 */
.dashboard-header {
  text-align: center;
  margin-bottom: 1.5rem;
}

.dashboard-header h1 {
  display: inline-block;
  color: #ffffff;
  background: linear-gradient(135deg, rgba(20, 20, 30, 0.9), rgba(10, 14, 23, 0.95));
  padding: 1rem 3rem;
  border-radius: 8px;
  border: 1px solid rgba(212, 175, 55, 0.5);
  box-shadow: 0 0 30px rgba(212, 175, 55, 0.2);
  font-size: 2.2rem;
  font-weight: 800;
  letter-spacing: 3px;
  margin-bottom: 0.5rem;
  text-transform: uppercase;
  font-style: italic;
  text-shadow: 0 2px 10px rgba(0,0,0,0.5);
  position: relative;
}

.dashboard-header h1::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 60%;
  height: 2px;
  background: linear-gradient(90deg, transparent, #d4af37, transparent);
}

.dashboard-header p {
  font-size: 1.2rem;
  color: rgba(255, 255, 255, 0.8);
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 2px;
  text-shadow: 0 2px 4px rgba(0,0,0,0.5);
}

/* 布局 */
.main-content {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  padding-bottom: 0.75rem;
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
}

.header-title {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.header-icon {
  font-size: 1.5rem;
  color: var(--color-accent);
}

.section-header h2 {
  font-size: 1.25rem;
  margin: 0;
}

/* 比赛卡片 */
.games-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.category-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.75rem;
  color: var(--color-text-secondary);
  font-size: 0.85rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.games-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.game-card {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  padding: 0.75rem;
  border: 1px solid rgba(255, 255, 255, 0.1);
  transition: all 0.2s ease;
}

.game-card:hover {
  background: rgba(255, 255, 255, 0.1);
  border-color: var(--color-accent);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.game-layout {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 0.75rem;
  padding: 0 0.5rem;
}

.team-logo-side {
  flex: 0 0 40px;
  display: flex;
  justify-content: center;
}

.team-logo {
  width: 40px;
  height: 40px;
  object-fit: contain;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.team-logo-placeholder {
  width: 40px;
  height: 40px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--color-accent);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.game-center {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.25rem;
  padding: 0 1rem;
}

.teams-row {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  width: 100%;
}

.team-name {
  font-weight: 600;
  font-size: 0.95rem;
  color: var(--color-text-primary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 100px;
}

.team-name.home {
  text-align: right;
}

.team-name.away {
  text-align: left;
}

.vs-badge {
  font-size: 0.75rem;
  font-weight: 700;
  color: var(--color-text-secondary);
  background: rgba(255, 255, 255, 0.1);
  padding: 0.1rem 0.4rem;
  border-radius: 8px;
}

.score-row, .time-row {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.score {
  font-size: 1.2rem;
  font-weight: 700;
  color: var(--color-accent);
}

.score-divider {
  color: var(--color-text-secondary);
  font-weight: 600;
}

.time {
  font-size: 0.9rem;
  color: var(--color-text-secondary);
}

.game-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.8rem;
  color: var(--color-text-secondary);
  padding-top: 0.75rem;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.winner, .venue {
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

/* 导航按钮 */
.navigation-section {
  margin-bottom: 1.5rem;
}

.nav-buttons {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
}

.nav-btn {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 1rem;
  text-decoration: none;
  color: var(--color-text-primary);
  transition: all 0.2s ease;
  border: none;
  cursor: pointer;
}

.nav-btn:hover:not(.disabled) {
  transform: translateY(-4px);
  background: rgba(255, 255, 255, 0.1);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.08);
}

.nav-icon-wrapper {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 0.75rem;
  font-size: 1.5rem;
  color: var(--color-accent);
}

.nav-btn span {
  font-weight: 500;
  font-size: 0.95rem;
}

.nav-btn.disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* 帖子列表 */
.view-all-link {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  font-size: 0.85rem;
  color: var(--color-accent);
  text-decoration: none;
  font-weight: 500;
  transition: opacity 0.2s;
}

.view-all-link:hover {
  opacity: 0.7;
}

.post-card-item {
  padding: 1rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  cursor: pointer;
  transition: background 0.2s;
  display: flex;
  gap: 1rem;
  align-items: flex-start;
}

.post-main-content {
  flex: 1;
}

.post-image-placeholder {
  width: 120px;
  height: 80px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--color-text-secondary);
  font-size: 0.8rem;
  border: 1px dashed rgba(255, 255, 255, 0.1);
  overflow: hidden;
}

.post-image-thumb {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.post-card-item:last-child {
  border-bottom: none;
}

.post-card-item:hover {
  background: rgba(255, 255, 255, 0.05);
}

.post-title {
  font-size: 1rem;
  margin: 0 0 0.25rem 0;
  line-height: 1.3;
  color: var(--color-text-primary);
}

.post-meta {
  font-size: 0.8rem;
  color: var(--color-text-secondary);
  margin-bottom: 0.5rem;
}

.author {
  font-weight: 500;
  color: var(--color-text-primary);
  margin-right: 0.5rem;
}

.post-content p {
  font-size: 0.9rem;
  color: var(--color-text-secondary);
  line-height: 1.5;
  margin-bottom: 0.5rem;
}

.post-stats {
  display: flex;
  gap: 1.5rem;
}

.stat {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  font-size: 0.85rem;
  color: var(--color-text-secondary);
}

/* 弹窗 */
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
  z-index: 2000;
}

.modal {
  width: 90%;
  max-width: 320px;
  padding: 2rem;
  text-align: center;
  background: var(--color-surface);
  border: 2px solid var(--color-accent);
}

.modal-icon {
  font-size: 3rem;
  color: #ff9f0a;
  margin-bottom: 1rem;
}

.modal h3 {
  margin-bottom: 0.5rem;
}

.modal p {
  margin-bottom: 1.5rem;
}

/* 响应式 */
@media (max-width: 900px) {
  .main-content {
    grid-template-columns: 1fr;
  }
  
  .games-grid {
    grid-template-columns: 1fr;
  }
}
</style>
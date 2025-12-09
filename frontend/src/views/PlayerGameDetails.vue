<template>
  <div class="player-detail-container">
    <div v-if="loading" class="loading-state">
      <el-icon class="is-loading"><Loading /></el-icon>
      <p>加载中...</p>
    </div>

    <template v-else-if="stats">
      <!-- Header -->
      <div class="detail-header glass-card">
        <div class="header-top">
          <button @click="$router.go(-1)" class="back-btn">
            <el-icon><ArrowLeft /></el-icon>
          </button>
          <div class="match-score">
            <span class="team-logo">{{ stats.team_name[0] }}</span>
            <span class="score-text">{{ stats.team_name }} vs {{ opponentName }}</span>
          </div>
        </div>
        
        <div class="player-profile">
          <div class="avatar-large">
            <img src="/images/default-avatar.png" alt="avatar" @error="handleImageError">
          </div>
          <div class="profile-info">
            <h1>{{ stats.player_name }}</h1>
            <p>{{ stats.team_name }} | #{{ stats.jersey_number }} | {{ stats.position }}</p>
          </div>
        </div>

        <!-- Stats Grid -->
        <div class="stats-grid">
          <div class="stat-item">
            <span class="stat-value">{{ stats.playing_time }}</span>
            <span class="stat-label">时间</span>
          </div>
          <div class="stat-item highlight">
            <span class="stat-value">{{ stats.points }}</span>
            <span class="stat-label">得分</span>
          </div>
          <div class="stat-item">
            <span class="stat-value">{{ stats.rebounds }}</span>
            <span class="stat-label">篮板</span>
          </div>
          <div class="stat-item">
            <span class="stat-value">{{ stats.assists }}</span>
            <span class="stat-label">助攻</span>
          </div>
          <div class="stat-item">
            <span class="stat-value">{{ stats.steals }}</span>
            <span class="stat-label">抢断</span>
          </div>
          <div class="stat-item">
            <span class="stat-value">{{ stats.blocks }}</span>
            <span class="stat-label">盖帽</span>
          </div>
          <div class="stat-item">
            <span class="stat-value">{{ stats.plus_minus > 0 ? '+' + stats.plus_minus : stats.plus_minus }}</span>
            <span class="stat-label">+/-</span>
          </div>
        </div>
      </div>

      <!-- Rating Section -->
      <div class="rating-section glass-card">
        <div class="rating-header">
          <h2>评分</h2>
          <div class="rating-summary">
            <span class="big-score">{{ stats.avg_rating.toFixed(1) }}</span>
            <span class="total-ratings">{{ stats.rating_count }}人评分</span>
          </div>
        </div>
        
        <div class="user-rating-action">
          <span>立即评分</span>
          <el-rate 
            v-model="tempRating" 
            :max="5" 
            :colors="['#99A9BF', '#F7BA2A', '#FF9900']"
            @change="submitRating"
            :disabled="!currentUser"
            size="large"
          />
        </div>
      </div>

      <!-- Comments Section -->
      <div class="comments-section">
        <div class="section-title">
          <h3>亮回复 / {{ comments.length }}</h3>
        </div>

        <div class="comments-list">
          <div v-for="comment in comments" :key="comment.comment_id" class="comment-item glass-card">
            <div class="comment-header">
              <span class="username">{{ comment.username }}</span>
              <span class="time">{{ comment.created_at }}</span>
            </div>
            <div class="comment-content">{{ comment.content }}</div>
          </div>
        </div>

        <!-- Add Comment -->
        <div class="add-comment glass-card">
          <textarea 
            v-model="newComment" 
            placeholder="认真表达，这里总有人聆听" 
            rows="3"
            class="glass-input"
          ></textarea>
          <button @click="submitComment" class="glass-btn primary-btn" :disabled="!newComment.trim()">
            发布
          </button>
        </div>
      </div>
    </template>
  </div>
</template>

<script>
import api from '../services/api'
import { Loading, ArrowLeft } from '@element-plus/icons-vue'

export default {
  name: 'PlayerGameDetails',
  components: { Loading, ArrowLeft },
  data() {
    return {
      stats: null,
      comments: [],
      loading: true,
      tempRating: 0,
      newComment: '',
      currentUser: null,
      opponentName: '对手' // This would ideally come from API
    }
  },
  async mounted() {
    this.currentUser = JSON.parse(localStorage.getItem('user') || 'null')
    await this.loadData()
  },
  methods: {
    async loadData() {
      this.loading = true
      const { gameId, playerId } = this.$route.params
      try {
        const [playerData, gameData] = await Promise.all([
          api.getPlayerGameDetail(gameId, playerId),
          api.getGameDetail(gameId)
        ])
        
        this.stats = playerData.stats
        this.comments = playerData.comments
        this.tempRating = playerData.stats.user_rating ? playerData.stats.user_rating / 2 : 0
        
        // Determine opponent
        if (this.stats.team_id === gameData.home_team_id) {
          this.opponentName = gameData.away_team
        } else {
          this.opponentName = gameData.home_team
        }
      } catch (error) {
        console.error('加载数据失败:', error)
      } finally {
        this.loading = false
      }
    },
    async submitRating(stars) {
      if (!this.currentUser) {
        alert('请先登录')
        return
      }
      try {
        const score = stars * 2
        const { gameId, playerId } = this.$route.params
        await api.submitRating(gameId, playerId, score)
        // Reload to update average
        const data = await api.getPlayerGameDetail(gameId, playerId)
        this.stats.avg_rating = data.stats.avg_rating
        this.stats.rating_count = data.stats.rating_count
      } catch (error) {
        console.error('评分失败:', error)
      }
    },
    async submitComment() {
      if (!this.currentUser) {
        alert('请先登录')
        return
      }
      try {
        const { gameId, playerId } = this.$route.params
        await api.submitPlayerComment(gameId, playerId, this.newComment)
        this.newComment = ''
        await this.loadData() // Reload comments
      } catch (error) {
        console.error('评论失败:', error)
        alert('评论失败')
      }
    },
    handleImageError(e) {
      e.target.src = 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png'
    }
  }
}
</script>

<style scoped>
.player-detail-container {
  padding: var(--spacing-md);
  max-width: 800px;
  margin: 0 auto;
}

.detail-header {
  padding: var(--spacing-lg);
  margin-bottom: var(--spacing-md);
}

.header-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-lg);
}

.back-btn {
  background: none;
  border: none;
  color: var(--text-primary);
  font-size: 1.5rem;
  cursor: pointer;
}

.player-profile {
  display: flex;
  align-items: center;
  gap: var(--spacing-lg);
  margin-bottom: var(--spacing-xl);
}

.avatar-large img {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  object-fit: cover;
  border: 3px solid var(--accent-color);
}

.profile-info h1 {
  font-size: 1.8rem;
  margin-bottom: var(--spacing-xs);
}

.profile-info p {
  color: var(--text-secondary);
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: var(--spacing-sm);
  text-align: center;
}

.stat-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.stat-value {
  font-size: 1.2rem;
  font-weight: bold;
}

.stat-label {
  font-size: 0.8rem;
  color: var(--text-secondary);
}

.rating-section {
  padding: var(--spacing-lg);
  margin-bottom: var(--spacing-md);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.rating-summary {
  display: flex;
  align-items: baseline;
  gap: var(--spacing-sm);
}

.big-score {
  font-size: 2.5rem;
  font-weight: 800;
  color: var(--accent-color);
}

.user-rating-action {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: var(--spacing-xs);
}

.comments-section {
  margin-top: var(--spacing-xl);
}

.section-title {
  margin-bottom: var(--spacing-md);
  font-size: 1.1rem;
  font-weight: bold;
}

.comment-item {
  padding: var(--spacing-md);
  margin-bottom: var(--spacing-md);
}

.comment-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: var(--spacing-sm);
  font-size: 0.9rem;
}

.username {
  font-weight: bold;
  color: var(--accent-color);
}

.time {
  color: var(--text-secondary);
}

.add-comment {
  padding: var(--spacing-md);
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
}

.add-comment textarea {
  width: 100%;
  resize: vertical;
  min-height: 80px;
}

.add-comment button {
  align-self: flex-end;
  padding: 8px 24px;
}

@media (max-width: 600px) {
  .stats-grid {
    grid-template-columns: repeat(4, 1fr);
    gap: var(--spacing-md);
  }
  
  .rating-section {
    flex-direction: column;
    align-items: flex-start;
    gap: var(--spacing-md);
  }
  
  .user-rating-action {
    align-items: flex-start;
  }
}
</style>
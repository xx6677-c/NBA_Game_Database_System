<template>
  <div class="game-details-container">
    <div v-if="loading" class="loading-state">
      <el-icon class="is-loading"><Loading /></el-icon>
      <p>加载中...</p>
    </div>

    <template v-else-if="game">
      <!-- Game Header -->
      <div class="game-header glass-card">
        <div class="team-section home">
          <div class="team-logo-placeholder">{{ game.home_team[0] }}</div>
          <span class="team-name">{{ game.home_team }}</span>
          <span class="score">{{ game.home_score !== null ? game.home_score : '-' }}</span>
        </div>
        
        <div class="game-info">
          <div class="status-badge" :class="game.status === '已结束' ? 'finished' : 'upcoming'">
            {{ game.status }}
          </div>
          <div class="date">{{ game.date }}</div>
          <div class="venue">{{ game.venue }}</div>
        </div>
        
        <div class="team-section away">
          <span class="score">{{ game.away_score !== null ? game.away_score : '-' }}</span>
          <span class="team-name">{{ game.away_team }}</span>
          <div class="team-logo-placeholder">{{ game.away_team[0] }}</div>
        </div>
      </div>

      <!-- Prediction Section -->
      <div class="prediction-section glass-card" v-if="game.prediction">
        <h3>
          <el-icon><Trophy /></el-icon> 胜负竞猜
          <span class="vote-count">({{ game.prediction.total_votes }} 人参与)</span>
        </h3>
        
        <!-- 投票按钮 (未开始且未投票) -->
        <div v-if="game.status === '未开始'" class="vote-buttons">
          <button 
            class="vote-btn home-btn" 
            :class="{ active: game.user_prediction === game.home_team_id }"
            @click="handleVote(game.home_team_id)"
          >
            支持 {{ game.home_team }}
            <el-icon v-if="game.user_prediction === game.home_team_id"><Select /></el-icon>
          </button>
          
          <div class="vs-text">VS</div>
          
          <button 
            class="vote-btn away-btn" 
            :class="{ active: game.user_prediction === game.away_team_id }"
            @click="handleVote(game.away_team_id)"
          >
            支持 {{ game.away_team }}
            <el-icon v-if="game.user_prediction === game.away_team_id"><Select /></el-icon>
          </button>
        </div>

        <!-- 进度条 (已结束或已投票) -->
        <div class="prediction-bar-container">
          <div class="prediction-bar">
            <div 
              class="bar-segment home" 
              :style="{ width: game.prediction.home_percent + '%' }"
            >
              <span v-if="game.prediction.home_percent > 10">{{ game.prediction.home_percent }}%</span>
            </div>
            <div 
              class="bar-segment away" 
              :style="{ width: game.prediction.away_percent + '%' }"
            >
              <span v-if="game.prediction.away_percent > 10">{{ game.prediction.away_percent }}%</span>
            </div>
          </div>
          <div class="bar-labels">
            <span :class="{ highlight: game.user_prediction === game.home_team_id }">
              {{ game.home_team }}
              <span v-if="game.user_prediction === game.home_team_id">(已投)</span>
            </span>
            <span :class="{ highlight: game.user_prediction === game.away_team_id }">
              {{ game.away_team }}
              <span v-if="game.user_prediction === game.away_team_id">(已投)</span>
            </span>
          </div>
        </div>

        <!-- 结果展示 (已结束) -->
        <div v-if="game.status === '已结束' && game.user_prediction" class="prediction-result">
          <div v-if="game.user_prediction === game.winner_team_id" class="result-container">
            <div class="result-badge win">
              <el-icon><Medal /></el-icon> 恭喜你猜对了！
            </div>
            
            <button 
              v-if="!game.is_claimed" 
              class="claim-btn" 
              @click="handleClaim"
              :disabled="claiming"
            >
              <el-icon><Present /></el-icon> 领取 100 积分
            </button>
            <div v-else class="claimed-badge">
              <el-icon><Check /></el-icon> 奖励已领取
            </div>
          </div>
          
          <div v-else class="result-badge lose">
            <el-icon><CloseBold /></el-icon> 很遗憾猜错了
          </div>
        </div>
      </div>

      <!-- Tabs -->
      <div class="tabs-container">
        <button 
          :class="['tab-btn', { active: activeTab === 'stats' }]" 
          @click="activeTab = 'stats'"
        >
          数据统计
        </button>
        <button 
          :class="['tab-btn', { active: activeTab === 'ratings' }]" 
          @click="activeTab = 'ratings'"
        >
          评分
        </button>
      </div>

      <!-- Stats View -->
      <div v-if="activeTab === 'stats'" class="tab-content">
        <div class="stats-section glass-card">
          <h3>{{ game.home_team }} 数据</h3>
          <div class="table-responsive">
            <table class="stats-table">
              <thead>
                <tr>
                  <th>球员</th>
                  <th>时间</th>
                  <th>得分</th>
                  <th>篮板</th>
                  <th>助攻</th>
                  <th>抢断</th>
                  <th>盖帽</th>
                  <th>失误</th>
                  <th>犯规</th>
                  <th>+/-</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="player in homeStats" :key="player.player_id">
                  <td>{{ player.player_name }}</td>
                  <td>{{ player.playing_time }}</td>
                  <td>{{ player.points }}</td>
                  <td>{{ player.rebounds }}</td>
                  <td>{{ player.assists }}</td>
                  <td>{{ player.steals }}</td>
                  <td>{{ player.blocks }}</td>
                  <td>{{ player.turnovers }}</td>
                  <td>{{ player.fouls }}</td>
                  <td>{{ player.plus_minus }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <div class="stats-section glass-card">
          <h3>{{ game.away_team }} 数据</h3>
          <div class="table-responsive">
            <table class="stats-table">
              <thead>
                <tr>
                  <th>球员</th>
                  <th>时间</th>
                  <th>得分</th>
                  <th>篮板</th>
                  <th>助攻</th>
                  <th>抢断</th>
                  <th>盖帽</th>
                  <th>失误</th>
                  <th>犯规</th>
                  <th>+/-</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="player in awayStats" :key="player.player_id">
                  <td>{{ player.player_name }}</td>
                  <td>{{ player.playing_time }}</td>
                  <td>{{ player.points }}</td>
                  <td>{{ player.rebounds }}</td>
                  <td>{{ player.assists }}</td>
                  <td>{{ player.steals }}</td>
                  <td>{{ player.blocks }}</td>
                  <td>{{ player.turnovers }}</td>
                  <td>{{ player.fouls }}</td>
                  <td>{{ player.plus_minus }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <!-- Ratings View -->
      <div v-if="activeTab === 'ratings'" class="tab-content ratings-layout">
        <div class="team-column">
          <h3 class="column-header">{{ game.home_team }}</h3>
          <div class="players-list">
            <div 
              v-for="player in homeRatings" 
              :key="player.player_id" 
              class="player-rating-card glass-card"
              @click="goToPlayerDetail(player.player_id)"
            >
              <div class="player-avatar">
                <img v-if="player.photo_url" :src="player.photo_url" alt="avatar" @error="handleImageError">
                <div v-else class="avatar-placeholder">
                  <el-icon><User /></el-icon>
                </div>
              </div>
              <div class="player-info">
                <div class="player-name">{{ player.name }}</div>
                <div class="rating-display">
                  <span class="avg-score">{{ player.avg_rating.toFixed(1) }}</span>
                  <span class="rating-count">{{ player.rating_count }}人评分</span>
                </div>
                <div class="user-rating" @click.stop>
                  <el-rate 
                    v-model="player.tempRating" 
                    :max="5" 
                    :colors="['#99A9BF', '#F7BA2A', '#FF9900']"
                    @change="(val) => submitRating(player, val)"
                    :disabled="!currentUser"
                  />
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="team-column">
          <h3 class="column-header">{{ game.away_team }}</h3>
          <div class="players-list">
            <div 
              v-for="player in awayRatings" 
              :key="player.player_id" 
              class="player-rating-card glass-card"
              @click="goToPlayerDetail(player.player_id)"
            >
              <div class="player-avatar">
                <img v-if="player.photo_url" :src="player.photo_url" alt="avatar" @error="handleImageError">
                <div v-else class="avatar-placeholder">
                  <el-icon><User /></el-icon>
                </div>
              </div>
              <div class="player-info">
                <div class="player-name">{{ player.name }}</div>
                <div class="rating-display">
                  <span class="avg-score">{{ player.avg_rating.toFixed(1) }}</span>
                  <span class="rating-count">{{ player.rating_count }}人评分</span>
                </div>
                <div class="user-rating" @click.stop>
                  <el-rate 
                    v-model="player.tempRating" 
                    :max="5" 
                    :colors="['#99A9BF', '#F7BA2A', '#FF9900']"
                    @change="(val) => submitRating(player, val)"
                    :disabled="!currentUser"
                  />
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </template>
    
    <div v-else class="empty-state">
      <el-empty description="未找到比赛信息" />
    </div>
  </div>
</template>

<script>
import api from '../services/api'
import { Loading, Trophy, Select, Medal, Present, Check, CloseBold, User } from '@element-plus/icons-vue'

export default {
  name: 'GameDetails',
  components: { 
    Loading,
    Trophy,
    Select,
    Medal,
    Present,
    Check,
    CloseBold,
    User
  },
  data() {
    return {
      game: null,
      loading: true,
      activeTab: 'stats',
      ratings: [],
      currentUser: null,
      claiming: false
    }
  },
  computed: {
    homeStats() {
      if (!this.game || !this.game.player_stats) return []
      return this.game.player_stats.filter(p => p.team_id === this.game.home_team_id)
    },
    awayStats() {
      if (!this.game || !this.game.player_stats) return []
      return this.game.player_stats.filter(p => p.team_id === this.game.away_team_id)
    },
    homeRatings() {
      if (!this.game) return []
      return this.ratings.filter(p => p.team_id === this.game.home_team_id)
    },
    awayRatings() {
      if (!this.game) return []
      return this.ratings.filter(p => p.team_id === this.game.away_team_id)
    }
  },
  async mounted() {
    this.currentUser = JSON.parse(localStorage.getItem('user') || 'null')
    await this.loadData()
  },
  methods: {
    async loadData() {
      this.loading = true
      const gameId = this.$route.params.id
      try {
        const [gameData, ratingsData] = await Promise.all([
          api.getGameDetail(gameId),
          api.getGameRatings(gameId)
        ])
        this.game = gameData
        
        // Process ratings to add tempRating for v-model
        this.ratings = ratingsData.map(r => ({
          ...r,
          tempRating: r.user_rating ? r.user_rating / 2 : 0 // Convert 10-point scale to 5-star
        }))
      } catch (error) {
        console.error('加载数据失败:', error)
      } finally {
        this.loading = false
      }
    },
    async handleVote(teamId) {
      if (!this.currentUser) {
        alert('请先登录参与竞猜')
        return
      }
      
      try {
        await api.predictGame(this.game.game_id, teamId)
        alert('投票成功')
        await this.loadData() // 重新加载数据以更新进度条
      } catch (error) {
        console.error('投票失败:', error)
        alert(error.message || '投票失败')
      }
    },
    async handleClaim() {
      if (this.claiming) return
      this.claiming = true
      
      try {
        const result = await api.claimReward(this.game.game_id)
        alert(result.message)
        this.game.is_claimed = true
        
        // 更新本地存储的用户积分
        if (result.points) {
          const user = JSON.parse(localStorage.getItem('user'))
          if (user) {
            user.points = (user.points || 0) + result.points
            localStorage.setItem('user', JSON.stringify(user))
          }
        }
      } catch (error) {
        console.error('领取失败:', error)
        alert(error.message || '领取失败')
      } finally {
        this.claiming = false
      }
    },
    async submitRating(player, stars) {
      if (!this.currentUser) {
        alert('请先登录')
        return
      }
      try {
        const score = stars * 2 // Convert 5-star to 10-point
        await api.submitRating(this.game.game_id, player.player_id, score)
        // Refresh ratings to update average
        const ratingsData = await api.getGameRatings(this.game.game_id)
        this.ratings = ratingsData.map(r => ({
          ...r,
          tempRating: r.user_rating ? r.user_rating / 2 : 0
        }))
      } catch (error) {
        console.error('评分失败:', error)
        alert('评分失败')
      }
    },
    goToPlayerDetail(playerId) {
      this.$router.push(`/games/${this.game.game_id}/players/${playerId}`)
    },
    handleImageError(e) {
      e.target.src = 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png'
    }
  }
}
</script>

<style scoped>
.game-details-container {
  padding: var(--spacing-lg);
  max-width: 1200px;
  margin: 0 auto;
}

.game-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--spacing-xl);
  margin-bottom: var(--spacing-xl);
}

.team-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--spacing-sm);
  flex: 1;
}

.team-logo-placeholder {
  width: 80px;
  height: 80px;
  background: rgba(255,255,255,0.1);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2rem;
  font-weight: bold;
  color: var(--accent-color);
}

.team-name {
  font-size: 1.2rem;
  font-weight: bold;
}

.score {
  font-size: 2.5rem;
  font-weight: 800;
  color: var(--accent-color);
}

.game-info {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--spacing-xs);
  color: var(--text-secondary);
}

.status-badge {
  padding: 4px 12px;
  border-radius: 20px;
  background: rgba(255,255,255,0.1);
  margin-bottom: var(--spacing-sm);
}

.status-badge.finished {
  background: rgba(16, 185, 129, 0.2);
  color: #10b981;
}

/* Prediction Styles */
.prediction-section {
  margin-bottom: 20px;
  padding: 20px;
}

.prediction-section h3 {
  color: white;
  margin-bottom: 15px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.vote-count {
  font-size: 0.8em;
  color: #a0a0a0;
  font-weight: normal;
}

.vote-buttons {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 20px;
  margin-bottom: 20px;
}

.vote-btn {
  padding: 10px 30px;
  border-radius: 25px;
  border: none;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  gap: 8px;
}

.vote-btn.home-btn {
  background: rgba(64, 158, 255, 0.2);
  color: #409EFF;
  border: 1px solid #409EFF;
}

.vote-btn.away-btn {
  background: rgba(245, 108, 108, 0.2);
  color: #F56C6C;
  border: 1px solid #F56C6C;
}

.vote-btn:hover {
  transform: translateY(-2px);
}

.vote-btn.active {
  background: #409EFF;
  color: white;
}

.vote-btn.away-btn.active {
  background: #F56C6C;
  color: white;
}

.vs-text {
  font-weight: bold;
  color: #a0a0a0;
}

.prediction-bar-container {
  margin-top: 15px;
}

.prediction-bar {
  height: 24px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  overflow: hidden;
  display: flex;
  margin-bottom: 8px;
}

.bar-segment {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: bold;
  color: white;
  transition: width 0.5s ease;
}

.bar-segment.home {
  background: #409EFF;
}

.bar-segment.away {
  background: #F56C6C;
}

.bar-labels {
  display: flex;
  justify-content: space-between;
  color: #a0a0a0;
  font-size: 14px;
}

.bar-labels span.highlight {
  color: #E6A23C;
  font-weight: bold;
}

.prediction-result {
  margin-top: 15px;
  text-align: center;
}

.result-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 8px 20px;
  border-radius: 20px;
  font-weight: bold;
}

.result-badge.win {
  background: rgba(103, 194, 58, 0.2);
  color: #67C23A;
  border: 1px solid #67C23A;
}

.result-badge.lose {
  background: rgba(144, 147, 153, 0.2);
  color: #909399;
  border: 1px solid #909399;
}

.result-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 15px;
}

.claim-btn {
  background: linear-gradient(45deg, #E6A23C, #F56C6C);
  color: white;
  border: none;
  padding: 10px 25px;
  border-radius: 25px;
  font-weight: bold;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  box-shadow: 0 4px 15px rgba(230, 162, 60, 0.3);
  transition: all 0.3s;
  animation: pulse 2s infinite;
}

.claim-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(230, 162, 60, 0.4);
}

.claim-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
  animation: none;
}

.claimed-badge {
  color: #67C23A;
  font-size: 0.9em;
  display: flex;
  align-items: center;
  gap: 5px;
}

@keyframes pulse {
  0% { transform: scale(1); }
  50% { transform: scale(1.05); }
  100% { transform: scale(1); }
}

.tabs-container {
  display: flex;
  justify-content: center;
  gap: var(--spacing-lg);
  margin-bottom: var(--spacing-lg);
  border-bottom: 1px solid var(--glass-border);
  padding-bottom: var(--spacing-sm);
}

.tab-btn {
  background: none;
  border: none;
  color: var(--text-secondary);
  font-size: 1.1rem;
  padding: var(--spacing-sm) var(--spacing-lg);
  cursor: pointer;
  position: relative;
  transition: all 0.3s ease;
}

.tab-btn.active {
  color: var(--accent-color);
  font-weight: bold;
}

.tab-btn.active::after {
  content: '';
  position: absolute;
  bottom: -9px;
  left: 0;
  width: 100%;
  height: 2px;
  background: var(--accent-color);
}

.stats-section {
  margin-bottom: var(--spacing-lg);
  padding: var(--spacing-lg);
}

.stats-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: var(--spacing-md);
}

.stats-table th, .stats-table td {
  padding: 12px;
  text-align: center;
  border-bottom: 1px solid var(--glass-border);
}

.stats-table th {
  color: var(--text-secondary);
  font-weight: normal;
}

.ratings-layout {
  display: flex;
  gap: var(--spacing-xl);
}

.team-column {
  flex: 1;
}

.column-header {
  text-align: center;
  margin-bottom: var(--spacing-lg);
  padding-bottom: var(--spacing-sm);
  border-bottom: 2px solid var(--accent-color);
}

.players-list {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
}

.player-rating-card {
  display: flex;
  align-items: center;
  padding: var(--spacing-md);
  gap: var(--spacing-md);
  cursor: pointer;
  transition: transform 0.2s;
}

.player-rating-card:hover {
  transform: translateY(-2px);
  background: rgba(255,255,255,0.08);
}

.player-avatar img {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  object-fit: cover;
}

.avatar-placeholder {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.1);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  color: var(--text-secondary);
}

.player-info {
  flex: 1;
}

.player-name {
  font-size: 1.1rem;
  font-weight: bold;
  margin-bottom: 4px;
}

.rating-display {
  display: flex;
  align-items: baseline;
  gap: 8px;
  margin-bottom: 4px;
}

.avg-score {
  font-size: 1.5rem;
  font-weight: 800;
  color: var(--accent-color);
}

.rating-count {
  font-size: 0.8rem;
  color: var(--text-secondary);
}

@media (max-width: 768px) {
  .game-header {
    flex-direction: column;
    gap: var(--spacing-lg);
  }
  
  .ratings-layout {
    flex-direction: column;
  }
  
  .table-responsive {
    overflow-x: auto;
  }
}
</style>
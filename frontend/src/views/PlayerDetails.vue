<template>
  <div class="player-details-container">
    <div v-if="loading" class="loading-state">
      <el-icon class="is-loading"><Loading /></el-icon>
      <p>加载中...</p>
    </div>

    <template v-else-if="player">
      <!-- Header Section -->
      <div class="profile-header glass-card">
        <button @click="$router.go(-1)" class="back-btn">
          <el-icon><ArrowLeft /></el-icon> 返回
        </button>
        
        <div class="profile-content">
          <div class="avatar-wrapper">
            <img v-if="player.photo_url" :src="player.photo_url" alt="player" class="player-avatar">
            <div v-else class="avatar-placeholder">
              <el-icon><User /></el-icon>
            </div>
          </div>
          
          <div class="info-wrapper">
            <h1 class="player-name">{{ player.name }}</h1>
            <div class="player-meta">
              <span class="team-name">{{ player.team_name }}</span>
              <span class="divider">|</span>
              <span class="jersey">#{{ player.jersey_number }}</span>
              <span class="divider">|</span>
              <span class="position">{{ player.position }}</span>
            </div>
            <div class="physical-info">
              <span>{{ player.height }}m</span>
              <span class="dot">•</span>
              <span>{{ player.weight }}kg</span>
              <span class="dot">•</span>
              <span>{{ player.nationality }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Charts Section -->
      <div class="charts-section">
        <!-- Trend Chart -->
        <div class="chart-card glass-card trend-chart">
          <h3>赛季表现趋势</h3>
          <div ref="trendChart" class="chart-container"></div>
        </div>
        
        <!-- Radar Chart -->
        <div class="chart-card glass-card radar-chart">
          <h3>能力雷达图</h3>
          <div ref="radarChart" class="chart-container"></div>
        </div>
      </div>

      <!-- Game Log Table -->
      <div class="table-section glass-card">
        <h3>比赛日志</h3>
        <div class="table-wrapper custom-scrollbar">
          <table class="stats-table">
            <thead>
              <tr>
                <th>日期</th>
                <th>对手</th>
                <th>上场时间</th>
                <th>得分</th>
                <th>篮板</th>
                <th>助攻</th>
                <th>抢断</th>
                <th>盖帽</th>
                <th>+/-</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="game in games" :key="game.game_id">
                <td>{{ game.date }}</td>
                <td>{{ game.opponent }}</td>
                <td>{{ game.minutes }}</td>
                <td class="highlight">{{ game.points }}</td>
                <td>{{ game.rebounds }}</td>
                <td>{{ game.assists }}</td>
                <td>{{ game.steals }}</td>
                <td>{{ game.blocks }}</td>
                <td :class="game.plus_minus > 0 ? 'positive' : (game.plus_minus < 0 ? 'negative' : '')">
                  {{ game.plus_minus > 0 ? '+' + game.plus_minus : game.plus_minus }}
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </template>
    
    <div v-else class="error-state">
      <p>未找到球员数据</p>
      <button @click="$router.go(-1)" class="glass-btn">返回</button>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted, nextTick } from 'vue'
import { useRoute } from 'vue-router'
import { Loading, ArrowLeft, User } from '@element-plus/icons-vue'
import * as echarts from 'echarts'
import api from '../services/api'

export default {
  name: 'PlayerDetails',
  components: { Loading, ArrowLeft, User },
  setup() {
    const route = useRoute()
    const loading = ref(true)
    const player = ref(null)
    const games = ref([])
    const averages = ref({})
    
    const trendChart = ref(null)
    const radarChart = ref(null)
    let trendChartInstance = null
    let radarChartInstance = null

    const initCharts = () => {
      if (!games.value.length) return

      // 1. Trend Chart
      if (trendChart.value) {
        trendChartInstance = echarts.init(trendChart.value)
        const dates = games.value.map(g => g.date)
        const points = games.value.map(g => g.points)
        const rebounds = games.value.map(g => g.rebounds)
        const assists = games.value.map(g => g.assists)

        trendChartInstance.setOption({
          tooltip: {
            trigger: 'axis',
            backgroundColor: 'rgba(0,0,0,0.7)',
            borderColor: '#333',
            textStyle: { color: '#fff' }
          },
          legend: {
            data: ['得分', '篮板', '助攻'],
            textStyle: { color: '#ccc' },
            bottom: 0
          },
          grid: {
            left: '3%',
            right: '4%',
            bottom: '10%',
            containLabel: true
          },
          xAxis: {
            type: 'category',
            boundaryGap: false,
            data: dates,
            axisLine: { lineStyle: { color: '#666' } },
            axisLabel: { color: '#999' }
          },
          yAxis: {
            type: 'value',
            splitLine: { lineStyle: { color: '#333' } },
            axisLabel: { color: '#999' }
          },
          series: [
            {
              name: '得分',
              type: 'line',
              data: points,
              smooth: true,
              itemStyle: { color: '#ff9f43' },
              areaStyle: {
                color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                  { offset: 0, color: 'rgba(255, 159, 67, 0.5)' },
                  { offset: 1, color: 'rgba(255, 159, 67, 0.0)' }
                ])
              }
            },
            {
              name: '篮板',
              type: 'line',
              data: rebounds,
              smooth: true,
              itemStyle: { color: '#54a0ff' }
            },
            {
              name: '助攻',
              type: 'line',
              data: assists,
              smooth: true,
              itemStyle: { color: '#1dd1a1' }
            }
          ]
        })
      }

      // 2. Radar Chart
      if (radarChart.value && averages.value) {
        radarChartInstance = echarts.init(radarChart.value)
        
        // Normalize data for radar chart (simple normalization for demo)
        // Assuming max values: PTS 30, REB 15, AST 10, STL 3, BLK 3
        const avg = averages.value
        const data = [
          avg.points,
          avg.rebounds,
          avg.assists,
          avg.steals,
          avg.blocks
        ]
        
        radarChartInstance.setOption({
          tooltip: {},
          radar: {
            indicator: [
              { name: '得分', max: 35 },
              { name: '篮板', max: 15 },
              { name: '助攻', max: 12 },
              { name: '抢断', max: 3 },
              { name: '盖帽', max: 3 }
            ],
            splitArea: {
              areaStyle: {
                color: ['rgba(255,255,255,0.05)', 'rgba(255,255,255,0.02)']
              }
            },
            axisName: { color: '#ccc' }
          },
          series: [{
            name: '场均数据',
            type: 'radar',
            data: [{
              value: data,
              name: '场均数据',
              itemStyle: { color: '#ee5253' },
              areaStyle: { color: 'rgba(238, 82, 83, 0.4)' }
            }]
          }]
        })
      }
    }

    const fetchData = async () => {
      try {
        const playerId = route.params.id
        const response = await api.get(`/players/${playerId}/details`)
        player.value = response.player
        games.value = response.games
        averages.value = response.averages
        
        loading.value = false
        nextTick(() => {
          initCharts()
        })
      } catch (error) {
        console.error('Failed to fetch player stats:', error)
        loading.value = false
      }
    }

    const handleResize = () => {
      trendChartInstance?.resize()
      radarChartInstance?.resize()
    }

    onMounted(() => {
      fetchData()
      window.addEventListener('resize', handleResize)
    })

    onUnmounted(() => {
      window.removeEventListener('resize', handleResize)
      trendChartInstance?.dispose()
      radarChartInstance?.dispose()
    })

    return {
      loading,
      player,
      games,
      trendChart,
      radarChart
    }
  }
}
</script>

<style scoped>
.player-details-container {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
  color: #fff;
}

.glass-card {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  padding: 20px;
  margin-bottom: 20px;
}

/* Header Styles */
.profile-header {
  display: flex;
  align-items: center;
  gap: 30px;
}

.back-btn {
  background: none;
  border: none;
  color: #fff;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 5px;
  font-size: 1rem;
  padding: 8px 12px;
  border-radius: 6px;
  transition: background 0.3s;
}

.back-btn:hover {
  background: rgba(255, 255, 255, 0.1);
}

.profile-content {
  display: flex;
  align-items: center;
  gap: 25px;
}

.avatar-wrapper {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  overflow: hidden;
  border: 3px solid rgba(255, 255, 255, 0.2);
  background: #333;
}

.player-avatar {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.avatar-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 40px;
  color: #666;
}

.player-name {
  margin: 0 0 10px 0;
  font-size: 2rem;
  font-weight: 700;
}

.player-meta {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 1.1rem;
  color: #ddd;
  margin-bottom: 8px;
}

.divider {
  color: #666;
}

.physical-info {
  color: #999;
  font-size: 0.9rem;
}

.dot {
  margin: 0 8px;
}

/* Charts Section */
.charts-section {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 20px;
  margin-bottom: 20px;
}

.chart-card {
  height: 400px;
  display: flex;
  flex-direction: column;
}

.chart-card h3 {
  margin: 0 0 15px 0;
  font-size: 1.1rem;
  color: #ddd;
}

.chart-container {
  flex: 1;
  width: 100%;
}

/* Table Section */
.table-section h3 {
  margin: 0 0 15px 0;
  color: #ddd;
}

.table-wrapper {
  overflow-x: auto;
}

.stats-table {
  width: 100%;
  border-collapse: collapse;
  color: #eee;
}

.stats-table th,
.stats-table td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.stats-table th {
  color: #999;
  font-weight: 600;
  font-size: 0.9rem;
}

.stats-table tr:hover {
  background: rgba(255, 255, 255, 0.05);
}

.highlight {
  color: #ff9f43;
  font-weight: bold;
}

.positive {
  color: #1dd1a1;
}

.negative {
  color: #ff6b6b;
}

@media (max-width: 768px) {
  .charts-section {
    grid-template-columns: 1fr;
  }
  
  .profile-header {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .profile-content {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>
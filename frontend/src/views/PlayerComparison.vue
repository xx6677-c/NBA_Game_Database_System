<template>
  <div class="player-comparison-container">
    <div class="page-header">
      <h1>球员能力对比</h1>
      <p>选择两名球员进行全方位能力对比</p>
    </div>

    <div class="comparison-controls">
      <div class="player-select">
        <h3>球员 A</h3>
        <el-select
          v-model="teamAId"
          placeholder="筛选球队"
          clearable
          @change="handleTeamAChange"
          class="team-filter"
        >
          <el-option
            v-for="team in teams"
            :key="team.team_id"
            :label="team.name"
            :value="team.team_id"
          />
        </el-select>
        <el-select
          v-model="playerAId"
          filterable
          placeholder="搜索并选择球员"
          @change="loadPlayerA"
          :disabled="!teamAId && filteredPlayersA.length === 0"
        >
          <el-option
            v-for="item in filteredPlayersA"
            :key="item.player_id"
            :label="item.name"
            :value="item.player_id"
          >
            <span style="float: left">{{ item.name }}</span>
            <span style="float: right; color: #8492a6; font-size: 13px">{{ item.team_name }}</span>
          </el-option>
        </el-select>
      </div>

      <div class="vs-badge">VS</div>

      <div class="player-select">
        <h3>球员 B</h3>
        <el-select
          v-model="teamBId"
          placeholder="筛选球队"
          clearable
          @change="handleTeamBChange"
          class="team-filter"
        >
          <el-option
            v-for="team in teams"
            :key="team.team_id"
            :label="team.name"
            :value="team.team_id"
          />
        </el-select>
        <el-select
          v-model="playerBId"
          filterable
          placeholder="搜索并选择球员"
          @change="loadPlayerB"
          :disabled="!teamBId && filteredPlayersB.length === 0"
        >
          <el-option
            v-for="item in filteredPlayersB"
            :key="item.player_id"
            :label="item.name"
            :value="item.player_id"
          >
            <span style="float: left">{{ item.name }}</span>
            <span style="float: right; color: #8492a6; font-size: 13px">{{ item.team_name }}</span>
          </el-option>
        </el-select>
      </div>
    </div>

    <div v-if="playerA && playerB" class="comparison-content">
      <!-- 雷达图区域 -->
      <div class="chart-section glass-card">
        <div ref="radarChart" class="radar-chart"></div>
      </div>

      <!-- 详细数据对比表 -->
      <div class="stats-table-section glass-card">
        <table class="comparison-table">
          <thead>
            <tr>
              <th class="player-a-col">{{ playerA.name }}</th>
              <th>对比项</th>
              <th class="player-b-col">{{ playerB.name }}</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>{{ playerA.team_name }}</td>
              <td>所属球队</td>
              <td>{{ playerB.team_name }}</td>
            </tr>
            <tr>
              <td>{{ playerA.position }}</td>
              <td>位置</td>
              <td>{{ playerB.position }}</td>
            </tr>
            <tr>
              <td>{{ playerA.stats?.games_played || 0 }}</td>
              <td>出场次数</td>
              <td>{{ playerB.stats?.games_played || 0 }}</td>
            </tr>
            <tr>
              <td>{{ playerA.stats?.ppg || 0 }}</td>
              <td>场均得分</td>
              <td>{{ playerB.stats?.ppg || 0 }}</td>
            </tr>
            <tr>
              <td>{{ playerA.stats?.rpg || 0 }}</td>
              <td>场均篮板</td>
              <td>{{ playerB.stats?.rpg || 0 }}</td>
            </tr>
            <tr>
              <td>{{ playerA.stats?.apg || 0 }}</td>
              <td>场均助攻</td>
              <td>{{ playerB.stats?.apg || 0 }}</td>
            </tr>
            <tr>
              <td>{{ playerA.stats?.spg || 0 }}</td>
              <td>场均抢断</td>
              <td>{{ playerB.stats?.spg || 0 }}</td>
            </tr>
            <tr>
              <td>{{ playerA.stats?.bpg || 0 }}</td>
              <td>场均盖帽</td>
              <td>{{ playerB.stats?.bpg || 0 }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    
    <div v-else class="empty-state glass-card">
      <el-empty description="请选择两名球员开始对比" />
    </div>
  </div>
</template>

<script>
import api from '../services/api'
import * as echarts from 'echarts'

export default {
  name: 'PlayerComparison',
  data() {
    return {
      teams: [],
      allPlayers: [],
      teamAId: null,
      teamBId: null,
      playerAId: null,
      playerBId: null,
      playerA: null,
      playerB: null,
      playerAStats: null,
      playerBStats: null,
      chartInstance: null
    }
  },
  async mounted() {
    await Promise.all([
      this.loadTeams(),
      this.loadAllPlayers()
    ])
    window.addEventListener('resize', this.handleResize)
  },
  computed: {
    filteredPlayersA() {
      if (!this.teamAId) return this.allPlayers
      return this.allPlayers.filter(p => p.current_team_id === this.teamAId)
    },
    filteredPlayersB() {
      if (!this.teamBId) return this.allPlayers
      return this.allPlayers.filter(p => p.current_team_id === this.teamBId)
    }
  },
  beforeUnmount() {
    window.removeEventListener('resize', this.handleResize)
    if (this.chartInstance) {
      this.chartInstance.dispose()
    }
  },
  methods: {
    async loadTeams() {
      try {
        const response = await api.getTeams()
        this.teams = response
      } catch (error) {
        console.error('加载球队失败', error)
      }
    },
    handleTeamAChange() {
      this.playerAId = null
      this.playerA = null
      this.playerAStats = null
      this.updateChart()
    },
    handleTeamBChange() {
      this.playerBId = null
      this.playerB = null
      this.playerBStats = null
      this.updateChart()
    },
    async loadAllPlayers() {
      try {
        const response = await api.getPlayers()
        this.allPlayers = response
      } catch (error) {
        this.$message.error('加载球员列表失败')
      }
    },
    async loadPlayerA() {
      if (!this.playerAId) return
      try {
        // 获取详情
        const detailRes = await api.getPlayer(this.playerAId)
        this.playerA = detailRes
        // 获取雷达图数据
        const statsRes = await api.getPlayerStats(this.playerAId)
        this.playerAStats = statsRes
        
        this.updateChart()
      } catch (error) {
        console.error(error)
        this.$message.error('获取球员A数据失败')
      }
    },
    async loadPlayerB() {
      if (!this.playerBId) return
      try {
        const detailRes = await api.getPlayer(this.playerBId)
        this.playerB = detailRes
        const statsRes = await api.getPlayerStats(this.playerBId)
        this.playerBStats = statsRes
        
        this.updateChart()
      } catch (error) {
        console.error(error)
        this.$message.error('获取球员B数据失败')
      }
    },
    updateChart() {
      if (!this.playerAStats || !this.playerBStats) return
      
      if (!this.chartInstance) {
        this.chartInstance = echarts.init(this.$refs.radarChart)
      }

      const indicators = Object.keys(this.playerAStats).map(key => ({
        name: key,
        max: 100
      }))

      const option = {
        title: {
          text: '综合能力雷达图',
          left: 'center',
          textStyle: { color: '#fff' }
        },
        legend: {
          data: [this.playerA.name, this.playerB.name],
          bottom: 0,
          textStyle: { color: '#fff' }
        },
        radar: {
          indicator: indicators,
          splitArea: {
            areaStyle: {
              color: ['rgba(255,255,255,0.1)', 'rgba(255,255,255,0.2)']
            }
          },
          axisName: {
            color: '#fff'
          }
        },
        series: [
          {
            name: 'Player Comparison',
            type: 'radar',
            data: [
              {
                value: Object.values(this.playerAStats),
                name: this.playerA.name,
                areaStyle: { color: 'rgba(64, 158, 255, 0.3)' },
                itemStyle: { color: '#409EFF' }
              },
              {
                value: Object.values(this.playerBStats),
                name: this.playerB.name,
                areaStyle: { color: 'rgba(245, 108, 108, 0.3)' },
                itemStyle: { color: '#F56C6C' }
              }
            ]
          }
        ]
      }

      this.chartInstance.setOption(option)
    },
    handleResize() {
      if (this.chartInstance) {
        this.chartInstance.resize()
      }
    },
    formatSalary(value) {
      if (!value) return '未知'
      return `$${(value / 1000000).toFixed(2)}M`
    }
  }
}
</script>

<style scoped>
.player-comparison-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.page-header {
  text-align: center;
  margin-bottom: 40px;
  color: white;
}

.comparison-controls {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 40px;
  margin-bottom: 40px;
}

.player-select {
  width: 300px;
}

.player-select h3 {
  color: white;
  margin-bottom: 10px;
  text-align: center;
}

.team-filter {
  width: 100%;
  margin-bottom: 10px;
}

.vs-badge {
  font-size: 32px;
  font-weight: bold;
  color: #ff4757;
  background: rgba(255, 255, 255, 0.1);
  padding: 10px 20px;
  border-radius: 50%;
  border: 2px solid #ff4757;
}

.comparison-content {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

.glass-card {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border-radius: 15px;
  padding: 20px;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.radar-chart {
  width: 100%;
  height: 400px;
}

.comparison-table {
  width: 100%;
  border-collapse: collapse;
  color: white;
}

.comparison-table th,
.comparison-table td {
  padding: 15px;
  text-align: center;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.comparison-table th {
  font-size: 1.1em;
  color: #a0a0a0;
}

.player-a-col {
  color: #409EFF !important;
  font-weight: bold;
  width: 35%;
}

.player-b-col {
  color: #F56C6C !important;
  font-weight: bold;
  width: 35%;
}

.empty-state {
  text-align: center;
  padding: 60px;
}

@media (max-width: 768px) {
  .comparison-controls {
    flex-direction: column;
    gap: 20px;
  }
  
  .comparison-content {
    grid-template-columns: 1fr;
  }
}
</style>

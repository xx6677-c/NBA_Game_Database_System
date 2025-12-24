<template>
  <div class="query-container">
    <div class="page-header">
      <div class="header-content">
        <h1>数据分析</h1>
        <p class="subtitle">使用SQL查询分析NBA比赛数据（仅限数据分析师）</p>
      </div>
    </div>

    <div class="query-content">
      <div class="glass-card query-editor">
        <div class="editor-header">
          <h3><el-icon><DataAnalysis /></el-icon> SQL查询编辑器</h3>
          <div class="editor-actions">
            <button @click="showExamples = true" class="glass-btn sm-btn">
              <el-icon><DocumentCopy /></el-icon> 查询示例
            </button>
            <button @click="clearQuery" class="glass-btn sm-btn danger">
              <el-icon><Delete /></el-icon> 清空
            </button>
          </div>
        </div>
        
        <div class="editor-wrapper">
          <textarea 
            v-model="sqlQuery" 
            placeholder="请输入SQL查询语句（仅支持SELECT查询）..."
            class="glass-input glass-textarea sql-input"
            rows="8"
          ></textarea>
        </div>
        
        <div class="query-actions">
          <button @click="executeQuery" :disabled="!sqlQuery.trim() || executing" class="glass-btn primary-btn execute-btn">
            <el-icon v-if="executing" class="is-loading"><Loading /></el-icon>
            <el-icon v-else><VideoPlay /></el-icon>
            {{ executing ? '执行中...' : '执行查询' }}
          </button>
        </div>
      </div>

      <div class="glass-card query-results" v-if="queryResult">
        <div class="results-header">
          <h3>查询结果</h3>
          <div class="results-actions">
            <span class="results-count">
              共 {{ queryResult.data.length }} 条记录
            </span>
            <button @click="downloadCSV" class="glass-btn sm-btn" :disabled="queryResult.data.length === 0">
              <el-icon><Download /></el-icon> 下载CSV
            </button>
          </div>
        </div>
        
        <div class="results-table-container custom-scrollbar">
          <table class="glass-table">
            <thead>
              <tr>
                <th v-for="column in queryResult.columns" :key="column">
                  {{ column }}
                </th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(row, index) in queryResult.data" :key="index">
                <td v-for="column in queryResult.columns" :key="column">
                  {{ row[column] }}
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        
        <div v-if="queryResult.data.length === 0" class="no-results">
          <el-icon><Search /></el-icon>
          <p>查询结果为空</p>
        </div>
      </div>

      <div class="glass-card query-error" v-if="queryError">
        <div class="error-header">
          <h3><el-icon><Warning /></el-icon> 查询错误</h3>
        </div>
        <div class="error-message">
          {{ queryError }}
        </div>
      </div>
    </div>

    <!-- Examples Modal -->
    <div v-if="showExamples" class="modal-overlay glass-overlay">
      <div class="glass-card modal-content">
        <div class="modal-header">
          <h3>SQL查询示例</h3>
          <button @click="showExamples = false" class="close-btn"><el-icon><Close /></el-icon></button>
        </div>
        <div class="examples-list custom-scrollbar">
          <div class="example-item glass-card inner-card">
            <h4>查询所有球员信息</h4>
            <pre><code>SELECT * FROM Player</code></pre>
            <button @click="useExample('SELECT * FROM Player')" class="glass-btn sm-btn">使用此示例</button>
          </div>
          
          <div class="example-item glass-card inner-card">
            <h4>查询东部球队</h4>
            <pre><code>SELECT * FROM Team WHERE 分区 = '东部'</code></pre>
            <button @click="useExample(`SELECT * FROM Team WHERE 分区 = '东部'`)" class="glass-btn sm-btn">使用此示例</button>
          </div>
          
          <div class="example-item glass-card inner-card">
            <h4>查询最近10场比赛</h4>
            <pre><code>SELECT g.game_id, g.赛季, g.日期, ht.名称 as 主队, at.名称 as 客队, g.主队得分, g.客队得分
FROM Game g
JOIN Team ht ON g.主队ID = ht.team_id
JOIN Team at ON g.客队ID = at.team_id
ORDER BY g.日期 DESC
LIMIT 10</code></pre>
            <button @click="useExample(`SELECT g.game_id, g.赛季, g.日期, ht.名称 as 主队, at.名称 as 客队, g.主队得分, g.客队得分 FROM Game g JOIN Team ht ON g.主队ID = ht.team_id JOIN Team at ON g.客队ID = at.team_id ORDER BY g.日期 DESC LIMIT 10`)" class="glass-btn sm-btn">使用此示例</button>
          </div>
          
          <div class="example-item glass-card inner-card">
            <h4>查询球员场均得分</h4>
            <pre><code>SELECT p.姓名, AVG(pg.得分) as 场均得分
FROM Player p
JOIN Player_Game pg ON p.player_id = pg.player_id
GROUP BY p.player_id, p.姓名
ORDER BY 场均得分 DESC</code></pre>
            <button @click="useExample(`SELECT p.姓名, AVG(pg.得分) as 场均得分 FROM Player p JOIN Player_Game pg ON p.player_id = pg.player_id GROUP BY p.player_id, p.姓名 ORDER BY 场均得分 DESC`)" class="glass-btn sm-btn">使用此示例</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from '../services/api'
import { 
  DataAnalysis, DocumentCopy, Delete, VideoPlay, Close, Warning, Loading, Search, Download 
} from '@element-plus/icons-vue'

export default {
  name: 'Query',
  components: {
    DataAnalysis, DocumentCopy, Delete, VideoPlay, Close, Warning, Loading, Search, Download
  },
  data() {
    return {
      sqlQuery: '',
      queryResult: null,
      queryError: null,
      executing: false,
      showExamples: false
    }
  },
  methods: {
    async executeQuery() {
      if (!this.sqlQuery.trim()) {
        alert('请输入SQL查询语句')
        return
      }
      
      this.executing = true
      this.queryError = null
      this.queryResult = null
      
      try {
        const result = await api.executeQuery(this.sqlQuery)
        this.queryResult = result
      } catch (error) {
        this.queryError = error.message
      } finally {
        this.executing = false
      }
    },
    clearQuery() {
      this.sqlQuery = ''
      this.queryResult = null
      this.queryError = null
    },
    useExample(example) {
      this.sqlQuery = example
      this.showExamples = false
    },
    downloadCSV() {
      if (!this.queryResult || !this.queryResult.data.length) return
      
      // 构建CSV内容
      const columns = this.queryResult.columns
      const rows = this.queryResult.data
      
      // 添加BOM以支持中文
      let csvContent = '\uFEFF'
      
      // 添加表头
      csvContent += columns.map(col => `"${col}"`).join(',') + '\n'
      
      // 添加数据行
      rows.forEach(row => {
        const rowData = columns.map(col => {
          const value = row[col]
          if (value === null || value === undefined) return ''
          // 处理包含逗号、引号或换行的值
          const strValue = String(value)
          if (strValue.includes(',') || strValue.includes('"') || strValue.includes('\n')) {
            return `"${strValue.replace(/"/g, '""')}"`
          }
          return strValue
        })
        csvContent += rowData.join(',') + '\n'
      })
      
      // 创建下载链接
      const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' })
      const link = document.createElement('a')
      const url = URL.createObjectURL(blob)
      
      link.setAttribute('href', url)
      link.setAttribute('download', `query_result_${new Date().toISOString().slice(0, 10)}.csv`)
      link.style.visibility = 'hidden'
      
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
      URL.revokeObjectURL(url)
    }
  }
}
</script>

<style scoped>
.query-container {
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
  text-shadow: none;
}

.subtitle {
  color: var(--text-secondary);
  font-size: 1.1rem;
}

.query-content {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-lg);
}

.query-editor {
  padding: var(--spacing-lg);
}

.editor-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-md);
}

.editor-header h3 {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 1.2rem;
  color: var(--text-primary);
  margin: 0;
}

.editor-actions {
  display: flex;
  gap: var(--spacing-sm);
}

.glass-textarea.sql-input {
  font-family: 'Courier New', monospace;
  min-height: 200px;
  line-height: 1.5;
}

.query-actions {
  margin-top: var(--spacing-md);
  display: flex;
  justify-content: flex-end;
}

.execute-btn {
  padding: 0.6rem 2rem;
  font-size: 1rem;
  display: flex;
  align-items: center;
  gap: 8px;
}

.query-results {
  padding: var(--spacing-lg);
}

.results-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-md);
}

.results-header h3 {
  margin: 0;
  color: var(--text-primary);
}

.results-actions {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
}

.results-count {
  color: var(--text-secondary);
  font-size: 0.9rem;
}

.results-table-container {
  max-height: 500px;
  overflow: auto;
  border-radius: 8px;
  border: 1px solid var(--glass-border);
}

.glass-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.95rem;
}

.glass-table th,
.glass-table td {
  padding: 12px 16px;
  text-align: left;
  border-bottom: 1px solid var(--glass-border);
  color: var(--text-primary);
}

.glass-table th {
  background: var(--color-surface);
  font-weight: 600;
  position: sticky;
  top: 0;
}

.glass-table tr:hover td {
  background: rgba(255, 255, 255, 0.05);
}

.no-results {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--spacing-sm);
  padding: var(--spacing-xl);
  color: var(--text-secondary);
}

.no-results .el-icon {
  font-size: 2rem;
  opacity: 0.5;
}

.query-error {
  padding: var(--spacing-lg);
  border-left: 4px solid #ef4444;
  background: rgba(239, 68, 68, 0.1);
}

.error-header h3 {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #ef4444;
  margin: 0 0 var(--spacing-sm) 0;
}

.error-message {
  font-family: 'Courier New', monospace;
  white-space: pre-wrap;
  color: #fca5a5;
}

/* Modal */
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
  max-width: 800px;
  max-height: 90vh;
  overflow-y: auto;
  padding: var(--spacing-xl);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-lg);
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

.examples-list {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
  max-height: 60vh;
  overflow-y: auto;
  padding-right: var(--spacing-sm);
}

.example-item {
  padding: var(--spacing-md);
}

.example-item h4 {
  margin: 0 0 var(--spacing-sm) 0;
  color: var(--text-primary);
}

.example-item pre {
  background: rgba(0, 0, 0, 0.05);
  padding: var(--spacing-md);
  border-radius: 6px;
  overflow-x: auto;
  margin: var(--spacing-sm) 0;
}

.example-item code {
  font-family: 'Courier New', monospace;
  font-size: 0.9rem;
  color: var(--text-primary);
}

@media (max-width: 768px) {
  .editor-header {
    flex-direction: column;
    gap: var(--spacing-md);
    align-items: stretch;
  }
  
  .editor-actions {
    justify-content: center;
  }
  
  .results-header {
    flex-direction: column;
    gap: var(--spacing-sm);
    align-items: stretch;
  }
}
</style>

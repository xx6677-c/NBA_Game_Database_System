<template>
  <div class="posts-container">
    <div class="page-header">
      <div class="header-content">
        <h1>社区讨论</h1>
        <p class="subtitle">分享你对NBA比赛的看法和评论</p>
      </div>
    </div>

    <div class="actions-bar glass-card">
      <button @click="showCreatePost = true" class="glass-btn primary-btn">
        <el-icon><EditPen /></el-icon> 发布新帖子
      </button>
      
      <div class="filter-wrapper">
        <el-icon class="filter-icon"><Trophy /></el-icon>
        <select v-model="selectedGame" @change="loadPosts" class="glass-select">
          <option value="">所有比赛</option>
          <option v-for="game in recentGames" :key="game.game_id" :value="game.game_id">
            {{ game.home_team }} vs {{ game.away_team }} ({{ game.date }})
          </option>
        </select>
      </div>
    </div>

    <!-- Create Post Modal -->
    <div v-if="showCreatePost" class="modal-overlay glass-overlay">
      <div class="glass-card modal-content">
        <div class="modal-header">
          <h3>发布新帖子</h3>
          <button @click="showCreatePost = false" class="close-btn"><el-icon><Close /></el-icon></button>
        </div>
        <form @submit.prevent="createPost" class="glass-form">
          <div class="form-group">
            <label>标题</label>
            <input v-model="newPost.title" type="text" required class="glass-input" placeholder="请输入标题">
          </div>
          <div class="form-group">
            <label>内容</label>
            <textarea v-model="newPost.content" rows="6" required class="glass-input glass-textarea" placeholder="请输入内容..."></textarea>
          </div>
          <div class="form-group">
            <label>关联比赛（可选）</label>
            <div class="input-wrapper">
              <el-icon><Trophy /></el-icon>
              <select v-model="newPost.game_id" class="glass-select">
                <option value="">不关联比赛</option>
                <option v-for="game in recentGames" :key="game.game_id" :value="game.game_id">
                  {{ game.home_team }} vs {{ game.away_team }} ({{ game.date }})
                </option>
              </select>
            </div>
          </div>
          <div class="form-actions">
            <button type="button" @click="showCreatePost = false" class="glass-btn">取消</button>
            <button type="submit" :disabled="creatingPost" class="glass-btn primary-btn">
              {{ creatingPost ? '发布中...' : '发布' }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <div class="posts-list">
      <div v-for="post in posts" :key="post.post_id" class="glass-card post-card">
        <div class="post-header">
          <h3>{{ post.title }}</h3>
          <div class="post-meta">
            <span class="meta-item">
              <el-icon><User /></el-icon> {{ post.username }}
            </span>
            <span class="meta-item">
              <el-icon><Timer /></el-icon> {{ post.create_time }}
            </span>
          </div>
        </div>
        
        <div class="post-content">
          <p>{{ post.content }}</p>
        </div>
        
        <div v-if="post.season" class="post-game-info glass-card inner-card">
          <el-icon><Trophy /></el-icon>
          <span><strong>关联比赛:</strong> {{ post.season }} - {{ post.home_team }} vs {{ post.away_team }}</span>
        </div>
        
        <div class="post-stats">
          <span class="stat-item"><el-icon><View /></el-icon> {{ post.view_count || 0 }} 浏览</span>
          <span class="stat-item"><el-icon><Star /></el-icon> {{ post.like_count || 0 }} 点赞</span>
        </div>
        
        <div class="post-actions">
          <button @click="togglePostLike(post)" :class="['glass-btn sm-btn', { 'active': isPostLiked(post) }]">
            <el-icon><StarFilled v-if="isPostLiked(post)" /><Star v-else /></el-icon> 
            {{ isPostLiked(post) ? '已点赞' : '点赞' }}
          </button>
          <button @click="toggleComments(post)" class="glass-btn sm-btn">
            <el-icon><ChatDotRound /></el-icon> 
            评论{{ post.comments && post.comments.length > 0 ? `(${post.comments.length})` : '' }}
          </button>
          <button @click="sharePost(post)" class="glass-btn sm-btn">
            <el-icon><Share /></el-icon> 分享
          </button>
        </div>
        
        <!-- Comments Section -->
        <div v-if="post.showComments" class="comments-section">
          <div class="comments-list">
            <div v-if="post.comments && post.comments.length > 0">
              <div v-for="comment in post.comments" :key="comment.comment_id" class="comment-item glass-card inner-card">
                <div class="comment-header">
                  <div class="comment-user">
                    <el-icon><User /></el-icon> <strong>{{ comment.username }}</strong>
                  </div>
                  <span class="comment-time">{{ comment.create_time }}</span>
                </div>
                <div class="comment-content">{{ comment.content }}</div>
                <div class="comment-actions">
                  <button 
                    @click="toggleCommentLike(comment)" 
                    :class="['glass-btn icon-only xs-btn', { 'active': isCommentLiked(comment) }]"
                  >
                    <el-icon><StarFilled v-if="isCommentLiked(comment)" /><Star v-else /></el-icon> 
                    {{ comment.like_count || 0 }}
                  </button>
                  <button 
                    v-if="canDeleteComment()" 
                    @click="deleteComment(post, comment)" 
                    class="glass-btn icon-only xs-btn danger"
                  >
                    <el-icon><Delete /></el-icon>
                  </button>
                </div>
              </div>
            </div>
            <div v-else class="no-comments">
              <el-icon><ChatDotRound /></el-icon>
              <p>暂无评论，快来发表第一条评论吧！</p>
            </div>
          </div>
          
          <!-- Add Comment -->
          <div class="add-comment glass-card inner-card">
            <div class="comment-form">
              <textarea 
                v-model="post.newComment" 
                placeholder="写下你的评论..." 
                rows="3"
                class="glass-input glass-textarea"
              ></textarea>
              <button 
                @click="submitComment(post)" 
                :disabled="!post.newComment || post.submittingComment"
                class="glass-btn primary-btn sm-btn submit-comment-btn"
              >
                {{ post.submittingComment ? '发布中...' : '发布评论' }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-if="loading" class="loading-state">
      <el-icon class="is-loading"><Loading /></el-icon>
      <p>加载中...</p>
    </div>

    <div v-if="!loading && posts.length === 0" class="empty-state">
      <el-icon><ChatDotRound /></el-icon>
      <p>暂无帖子数据</p>
    </div>
  </div>
</template>

<script>
import api from '../services/api'
import { 
  EditPen, ChatDotRound, View, Star, StarFilled, Share, User, Timer, 
  Trophy, Close, Delete, Loading 
} from '@element-plus/icons-vue'

export default {
  name: 'Posts',
  components: {
    EditPen, ChatDotRound, View, Star, StarFilled, Share, User, Timer, 
    Trophy, Close, Delete, Loading
  },
  data() {
    return {
      posts: [],
      recentGames: [],
      selectedGame: '',
      showCreatePost: false,
      newPost: {
        title: '',
        content: '',
        game_id: ''
      },
      creatingPost: false,
      loading: false,
      currentUser: null,
      postLikeStatus: {}, // 存储每个帖子的点赞状态
      commentLikeStatus: {} // 存储每个评论的点赞状态
    }
  },
  async mounted() {
    // 从URL参数获取game_id
    const gameId = this.$route.query.game_id
    if (gameId) {
      this.selectedGame = parseInt(gameId)
    }
    await Promise.all([this.loadRecentGames(), this.loadPosts(), this.loadCurrentUser()])
  },
  methods: {
    async loadRecentGames() {
      try {
        const games = await api.getGames()
        this.recentGames = games.slice(0, 10) // 最近10场比赛
      } catch (error) {
        console.error('加载比赛数据失败:', error)
      }
    },
    async loadPosts() {
      this.loading = true
      try {
        this.posts = await api.getPosts(this.selectedGame || null)
        
        // 为每个帖子增加浏览量
        for (const post of this.posts) {
          await this.incrementPostView(post)
        }
      } catch (error) {
        console.error('加载帖子数据失败:', error)
        // alert('加载帖子数据失败')
      } finally {
        this.loading = false
      }
    },
    async createPost() {
      if (!this.newPost.title || !this.newPost.content) {
        alert('标题和内容不能为空')
        return
      }
      
      this.creatingPost = true
      try {
        // 准备发送的数据，确保 game_id 为空时发送 null
        const postData = {
          title: this.newPost.title,
          content: this.newPost.content,
          game_id: this.newPost.game_id ? this.newPost.game_id : null
        }
        
        await api.createPost(postData)
        this.showCreatePost = false
        this.newPost = { title: '', content: '', game_id: '' }
        await this.loadPosts()
        // alert('帖子发布成功')
      } catch (error) {
        alert(error.message || '发布失败')
      } finally {
        this.creatingPost = false
      }
    },
    async loadCurrentUser() {
      try {
        this.currentUser = await api.getCurrentUser()
      } catch (error) {
        console.error('获取当前用户信息失败:', error)
        // alert('请先登录后再使用评论功能')
      }
    },
    
    // 加载帖子时增加浏览量
    async incrementPostView(post) {
      try {
        await api.incrementPostView(post.post_id)
        post.view_count = (post.view_count || 0) + 1
      } catch (error) {
        console.error('增加浏览量失败:', error)
      }
    },
    
    // 切换帖子点赞状态
    async togglePostLike(post) {
      if (!this.currentUser) {
        alert('请先登录后再点赞')
        return
      }
      
      try {
        const isLiked = this.isPostLiked(post)
        
        if (isLiked) {
          await api.unlikePost(post.post_id)
          this.postLikeStatus[post.post_id] = false
          post.like_count = Math.max(0, (post.like_count || 0) - 1)
        } else {
          await api.togglePostLike(post.post_id)
          this.postLikeStatus[post.post_id] = true
          post.like_count = (post.like_count || 0) + 1
        }
      } catch (error) {
        console.error('点赞操作失败:', error)
        alert(error.message || '操作失败')
      }
    },
    
    // 切换评论点赞状态
    async toggleCommentLike(comment) {
      if (!this.currentUser) {
        alert('请先登录后再点赞')
        return
      }
      
      try {
        const isLiked = this.isCommentLiked(comment)
        
        if (isLiked) {
          await api.unlikeComment(comment.comment_id)
          this.commentLikeStatus[comment.comment_id] = false
          comment.like_count = Math.max(0, (comment.like_count || 0) - 1)
        } else {
          await api.toggleCommentLike(comment.comment_id)
          this.commentLikeStatus[comment.comment_id] = true
          comment.like_count = (comment.like_count || 0) + 1
        }
      } catch (error) {
        console.error('点赞操作失败:', error)
        alert(error.message || '操作失败')
      }
    },
    
    // 检查帖子是否已点赞
    isPostLiked(post) {
      return this.postLikeStatus[post.post_id] === true
    },
    
    // 检查评论是否已点赞
    isCommentLiked(comment) {
      return this.commentLikeStatus[comment.comment_id] === true
    },
    async toggleComments(post) {
      // 切换评论显示状态
      post.showComments = !post.showComments
      
      // 如果展开评论且还未加载过评论，则加载评论
      if (post.showComments && !post.comments) {
        await this.loadComments(post)
      }
    },
    async loadComments(post) {
      try {
        const comments = await api.getPostComments(post.post_id)
        
        // 在Vue 3中直接赋值即可实现响应式
        post.comments = comments
        post.newComment = ''
        post.submittingComment = false
      } catch (error) {
        console.error('加载评论失败:', error)
        alert('加载评论失败: ' + (error.message || error))
      }
    },
    async submitComment(post) {
      if (!post.newComment || !post.newComment.trim()) {
        alert('评论内容不能为空')
        return
      }
      
      post.submittingComment = true
      try {
        await api.createComment(post.post_id, {
          content: post.newComment.trim()
        })
        
        // 重新加载评论
        await this.loadComments(post)
        // alert('评论发布成功')
      } catch (error) {
        alert(error.message || '评论发布失败')
      } finally {
        post.submittingComment = false
      }
    },
    async deleteComment(post, comment) {
      if (!confirm('确定要删除这条评论吗？')) {
        return
      }
      
      try {
        await api.deleteComment(comment.comment_id)
        // 从评论列表中移除
        const index = post.comments.findIndex(c => c.comment_id === comment.comment_id)
        if (index > -1) {
          post.comments.splice(index, 1)
        }
        // alert('评论删除成功')
      } catch (error) {
        alert(error.message || '评论删除失败')
      }
    },
    canDeleteComment() {
      // 临时允许删除评论用于测试
      return true
    },
    likePost(post) {
      this.togglePostLike(post)
    },
    commentPost(post) {
      this.toggleComments(post)
    },
    sharePost(post) {
      alert(`分享帖子 "${post.title}" 功能开发中...`)
    }
  }
}
</script>

<style scoped>
.posts-container {
  padding: var(--spacing-lg);
  max-width: 1000px;
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

.actions-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--spacing-md);
  margin-bottom: var(--spacing-xl);
  gap: var(--spacing-md);
}

.filter-wrapper {
  position: relative;
  display: flex;
  align-items: center;
  min-width: 250px;
}

.filter-icon {
  position: absolute;
  left: 12px;
  color: var(--text-secondary);
  z-index: 1;
}

.glass-select {
  width: 100%;
  padding: 10px 12px 10px 36px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid var(--glass-border);
  border-radius: 8px;
  font-size: 1rem;
  color: var(--text-primary);
  transition: all 0.3s ease;
}

.glass-select:focus {
  outline: none;
  background: rgba(255, 255, 255, 0.1);
  border-color: var(--accent-color);
  box-shadow: 0 0 0 3px rgba(212, 175, 55, 0.1);
}

.posts-list {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-lg);
}

.post-card {
  padding: var(--spacing-lg);
  transition: all 0.3s ease;
}

.post-card:hover {
  transform: translateY(-3px);
  box-shadow: var(--glass-shadow-hover);
}

.post-header {
  margin-bottom: var(--spacing-md);
}

.post-header h3 {
  font-size: 1.4rem;
  color: var(--text-primary);
  margin: 0 0 var(--spacing-xs) 0;
}

.post-meta {
  display: flex;
  gap: var(--spacing-md);
  color: var(--text-secondary);
  font-size: 0.9rem;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 6px;
}

.post-content {
  margin-bottom: var(--spacing-md);
  color: var(--text-primary);
  line-height: 1.6;
}

.post-game-info {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  padding: var(--spacing-sm) var(--spacing-md);
  margin-bottom: var(--spacing-md);
  color: var(--text-secondary);
  font-size: 0.95rem;
}

.post-stats {
  display: flex;
  gap: var(--spacing-lg);
  margin-bottom: var(--spacing-md);
  color: var(--text-secondary);
  font-size: 0.9rem;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 6px;
}

.post-actions {
  display: flex;
  gap: var(--spacing-sm);
  padding-top: var(--spacing-md);
  border-top: 1px solid var(--glass-border);
}

.glass-btn.sm-btn {
  padding: 0.5rem 1rem;
  font-size: 0.9rem;
  display: flex;
  align-items: center;
  gap: 6px;
}

.glass-btn.active {
  background: rgba(245, 158, 11, 0.15);
  color: #f59e0b;
  border-color: rgba(245, 158, 11, 0.3);
}

/* Comments */
.comments-section {
  margin-top: var(--spacing-lg);
  padding-top: var(--spacing-lg);
  border-top: 1px solid var(--glass-border);
}

.comments-list {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
  margin-bottom: var(--spacing-lg);
}

.comment-item {
  padding: var(--spacing-md);
}

.comment-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-xs);
}

.comment-user {
  display: flex;
  align-items: center;
  gap: 6px;
  color: var(--text-primary);
}

.comment-time {
  font-size: 0.85rem;
  color: var(--text-secondary);
}

.comment-content {
  margin-bottom: var(--spacing-sm);
  color: var(--text-primary);
  font-size: 0.95rem;
  line-height: 1.5;
}

.comment-actions {
  display: flex;
  gap: var(--spacing-sm);
  justify-content: flex-end;
}

.glass-btn.xs-btn {
  padding: 2px 8px;
  font-size: 0.8rem;
  min-height: 24px;
}

.glass-btn.danger {
  color: #ef4444;
}

.glass-btn.danger:hover {
  background: rgba(239, 68, 68, 0.1);
}

.no-comments {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--spacing-sm);
  padding: var(--spacing-lg);
  color: var(--text-secondary);
}

.no-comments .el-icon {
  font-size: 2rem;
  opacity: 0.5;
}

.add-comment {
  padding: var(--spacing-md);
}

.comment-form {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
}

.glass-textarea {
  min-height: 80px;
  resize: vertical;
  font-family: inherit;
}

.submit-comment-btn {
  align-self: flex-end;
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
  max-width: 600px;
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

.glass-form .form-group {
  margin-bottom: var(--spacing-lg);
}

.glass-form label {
  display: block;
  margin-bottom: var(--spacing-xs);
  color: var(--text-primary);
  font-weight: 500;
}

.glass-input {
  width: 100%;
  padding: 10px 12px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid var(--glass-border);
  border-radius: 8px;
  font-size: 1rem;
  color: var(--text-primary);
  transition: all 0.3s ease;
}

.glass-input:focus {
  outline: none;
  background: rgba(255, 255, 255, 0.1);
  border-color: var(--accent-color);
  box-shadow: 0 0 0 3px rgba(212, 175, 55, 0.1);
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: var(--spacing-md);
  margin-top: var(--spacing-xl);
}

/* Loading & Empty States */
.loading-state, .empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem;
  color: var(--text-secondary);
  gap: var(--spacing-md);
}

.loading-state .el-icon, .empty-state .el-icon {
  font-size: 3rem;
  color: var(--accent-color);
  opacity: 0.8;
}

@media (max-width: 768px) {
  .actions-bar {
    flex-direction: column;
    align-items: stretch;
  }
  
  .filter-wrapper {
    width: 100%;
  }
  
  .post-actions {
    flex-wrap: wrap;
  }
  
  .glass-btn.sm-btn {
    flex: 1;
    justify-content: center;
  }
}
</style>

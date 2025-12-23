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
            <label>图片（可选，支持多选）</label>
            <div class="input-wrapper">
              <el-icon><Picture /></el-icon>
              <input type="file" @change="handleImageUpload" accept="image/*" multiple class="glass-input">
            </div>
            <div v-if="uploadingImage" class="upload-status">图片上传中...</div>
            <div v-if="newPost.image_ids.length > 0" class="upload-success">已上传 {{ newPost.image_ids.length }} 张图片</div>
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
        <div class="post-card-layout">
          <!-- 左侧内容区 -->
          <div class="post-left">
            <div class="post-header">
              <div class="title-row">
                <h3>{{ post.title }}</h3>
                <button v-if="canDeletePost(post)" @click.stop="deletePost(post)" class="delete-post-btn" title="删除帖子">
                  <el-icon><Delete /></el-icon>
                </button>
              </div>
              <div class="post-meta">
                <span class="meta-item">
                  <el-icon><User /></el-icon> {{ post.username }}
                </span>
                <span class="meta-item">
                  <el-icon><Timer /></el-icon> {{ post.create_time }}
                </span>
              </div>
            </div>
            
            <div v-if="post.season" class="post-game-info glass-card inner-card">
              <el-icon><Trophy /></el-icon>
              <span><strong>关联比赛:</strong> {{ post.season }} - {{ post.home_team }} vs {{ post.away_team }}</span>
            </div>
            
            <div class="post-stats">
              <span class="stat-item"><el-icon><View /></el-icon> {{ post.view_count || 0 }} 浏览</span>
              <span class="stat-item"><el-icon><Star /></el-icon> {{ post.like_count || 0 }} 点赞</span>
            </div>
          </div>
          
          <!-- 右侧图片区 -->
          <div class="post-right">
            <div v-if="post.images && post.images.length > 0" class="post-image-container">
              <img :src="post.images[0]" alt="Post Image" class="post-image">
            </div>
            <div v-else-if="post.image_url" class="post-image-container">
              <img :src="post.image_url" alt="Post Image" class="post-image">
            </div>
            <div v-else class="post-image-placeholder">
              <el-icon><Picture /></el-icon>
            </div>
          </div>
        </div>
        
        <div class="post-actions">
          <button 
            @click="likePost(post)" 
            class="glass-btn sm-btn"
            :class="{ 'active': isPostLiked(post) }"
          >
            <el-icon v-if="isPostLiked(post)"><StarFilled /></el-icon>
            <el-icon v-else><Star /></el-icon>
            {{ isPostLiked(post) ? '已点赞' : '点赞' }}
          </button>
          <button @click="openPostDetail(post)" class="glass-btn sm-btn primary-btn">
            <el-icon><ChatDotRound /></el-icon> 详情 / 评论
          </button>
        </div>
        
        <!-- Comments Section (Removed from list view) -->
        <!-- <div v-if="post.showComments" class="comments-section">
          ...
        </div> -->
      </div>
    </div>

    <!-- Post Detail Modal -->
    <div v-if="showPostDetailModal && selectedPost" class="modal-overlay glass-overlay" @click="closePostDetail">
      <div class="glass-card modal-content post-detail-modal" @click.stop>
        <div class="modal-header">
          <h3>{{ selectedPost.title }}</h3>
          <button @click="closePostDetail" class="close-btn"><el-icon><Close /></el-icon></button>
        </div>
        
        <div class="modal-body custom-scrollbar">
          <div class="post-header-detail">
             <div class="post-meta">
                <span class="meta-item"><el-icon><User /></el-icon> {{ selectedPost.username }}</span>
                <span class="meta-item"><el-icon><Timer /></el-icon> {{ selectedPost.create_time }}</span>
             </div>
          </div>

          <div class="post-content full-content">
            <p>{{ selectedPost.content }}</p>
            
            <!-- All Images -->
            <div v-if="selectedPost.images && selectedPost.images.length > 0" class="post-images-list-full">
              <div v-for="(img, index) in selectedPost.images" :key="index" class="post-image-full-item">
                <img :src="img" alt="Post Image" class="post-image-full">
              </div>
            </div>
            <div v-else-if="selectedPost.image_url" class="post-image-container-full">
               <img :src="selectedPost.image_url" alt="Post Image" class="post-image-full">
            </div>
          </div>

          <div class="post-stats">
             <span class="stat-item"><el-icon><View /></el-icon> {{ selectedPost.view_count || 0 }} 浏览</span>
             <span class="stat-item"><el-icon><Star /></el-icon> {{ selectedPost.like_count || 0 }} 点赞</span>
          </div>

          <div class="post-actions">
             <button @click="likePost(selectedPost)" class="glass-btn sm-btn" :class="{ 'active': isPostLiked(selectedPost) }">
                <el-icon v-if="isPostLiked(selectedPost)"><StarFilled /></el-icon>
                <el-icon v-else><Star /></el-icon>
                {{ isPostLiked(selectedPost) ? '已点赞' : '点赞' }}
             </button>
          </div>

          <!-- Comments Section -->
          <div class="comments-section">
            <h4>评论 ({{ selectedPost.comments ? selectedPost.comments.length : (selectedPost.comment_count || 0) }})</h4>
            
            <div class="comments-list">
              <div v-if="selectedPost.comments && selectedPost.comments.length > 0">
                <div v-for="comment in selectedPost.comments" :key="comment.comment_id" class="comment-item glass-card inner-card">
                  <div class="comment-header">
                    <div class="comment-user">
                      <el-icon><User /></el-icon> <strong>{{ comment.username }}</strong>
                    </div>
                    <span class="comment-time">{{ comment.create_time }}</span>
                  </div>
                  <div class="comment-content">{{ comment.content }}</div>
                  <div class="comment-actions">
                    <button @click="toggleCommentLike(comment)" :class="['glass-btn icon-only xs-btn', { 'active': isCommentLiked(comment) }]">
                      <el-icon><StarFilled v-if="isCommentLiked(comment)" /><Star v-else /></el-icon> {{ comment.like_count || 0 }}
                    </button>
                    <button v-if="canDeleteComment()" @click="deleteComment(selectedPost, comment)" class="glass-btn icon-only xs-btn danger">
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
                <textarea v-model="selectedPost.newComment" placeholder="写下你的评论..." rows="3" class="glass-input glass-textarea"></textarea>
                <button @click="submitComment(selectedPost)" :disabled="!selectedPost.newComment || selectedPost.submittingComment" class="glass-btn primary-btn sm-btn submit-comment-btn">
                  {{ selectedPost.submittingComment ? '发布中...' : '发布评论' }}
                </button>
              </div>
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
  EditPen, ChatDotRound, View, Star, StarFilled, User, Timer, 
  Trophy, Close, Delete, Loading, Picture 
} from '@element-plus/icons-vue'

export default {
  name: 'Posts',
  components: {
    EditPen, ChatDotRound, View, Star, StarFilled, User, Timer, 
    Trophy, Close, Delete, Loading, Picture
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
        game_id: '',
        image_ids: []
      },
      creatingPost: false,
      uploadingImage: false,
      loading: false,
      currentUser: null,
      postLikeStatus: {}, // 存储每个帖子的点赞状态
      commentLikeStatus: {}, // 存储每个评论的点赞状态
      showPostDetailModal: false,
      selectedPost: null
    }
  },
  async mounted() {
    // 从URL参数获取game_id
    const gameId = this.$route.query.game_id
    if (gameId) {
      this.selectedGame = parseInt(gameId)
    }
    await Promise.all([this.loadRecentGames(), this.loadPosts(), this.loadCurrentUser()])

    // Check for post ID in query to open detail modal
    const postId = this.$route.query.id
    if (postId) {
      const post = this.posts.find(p => p.post_id == postId)
      if (post) {
        this.openPostDetail(post)
      }
    }
  },
  methods: {
    async loadRecentGames() {
      try {
        const games = await api.getGames()
        // 只加载已结束的比赛供选择
        this.recentGames = games.filter(game => game.status === '已结束')
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
          game_id: this.newPost.game_id ? this.newPost.game_id : null,
          image_ids: this.newPost.image_ids
        }
        
        await api.createPost(postData)
        this.showCreatePost = false
        this.newPost = { title: '', content: '', game_id: '', image_ids: [] }
        await this.loadPosts()
        // alert('帖子发布成功')
      } catch (error) {
        alert(error.message || '发布失败')
      } finally {
        this.creatingPost = false
      }
    },

    async handleImageUpload(event) {
      const files = event.target.files
      if (!files || files.length === 0) return
      
      this.uploadingImage = true
      try {
        // 支持多图上传
        for (let i = 0; i < files.length; i++) {
          const result = await api.uploadImage(files[i])
          this.newPost.image_ids.push(result.image_id)
        }
      } catch (error) {
        console.error('图片上传失败:', error)
        alert('图片上传失败: ' + error.message)
      } finally {
        this.uploadingImage = false
        // 清空input，允许重复选择同一文件
        event.target.value = ''
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
    // commentPost(post) {
    //   this.toggleComments(post)
    // },
    async deletePost(post) {
      if (!confirm('确定要删除这个帖子吗？此操作不可恢复。')) {
        return
      }
      
      try {
        await api.deletePost(post.post_id)
        // 从列表中移除
        const index = this.posts.findIndex(p => p.post_id === post.post_id)
        if (index > -1) {
          this.posts.splice(index, 1)
        }
        // alert('帖子删除成功')
      } catch (error) {
        alert(error.message || '删除失败')
      }
    },
    canDeletePost(post) {
      if (!this.currentUser) return false
      return this.currentUser.role === 'admin' || this.currentUser.user_id === post.user_id
    },
    openPostDetail(post) {
      this.selectedPost = post
      this.showPostDetailModal = true
      // 如果未加载评论，可以在这里加载
      if (!post.comments) {
        this.loadComments(post)
      }
    },
    closePostDetail() {
      this.showPostDetailModal = false
      this.selectedPost = null
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

.post-card-layout {
  display: flex;
  gap: var(--spacing-lg);
  margin-bottom: var(--spacing-md);
}

.post-left {
  flex: 0 0 60%;
  display: flex;
  flex-direction: column;
  gap: var(--spacing-sm);
}

.post-right {
  flex: 0 0 38%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.post-image-container {
  width: 100%;
  height: 180px;
  border-radius: 8px;
  overflow: hidden;
}

.post-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.post-image-placeholder {
  width: 100%;
  height: 120px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--text-secondary);
  font-size: 2rem;
}

.post-header {
  margin-bottom: var(--spacing-xs);
}

.title-row {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 10px;
  margin-bottom: var(--spacing-xs);
}

.post-header h3 {
  font-size: 1.4rem;
  color: var(--text-primary);
  margin: 0;
  flex: 1;
}

.delete-post-btn {
  background: none;
  border: none;
  color: var(--text-secondary);
  cursor: pointer;
  padding: 6px;
  border-radius: 4px;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.delete-post-btn:hover {
  color: #ef4444;
  background: rgba(239, 68, 68, 0.1);
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

.post-game-info {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  padding: var(--spacing-xs) var(--spacing-sm);
  color: var(--text-secondary);
  font-size: 0.85rem;
}

.post-stats {
  display: flex;
  gap: var(--spacing-md);
  color: var(--text-secondary);
  font-size: 0.85rem;
  margin-top: auto;
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

.post-images-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
  margin-top: 15px;
}

.post-image-item {
  aspect-ratio: 1;
  overflow: hidden;
  border-radius: 8px;
}

.post-image-item img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.post-image-item img:hover {
  transform: scale(1.05);
}

.post-image-container {
  margin-top: 1rem;
  border-radius: 8px;
  overflow: hidden;
  max-height: 400px;
}

.post-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.upload-status {
  font-size: 0.9rem;
  color: var(--text-secondary);
  margin-top: 0.5rem;
}

.upload-success {
  font-size: 0.9rem;
  color: var(--accent-color);
  margin-top: 0.5rem;
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

.post-detail-modal {
  max-width: 800px; /* Wider modal for details */
}

.post-detail-content .post-content {
  font-size: 1.1rem;
  margin-bottom: var(--spacing-lg);
}

.post-images-list-full {
  display: flex;
  flex-direction: column;
  gap: 15px;
  margin-top: 20px;
}

.post-image-full-item, .post-image-full-container {
  width: 100%;
  border-radius: 8px;
  overflow: hidden;
  background: rgba(0,0,0,0.2);
}

.post-image-full {
  width: 100%;
  height: auto;
  display: block;
  object-fit: contain; /* Ensure full image is visible */
  max-height: 80vh; /* Prevent image from being too tall */
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

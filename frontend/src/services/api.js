const API_BASE_URL = process.env.VUE_APP_API_BASE_URL || 'http://127.0.0.1:5000/api'

class ApiService {
  constructor() {
    this.token = localStorage.getItem('token')
    this.refreshToken = localStorage.getItem('refreshToken')
  }

  /**
   * 统一请求方法，支持请求拦截和错误处理
   */
  async request(endpoint, options = {}) {
    const url = `${API_BASE_URL}${endpoint}`
    const config = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers
      },
      ...options
    }

    // 添加认证令牌
    if (this.token) {
      config.headers.Authorization = `Bearer ${this.token}`
    }

    try {
      const response = await fetch(url, config)
      const data = await response.json()
      
      // 处理未授权错误（token过期）
      if (response.status === 401) {
        this.handleUnauthorized()
        throw new Error('登录已过期，请重新登录')
      }
      
      // 处理其他HTTP错误
      if (!response.ok) {
        throw new Error(data.error || data.message || `请求失败: ${response.status}`)
      }
      
      return data
    } catch (error) {
      console.error('API请求错误:', error)
      
      // 网络错误处理
      if (error.name === 'TypeError' && error.message.includes('fetch')) {
        throw new Error('网络连接失败，请检查您的网络')
      }
      
      throw error
    }
  }

  /**
   * 处理未授权错误
   */
  handleUnauthorized() {
    // 清除本地存储
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    localStorage.removeItem('refreshToken')
    
    // 触发登出事件
    window.dispatchEvent(new Event('userLogout'))
    
    // 跳转到登录页
    if (window.location.pathname !== '/login') {
      window.location.href = '/login'
    }
  }

  // 用户认证
  async login(username, password) {
    const data = await this.request('/auth/login', {
      method: 'POST',
      body: JSON.stringify({ username, password })
    })
    
    if (data.access_token) {
      this.token = data.access_token
      localStorage.setItem('token', data.access_token)
      localStorage.setItem('user', JSON.stringify({
        user_id: data.user_id,
        username: data.username,
        role: data.role
      }))
      
      // 触发自定义事件，通知Navbar组件更新用户信息
      window.dispatchEvent(new Event('userInfoChanged'))
    }
    
    return data
  }

  async register(username, password, role = 'user', secretKey = '') {
    return this.request('/auth/register', {
      method: 'POST',
      body: JSON.stringify({ username, password, role, secret_key: secretKey })
    })
  }



  // 球队管理
  async getTeams() {
    return this.request('/teams')
  }

  async createTeam(teamData) {
    return this.request('/teams', {
      method: 'POST',
      body: JSON.stringify(teamData)
    })
  }

  async updateTeam(teamId, teamData) {
    return this.request(`/teams/${teamId}`, {
      method: 'PUT',
      body: JSON.stringify(teamData)
    })
  }

  async deleteTeam(teamId) {
    return this.request(`/teams/${teamId}`, {
      method: 'DELETE'
    })
  }

  // 球员管理
  async getPlayers(teamId = null) {
    const params = teamId ? `?team_id=${teamId}` : ''
    return this.request(`/players${params}`)
  }

  async createPlayer(playerData) {
    return this.request('/players', {
      method: 'POST',
      body: JSON.stringify(playerData)
    })
  }

  async updatePlayer(playerId, playerData) {
    return this.request(`/players/${playerId}`, {
      method: 'PUT',
      body: JSON.stringify(playerData)
    })
  }

  async deletePlayer(playerId) {
    return this.request(`/players/${playerId}`, {
      method: 'DELETE'
    })
  }

  // 比赛管理
  async getGames(filters = {}) {
    const params = new URLSearchParams(filters).toString()
    return this.request(`/games${params ? '?' + params : ''}`)
  }

  async createGame(gameData) {
    return this.request('/games', {
      method: 'POST',
      body: JSON.stringify(gameData)
    })
  }

  async getGameDetail(gameId) {
    return this.request(`/games/${gameId}`)
  }

  async updateGame(gameId, gameData) {
    return this.request(`/games/${gameId}`, {
      method: 'PUT',
      body: JSON.stringify(gameData)
    })
  }

  async deleteGame(gameId) {
    return this.request(`/games/${gameId}`, {
      method: 'DELETE'
    })
  }

  async getGamePlayerTemplate(gameId) {
    return this.request(`/games/${gameId}/player-template`)
  }

  // 帖子管理
  async getPosts(gameId = null) {
    const params = gameId ? `?game_id=${gameId}` : ''
    return this.request(`/posts${params}`)
  }

  async createPost(postData) {
    return this.request('/posts', {
      method: 'POST',
      body: JSON.stringify(postData)
    })
  }

  // 获取帖子评论
  async getPostComments(postId) {
    return this.request(`/posts/${postId}/comments`)
  }

  // 创建评论
  async createComment(postId, commentData) {
    return this.request(`/posts/${postId}/comments`, {
      method: 'POST',
      body: JSON.stringify(commentData)
    })
  }

  // 删除评论
  async deleteComment(commentId) {
    return this.request(`/comments/${commentId}`, {
      method: 'DELETE'
    })
  }

  // 增加帖子浏览量
  async incrementPostView(postId) {
    return this.request(`/posts/${postId}/view`, {
      method: 'POST'
    })
  }

  // 点赞/取消点赞帖子
  async togglePostLike(postId) {
    return this.request(`/posts/${postId}/like`, {
      method: 'POST'
    })
  }

  // 取消点赞帖子
  async unlikePost(postId) {
    return this.request(`/posts/${postId}/like`, {
      method: 'DELETE'
    })
  }

  // 点赞/取消点赞评论
  async toggleCommentLike(commentId) {
    return this.request(`/comments/${commentId}/like`, {
      method: 'POST'
    })
  }

  // 取消点赞评论
  async unlikeComment(commentId) {
    return this.request(`/comments/${commentId}/like`, {
      method: 'DELETE'
    })
  }

  // 获取帖子点赞状态
  async getPostLikeStatus(postId) {
    return this.request(`/posts/${postId}/like-status`)
  }

  // 获取评论点赞状态
  async getCommentLikeStatus(commentId) {
    return this.request(`/comments/${commentId}/like-status`)
  }

  // SQL查询（仅数据分析师）
  async executeQuery(sqlQuery) {
    return this.request('/query', {
      method: 'POST',
      body: JSON.stringify({ query: sqlQuery })
    })
  }

  // 用户信息管理
  async getCurrentUser() {
    return this.request('/auth/me')
  }

  async updateUserProfile(profileData) {
    return this.request('/auth/me', {
      method: 'PUT',
      body: JSON.stringify(profileData)
    })
  }

  async getUserPosts() {
    return this.request('/auth/me/posts')
  }

  async getUserRatings() {
    return this.request('/auth/me/ratings')
  }

  async logout() {
    try {
      await this.request('/auth/logout', {
        method: 'POST'
      })
    } catch (error) {
      console.error('登出请求失败:', error)
    } finally {
      this.token = null
      localStorage.removeItem('token')
      localStorage.removeItem('user')
    }
  }

  // 注销账户
  async deleteAccount(password) {
    return this.request('/auth/delete-account', {
      method: 'DELETE',
      body: JSON.stringify({ password })
    })
  }

  // 验证密码
  async verifyPassword(password) {
    return this.request('/auth/verify-password', {
      method: 'POST',
      body: JSON.stringify({ password })
    })
  }

  // 比赛评分相关
  async getGameRatings(gameId) {
    return this.request(`/games/${gameId}/ratings`)
  }

  async submitRating(gameId, playerId, rating) {
    return this.request(`/games/${gameId}/ratings`, {
      method: 'POST',
      body: JSON.stringify({ player_id: playerId, rating })
    })
  }

  async getPlayerGameDetail(gameId, playerId) {
    return this.request(`/games/${gameId}/players/${playerId}`)
  }

  async submitPlayerComment(gameId, playerId, content) {
    return this.request(`/games/${gameId}/players/${playerId}/comments`, {
      method: 'POST',
      body: JSON.stringify({ content })
    })
  }
}

export default new ApiService()
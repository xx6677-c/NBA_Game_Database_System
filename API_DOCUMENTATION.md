# NBA比赛数据库系统 API文档

## 目录
- [认证接口 (Auth)](#认证接口-auth)
- [球队接口 (Teams)](#球队接口-teams)
- [球员接口 (Players)](#球员接口-players)
- [比赛接口 (Games)](#比赛接口-games)
- [帖子接口 (Posts)](#帖子接口-posts)
- [评论接口 (Comments)](#评论接口-comments)
- [SQL查询接口 (Query)](#sql查询接口-query)
- [榜单接口 (Rankings)](#榜单接口-rankings)
- [图片接口 (Images)](#图片接口-images)
- [商店接口 (Shop)](#商店接口-shop)

---

## 认证接口 (Auth)
Base URL: `/api/auth`

### 用户注册
- **URL**: `/register`
- **Method**: `POST`
- **Auth**: 不需要
- **Request Body**:
```json
{
  "username": "string",
  "password": "string",
  "role": "user|admin|analyst",
  "secret_key": "string (role为admin或analyst时必填)"
}
```

### 用户登录
- **URL**: `/login`
- **Method**: `POST`
- **Auth**: 不需要
- **Request Body**:
```json
{
  "username": "string",
  "password": "string"
}
```
- **Response**:
```json
{
  "access_token": "string",
  "user_id": "integer",
  "username": "string",
  "role": "string"
}
```

### 用户登出
- **URL**: `/logout`
- **Method**: `POST`
- **Auth**: Bearer Token

### 获取当前用户信息
- **URL**: `/me`
- **Method**: `GET`
- **Auth**: Bearer Token

### 更新用户信息
- **URL**: `/me`
- **Method**: `PUT`
- **Auth**: Bearer Token
- **Request Body**:
```json
{
  "email": "string",
  "phone": "string"
}
```

### 获取当前用户的帖子
- **URL**: `/me/posts`
- **Method**: `GET`
- **Auth**: Bearer Token

### 获取当前用户的评分
- **URL**: `/me/ratings`
- **Method**: `GET`
- **Auth**: Bearer Token

### 验证密码
- **URL**: `/verify-password`
- **Method**: `POST`
- **Auth**: Bearer Token
- **Request Body**:
```json
{
  "password": "string"
}
```

### 注销账户
- **URL**: `/delete-account`
- **Method**: `DELETE`
- **Auth**: Bearer Token
- **Request Body**:
```json
{
  "password": "string"
}
```

### 获取用户积分历史
- **URL**: `/me/points-history`
- **Method**: `GET`
- **Auth**: Bearer Token

---

## 球队接口 (Teams)
Base URL: `/api/teams`

### 获取所有球队
- **URL**: `/`
- **Method**: `GET`
- **Auth**: 不需要

### 创建球队
- **URL**: `/`
- **Method**: `POST`
- **Auth**: Bearer Token (管理员)
- **Request Body**:
```json
{
  "name": "string",
  "city": "string",
  "arena": "string",
  "conference": "东部|西部",
  "founded_year": "integer"
}
```

### 更新球队
- **URL**: `/{team_id}`
- **Method**: `PUT`
- **Auth**: Bearer Token (管理员)
- **Request Body**: 同创建球队

### 删除球队
- **URL**: `/{team_id}`
- **Method**: `DELETE`
- **Auth**: Bearer Token (管理员)

### 上传球队Logo
- **URL**: `/{team_id}/logo`
- **Method**: `POST`
- **Auth**: Bearer Token (管理员)
- **Content-Type**: `multipart/form-data`
- **Form Data**: `file` (image file)

---

## 球员接口 (Players)
Base URL: `/api/players`

### 获取球员列表
- **URL**: `/`
- **Method**: `GET`
- **Auth**: 不需要
- **Query Params**:
  - `team_id` (可选): 按球队筛选

### 创建球员
- **URL**: `/`
- **Method**: `POST`
- **Auth**: Bearer Token (管理员)
- **Request Body**:
```json
{
  "name": "string",
  "position": "string",
  "jersey_number": "integer",
  "height": "decimal",
  "weight": "decimal",
  "birth_date": "string (YYYY-MM-DD)",
  "nationality": "string",
  "current_team_id": "integer",
  "contract_expiry": "string (YYYY-MM-DD)",
  "salary": "decimal"
}
```

### 更新球员
- **URL**: `/{player_id}`
- **Method**: `PUT`
- **Auth**: Bearer Token (管理员)
- **Request Body**: 同创建球员

### 获取单个球员详情
- **URL**: `/{player_id}`
- **Method**: `GET`
- **Auth**: 不需要

### 删除球员
- **URL**: `/{player_id}`
- **Method**: `DELETE`
- **Auth**: Bearer Token (管理员)

### 上传球员照片
- **URL**: `/{player_id}/photo`
- **Method**: `POST`
- **Auth**: Bearer Token (管理员)
- **Content-Type**: `multipart/form-data`
- **Form Data**: `image` (image file)

### 获取球员雷达图数据
- **URL**: `/{player_id}/stats`
- **Method**: `GET`
- **Auth**: 不需要

### 获取球员详细统计数据
- **URL**: `/{player_id}/details`
- **Method**: `GET`
- **Auth**: 不需要

---

## 比赛接口 (Games)
Base URL: `/api/games`

### 获取比赛列表
- **URL**: `/`
- **Method**: `GET`
- **Auth**: 不需要
- **Query Params**:
  - `date_from` (可选): 开始日期
  - `date_to` (可选): 结束日期
  - `team_id` (可选): 球队ID

### 创建比赛
- **URL**: `/`
- **Method**: `POST`
- **Auth**: Bearer Token (管理员)
- **Request Body**:
```json
{
  "season": "string",
  "date": "string (YYYY-MM-DD HH:MM)",
  "home_team_id": "integer",
  "away_team_id": "integer",
  "status": "未开始|进行中|已结束",
  "home_score": "integer (可选)",
  "away_score": "integer (可选)",
  "venue": "string",
  "player_data": [
      {
          "player_id": "integer",
          "上场时间": "decimal",
          "得分": "integer",
          "篮板": "integer",
          "助攻": "integer",
          "抢断": "integer",
          "盖帽": "integer",
          "失误": "integer",
          "犯规": "integer",
          "正负值": "integer"
      }
  ]
}
```

### 更新比赛
- **URL**: `/{game_id}`
- **Method**: `PUT`
- **Auth**: Bearer Token (管理员)
- **Request Body**: 同创建比赛

### 删除比赛
- **URL**: `/{game_id}`
- **Method**: `DELETE`
- **Auth**: Bearer Token (管理员)

### 获取比赛详情
- **URL**: `/{game_id}`
- **Method**: `GET`
- **Auth**: 不需要 (登录用户可获取投票状态)

### 比赛竞猜投票
- **URL**: `/{game_id}/predict`
- **Method**: `POST`
- **Auth**: Bearer Token
- **Request Body**:
```json
{
  "team_id": "integer"
}
```

### 领取竞猜奖励
- **URL**: `/{game_id}/claim`
- **Method**: `POST`
- **Auth**: Bearer Token

### 获取比赛球员评分
- **URL**: `/{game_id}/ratings`
- **Method**: `GET`
- **Auth**: 不需要 (登录用户可获取自己的评分)

### 提交球员评分
- **URL**: `/{game_id}/ratings`
- **Method**: `POST`
- **Auth**: Bearer Token
- **Request Body**:
```json
{
  "player_id": "integer",
  "rating": "decimal (0-10)"
}
```

### 获取球员单场比赛详情（数据+评论）
- **URL**: `/{game_id}/players/{player_id}`
- **Method**: `GET`
- **Auth**: 不需要

### 提交球员评论
- **URL**: `/{game_id}/players/{player_id}/comments`
- **Method**: `POST`
- **Auth**: Bearer Token
- **Request Body**:
```json
{
  "content": "string"
}
```

---

## 帖子接口 (Posts)
Base URL: `/api/posts`

### 获取帖子列表
- **URL**: `/`
- **Method**: `GET`
- **Auth**: 不需要
- **Query Params**:
  - `game_id` (可选)

### 创建帖子
- **URL**: `/`
- **Method**: `POST`
- **Auth**: Bearer Token
- **Request Body**:
```json
{
  "title": "string",
  "content": "string",
  "game_id": "integer (可选)",
  "image_ids": ["integer"] (可选)
}
```

### 删除帖子
- **URL**: `/{post_id}`
- **Method**: `DELETE`
- **Auth**: Bearer Token (作者或管理员)

### 增加浏览量
- **URL**: `/{post_id}/view`
- **Method**: `POST`
- **Auth**: 不需要

### 点赞/取消点赞
- **URL**: `/{post_id}/like`
- **Method**: `POST` (点赞) | `DELETE` (取消点赞)
- **Auth**: Bearer Token

### 获取点赞状态
- **URL**: `/{post_id}/like-status`
- **Method**: `GET`
- **Auth**: Bearer Token

### 获取帖子评论
- **URL**: `/{post_id}/comments`
- **Method**: `GET`
- **Auth**: 不需要

### 创建帖子评论
- **URL**: `/{post_id}/comments`
- **Method**: `POST`
- **Auth**: Bearer Token
- **Request Body**:
```json
{
  "content": "string"
}
```

---

## 评论接口 (Comments)
Base URL: `/api/comments`

### 删除评论
- **URL**: `/{comment_id}`
- **Method**: `DELETE`
- **Auth**: Bearer Token (作者或管理员)

### 点赞/取消点赞评论
- **URL**: `/{comment_id}/like`
- **Method**: `POST` (点赞) | `DELETE` (取消点赞)
- **Auth**: Bearer Token

---

## SQL查询接口 (Query)
Base URL: `/api/query`

### 执行SQL查询
- **URL**: `/execute`
- **Method**: `POST`
- **Auth**: Bearer Token (数据分析师)
- **Request Body**:
```json
{
  "query": "SELECT * FROM Player LIMIT 10"
}
```

---

## 榜单接口 (Rankings)
Base URL: `/api/rankings`

### 获取球队战绩榜单
- **URL**: `/teams`
- **Method**: `GET`
- **Auth**: 不需要

### 获取球员数据榜单
- **URL**: `/players`
- **Method**: `GET`
- **Auth**: 不需要
- **Query Params**:
  - `stat`: `points`|`rebounds`|`assists`|`steals`|`blocks`|`minutes` (默认 `points`)
  - `limit`: integer (默认 10)

### 获取各项数据领跑者
- **URL**: `/players/leaders`
- **Method**: `GET`
- **Auth**: 不需要

---

## 图片接口 (Images)
Base URL: `/api/images`

### 上传图片
- **URL**: `/upload`
- **Method**: `POST`
- **Auth**: Bearer Token
- **Content-Type**: `multipart/form-data`
- **Form Data**: `file` (image file)

### 上传用户头像
- **URL**: `/avatar`
- **Method**: `POST`
- **Auth**: Bearer Token
- **Content-Type**: `multipart/form-data`
- **Form Data**: `file` (image file)

### 获取图片
- **URL**: `/{image_id}`
- **Method**: `GET`
- **Auth**: 不需要

---

## 商店接口 (Shop)
Base URL: `/api/shop`

### 抽取球星卡
- **URL**: `/draw`
- **Method**: `POST`
- **Auth**: Bearer Token
- **Cost**: 50 积分

### 获取我的球星卡
- **URL**: `/my-cards`
- **Method**: `GET`
- **Auth**: Bearer Token

---

## 错误响应格式

所有接口在出错时返回统一格式：
```json
{
  "error": "错误信息"
}
```

## HTTP状态码

- `200`: 成功
- `201`: 创建成功
- `400`: 请求参数错误
- `401`: 未授权 (未登录或Token无效)
- `403`: 权限不足
- `404`: 资源不存在
- `500`: 服务器内部错误

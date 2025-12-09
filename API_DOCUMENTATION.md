# NBA比赛数据库系统 API文档

## 目录
- [认证接口](#认证接口)
- [球队接口](#球队接口)
- [球员接口](#球员接口)
- [比赛接口](#比赛接口)
- [帖子接口](#帖子接口)
- [评论接口](#评论接口)
- [SQL查询接口](#sql查询接口)

---

## 认证接口

### 用户注册
- **URL**: `/api/auth/register`
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
- **Response**:
```json
{
  "message": "注册成功"
}
```

### 用户登录
- **URL**: `/api/auth/login`
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
- **URL**: `/api/auth/logout`
- **Method**: `POST`
- **Auth**: Bearer Token
- **Response**:
```json
{
  "message": "登出成功"
}
```

### 获取当前用户信息
- **URL**: `/api/auth/me`
- **Method**: `GET`
- **Auth**: Bearer Token
- **Response**:
```json
{
  "user_id": "integer",
  "username": "string",
  "role": "string",
  "register_time": "string",
  "last_login": "string",
  "email": "string",
  "phone": "string"
}
```

---

## 球队接口

### 获取所有球队
- **URL**: `/api/teams`
- **Method**: `GET`
- **Auth**: 不需要
- **Response**:
```json
[
  {
    "team_id": "integer",
    "name": "string",
    "city": "string",
    "arena": "string",
    "conference": "东部|西部",
    "founded_year": "integer"
  }
]
```

### 创建球队
- **URL**: `/api/teams`
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
- **URL**: `/api/teams/{team_id}`
- **Method**: `PUT`
- **Auth**: Bearer Token (管理员)
- **Request Body**: 同创建球队

### 删除球队
- **URL**: `/api/teams/{team_id}`
- **Method**: `DELETE`
- **Auth**: Bearer Token (管理员)

---

## 球员接口

### 获取球员列表
- **URL**: `/api/players?team_id={team_id}`
- **Method**: `GET`
- **Auth**: 不需要
- **Query Params**:
  - `team_id` (可选): 按球队筛选
- **Response**:
```json
[
  {
    "player_id": "integer",
    "name": "string",
    "position": "string",
    "jersey_number": "integer",
    "height": "decimal",
    "weight": "decimal",
    "birth_date": "string",
    "nationality": "string",
    "current_team_id": "integer",
    "team_name": "string",
    "contract_expiry": "string",
    "salary": "decimal"
  }
]
```

### 创建球员
- **URL**: `/api/players`
- **Method**: `POST`
- **Auth**: Bearer Token (管理员)

### 更新球员
- **URL**: `/api/players/{player_id}`
- **Method**: `PUT`
- **Auth**: Bearer Token (管理员)

### 删除球员
- **URL**: `/api/players/{player_id}`
- **Method**: `DELETE`
- **Auth**: Bearer Token (管理员)

---

## 比赛接口

### 获取比赛列表
- **URL**: `/api/games`
- **Method**: `GET`
- **Auth**: 不需要
- **Query Params**:
  - `date_from` (可选): 开始日期
  - `date_to` (可选): 结束日期
  - `team_id` (可选): 球队ID

### 获取比赛详情
- **URL**: `/api/games/{game_id}`
- **Method**: `GET`
- **Auth**: 不需要

---

## 帖子接口

### 获取帖子列表
- **URL**: `/api/posts?game_id={game_id}`
- **Method**: `GET`
- **Auth**: 不需要

### 创建帖子
- **URL**: `/api/posts`
- **Method**: `POST`
- **Auth**: Bearer Token
- **Request Body**:
```json
{
  "title": "string",
  "content": "string",
  "game_id": "integer (可选)"
}
```

### 增加浏览量
- **URL**: `/api/posts/{post_id}/view`
- **Method**: `POST`
- **Auth**: 不需要

### 点赞/取消点赞
- **URL**: `/api/posts/{post_id}/like`
- **Method**: `POST|DELETE`
- **Auth**: Bearer Token

### 获取点赞状态
- **URL**: `/api/posts/{post_id}/like-status`
- **Method**: `GET`
- **Auth**: Bearer Token

---

## SQL查询接口

### 执行SQL查询
- **URL**: `/api/query/execute`
- **Method**: `POST`
- **Auth**: Bearer Token (数据分析师)
- **Request Body**:
```json
{
  "query": "SELECT * FROM Player LIMIT 10"
}
```
- **Response**:
```json
{
  "success": true,
  "columns": ["column1", "column2"],
  "data": [{}, {}],
  "row_count": "integer"
}
```

---

## 错误响应格式

所有接口在出错时返回统一格式：
```json
{
  "success": false,
  "error": "错误信息",
  "error_code": "错误代码 (可选)"
}
```

## HTTP状态码

- `200`: 成功
- `201`: 创建成功
- `400`: 请求参数错误
- `401`: 未授权
- `403`: 权限不足
- `404`: 资源不存在
- `500`: 服务器内部错误

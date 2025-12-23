# NBA数据管理系统实现报告

## 1. 实现环境

本系统采用前后端分离的架构进行开发，具体实现环境如下：

### 1.1 硬件环境
- **操作系统**: Windows 10/11 / Linux (部署环境)
- **CPU**: Intel Core i5 及以上
- **内存**: 8GB 及以上
- **硬盘**: 256GB SSD 及以上

### 1.2 软件环境
- **数据库管理系统**: MySQL 8.0 / Huawei Cloud TaurusDB
- **后端开发语言**: Python 3.8+
- **后端框架**: Flask 2.3.3
- **前端开发框架**: Vue.js 3.2
- **前端UI库**: Element Plus
- **开发工具**: Visual Studio Code
- **接口测试工具**: Postman / Swagger

### 1.3 依赖库
- **后端**:
  - `Flask`: Web应用框架
  - `PyMySQL`: MySQL数据库驱动
  - `Flask-JWT-Extended`: JWT认证处理
  - `Flask-CORS`: 跨域资源共享处理
- **前端**:
  - `vue-router`: 路由管理
  - `echarts`: 数据可视化图表
  - `axios`: HTTP客户端

---

## 2. 基本表的定义

系统数据库设计包含18个基本表，涵盖了用户、球队、球员、比赛、社区互动及商城等功能模块。

### 2.1 核心实体表

#### (1) 用户表 (User)
```sql
CREATE TABLE IF NOT EXISTS User (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    用户名 VARCHAR(50) UNIQUE NOT NULL,
    密码 VARCHAR(255) NOT NULL,
    角色 ENUM('user', 'admin', 'analyst') DEFAULT 'user' NOT NULL,
    注册时间 DATETIME DEFAULT CURRENT_TIMESTAMP,
    最后登录时间 DATETIME,
    邮箱 VARCHAR(100),
    手机号 VARCHAR(20),
    points INT DEFAULT 0
);
```

#### (2) 球队表 (Team)
```sql
CREATE TABLE IF NOT EXISTS Team (
    team_id INT AUTO_INCREMENT PRIMARY KEY,
    名称 VARCHAR(10) UNIQUE NOT NULL,
    城市 VARCHAR(30) DEFAULT '',
    场馆 VARCHAR(30) DEFAULT '',
    分区 ENUM('东部', '西部') NOT NULL,
    成立年份 INT CHECK(成立年份 > 1900)
);
```

#### (3) 球员表 (Player)
```sql
CREATE TABLE IF NOT EXISTS Player (
    player_id INT AUTO_INCREMENT PRIMARY KEY,
    姓名 VARCHAR(50) NOT NULL,
    位置 ENUM('控球后卫', '得分后卫', '小前锋', '大前锋', '中锋') NOT NULL,
    球衣号 INT,
    身高 DECIMAL(3,2),
    体重 DECIMAL(5,2),
    出生日期 DATE,
    国籍 VARCHAR(50),
    当前球队ID INT,
    合同到期 DATE,
    薪资 DECIMAL(10,2),
    FOREIGN KEY (当前球队ID) REFERENCES Team(team_id) ON DELETE SET NULL
);
```

#### (4) 比赛表 (Game)
```sql
CREATE TABLE IF NOT EXISTS Game (
    game_id INT AUTO_INCREMENT PRIMARY KEY,
    赛季 VARCHAR(20) NOT NULL,
    日期 DATETIME NOT NULL,
    主队ID INT NOT NULL,
    客队ID INT NOT NULL,
    主队得分 INT,
    客队得分 INT,
    状态 ENUM('未开始','已结束') DEFAULT '未开始',
    获胜球队ID INT,
    场馆 VARCHAR(100),
    FOREIGN KEY (主队ID) REFERENCES Team(team_id),
    FOREIGN KEY (客队ID) REFERENCES Team(team_id),
    FOREIGN KEY (获胜球队ID) REFERENCES Team(team_id) ON DELETE SET NULL
);
```

### 2.2 社区与互动表

#### (5) 帖子表 (Post)
```sql
CREATE TABLE IF NOT EXISTS Post (
    post_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    标题 VARCHAR(50) NOT NULL,
    内容 TEXT NOT NULL,
    game_id INT,
    创建时间 DATETIME DEFAULT CURRENT_TIMESTAMP,
    浏览量 INT DEFAULT 0,
    点赞数 INT DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES User(user_id),
    FOREIGN KEY (game_id) REFERENCES Game(game_id) ON DELETE SET NULL
);
```

#### (6) 评论表 (Comment)
```sql
CREATE TABLE IF NOT EXISTS Comment (
    comment_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    player_id INT,
    game_id INT,
    post_id INT,
    内容 TEXT NOT NULL,
    创建时间 DATETIME DEFAULT CURRENT_TIMESTAMP,
    点赞数 INT DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES User(user_id),
    FOREIGN KEY (player_id) REFERENCES Player(player_id),
    FOREIGN KEY (game_id) REFERENCES Game(game_id),
    FOREIGN KEY (post_id) REFERENCES Post(post_id)
);
```

#### (7) 评分表 (Rating)
```sql
CREATE TABLE IF NOT EXISTS Rating (
    user_id INT NOT NULL,
    player_id INT NOT NULL,
    game_id INT NOT NULL,
    分数 DECIMAL(2,0) DEFAULT 0 CHECK(分数 BETWEEN 0 AND 10) NOT NULL,
    创建时间 DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, player_id, game_id),
    FOREIGN KEY (user_id) REFERENCES User(user_id),
    FOREIGN KEY (player_id) REFERENCES Player(player_id),
    FOREIGN KEY (game_id) REFERENCES Game(game_id)
);
```

#### (8) 图片表 (Image)
```sql
CREATE TABLE IF NOT EXISTS Image (
    image_id INT AUTO_INCREMENT PRIMARY KEY,
    名称 VARCHAR(50) NOT NULL,
    数据 LONGBLOB NOT NULL,
    MIME类型 VARCHAR(50) NOT NULL,
    上传时间 DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

#### (9) 竞猜表 (Prediction)
```sql
CREATE TABLE IF NOT EXISTS Prediction (
    prediction_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    game_id INT NOT NULL,
    predicted_team_id INT NOT NULL,
    is_claimed BOOLEAN DEFAULT FALSE,
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    update_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY unique_user_game (user_id, game_id),
    FOREIGN KEY (user_id) REFERENCES User(user_id),
    FOREIGN KEY (game_id) REFERENCES Game(game_id),
    FOREIGN KEY (predicted_team_id) REFERENCES Team(team_id)
);
```

#### (10) 帖子点赞表 (Post_Like)
```sql
CREATE TABLE IF NOT EXISTS Post_Like (
    like_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    post_id INT NOT NULL,
    创建时间 DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY unique_user_post (user_id, post_id),
    FOREIGN KEY (user_id) REFERENCES User(user_id) ON DELETE CASCADE,
    FOREIGN KEY (post_id) REFERENCES Post(post_id) ON DELETE CASCADE
);
```

#### (11) 评论点赞表 (Comment_Like)
```sql
CREATE TABLE IF NOT EXISTS Comment_Like (
    like_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    comment_id INT NOT NULL,
    创建时间 DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY unique_user_comment (user_id, comment_id),
    FOREIGN KEY (user_id) REFERENCES User(user_id) ON DELETE CASCADE,
    FOREIGN KEY (comment_id) REFERENCES Comment(comment_id) ON DELETE CASCADE
);
```

#### (12) 用户卡片表 (User_Card)
```sql
CREATE TABLE IF NOT EXISTS User_Card (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    player_id INT NOT NULL,
    get_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES User(user_id),
    FOREIGN KEY (player_id) REFERENCES Player(player_id)
);
```

### 2.3 关联关系表

#### (13) 球队-比赛关系表 (Team_Game)
```sql
CREATE TABLE IF NOT EXISTS Team_Game (
    team_id INT NOT NULL,
    game_id INT NOT NULL,
    主客类型 ENUM('主场', '客场') NOT NULL,
    PRIMARY KEY (team_id, game_id),
    FOREIGN KEY (team_id) REFERENCES Team(team_id),
    FOREIGN KEY (game_id) REFERENCES Game(game_id)
);
```

#### (14) 球员-比赛数据表 (Player_Game)
```sql
CREATE TABLE IF NOT EXISTS Player_Game (
    player_id INT NOT NULL,
    game_id INT NOT NULL,
    上场时间 DECIMAL(4,1) DEFAULT 0 CHECK(上场时间 >= 0) NOT NULL,
    得分 INT DEFAULT 0 CHECK(得分 >= 0) NOT NULL,
    篮板 INT DEFAULT 0 CHECK(篮板 >= 0) NOT NULL,
    助攻 INT DEFAULT 0 CHECK(助攻 >= 0) NOT NULL,
    抢断 INT DEFAULT 0 CHECK(抢断 >= 0) NOT NULL,
    盖帽 INT DEFAULT 0 CHECK(盖帽 >= 0) NOT NULL,
    失误 INT DEFAULT 0 CHECK(失误 >= 0) NOT NULL,
    犯规 INT DEFAULT 0 CHECK(犯规 >= 0) NOT NULL,
    正负值 INT,
    PRIMARY KEY (player_id, game_id),
    FOREIGN KEY (player_id) REFERENCES Player(player_id),
    FOREIGN KEY (game_id) REFERENCES Game(game_id)
);
```

#### (15) 用户-头像关系表 (User_Avatar)
```sql
CREATE TABLE IF NOT EXISTS User_Avatar (
    user_id INT PRIMARY KEY,
    image_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES User(user_id),
    FOREIGN KEY (image_id) REFERENCES Image(image_id)
);
```

#### (16) 帖子-图片关系表 (Post_Image)
```sql
CREATE TABLE IF NOT EXISTS Post_Image (
    post_id INT NOT NULL,
    image_id INT NOT NULL,
    PRIMARY KEY (image_id),
    FOREIGN KEY (post_id) REFERENCES Post(post_id),
    FOREIGN KEY (image_id) REFERENCES Image(image_id)
);
```

#### (17) 球员-图片关系表 (Player_Image)
```sql
CREATE TABLE IF NOT EXISTS Player_Image (
    player_id INT PRIMARY KEY,
    image_id INT NOT NULL UNIQUE,
    FOREIGN KEY (player_id) REFERENCES Player(player_id) ON DELETE CASCADE,
    FOREIGN KEY (image_id) REFERENCES Image(image_id) ON DELETE CASCADE
);
```

#### (18) 球队-队标关系表 (Team_Logo)
```sql
CREATE TABLE IF NOT EXISTS Team_Logo (
    team_id INT PRIMARY KEY,
    image_id INT NOT NULL UNIQUE,
    FOREIGN KEY (team_id) REFERENCES Team(team_id) ON DELETE CASCADE,
    FOREIGN KEY (image_id) REFERENCES Image(image_id) ON DELETE CASCADE
);
```

---

## 3. 触发器与存储过程的设计与实现说明

### 3.1 触发器 (Triggers)

#### 3.1.1 比赛获胜球队更新触发器 (Update)
**触发器名称**： `trg_game_update_winner`
**触发时机**： `BEFORE UPDATE ON Game`
**触发条件**： 比赛状态变更为'已结束'且比分不为空
**功能**：
当比赛状态更新为"已结束"时，自动根据主客队得分比较结果，更新 `获胜球队ID` 字段。
**关键设计**：
*   **状态检测**： `NEW.状态 = '已结束'` 确保仅在比赛结束时计算。
*   **胜负逻辑**： 比较 `主队得分` 和 `客队得分`，将胜者ID写入 `获胜球队ID`。
*   **平局处理**： 若平局则抛出错误 `SIGNAL SQLSTATE '45000'`，符合NBA规则。

#### 3.1.2 比赛获胜球队插入触发器 (Insert)
**触发器名称**： `trg_game_insert_winner`
**触发时机**： `BEFORE INSERT ON Game`
**触发条件**： 插入的比赛状态为'已结束'
**功能**：
当直接插入已结束的比赛记录时，自动计算并设置 `获胜球队ID`。
**关键设计**：
*   **数据完整性**： 检查 `NEW.主队ID = NEW.客队ID`，防止主客队相同。
*   **逻辑复用**： 包含与更新触发器相同的胜负判断逻辑。

#### 3.1.3 帖子点赞数增加触发器
**触发器名称**： `trg_post_like_increment`
**触发时机**： `AFTER INSERT ON Post_Like`
**触发条件**： 用户点赞帖子
**功能**：
当 `Post_Like` 表插入新记录时，自动将对应 `Post` 表的 `点赞数` 加 1。
**关键设计**：
*   **自动化统计**： 避免应用层多次查询更新，保证数据实时一致性。

#### 3.1.4 帖子点赞数减少触发器
**触发器名称**： `trg_post_like_decrement`
**触发时机**： `AFTER DELETE ON Post_Like`
**触发条件**： 用户取消点赞
**功能**：
当 `Post_Like` 表删除记录时，自动将对应 `Post` 表的 `点赞数` 减 1。
**关键设计**：
*   **边界保护**： 使用 `GREATEST(点赞数 - 1, 0)` 防止点赞数出现负数。

#### 3.1.5 用户注销清理触发器
**触发器名称**： `trg_user_delete_cleanup`
**触发时机**： `BEFORE DELETE ON User`
**触发条件**： 删除用户账号
**功能**：
在删除用户前，级联删除该用户关联的所有数据（帖子、评论、评分、竞猜、头像、卡片）。
**关键设计**：
*   **级联清理**： 确保不留孤儿数据，维护数据库整洁。
*   **完整性维护**： 显式删除 `Post`, `Comment`, `Rating` 等表中的关联记录。

### 3.2 存储过程 (Stored Procedures)

#### 3.2.1 用户注册存储过程
**存储过程名称**： `sp_register_user`
**输入参数**：
*   `p_username VARCHAR(50)` - 用户名
*   `p_password VARCHAR(255)` - 加密后的密码
*   `p_role VARCHAR(20)` - 用户角色
*   `p_created_at DATETIME` - 注册时间
**输出参数**： 无
**功能**： 向 User 表插入新用户记录。
**关键设计**：
*   **基础插入**： 封装 INSERT 操作，简化应用层调用。

#### 3.2.2 用户登录查询存储过程
**存储过程名称**： `sp_login_user`
**输入参数**：
*   `p_username VARCHAR(50)` - 用户名
**输出参数**： 无 (返回结果集)
**功能**： 根据用户名查询用户ID、密码哈希和角色，用于身份验证。
**关键设计**：
*   **安全查询**： 仅返回验证所需的必要字段。

#### 3.2.3 更新最后登录时间存储过程
**存储过程名称**： `sp_update_last_login`
**输入参数**：
*   `p_user_id INT` - 用户ID
*   `p_login_time DATETIME` - 登录时间
**输出参数**： 无
**功能**： 更新用户的最后登录时间字段。

#### 3.2.4 获取用户个人资料存储过程
**存储过程名称**： `sp_get_user_profile`
**输入参数**：
*   `p_user_id INT` - 用户ID
**输出参数**： 无 (返回结果集)
**功能**： 获取用户的详细信息，包括头像ID。
**关键设计**：
*   **联表查询**： 使用 `LEFT JOIN User_Avatar` 同时获取用户基本信息和头像信息。

#### 3.2.5 更新用户资料存储过程
**存储过程名称**： `sp_update_user_profile`
**输入参数**：
*   `p_user_id INT` - 用户ID
*   `p_email VARCHAR(100)` - 邮箱
*   `p_phone VARCHAR(20)` - 手机号
**输出参数**： 无
**功能**： 更新用户的邮箱和手机号。

#### 3.2.6 获取用户帖子列表存储过程
**存储过程名称**： `sp_get_user_posts`
**输入参数**：
*   `p_user_id INT` - 用户ID
**输出参数**： 无 (返回结果集)
**功能**： 获取指定用户发布的所有帖子，包含关联的比赛信息。
**关键设计**：
*   **多表关联**： 关联 `Game` 和 `Team` 表，展示帖子相关的比赛对阵信息。

#### 3.2.7 获取用户评分记录存储过程
**存储过程名称**： `sp_get_user_ratings`
**输入参数**：
*   `p_user_id INT` - 用户ID
**输出参数**： 无 (返回结果集)
**功能**： 获取用户的所有球员评分记录。

#### 3.2.8 获取用户密码哈希存储过程
**存储过程名称**： `sp_get_user_password_hash`
**输入参数**：
*   `p_user_id INT` - 用户ID
**输出参数**： 无 (返回结果集)
**功能**： 获取指定用户的密码哈希值，用于修改密码时的旧密码验证。

#### 3.2.9 删除用户账号存储过程
**存储过程名称**： `sp_delete_account`
**输入参数**：
*   `p_user_id INT` - 用户ID
**输出参数**： 无
**功能**： 删除用户记录。
**关键设计**：
*   **触发器依赖**： 依赖 `trg_user_delete_cleanup` 触发器自动清理关联数据。

#### 3.2.10 获取用户积分历史存储过程
**存储过程名称**： `sp_get_user_points_history`
**输入参数**：
*   `p_user_id INT` - 用户ID
**输出参数**： 无 (返回结果集)
**功能**： 获取用户通过竞猜获胜的历史记录。

#### 3.2.11 获取比赛列表存储过程
**存储过程名称**： `sp_get_games`
**输入参数**：
*   `p_date_from DATETIME` - 起始日期
*   `p_date_to DATETIME` - 结束日期
*   `p_team_id INT` - 球队ID筛选
**输出参数**： 无 (返回结果集)
**功能**： 根据日期范围和球队筛选比赛列表。
**关键设计**：
*   **动态筛选**： 使用 `(p_date_from IS NULL OR ...)` 实现可选参数查询。
*   **信息聚合**： 关联 `Team` 和 `Team_Logo` 表获取完整的比赛展示信息。

#### 3.2.12 获取比赛详情存储过程
**存储过程名称**： `sp_get_game_detail`
**输入参数**：
*   `p_game_id INT` - 比赛ID
**输出参数**： 无 (返回结果集)
**功能**： 获取单场比赛的详细信息。

#### 3.2.13 获取比赛竞猜统计存储过程
**存储过程名称**： `sp_get_game_prediction_stats`
**输入参数**：
*   `p_game_id INT` - 比赛ID
**输出参数**： 无 (返回结果集)
**功能**： 统计某场比赛各球队的支持人数。

#### 3.2.14 获取用户竞猜记录存储过程
**存储过程名称**： `sp_get_user_prediction`
**输入参数**：
*   `p_game_id INT` - 比赛ID
*   `p_user_id INT` - 用户ID
**输出参数**： 无 (返回结果集)
**功能**： 查询用户对某场比赛的竞猜情况。

#### 3.2.15 获取比赛球员数据存储过程
**存储过程名称**： `sp_get_game_player_stats`
**输入参数**：
*   `p_game_id INT` - 比赛ID
**输出参数**： 无 (返回结果集)
**功能**： 获取某场比赛所有球员的技术统计数据。

#### 3.2.16 检查竞猜状态存储过程
**存储过程名称**： `sp_check_prediction_status`
**输入参数**：
*   `p_game_id INT` - 比赛ID
*   `p_user_id INT` - 用户ID
**输出参数**： 无 (返回结果集)
**功能**： 检查比赛结果与用户竞猜是否一致，用于结算。

#### 3.2.17 领取竞猜奖励存储过程
**存储过程名称**： `sp_claim_reward`
**输入参数**：
*   `p_game_id INT` - 比赛ID
*   `p_user_id INT` - 用户ID
*   `p_reward_points INT` - 奖励积分数
**输出参数**： 无
**功能**： 发放竞猜奖励积分并标记为已领取。
**关键设计**：
*   **原子更新**： 同时更新 `User` 表积分和 `Prediction` 表状态。

#### 3.2.18 检查比赛状态存储过程
**存储过程名称**： `sp_check_game_status`
**输入参数**：
*   `p_game_id INT` - 比赛ID
**输出参数**： 无 (返回结果集)
**功能**： 获取比赛当前状态。

#### 3.2.19 用户竞猜存储过程
**存储过程名称**： `sp_predict_game`
**输入参数**：
*   `p_user_id INT` - 用户ID
*   `p_game_id INT` - 比赛ID
*   `p_team_id INT` - 预测获胜球队ID
**输出参数**： 无
**功能**： 插入或更新用户的竞猜记录。
**关键设计**：
*   **Upsert操作**： 使用 `ON DUPLICATE KEY UPDATE` 允许用户修改竞猜。

#### 3.2.20 创建比赛存储过程
**存储过程名称**： `sp_create_game`
**输入参数**：
*   `p_season`, `p_date`, `p_home_team_id`, `p_away_team_id`, `p_home_score`, `p_away_score`, `p_status`, `p_venue`
**输出参数**：
*   `p_game_id INT` - 新创建的比赛ID
**功能**： 创建新比赛并初始化主客场关系。
**关键设计**：
*   **事务性操作**： 同时插入 `Game` 表和 `Team_Game` 表，确保数据一致性。

#### 3.2.21 添加球员比赛数据存储过程
**存储过程名称**： `sp_add_player_game_stat`
**输入参数**：
*   `p_player_id`, `p_game_id`, `p_minutes`, `p_points` 等统计数据
**输出参数**： 无
**功能**： 录入球员单场比赛数据。

#### 3.2.22 更新比赛信息存储过程
**存储过程名称**： `sp_update_game`
**输入参数**：
*   `p_game_id` 及各比赛字段
**输出参数**： 无
**功能**： 更新比赛信息。
**关键设计**：
*   **动态更新**： 使用 `COALESCE` 函数仅更新非空参数对应的字段。
*   **关联同步**： 若球队ID变更，同步更新 `Team_Game` 表。

#### 3.2.23 删除球员比赛数据存储过程
**存储过程名称**： `sp_delete_player_game_stats`
**输入参数**：
*   `p_game_id INT` - 比赛ID
**输出参数**： 无
**功能**： 清空某场比赛的所有球员数据。

#### 3.2.24 删除比赛存储过程
**存储过程名称**： `sp_delete_game`
**输入参数**：
*   `p_game_id INT` - 比赛ID
**输出参数**： 无
**功能**： 删除比赛及其所有关联数据。
**关键设计**：
*   **手动级联**： 显式删除 `Rating`, `Player_Game`, `Team_Game`, `Post`, `Comment` 等表中的关联数据。

#### 3.2.25 获取帖子列表存储过程
**存储过程名称**： `sp_get_posts`
**输入参数**：
*   `p_game_id INT` - 比赛ID (可选)
**输出参数**： 无 (返回结果集)
**功能**： 获取帖子列表，支持按比赛筛选。
**关键设计**：
*   **子查询聚合**： 使用 `GROUP_CONCAT` 获取帖子关联的所有图片ID。

#### 3.2.26 创建帖子存储过程
**存储过程名称**： `sp_create_post`
**输入参数**：
*   `p_user_id`, `p_title`, `p_content`, `p_game_id`, `p_created_at`
**输出参数**：
*   `p_post_id INT` - 新帖子ID
**功能**： 发布新帖子。

#### 3.2.27 添加帖子图片存储过程
**存储过程名称**： `sp_add_post_image`
**输入参数**：
*   `p_post_id`, `p_image_id`
**输出参数**： 无
**功能**： 关联图片到帖子。

#### 3.2.28 增加帖子浏览量存储过程
**存储过程名称**： `sp_increment_post_view`
**输入参数**：
*   `p_post_id INT`
**输出参数**： 无
**功能**： 帖子浏览量加1。

#### 3.2.29 检查帖子点赞状态存储过程
**存储过程名称**： `sp_check_post_like`
**输入参数**：
*   `p_user_id`, `p_post_id`
**输出参数**： 无 (返回结果集)
**功能**： 检查用户是否已点赞某帖子。

#### 3.2.30 添加帖子点赞存储过程
**存储过程名称**： `sp_add_post_like`
**输入参数**：
*   `p_user_id`, `p_post_id`
**输出参数**： 无
**功能**： 用户点赞帖子。

#### 3.2.31 取消帖子点赞存储过程
**存储过程名称**： `sp_remove_post_like`
**输入参数**：
*   `p_user_id`, `p_post_id`
**输出参数**： 无
**功能**： 用户取消点赞。

#### 3.2.32 获取帖子评论存储过程
**存储过程名称**： `sp_get_post_comments`
**输入参数**：
*   `p_post_id INT`
**输出参数**： 无 (返回结果集)
**功能**： 获取帖子的所有评论。

#### 3.2.33 创建评论存储过程
**存储过程名称**： `sp_create_post_comment`
**输入参数**：
*   `p_user_id`, `p_post_id`, `p_content`, `p_created_at`
**输出参数**： 无
**功能**： 发布新评论。

#### 3.2.34 检查评论点赞状态存储过程
**存储过程名称**： `sp_check_comment_like`
**输入参数**：
*   `p_user_id`, `p_comment_id`
**输出参数**： 无 (返回结果集)
**功能**： 检查用户是否已点赞某评论。

#### 3.2.35 添加评论点赞存储过程
**存储过程名称**： `sp_add_comment_like`
**输入参数**：
*   `p_user_id`, `p_comment_id`
**输出参数**： 无
**功能**： 用户点赞评论，并更新计数。

#### 3.2.36 取消评论点赞存储过程
**存储过程名称**： `sp_remove_comment_like`
**输入参数**：
*   `p_user_id`, `p_comment_id`
**输出参数**： 无
**功能**： 用户取消点赞评论，并更新计数。

#### 3.2.37 获取球队排名存储过程
**存储过程名称**： `sp_get_team_standings`
**输入参数**：
*   `season_param VARCHAR(20)` - 赛季
**输出参数**： 无 (返回结果集)
**功能**： 计算并返回球队排名。
**关键设计**：
*   **复杂聚合**： 使用 `CASE WHEN` 统计胜负场次，动态计算胜率。

#### 3.2.38 删除帖子存储过程
**存储过程名称**： `sp_delete_post`
**输入参数**：
*   `p_post_id INT`
**输出参数**： 无
**功能**： 删除帖子及其所有关联内容。
**关键设计**：
*   **深度清理**： 删除帖子前先删除图片关联、评论点赞、评论、帖子点赞，最后删除帖子本身。

#### 3.2.39 获取球员排名存储过程
**存储过程名称**： `sp_get_player_rankings`
**输入参数**：
*   `p_stat_field VARCHAR(20)` - 排序字段 (得分/篮板等)
*   `p_limit INT` - 返回数量
**输出参数**： 无 (返回结果集)
**功能**： 根据指定数据维度获取球员排名。
**关键设计**：
*   **动态SQL**： 使用 `PREPARE` 和 `EXECUTE` 实现动态字段排序。

#### 3.2.40 获取球员列表存储过程
**存储过程名称**： `sp_get_players`
**输入参数**：
*   `p_team_id INT` - 球队ID (可选)
**输出参数**： 无 (返回结果集)
**功能**： 获取球员列表。

#### 3.2.41 创建球员存储过程
**存储过程名称**： `sp_create_player`
**输入参数**：
*   `p_name`, `p_position`, `p_jersey_number` 等球员信息
**输出参数**：
*   `p_player_id INT`
**功能**： 创建新球员。

#### 3.2.42 获取球员详情存储过程
**存储过程名称**： `sp_get_player_detail`
**输入参数**：
*   `p_player_id INT`
**输出参数**： 无 (返回结果集)
**功能**： 获取球员详细信息。

#### 3.2.43 更新球员信息存储过程
**存储过程名称**： `sp_update_player`
**输入参数**：
*   `p_player_id` 及各球员字段
**输出参数**： 无
**功能**： 更新球员信息。

#### 3.2.44 删除球员存储过程
**存储过程名称**： `sp_delete_player`
**输入参数**：
*   `p_player_id INT`
**输出参数**： 无
**功能**： 删除球员及其关联数据。

#### 3.2.45 获取球员生涯数据存储过程
**存储过程名称**： `sp_get_player_career_stats`
**输入参数**：
*   `p_player_id INT`
**输出参数**： 无 (返回结果集)
**功能**： 计算球员生涯平均数据。

#### 3.2.46 获取球员近期比赛存储过程
**存储过程名称**： `sp_get_player_recent_games`
**输入参数**：
*   `p_player_id INT`
**输出参数**： 无 (返回结果集)
**功能**： 获取球员最近10场比赛数据。

#### 3.2.47 获取所有球队存储过程
**存储过程名称**： `sp_get_all_teams`
**输入参数**： 无
**输出参数**： 无 (返回结果集)
**功能**： 获取所有球队列表。

#### 3.2.48 创建球队存储过程
**存储过程名称**： `sp_create_team`
**输入参数**：
*   `p_name`, `p_city`, `p_arena`, `p_conference`, `p_founded_year`
**输出参数**：
*   `p_team_id INT`
**功能**： 创建新球队。

#### 3.2.49 更新球队存储过程
**存储过程名称**： `sp_update_team`
**输入参数**：
*   `p_team_id` 及各球队字段
**输出参数**： 无
**功能**： 更新球队信息。

#### 3.2.50 删除球队存储过程
**存储过程名称**： `sp_delete_team`
**输入参数**：
*   `p_team_id INT`
**输出参数**： 无
**功能**： 删除球队及其关联数据。

#### 3.2.51 上传图片存储过程
**存储过程名称**： `sp_upload_image`
**输入参数**：
*   `p_name`, `p_data`, `p_mime_type`
**输出参数**：
*   `p_image_id INT`
**功能**： 上传图片数据。

#### 3.2.52 获取图片存储过程
**存储过程名称**： `sp_get_image`
**输入参数**：
*   `p_image_id INT`
**输出参数**： 无 (返回结果集)
**功能**： 获取图片二进制数据。

#### 3.2.53 更新用户头像存储过程
**存储过程名称**： `sp_update_user_avatar`
**输入参数**：
*   `p_user_id`, `p_image_id`
**输出参数**： 无
**功能**： 更新用户头像关联。

#### 3.2.54 积分抽卡存储过程
**存储过程名称**： `sp_draw_card`
**输入参数**：
*   `p_user_id INT` - 用户ID
*   `p_cost INT` - 抽卡消耗积分
**输出参数**：
*   `p_success BOOLEAN` - 是否成功
*   `p_message VARCHAR(255)` - 结果消息
*   `p_player_id`, `p_player_name`, `p_position`, `p_jersey_number`, `p_team_name`, `p_image_id` - 抽到的球员信息
*   `p_remaining_points INT` - 剩余积分
**功能**： 核心抽卡逻辑，扣除积分并随机发放球员卡。
**关键设计**：
*   **事务逻辑**： 检查积分 -> 扣除积分 -> 随机抽取 -> 发放卡片，保证原子性。
*   **随机算法**： `ORDER BY RAND() LIMIT 1` 实现随机抽取。

#### 3.2.55 获取我的卡片存储过程
**存储过程名称**： `sp_get_my_cards`
**输入参数**：
*   `p_user_id INT`
**输出参数**： 无 (返回结果集)
**功能**： 获取用户拥有的所有球星卡。

---

## 4. 支撑系统各功能实现的数据库操作SQL语句及其运行结果

### 4.1 用户注册
**操作**: 调用 `sp_register_user`
```sql
CALL sp_register_user('test_user', 'hashed_password', 'user', NOW());
```
**运行结果**: 用户表中新增一条记录，返回成功。

### 4.2 创建比赛与录入数据
**操作**: 调用 `sp_create_game` 和 `sp_add_player_game_stat`
```sql
-- 创建比赛
SET @game_id = 0;
CALL sp_create_game('2023-2024', '2023-12-25 20:00:00', 1, 2, 110, 105, '已结束', 'Crypto.com Arena', @game_id);
SELECT @game_id;

-- 录入球员数据
CALL sp_add_player_game_stat(101, @game_id, 35.5, 30, 5, 8, 2, 1, 3, 2, 15);
```
**运行结果**: 
- `Game` 表新增比赛记录，触发器自动计算获胜球队为ID 1。
- `Player_Game` 表新增球员数据记录。

### 4.3 积分抽卡
**操作**: 调用 `sp_draw_card`
```sql
SET @success = FALSE, @msg = '', @pid = 0, @pname = '', @pos = '', @num = 0, @tname = '', @img = 0, @rem = 0;
CALL sp_draw_card(1, 50, @success, @msg, @pid, @pname, @pos, @num, @tname, @img, @rem);
SELECT @success, @msg, @pname, @rem;
```
**运行结果**:
- 若积分充足：`@success`=1, `@msg`='恭喜获得球星卡！', `@pname`='Stephen Curry', `@rem`=剩余积分。
- 若积分不足：`@success`=0, `@msg`='积分不足'。

### 4.4 球员数据排名
**操作**: 调用 `sp_get_player_rankings`
```sql
CALL sp_get_player_rankings('得分', 5);
```
**运行结果**: 返回场均得分最高的前5名球员列表。
| player_id | name | avg_points | ... |
|-----------|------|------------|-----|
| 23 | LeBron James | 28.5 | ... |
| 30 | Stephen Curry | 27.8 | ... |

---

## 5. 总结与体会

### 5.1 任务总结
本项目成功构建了一个功能完善的NBA数据管理系统。
1.  **数据库设计**: 设计了符合第三范式的数据库模式，合理利用外键约束维护数据完整性。
2.  **后端开发**: 使用Flask框架搭建了RESTful API，通过PyMySQL与数据库交互，实现了所有核心业务逻辑。
3.  **数据库编程**: 大量使用存储过程和触发器，将复杂的业务逻辑（如抽卡、胜负判断、级联删除）下沉到数据库层，提高了系统的性能和安全性。
4.  **前端实现**: 构建了直观的用户界面，实现了数据的可视化展示和交互。

### 5.2 大作业体会
通过本次大作业，深入理解了数据库系统在实际应用开发中的核心地位。
-   **存储过程的优势**: 体会到了存储过程在处理复杂事务（如积分抽卡）时的原子性保障和性能优势，减少了网络传输开销。
-   **触发器的应用**: 学会了利用触发器自动维护数据一致性（如比赛胜负判定），简化了应用层代码。
-   **全栈开发视角**: 从数据库设计到后端API再到前端展示的完整流程，锻炼了全栈开发思维，理解了各层级之间的数据流转。
-   **问题解决**: 在开发过程中遇到了如参数传递不匹配（Python `callproc` 与 SQL `OUT` 参数）、事务隔离级别等问题，通过查阅文档和调试脚本逐一解决，提升了工程实践能力。

---
*生成时间: 2025年12月23日*
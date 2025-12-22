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
存储系统用户及其基本信息。
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
存储NBA球队的基本信息。
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
存储球员个人信息及合同状况。
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
存储比赛赛程及结果信息。
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

#### (7) 竞猜表 (Prediction)
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

### 2.3 资源与关联表

- **Image**: 存储图片二进制数据。
- **Team_Game**: 记录球队与比赛的主客场关系。
- **Player_Game**: 记录球员在单场比赛中的详细数据（得分、篮板、助攻等）。
- **User_Card**: 存储用户抽取的球星卡。
- **Post_Like / Comment_Like**: 记录点赞信息。
- **User_Avatar / Post_Image / Player_Image / Team_Logo**: 图片关联表。

---

## 3. 触发器与存储过程的设计与实现说明

### 3.1 触发器 (Triggers)

系统设计了5个触发器，用于维护数据一致性和自动化业务逻辑。

1.  **`trg_game_update_winner` & `trg_game_insert_winner`**
    -   **功能**: 当比赛状态更新为"已结束"或插入已结束的比赛时，自动根据主客队得分比较结果，更新 `获胜球队ID` 字段。
    -   **逻辑**: 比较 `主队得分` 和 `客队得分`，将胜者ID写入 `获胜球队ID`。若平局则抛出错误（NBA规则不允许平局结束）。

2.  **`trg_post_like_increment`**
    -   **功能**: 当 `Post_Like` 表插入新记录时触发。
    -   **逻辑**: 自动将对应 `Post` 表的 `点赞数` 加 1。

3.  **`trg_post_like_decrement`**
    -   **功能**: 当 `Post_Like` 表删除记录时触发。
    -   **逻辑**: 自动将对应 `Post` 表的 `点赞数` 减 1。

4.  **`trg_user_delete_cleanup`**
    -   **功能**: 在删除用户前触发。
    -   **逻辑**: 级联删除该用户关联的所有数据（帖子、评论、评分、竞猜、头像、卡片），确保不留孤儿数据。

### 3.2 存储过程 (Stored Procedures)

系统全面采用存储过程封装业务逻辑，共实现了约40个存储过程，主要分为以下几类：

#### (1) 用户认证与管理
-   `sp_register_user`: 用户注册。
-   `sp_login_user`: 用户登录验证。
-   `sp_get_user_profile` / `sp_update_user_profile`: 个人信息管理。

#### (2) 比赛业务
-   `sp_create_game`: 创建新比赛，同时初始化 `Team_Game` 关联。
-   `sp_get_games`: 支持按日期范围、球队筛选比赛列表。
-   `sp_add_player_game_stat`: 录入球员比赛数据。
-   `sp_predict_game`: 用户进行胜负竞猜。

#### (3) 球队与球员
-   `sp_create_team` / `sp_update_team`: 球队管理。
-   `sp_create_player` / `sp_update_player`: 球员管理。
-   `sp_get_player_rankings`: 根据指定数据维度（得分、篮板等）获取球员排名。

#### (4) 社区互动
-   `sp_create_post`: 发布帖子，支持事务处理。
-   `sp_add_post_like` / `sp_remove_post_like`: 点赞管理。
-   `sp_upload_image`: 图片上传处理。

#### (5) 积分商城
-   `sp_draw_card`: 核心抽卡逻辑。
    -   **实现细节**: 开启事务 -> 检查用户积分 -> 扣除积分 -> 随机选取一名球员 -> 插入 `User_Card` 表 -> 返回结果。保证了抽卡过程的原子性。

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
*生成时间: 2025年12月22日*

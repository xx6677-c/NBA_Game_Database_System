-- NBA比赛数据库系统初始化脚本
-- 使用现有数据库
USE h_db23373502;

-- 1. 用户表
CREATE TABLE IF NOT EXISTS User (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    用户名 VARCHAR(50) UNIQUE NOT NULL,
    密码 VARCHAR(255) NOT NULL,
    角色 ENUM('user', 'admin', 'analyst') DEFAULT 'user' NOT NULL,
    注册时间 DATETIME DEFAULT CURRENT_TIMESTAMP,
    最后登录时间 DATETIME,
    邮箱 VARCHAR(100),
    手机号 VARCHAR(20)
);

-- 2. 球队表
CREATE TABLE IF NOT EXISTS Team (
    team_id INT AUTO_INCREMENT PRIMARY KEY,
    名称 VARCHAR(10) UNIQUE NOT NULL,
    城市 VARCHAR(30) DEFAULT '',
    场馆 VARCHAR(30) DEFAULT '',
    分区 ENUM('东部', '西部') NOT NULL,
    成立年份 INT CHECK(成立年份 > 1900)
);

-- 3. 球员表
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

-- 4. 比赛表
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

-- 5. 帖子表
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

-- 6. 评论表
CREATE TABLE IF NOT EXISTS Comment (
    comment_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    player_id INT,
    game_id INT,
    post_id INT,
    内容 TEXT NOT NULL,
    创建时间 DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES User(user_id),
    FOREIGN KEY (player_id) REFERENCES Player(player_id),
    FOREIGN KEY (game_id) REFERENCES Game(game_id),
    FOREIGN KEY (post_id) REFERENCES Post(post_id)
);

-- 7. 评分表
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

-- 8. 图片表
CREATE TABLE IF NOT EXISTS Image (
    image_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    名称 VARCHAR(50) NOT NULL,
    数据 LONGBLOB NOT NULL,
    MIME类型 VARCHAR(50) NOT NULL,
    上传时间 DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES User(user_id)
);

-- 10. 球队-比赛关系表
CREATE TABLE IF NOT EXISTS Team_Game (
    team_id INT NOT NULL,
    game_id INT NOT NULL,
    主客类型 ENUM('主场', '客场') NOT NULL,
    PRIMARY KEY (team_id, game_id),
    FOREIGN KEY (team_id) REFERENCES Team(team_id),
    FOREIGN KEY (game_id) REFERENCES Game(game_id)
);

-- 11. 球员-比赛数据表
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

-- 12. 用户-头像关系表
CREATE TABLE IF NOT EXISTS User_Avatar (
    user_id INT PRIMARY KEY,
    image_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES User(user_id),
    FOREIGN KEY (image_id) REFERENCES Image(image_id)
);

-- 13. 帖子-图片关系表
CREATE TABLE IF NOT EXISTS Post_Image (
    post_id INT NOT NULL,
    image_id INT NOT NULL,
    PRIMARY KEY (image_id),
    FOREIGN KEY (post_id) REFERENCES Post(post_id),
    FOREIGN KEY (image_id) REFERENCES Image(image_id)
);

-- 14. 球员-图片关系表
CREATE TABLE IF NOT EXISTS Player_Image (
    player_id INT NOT NULL,
    image_id INT NOT NULL,
    类型 ENUM('头像', '生活照', '比赛照') NOT NULL,
    是否主图 BOOLEAN DEFAULT FALSE,
    PRIMARY KEY (image_id),
    FOREIGN KEY (player_id) REFERENCES Player(player_id),
    FOREIGN KEY (image_id) REFERENCES Image(image_id)
);

-- 15. 球队-队标关系表
CREATE TABLE IF NOT EXISTS Team_Logo (
    team_id INT PRIMARY KEY,
    image_id INT NOT NULL UNIQUE,
    FOREIGN KEY (team_id) REFERENCES Team(team_id) ON DELETE CASCADE,
    FOREIGN KEY (image_id) REFERENCES Image(image_id) ON DELETE CASCADE
);

-- 16. 管理员-比赛数据录入关系表
CREATE TABLE IF NOT EXISTS Admin_Insert (
    user_id INT NOT NULL,
    game_id INT NOT NULL,
    操作时间 DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (game_id),
    FOREIGN KEY (user_id) REFERENCES User(user_id),
    FOREIGN KEY (game_id) REFERENCES Game(game_id)
);

-- 插入初始数据
-- 插入管理员用户
INSERT IGNORE INTO User (用户名, 密码, 角色) VALUES 
('admin', 'admin123', 'admin'),
('analyst1', 'analyst123', 'analyst'),
('user1', 'user123', 'user');

-- 插入示例球队
INSERT IGNORE INTO Team (名称, 城市, 场馆, 分区, 成立年份) VALUES 
('湖人', '洛杉矶', 'Crypto.com球馆', '西部', 1947),
('勇士', '旧金山', '大通中心', '西部', 1946),
('凯尔特人', '波士顿', 'TD花园', '东部', 1946),
('热火', '迈阿密', 'FTX球馆', '东部', 1988);

-- 创建索引优化查询性能
CREATE INDEX idx_game_date ON Game(日期);
CREATE INDEX idx_player_team ON Player(当前球队ID);
CREATE INDEX idx_post_game ON Post(game_id);
CREATE INDEX idx_comment_post ON Comment(post_id);
CREATE INDEX idx_rating_player_game ON Rating(player_id, game_id);
-- NBA比赛数据库系统完整初始化脚本
-- 包含所有表结构、初始数据和功能扩展
USE h_db23373502;

-- ==========================================
-- 1. 基础表结构定义
-- ==========================================

-- 1. 用户表
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
    点赞数 INT DEFAULT 0,
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
    名称 VARCHAR(50) NOT NULL,
    数据 LONGBLOB NOT NULL,
    MIME类型 VARCHAR(50) NOT NULL,
    上传时间 DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 9. 竞猜表
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

-- 10. 帖子点赞表
CREATE TABLE IF NOT EXISTS Post_Like (
    like_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    post_id INT NOT NULL,
    创建时间 DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY unique_user_post (user_id, post_id),
    FOREIGN KEY (user_id) REFERENCES User(user_id) ON DELETE CASCADE,
    FOREIGN KEY (post_id) REFERENCES Post(post_id) ON DELETE CASCADE
);

-- 11. 评论点赞表
CREATE TABLE IF NOT EXISTS Comment_Like (
    like_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    comment_id INT NOT NULL,
    创建时间 DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY unique_user_comment (user_id, comment_id),
    FOREIGN KEY (user_id) REFERENCES User(user_id) ON DELETE CASCADE,
    FOREIGN KEY (comment_id) REFERENCES Comment(comment_id) ON DELETE CASCADE
);

-- 12. 用户卡片表
CREATE TABLE IF NOT EXISTS User_Card (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    player_id INT NOT NULL,
    get_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES User(user_id),
    FOREIGN KEY (player_id) REFERENCES Player(player_id)
);

-- ==========================================
-- 2. 关联关系表定义
-- ==========================================

-- 13. 球队-比赛关系表
CREATE TABLE IF NOT EXISTS Team_Game (
    team_id INT NOT NULL,
    game_id INT NOT NULL,
    主客类型 ENUM('主场', '客场') NOT NULL,
    PRIMARY KEY (team_id, game_id),
    FOREIGN KEY (team_id) REFERENCES Team(team_id),
    FOREIGN KEY (game_id) REFERENCES Game(game_id)
);

-- 14. 球员-比赛数据表
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

-- 15. 用户-头像关系表
CREATE TABLE IF NOT EXISTS User_Avatar (
    user_id INT PRIMARY KEY,
    image_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES User(user_id),
    FOREIGN KEY (image_id) REFERENCES Image(image_id)
);

-- 16. 帖子-图片关系表
CREATE TABLE IF NOT EXISTS Post_Image (
    post_id INT NOT NULL,
    image_id INT NOT NULL,
    PRIMARY KEY (image_id),
    FOREIGN KEY (post_id) REFERENCES Post(post_id),
    FOREIGN KEY (image_id) REFERENCES Image(image_id)
);

-- 17. 球员-图片关系表
CREATE TABLE IF NOT EXISTS Player_Image (
    player_id INT PRIMARY KEY,
    image_id INT NOT NULL UNIQUE,
    FOREIGN KEY (player_id) REFERENCES Player(player_id) ON DELETE CASCADE,
    FOREIGN KEY (image_id) REFERENCES Image(image_id) ON DELETE CASCADE
);

-- 18. 球队-队标关系表
CREATE TABLE IF NOT EXISTS Team_Logo (
    team_id INT PRIMARY KEY,
    image_id INT NOT NULL UNIQUE,
    FOREIGN KEY (team_id) REFERENCES Team(team_id) ON DELETE CASCADE,
    FOREIGN KEY (image_id) REFERENCES Image(image_id) ON DELETE CASCADE
);

-- ==========================================
-- 3. 索引定义
-- ==========================================

-- 现有索引
CREATE INDEX idx_game_date ON Game(日期);
CREATE INDEX idx_player_team ON Player(当前球队ID);
CREATE INDEX idx_post_game ON Post(game_id);
CREATE INDEX idx_comment_post ON Comment(post_id);
CREATE INDEX idx_rating_player_game ON Rating(player_id, game_id);
CREATE INDEX idx_post_like_user ON Post_Like(user_id);
CREATE INDEX idx_post_like_post ON Post_Like(post_id);
CREATE INDEX idx_comment_like_user ON Comment_Like(user_id);
CREATE INDEX idx_comment_like_comment ON Comment_Like(comment_id);

-- 新增性能优化索引
-- 用户表
CREATE INDEX idx_user_role ON User(角色);

-- 球员表
CREATE INDEX idx_player_name ON Player(姓名);
CREATE INDEX idx_player_position ON Player(位置);

-- 比赛表
CREATE INDEX idx_game_season ON Game(赛季);
CREATE INDEX idx_game_status ON Game(状态);
CREATE INDEX idx_game_home_team ON Game(主队ID);
CREATE INDEX idx_game_away_team ON Game(客队ID);

-- 帖子表
CREATE INDEX idx_post_user ON Post(user_id);
CREATE INDEX idx_post_created ON Post(创建时间);
CREATE INDEX idx_post_likes ON Post(点赞数);

-- 评论表
CREATE INDEX idx_comment_user ON Comment(user_id);
CREATE INDEX idx_comment_created ON Comment(创建时间);

-- 球员比赛数据表
CREATE INDEX idx_pg_points ON Player_Game(得分);
CREATE INDEX idx_pg_rebounds ON Player_Game(篮板);
CREATE INDEX idx_pg_assists ON Player_Game(助攻);
CREATE INDEX idx_pg_game_id ON Player_Game(game_id);

-- 竞猜表
CREATE INDEX idx_prediction_user ON Prediction(user_id);
CREATE INDEX idx_prediction_game ON Prediction(game_id);

-- ==========================================
-- 4. 初始数据插入
-- ==========================================

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

-- 插入示例点赞数据 (如果存在对应ID)
-- 注意：实际运行时需确保ID存在，这里使用 IGNORE 避免错误
INSERT IGNORE INTO Post_Like (user_id, post_id, 创建时间) VALUES
(1, 1, NOW()), (2, 1, NOW()), (3, 2, NOW()),
(1, 3, NOW()), (2, 3, NOW()), (1, 2, NOW()), (3, 1, NOW());

INSERT IGNORE INTO Comment_Like (user_id, comment_id, 创建时间) VALUES
(1, 1, NOW()), (2, 1, NOW()), (3, 2, NOW()),
(1, 3, NOW()), (2, 2, NOW()), (1, 2, NOW()), (3, 3, NOW());

-- ==========================================
-- 5. 触发器定义
-- ==========================================

-- 1. 自动更新比赛获胜球队
DELIMITER //
CREATE TRIGGER trg_game_update_winner
BEFORE UPDATE ON Game
FOR EACH ROW
BEGIN
    IF NEW.状态 = '已结束' AND NEW.主队得分 IS NOT NULL AND NEW.客队得分 IS NOT NULL THEN
        IF NEW.主队得分 > NEW.客队得分 THEN
            SET NEW.获胜球队ID = NEW.主队ID;
        ELSEIF NEW.客队得分 > NEW.主队得分 THEN
            SET NEW.获胜球队ID = NEW.客队ID;
        ELSE
            SIGNAL SQLSTATE '45000' 
            SET MESSAGE_TEXT = '错误：比赛结束时不能平局';
        END IF;
    END IF;
END//
DELIMITER ;

DELIMITER //
CREATE TRIGGER trg_game_insert_winner
BEFORE INSERT ON Game
FOR EACH ROW
BEGIN
    -- 自动计算获胜球队
    IF NEW.状态 = '已结束' AND NEW.主队得分 IS NOT NULL AND NEW.客队得分 IS NOT NULL THEN
        IF NEW.主队得分 > NEW.客队得分 THEN
            SET NEW.获胜球队ID = NEW.主队ID;
        ELSEIF NEW.客队得分 > NEW.主队得分 THEN
            SET NEW.获胜球队ID = NEW.客队ID;
        ELSE
            SIGNAL SQLSTATE '45000' 
            SET MESSAGE_TEXT = '错误：比赛结束时不能平局';
        END IF;
    END IF;
    
    -- 检查主客队是否相同
    IF NEW.主队ID = NEW.客队ID THEN
        SIGNAL SQLSTATE '45000' 
        SET MESSAGE_TEXT = '错误：主队和客队不能是同一支球队';
    END IF;
END//
DELIMITER ;

-- 2. 帖子点赞自动计数
DELIMITER //
CREATE TRIGGER trg_post_like_increment
AFTER INSERT ON Post_Like
FOR EACH ROW
BEGIN
    UPDATE Post SET 点赞数 = 点赞数 + 1 WHERE post_id = NEW.post_id;
END//
DELIMITER ;

DELIMITER //
CREATE TRIGGER trg_post_like_decrement
AFTER DELETE ON Post_Like
FOR EACH ROW
BEGIN
    UPDATE Post SET 点赞数 = GREATEST(点赞数 - 1, 0) WHERE post_id = OLD.post_id;
END//
DELIMITER ;

-- 3. 用户注销清理关联数据
DELIMITER //
CREATE TRIGGER trg_user_delete_cleanup
BEFORE DELETE ON User
FOR EACH ROW
BEGIN
    -- 删除用户相关的帖子
    DELETE FROM Post WHERE user_id = OLD.user_id;
    -- 删除用户相关的评论
    DELETE FROM Comment WHERE user_id = OLD.user_id;
    -- 删除用户相关的评分
    DELETE FROM Rating WHERE user_id = OLD.user_id;
    -- 删除用户相关的竞猜
    DELETE FROM Prediction WHERE user_id = OLD.user_id;
    -- 删除用户头像关联
    DELETE FROM User_Avatar WHERE user_id = OLD.user_id;
    -- 删除用户卡片
    DELETE FROM User_Card WHERE user_id = OLD.user_id;
    
    -- 注意：Post_Like 和 Comment_Like 表已设置 ON DELETE CASCADE，会自动删除
END//
DELIMITER ;

-- 4. 比赛删除时清理关联数据
DELIMITER //
CREATE TRIGGER trg_game_delete_cleanup
BEFORE DELETE ON Game
FOR EACH ROW
BEGIN
    -- 删除比赛相关的球队-比赛关联数据
    DELETE FROM Team_Game WHERE game_id = OLD.game_id;
    -- 删除比赛相关的球员-比赛数据
    DELETE FROM Player_Game WHERE game_id = OLD.game_id;
    -- 删除比赛相关的评分
    DELETE FROM Rating WHERE game_id = OLD.game_id;
    -- 删除比赛相关的竞猜
    DELETE FROM Prediction WHERE game_id = OLD.game_id;
END//
DELIMITER ;


-- ==========================================
-- 6. 存储过程定义 (Merged from all_procedures.sql)
-- ==========================================

USE h_db23373502;

-- ==========================================
-- 存储过程集合
-- ==========================================

-- ------------------------------------------
-- Auth 相关
-- ------------------------------------------

DROP PROCEDURE IF EXISTS sp_register_user;
DELIMITER //
CREATE PROCEDURE sp_register_user(
    IN p_username VARCHAR(50),
    IN p_password VARCHAR(255),
    IN p_role VARCHAR(20),
    IN p_created_at DATETIME
)
BEGIN
    INSERT INTO User (用户名, 密码, 角色, 注册时间) 
    VALUES (p_username, p_password, p_role, p_created_at);
END//
DELIMITER ;

DROP PROCEDURE IF EXISTS sp_login_user;
DELIMITER //
CREATE PROCEDURE sp_login_user(IN p_username VARCHAR(50))
BEGIN
    SELECT user_id, 密码, 角色 FROM User WHERE 用户名 = p_username;
END//
DELIMITER ;

DROP PROCEDURE IF EXISTS sp_update_last_login;
DELIMITER //
CREATE PROCEDURE sp_update_last_login(
    IN p_user_id INT,
    IN p_login_time DATETIME
)
BEGIN
    UPDATE User SET 最后登录时间 = p_login_time WHERE user_id = p_user_id;
END//
DELIMITER ;

DROP PROCEDURE IF EXISTS sp_get_user_profile;
DELIMITER //
CREATE PROCEDURE sp_get_user_profile(IN p_user_id INT)
BEGIN
    SELECT u.user_id, u.用户名, u.角色, u.注册时间, u.最后登录时间, u.邮箱, u.手机号, u.points, ua.image_id
    FROM User u
    LEFT JOIN User_Avatar ua ON u.user_id = ua.user_id
    WHERE u.user_id = p_user_id;
END//
DELIMITER ;

DROP PROCEDURE IF EXISTS sp_update_user_profile;
DELIMITER //
CREATE PROCEDURE sp_update_user_profile(
    IN p_user_id INT,
    IN p_email VARCHAR(100),
    IN p_phone VARCHAR(20)
)
BEGIN
    UPDATE User SET 邮箱 = p_email, 手机号 = p_phone 
    WHERE user_id = p_user_id;
END//
DELIMITER ;

DROP PROCEDURE IF EXISTS sp_get_user_posts;
DELIMITER //
CREATE PROCEDURE sp_get_user_posts(IN p_user_id INT)
BEGIN
    SELECT p.post_id, p.标题, p.内容, p.创建时间, p.浏览量, p.点赞数,
           g.赛季, ht.名称 as home_team, at.名称 as away_team
    FROM Post p
    LEFT JOIN Game g ON p.game_id = g.game_id
    LEFT JOIN Team ht ON g.主队ID = ht.team_id
    LEFT JOIN Team at ON g.客队ID = at.team_id
    WHERE p.user_id = p_user_id
    ORDER BY p.创建时间 DESC;
END//
DELIMITER ;

DROP PROCEDURE IF EXISTS sp_get_user_ratings;
DELIMITER //
CREATE PROCEDURE sp_get_user_ratings(IN p_user_id INT)
BEGIN
    SELECT r.user_id, r.player_id, r.game_id, r.分数, r.创建时间,
           p.姓名 as player_name, p.位置, t.名称 as team_name,
           g.赛季, g.日期, ht.名称 as home_team, at.名称 as away_team
    FROM Rating r
    JOIN Player p ON r.player_id = p.player_id
    LEFT JOIN Team t ON p.当前球队ID = t.team_id
    JOIN Game g ON r.game_id = g.game_id
    JOIN Team ht ON g.主队ID = ht.team_id
    JOIN Team at ON g.客队ID = at.team_id
    WHERE r.user_id = p_user_id
    ORDER BY r.创建时间 DESC;
END//
DELIMITER ;

DROP PROCEDURE IF EXISTS sp_get_user_password_hash;
DELIMITER //
CREATE PROCEDURE sp_get_user_password_hash(IN p_user_id INT)
BEGIN
    SELECT 密码 FROM User WHERE user_id = p_user_id;
END//
DELIMITER ;

DROP PROCEDURE IF EXISTS sp_delete_account;
DELIMITER //
CREATE PROCEDURE sp_delete_account(IN p_user_id INT)
BEGIN
    -- 触发器 trg_user_delete_cleanup 会处理关联数据的删除
    DELETE FROM User WHERE user_id = p_user_id;
END//
DELIMITER ;

DROP PROCEDURE IF EXISTS sp_get_user_points_history;
DELIMITER //
CREATE PROCEDURE sp_get_user_points_history(IN p_user_id INT)
BEGIN
    SELECT p.update_time, g.主队ID, g.客队ID, ht.名称 as home_team, at.名称 as away_team, 
           g.主队得分, g.客队得分, g.日期
    FROM Prediction p
    JOIN Game g ON p.game_id = g.game_id
    JOIN Team ht ON g.主队ID = ht.team_id
    JOIN Team at ON g.客队ID = at.team_id
    WHERE p.user_id = p_user_id AND p.is_claimed = TRUE
    ORDER BY p.update_time DESC;
END//
DELIMITER ;

-- ------------------------------------------
-- Games 相关
-- ------------------------------------------

DROP PROCEDURE IF EXISTS sp_get_games;
DELIMITER //
CREATE PROCEDURE sp_get_games(
    IN p_date_from DATETIME,
    IN p_date_to DATETIME,
    IN p_team_id INT
)
BEGIN
    SELECT g.game_id, g.赛季, g.日期, g.状态, g.主队得分, g.客队得分,
           ht.名称 as home_team, at.名称 as away_team,
           wt.名称 as winner_team, g.场馆,
           htl.image_id as home_logo_id, atl.image_id as away_logo_id,
           g.主队ID, g.客队ID
    FROM Game g
    JOIN Team ht ON g.主队ID = ht.team_id
    JOIN Team at ON g.客队ID = at.team_id
    LEFT JOIN Team wt ON g.获胜球队ID = wt.team_id
    LEFT JOIN Team_Logo htl ON ht.team_id = htl.team_id
    LEFT JOIN Team_Logo atl ON at.team_id = atl.team_id
    WHERE (p_date_from IS NULL OR g.日期 >= p_date_from)
      AND (p_date_to IS NULL OR g.日期 <= p_date_to)
      AND (p_team_id IS NULL OR g.主队ID = p_team_id OR g.客队ID = p_team_id)
    ORDER BY g.日期 DESC;
END//
DELIMITER ;

DROP PROCEDURE IF EXISTS sp_get_game_detail;
DELIMITER //
CREATE PROCEDURE sp_get_game_detail(IN p_game_id INT)
BEGIN
    SELECT g.game_id, g.赛季, g.日期, g.状态, g.主队得分, g.客队得分,
           g.主队ID, g.客队ID,
           ht.名称 as home_team, at.名称 as away_team,
           wt.名称 as winner_team, g.场馆, g.获胜球队ID
    FROM Game g
    JOIN Team ht ON g.主队ID = ht.team_id
    JOIN Team at ON g.客队ID = at.team_id
    LEFT JOIN Team wt ON g.获胜球队ID = wt.team_id
    WHERE g.game_id = p_game_id;
END//
DELIMITER ;

DROP PROCEDURE IF EXISTS sp_get_game_prediction_stats;
DELIMITER //
CREATE PROCEDURE sp_get_game_prediction_stats(IN p_game_id INT)
BEGIN
    SELECT predicted_team_id, COUNT(*) 
    FROM Prediction 
    WHERE game_id = p_game_id 
    GROUP BY predicted_team_id;
END//
DELIMITER ;

DROP PROCEDURE IF EXISTS sp_get_user_prediction;
DELIMITER //
CREATE PROCEDURE sp_get_user_prediction(
    IN p_game_id INT,
    IN p_user_id INT
)
BEGIN
    SELECT predicted_team_id, is_claimed
    FROM Prediction 
    WHERE game_id = p_game_id AND user_id = p_user_id;
END//
DELIMITER ;

DROP PROCEDURE IF EXISTS sp_get_game_player_stats;
DELIMITER //
CREATE PROCEDURE sp_get_game_player_stats(IN p_game_id INT)
BEGIN
    SELECT pg.player_id, pg.上场时间, pg.得分, pg.篮板, pg.助攻, 
           pg.抢断, pg.盖帽, pg.失误, pg.犯规, pg.正负值,
           p.姓名, p.位置, p.球衣号, t.名称 as team_name, t.team_id
    FROM Player_Game pg
    JOIN Player p ON pg.player_id = p.player_id
    JOIN Team t ON p.当前球队ID = t.team_id
    WHERE pg.game_id = p_game_id
    ORDER BY t.名称, p.球衣号;
END//
DELIMITER ;

DROP PROCEDURE IF EXISTS sp_check_prediction_status;
DELIMITER //
CREATE PROCEDURE sp_check_prediction_status(
    IN p_game_id INT,
    IN p_user_id INT
)
BEGIN
    SELECT g.状态, g.获胜球队ID, p.predicted_team_id, p.is_claimed
    FROM Prediction p
    JOIN Game g ON p.game_id = g.game_id
    WHERE p.game_id = p_game_id AND p.user_id = p_user_id;
END//
DELIMITER ;

DROP PROCEDURE IF EXISTS sp_claim_reward;
DELIMITER //
CREATE PROCEDURE sp_claim_reward(
    IN p_game_id INT,
    IN p_user_id INT,
    IN p_reward_points INT
)
BEGIN
    UPDATE User SET points = points + p_reward_points WHERE user_id = p_user_id;
    UPDATE Prediction SET is_claimed = TRUE WHERE game_id = p_game_id AND user_id = p_user_id;
END//
DELIMITER ;

DROP PROCEDURE IF EXISTS sp_check_game_status;
DELIMITER //
CREATE PROCEDURE sp_check_game_status(IN p_game_id INT)
BEGIN
    SELECT 状态, 日期 FROM Game WHERE game_id = p_game_id;
END//
DELIMITER ;

DROP PROCEDURE IF EXISTS sp_predict_game;
DELIMITER //
CREATE PROCEDURE sp_predict_game(
    IN p_user_id INT,
    IN p_game_id INT,
    IN p_team_id INT
)
BEGIN
    INSERT INTO Prediction (user_id, game_id, predicted_team_id)
    VALUES (p_user_id, p_game_id, p_team_id)
    ON DUPLICATE KEY UPDATE predicted_team_id = VALUES(predicted_team_id);
END//
DELIMITER ;

DROP PROCEDURE IF EXISTS sp_create_game;
DELIMITER //
CREATE PROCEDURE sp_create_game(
    IN p_season VARCHAR(20),
    IN p_date DATETIME,
    IN p_home_team_id INT,
    IN p_away_team_id INT,
    IN p_home_score INT,
    IN p_away_score INT,
    IN p_status VARCHAR(20),
    IN p_venue VARCHAR(100),
    OUT p_game_id INT
)
BEGIN
    INSERT INTO Game (赛季, 日期, 主队ID, 客队ID, 主队得分, 客队得分, 状态, 场馆)
    VALUES (p_season, p_date, p_home_team_id, p_away_team_id, p_home_score, p_away_score, p_status, p_venue);
    
    SET p_game_id = LAST_INSERT_ID();
    
    INSERT INTO Team_Game (team_id, game_id, 主客类型) VALUES (p_home_team_id, p_game_id, '主场');
    INSERT INTO Team_Game (team_id, game_id, 主客类型) VALUES (p_away_team_id, p_game_id, '客场');
END//
DELIMITER ;

DROP PROCEDURE IF EXISTS sp_add_player_game_stat;
DELIMITER //
CREATE PROCEDURE sp_add_player_game_stat(
    IN p_player_id INT,
    IN p_game_id INT,
    IN p_minutes DECIMAL(4,1),
    IN p_points INT,
    IN p_rebounds INT,
    IN p_assists INT,
    IN p_steals INT,
    IN p_blocks INT,
    IN p_turnovers INT,
    IN p_fouls INT,
    IN p_plus_minus INT
)
BEGIN
    INSERT INTO Player_Game (player_id, game_id, 上场时间, 得分, 篮板, 助攻, 抢断, 盖帽, 失误, 犯规, 正负值)
    VALUES (p_player_id, p_game_id, p_minutes, p_points, p_rebounds, p_assists, p_steals, p_blocks, p_turnovers, p_fouls, p_plus_minus);
END//
DELIMITER ;

DROP PROCEDURE IF EXISTS sp_update_game;
DELIMITER //
CREATE PROCEDURE sp_update_game(
    IN p_game_id INT,
    IN p_season VARCHAR(20),
    IN p_date DATETIME,
    IN p_home_team_id INT,
    IN p_away_team_id INT,
    IN p_status VARCHAR(20),
    IN p_home_score INT,
    IN p_away_score INT,
    IN p_venue VARCHAR(100)
)
BEGIN
    UPDATE Game 
    SET 赛季 = COALESCE(p_season, 赛季),
        日期 = COALESCE(p_date, 日期),
        主队ID = COALESCE(p_home_team_id, 主队ID),
        客队ID = COALESCE(p_away_team_id, 客队ID),
        状态 = COALESCE(p_status, 状态),
        主队得分 = COALESCE(p_home_score, 主队得分),
        客队得分 = COALESCE(p_away_score, 客队得分),
        场馆 = COALESCE(p_venue, 场馆)
    WHERE game_id = p_game_id;
    
    IF p_home_team_id IS NOT NULL THEN
        UPDATE Team_Game SET team_id = p_home_team_id WHERE game_id = p_game_id AND 主客类型 = '主场';
    END IF;
    
    IF p_away_team_id IS NOT NULL THEN
        UPDATE Team_Game SET team_id = p_away_team_id WHERE game_id = p_game_id AND 主客类型 = '客场';
    END IF;
END//
DELIMITER ;

DROP PROCEDURE IF EXISTS sp_delete_player_game_stats;
DELIMITER //
CREATE PROCEDURE sp_delete_player_game_stats(IN p_game_id INT)
BEGIN
    DELETE FROM Player_Game WHERE game_id = p_game_id;
END//
DELIMITER ;

DROP PROCEDURE IF EXISTS sp_delete_game;
DELIMITER //
CREATE PROCEDURE sp_delete_game(IN p_game_id INT)
BEGIN
    DELETE FROM Rating WHERE game_id = p_game_id;
    DELETE FROM Player_Game WHERE game_id = p_game_id;
    DELETE FROM Team_Game WHERE game_id = p_game_id;
    DELETE FROM Post WHERE game_id = p_game_id;
    DELETE FROM Comment WHERE game_id = p_game_id;
    DELETE FROM Game WHERE game_id = p_game_id;
END//
DELIMITER ;

-- ------------------------------------------
-- Posts 相关
-- ------------------------------------------

DROP PROCEDURE IF EXISTS sp_get_posts;
DELIMITER //
CREATE PROCEDURE sp_get_posts(IN p_game_id INT)
BEGIN
    SELECT p.post_id, p.标题, p.内容, p.创建时间, p.浏览量, p.点赞数,
           u.用户名, g.赛季, ht.名称 as home_team, at.名称 as away_team,
           (SELECT GROUP_CONCAT(image_id) FROM Post_Image WHERE post_id = p.post_id) as image_ids,
           p.user_id
    FROM Post p
    JOIN User u ON p.user_id = u.user_id
    LEFT JOIN Game g ON p.game_id = g.game_id
    LEFT JOIN Team ht ON g.主队ID = ht.team_id
    LEFT JOIN Team at ON g.客队ID = at.team_id
    WHERE (p_game_id IS NULL OR p.game_id = p_game_id)
    ORDER BY p.创建时间 DESC;
END//
DELIMITER ;

DROP PROCEDURE IF EXISTS sp_create_post;
DELIMITER //
CREATE PROCEDURE sp_create_post(
    IN p_user_id INT,
    IN p_title VARCHAR(50),
    IN p_content TEXT,
    IN p_game_id INT,
    IN p_created_at DATETIME,
    OUT p_post_id INT
)
BEGIN
    INSERT INTO Post (user_id, 标题, 内容, game_id, 创建时间)
    VALUES (p_user_id, p_title, p_content, p_game_id, p_created_at);
    SET p_post_id = LAST_INSERT_ID();
END//
DELIMITER ;

DROP PROCEDURE IF EXISTS sp_add_post_image;
DELIMITER //
CREATE PROCEDURE sp_add_post_image(
    IN p_post_id INT,
    IN p_image_id INT
)
BEGIN
    INSERT INTO Post_Image (post_id, image_id) VALUES (p_post_id, p_image_id);
END//
DELIMITER ;

DROP PROCEDURE IF EXISTS sp_increment_post_view;
DELIMITER //
CREATE PROCEDURE sp_increment_post_view(IN p_post_id INT)
BEGIN
    UPDATE Post SET 浏览量 = 浏览量 + 1 WHERE post_id = p_post_id;
END//
DELIMITER ;

DROP PROCEDURE IF EXISTS sp_check_post_like;
DELIMITER //
CREATE PROCEDURE sp_check_post_like(
    IN p_user_id INT,
    IN p_post_id INT
)
BEGIN
    SELECT COUNT(*) FROM Post_Like WHERE user_id = p_user_id AND post_id = p_post_id;
END//
DELIMITER ;

DROP PROCEDURE IF EXISTS sp_add_post_like;
DELIMITER //
CREATE PROCEDURE sp_add_post_like(
    IN p_user_id INT,
    IN p_post_id INT
)
BEGIN
    INSERT INTO Post_Like (user_id, post_id) VALUES (p_user_id, p_post_id);
END//
DELIMITER ;

DROP PROCEDURE IF EXISTS sp_remove_post_like;
DELIMITER //
CREATE PROCEDURE sp_remove_post_like(
    IN p_user_id INT,
    IN p_post_id INT
)
BEGIN
    DELETE FROM Post_Like WHERE user_id = p_user_id AND post_id = p_post_id;
END//
DELIMITER ;

DROP PROCEDURE IF EXISTS sp_get_post_comments;
DELIMITER //
CREATE PROCEDURE sp_get_post_comments(IN p_post_id INT)
BEGIN
    SELECT c.comment_id, c.内容, c.创建时间, u.用户名, u.user_id
    FROM Comment c
    JOIN User u ON c.user_id = u.user_id
    WHERE c.post_id = p_post_id
    ORDER BY c.创建时间 ASC;
END//
DELIMITER ;

DROP PROCEDURE IF EXISTS sp_create_post_comment;
DELIMITER //
CREATE PROCEDURE sp_create_post_comment(
    IN p_user_id INT,
    IN p_post_id INT,
    IN p_content TEXT,
    IN p_created_at DATETIME
)
BEGIN
    INSERT INTO Comment (user_id, post_id, 内容, 创建时间)
    VALUES (p_user_id, p_post_id, p_content, p_created_at);
END//
DELIMITER ;

-- ------------------------------------------
-- Comments 相关
-- ------------------------------------------

DROP PROCEDURE IF EXISTS sp_check_comment_like;
DELIMITER //
CREATE PROCEDURE sp_check_comment_like(
    IN p_user_id INT,
    IN p_comment_id INT
)
BEGIN
    SELECT COUNT(*) FROM Comment_Like WHERE user_id = p_user_id AND comment_id = p_comment_id;
END//
DELIMITER ;

DROP PROCEDURE IF EXISTS sp_add_comment_like;
DELIMITER //
CREATE PROCEDURE sp_add_comment_like(
    IN p_user_id INT,
    IN p_comment_id INT
)
BEGIN
    INSERT INTO Comment_Like (user_id, comment_id) VALUES (p_user_id, p_comment_id);
    UPDATE Comment SET 点赞数 = 点赞数 + 1 WHERE comment_id = p_comment_id;
END//
DELIMITER ;

DROP PROCEDURE IF EXISTS sp_remove_comment_like;
DELIMITER //
CREATE PROCEDURE sp_remove_comment_like(
    IN p_user_id INT,
    IN p_comment_id INT
)
BEGIN
    DELETE FROM Comment_Like WHERE user_id = p_user_id AND comment_id = p_comment_id;
    UPDATE Comment SET 点赞数 = 点赞数 - 1 WHERE comment_id = p_comment_id;
END//
DELIMITER ;

-- ------------------------------------------
-- Rankings 相关
-- ------------------------------------------

DROP PROCEDURE IF EXISTS sp_get_team_standings;
DELIMITER //
CREATE PROCEDURE sp_get_team_standings(IN season_param VARCHAR(20))
BEGIN
    SELECT 
        t.team_id,
        t.名称 as name,
        t.城市 as city,
        t.分区 as conference,
        COUNT(CASE WHEN g.获胜球队ID = t.team_id THEN 1 END) as wins,
        COUNT(CASE WHEN g.状态 = '已结束' AND g.获胜球队ID != t.team_id 
                   AND (g.主队ID = t.team_id OR g.客队ID = t.team_id) THEN 1 END) as losses,
        COUNT(CASE WHEN g.状态 = '已结束' 
                   AND (g.主队ID = t.team_id OR g.客队ID = t.team_id) THEN 1 END) as games_played
    FROM Team t
    LEFT JOIN Game g ON (g.主队ID = t.team_id OR g.客队ID = t.team_id) 
        AND g.状态 = '已结束'
        AND (season_param IS NULL OR season_param = '' OR g.赛季 = season_param)
    GROUP BY t.team_id, t.名称, t.城市, t.分区
    ORDER BY t.分区, 
        CASE WHEN COUNT(CASE WHEN g.状态 = '已结束' 
                            AND (g.主队ID = t.team_id OR g.客队ID = t.team_id) THEN 1 END) > 0 
             THEN COUNT(CASE WHEN g.获胜球队ID = t.team_id THEN 1 END) * 1.0 / 
                  COUNT(CASE WHEN g.状态 = '已结束' 
                            AND (g.主队ID = t.team_id OR g.客队ID = t.team_id) THEN 1 END)
             ELSE 0 END DESC;
END//
DELIMITER ;


-- Merged from add_delete_post_procedure.sql
USE h_db23373502;

DROP PROCEDURE IF EXISTS sp_delete_post;
DELIMITER //
CREATE PROCEDURE sp_delete_post(IN p_post_id INT)
BEGIN
    DELETE FROM Post_Image WHERE post_id = p_post_id;
    
    DELETE FROM Comment_Like 
    WHERE comment_id IN (SELECT comment_id FROM Comment WHERE post_id = p_post_id);
    
    DELETE FROM Comment WHERE post_id = p_post_id;
    
    DELETE FROM Post_Like WHERE post_id = p_post_id;
    
    DELETE FROM Post WHERE post_id = p_post_id;
END//
DELIMITER ;


-- Merged from add_player_rankings_procedure.sql
USE h_db23373502;

DROP PROCEDURE IF EXISTS sp_get_player_rankings;
DELIMITER //
CREATE PROCEDURE sp_get_player_rankings(
    IN p_stat_field VARCHAR(20),
    IN p_limit INT
)
BEGIN
    -- 简单的防注入检查
    IF p_stat_field NOT IN ('得分', '篮板', '助攻', '抢断', '盖帽') THEN
        SET p_stat_field = '得分';
    END IF;

    SET @sql = CONCAT('
        SELECT 
            p.player_id,
            p.姓名 as name,
            p.位置 as position,
            t.名称 as team_name,
            COUNT(pg.game_id) as games_played,
            ROUND(AVG(COALESCE(pg.得分, 0)), 1) as avg_points,
            ROUND(AVG(COALESCE(pg.篮板, 0)), 1) as avg_rebounds,
            ROUND(AVG(COALESCE(pg.助攻, 0)), 1) as avg_assists,
            ROUND(AVG(COALESCE(pg.抢断, 0)), 1) as avg_steals,
            ROUND(AVG(COALESCE(pg.盖帽, 0)), 1) as avg_blocks,
            ROUND(AVG(COALESCE(pg.上场时间, 0)), 1) as avg_minutes
        FROM Player p
        LEFT JOIN Player_Game pg ON p.player_id = pg.player_id
        LEFT JOIN Team t ON p.当前球队ID = t.team_id
        GROUP BY p.player_id, p.姓名, p.位置, t.名称
        ORDER BY AVG(COALESCE(pg.', p_stat_field, ', 0)) DESC, p.player_id
        LIMIT ', p_limit
    );
    
    PREPARE stmt FROM @sql;
    EXECUTE stmt;
    DEALLOCATE PREPARE stmt;
END//
DELIMITER ;


-- Merged from add_player_procedures.sql
USE h_db23373502;

DROP PROCEDURE IF EXISTS sp_get_players;
DELIMITER //
CREATE PROCEDURE sp_get_players(IN p_team_id INT)
BEGIN
    SELECT p.player_id, p.姓名, p.位置, p.球衣号, p.身高, p.体重, 
           p.出生日期, p.国籍, p.当前球队ID, t.名称 as team_name,
           p.合同到期, p.薪资, pi.image_id
    FROM Player p 
    LEFT JOIN Team t ON p.当前球队ID = t.team_id
    LEFT JOIN Player_Image pi ON p.player_id = pi.player_id
    WHERE (p_team_id IS NULL OR p.当前球队ID = p_team_id)
    ORDER BY t.名称, p.球衣号;
END//
DELIMITER ;

DROP PROCEDURE IF EXISTS sp_create_player;
DELIMITER //
CREATE PROCEDURE sp_create_player(
    IN p_name VARCHAR(50),
    IN p_position VARCHAR(20),
    IN p_jersey_number INT,
    IN p_height DECIMAL(3,2),
    IN p_weight DECIMAL(4,1),
    IN p_birth_date DATE,
    IN p_nationality VARCHAR(50),
    IN p_current_team_id INT,
    IN p_contract_expiry DATE,
    IN p_salary DECIMAL(12,2),
    OUT p_player_id INT
)
BEGIN
    INSERT INTO Player (姓名, 位置, 球衣号, 身高, 体重, 出生日期, 国籍, 当前球队ID, 合同到期, 薪资)
    VALUES (p_name, p_position, p_jersey_number, p_height, p_weight, p_birth_date, p_nationality, p_current_team_id, p_contract_expiry, p_salary);
    SET p_player_id = LAST_INSERT_ID();
END//
DELIMITER ;

DROP PROCEDURE IF EXISTS sp_get_player_detail;
DELIMITER //
CREATE PROCEDURE sp_get_player_detail(IN p_player_id INT)
BEGIN
    SELECT p.player_id, p.姓名, p.位置, p.球衣号, p.身高, p.体重, 
           p.出生日期, p.国籍, p.当前球队ID, t.名称 as team_name,
           p.合同到期, p.薪资, pi.image_id
    FROM Player p 
    LEFT JOIN Team t ON p.当前球队ID = t.team_id
    LEFT JOIN Player_Image pi ON p.player_id = pi.player_id
    WHERE p.player_id = p_player_id;
END//
DELIMITER ;

DROP PROCEDURE IF EXISTS sp_update_player;
DELIMITER //
CREATE PROCEDURE sp_update_player(
    IN p_player_id INT,
    IN p_name VARCHAR(50),
    IN p_position VARCHAR(20),
    IN p_jersey_number INT,
    IN p_height DECIMAL(3,2),
    IN p_weight DECIMAL(4,1),
    IN p_birth_date DATE,
    IN p_nationality VARCHAR(50),
    IN p_current_team_id INT,
    IN p_contract_expiry DATE,
    IN p_salary DECIMAL(12,2)
)
BEGIN
    UPDATE Player 
    SET 姓名 = COALESCE(p_name, 姓名),
        位置 = COALESCE(p_position, 位置),
        球衣号 = COALESCE(p_jersey_number, 球衣号),
        身高 = COALESCE(p_height, 身高),
        体重 = COALESCE(p_weight, 体重),
        出生日期 = COALESCE(p_birth_date, 出生日期),
        国籍 = COALESCE(p_nationality, 国籍),
        当前球队ID = COALESCE(p_current_team_id, 当前球队ID),
        合同到期 = COALESCE(p_contract_expiry, 合同到期),
        薪资 = COALESCE(p_salary, 薪资)
    WHERE player_id = p_player_id;
END//
DELIMITER ;

DROP PROCEDURE IF EXISTS sp_delete_player;
DELIMITER //
CREATE PROCEDURE sp_delete_player(IN p_player_id INT)
BEGIN
    DELETE FROM Player_Image WHERE player_id = p_player_id;
    DELETE FROM Player_Game WHERE player_id = p_player_id;
    DELETE FROM Rating WHERE player_id = p_player_id;
    DELETE FROM Comment WHERE player_id = p_player_id;
    DELETE FROM Player WHERE player_id = p_player_id;
END//
DELIMITER ;

DROP PROCEDURE IF EXISTS sp_get_player_career_stats;
DELIMITER //
CREATE PROCEDURE sp_get_player_career_stats(IN p_player_id INT)
BEGIN
    SELECT 
        COUNT(pg.game_id) as games_played,
        AVG(pg.上场时间) as avg_minutes,
        AVG(pg.得分) as avg_points,
        AVG(pg.篮板) as avg_rebounds,
        AVG(pg.助攻) as avg_assists,
        AVG(pg.抢断) as avg_steals,
        AVG(pg.盖帽) as avg_blocks,
        AVG(pg.失误) as avg_turnovers,
        AVG(pg.犯规) as avg_fouls,
        AVG(pg.正负值) as avg_plus_minus
    FROM Player_Game pg
    WHERE pg.player_id = p_player_id;
END//
DELIMITER ;

DROP PROCEDURE IF EXISTS sp_get_player_recent_games;
DELIMITER //
CREATE PROCEDURE sp_get_player_recent_games(IN p_player_id INT)
BEGIN
    SELECT 
        g.game_id, g.日期, g.赛季,
        ht.名称 as home_team, at.名称 as away_team,
        pg.上场时间, pg.得分, pg.篮板, pg.助攻, pg.抢断, pg.盖帽
    FROM Player_Game pg
    JOIN Game g ON pg.game_id = g.game_id
    JOIN Team ht ON g.主队ID = ht.team_id
    JOIN Team at ON g.客队ID = at.team_id
    WHERE pg.player_id = p_player_id
    ORDER BY g.日期 DESC
    LIMIT 10;
END//
DELIMITER ;


-- Merged from add_team_procedures.sql
USE h_db23373502;

DROP PROCEDURE IF EXISTS sp_get_all_teams;
DELIMITER //
CREATE PROCEDURE sp_get_all_teams()
BEGIN
    SELECT t.team_id, t.名称, t.城市, t.场馆, t.分区, t.成立年份, tl.image_id
    FROM Team t
    LEFT JOIN Team_Logo tl ON t.team_id = tl.team_id
    ORDER BY t.名称;
END//
DELIMITER ;

DROP PROCEDURE IF EXISTS sp_create_team;
DELIMITER //
CREATE PROCEDURE sp_create_team(
    IN p_name VARCHAR(50),
    IN p_city VARCHAR(50),
    IN p_arena VARCHAR(100),
    IN p_conference VARCHAR(20),
    IN p_founded_year INT,
    OUT p_team_id INT
)
BEGIN
    INSERT INTO Team (名称, 城市, 场馆, 分区, 成立年份) 
    VALUES (p_name, p_city, p_arena, p_conference, p_founded_year);
    SET p_team_id = LAST_INSERT_ID();
END//
DELIMITER ;

DROP PROCEDURE IF EXISTS sp_update_team;
DELIMITER //
CREATE PROCEDURE sp_update_team(
    IN p_team_id INT,
    IN p_name VARCHAR(50),
    IN p_city VARCHAR(50),
    IN p_arena VARCHAR(100),
    IN p_conference VARCHAR(20),
    IN p_founded_year INT
)
BEGIN
    UPDATE Team 
    SET 名称 = COALESCE(p_name, 名称),
        城市 = COALESCE(p_city, 城市),
        场馆 = COALESCE(p_arena, 场馆),
        分区 = COALESCE(p_conference, 分区),
        成立年份 = COALESCE(p_founded_year, 成立年份)
    WHERE team_id = p_team_id;
END//
DELIMITER ;

DROP PROCEDURE IF EXISTS sp_delete_team;
DELIMITER //
CREATE PROCEDURE sp_delete_team(IN p_team_id INT)
BEGIN
    DELETE FROM Team_Logo WHERE team_id = p_team_id;
    DELETE FROM Team_Game WHERE team_id = p_team_id;
    -- 注意：删除球队可能需要处理球员关联，这里假设球员关联设置为NULL或级联删除
    -- 如果有外键约束，可能需要先更新球员
    UPDATE Player SET 当前球队ID = NULL WHERE 当前球队ID = p_team_id;
    DELETE FROM Team WHERE team_id = p_team_id;
END//
DELIMITER ;

DROP PROCEDURE IF EXISTS sp_get_team_detail;
DELIMITER //
CREATE PROCEDURE sp_get_team_detail(IN p_team_id INT)
BEGIN
    SELECT t.team_id, t.名称, t.城市, t.场馆, t.分区, t.成立年份, tl.image_id
    FROM Team t
    LEFT JOIN Team_Logo tl ON t.team_id = tl.team_id
    WHERE t.team_id = p_team_id;
END//
DELIMITER ;


-- Merged from add_image_procedures.sql
USE h_db23373502;

DROP PROCEDURE IF EXISTS sp_upload_image;
DELIMITER //
CREATE PROCEDURE sp_upload_image(
    IN p_name VARCHAR(255),
    IN p_data LONGBLOB,
    IN p_mime_type VARCHAR(50),
    OUT p_image_id INT
)
BEGIN
    INSERT INTO Image (名称, 数据, MIME类型)
    VALUES (p_name, p_data, p_mime_type);
    SET p_image_id = LAST_INSERT_ID();
END//
DELIMITER ;

DROP PROCEDURE IF EXISTS sp_get_image;
DELIMITER //
CREATE PROCEDURE sp_get_image(IN p_image_id INT)
BEGIN
    SELECT 数据, MIME类型 FROM Image WHERE image_id = p_image_id;
END//
DELIMITER ;


-- Merged from add_user_avatar_procedure.sql
USE h_db23373502;

DROP PROCEDURE IF EXISTS sp_update_user_avatar;
DELIMITER //
CREATE PROCEDURE sp_update_user_avatar(
    IN p_user_id INT,
    IN p_image_id INT
)
BEGIN
    INSERT INTO User_Avatar (user_id, image_id)
    VALUES (p_user_id, p_image_id)
    ON DUPLICATE KEY UPDATE image_id = VALUES(image_id);
END//
DELIMITER ;


-- Merged from add_shop_procedures.sql
DROP PROCEDURE IF EXISTS sp_draw_card;
DELIMITER //

CREATE PROCEDURE sp_draw_card(
    IN p_user_id INT,
    IN p_cost INT,
    OUT p_success BOOLEAN,
    OUT p_message VARCHAR(255),
    OUT p_player_id INT,
    OUT p_player_name VARCHAR(100),
    OUT p_position VARCHAR(50),
    OUT p_jersey_number INT,
    OUT p_team_name VARCHAR(100),
    OUT p_image_id INT,
    OUT p_remaining_points INT
)
BEGIN
    DECLARE v_points INT;
    
    -- Check points
    SELECT points INTO v_points FROM User WHERE user_id = p_user_id;
    
    IF v_points < p_cost THEN
        SET p_success = FALSE;
        SET p_message = '积分不足';
        SET p_remaining_points = v_points;
    ELSE
        -- Select random player
        SELECT p.player_id, p.姓名, p.位置, p.球衣号, t.名称, pi.image_id
        INTO p_player_id, p_player_name, p_position, p_jersey_number, p_team_name, p_image_id
        FROM Player p
        JOIN Team t ON p.当前球队ID = t.team_id
        LEFT JOIN Player_Image pi ON p.player_id = pi.player_id
        ORDER BY RAND() LIMIT 1;
        
        IF p_player_id IS NULL THEN
            SET p_success = FALSE;
            SET p_message = '卡池为空';
            SET p_remaining_points = v_points;
        ELSE
            -- Deduct points
            UPDATE User SET points = points - p_cost WHERE user_id = p_user_id;
            
            -- Add card
            INSERT INTO User_Card (user_id, player_id) VALUES (p_user_id, p_player_id);
            
            SET p_success = TRUE;
            SET p_message = '恭喜获得球星卡！';
            SET p_remaining_points = v_points - p_cost;
        END IF;
    END IF;
END //
DELIMITER ;

DROP PROCEDURE IF EXISTS sp_get_my_cards;
DELIMITER //
CREATE PROCEDURE sp_get_my_cards(
    IN p_user_id INT
)
BEGIN
    SELECT uc.id, uc.get_time,
           p.player_id, p.姓名, p.位置, p.球衣号, t.名称 as team_name, pi.image_id
    FROM User_Card uc
    JOIN Player p ON uc.player_id = p.player_id
    JOIN Team t ON p.当前球队ID = t.team_id
    LEFT JOIN Player_Image pi ON p.player_id = pi.player_id
    WHERE uc.user_id = p_user_id
    ORDER BY uc.get_time DESC;
END //

DELIMITER ;

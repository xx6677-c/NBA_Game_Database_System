USE h_db23373502;

-- ==========================================
-- 补充存储过程
-- ==========================================

-- 1. 获取某场比赛所有球员及其评分
DROP PROCEDURE IF EXISTS sp_get_game_players_with_ratings;
DELIMITER //
CREATE PROCEDURE sp_get_game_players_with_ratings(IN p_game_id INT)
BEGIN
    SELECT p.player_id, p.姓名, p.当前球队ID, t.名称 as team_name,
           AVG(r.分数) as avg_rating, COUNT(r.user_id) as rating_count,
           pi.image_id
    FROM Player_Game pg
    JOIN Player p ON pg.player_id = p.player_id
    JOIN Team t ON p.当前球队ID = t.team_id
    LEFT JOIN Rating r ON p.player_id = r.player_id AND r.game_id = pg.game_id
    LEFT JOIN Player_Image pi ON p.player_id = pi.player_id
    WHERE pg.game_id = p_game_id
    GROUP BY p.player_id
    ORDER BY t.team_id, p.球衣号;
END//
DELIMITER ;

-- 2. 获取特定用户对特定球员在特定比赛的评分
DROP PROCEDURE IF EXISTS sp_get_user_player_rating;
DELIMITER //
CREATE PROCEDURE sp_get_user_player_rating(
    IN p_user_id INT,
    IN p_player_id INT,
    IN p_game_id INT
)
BEGIN
    SELECT 分数 FROM Rating 
    WHERE user_id = p_user_id AND player_id = p_player_id AND game_id = p_game_id;
END//
DELIMITER ;

-- 3. 提交或更新评分
DROP PROCEDURE IF EXISTS sp_upsert_rating;
DELIMITER //
CREATE PROCEDURE sp_upsert_rating(
    IN p_user_id INT,
    IN p_player_id INT,
    IN p_game_id INT,
    IN p_rating DECIMAL(3,1)
)
BEGIN
    INSERT INTO Rating (user_id, player_id, game_id, 分数)
    VALUES (p_user_id, p_player_id, p_game_id, p_rating)
    ON DUPLICATE KEY UPDATE 分数 = p_rating, 创建时间 = CURRENT_TIMESTAMP;
END//
DELIMITER ;

-- 4. 获取单个球员在某场比赛的数据
DROP PROCEDURE IF EXISTS sp_get_player_game_stats_single;
DELIMITER //
CREATE PROCEDURE sp_get_player_game_stats_single(
    IN p_game_id INT,
    IN p_player_id INT
)
BEGIN
    SELECT pg.上场时间, pg.得分, pg.篮板, pg.助攻, 
           pg.抢断, pg.盖帽, pg.失误, pg.犯规, pg.正负值,
           p.姓名, p.位置, p.球衣号, t.名称 as team_name, t.team_id
    FROM Player_Game pg
    JOIN Player p ON pg.player_id = p.player_id
    JOIN Team t ON p.当前球队ID = t.team_id
    WHERE pg.game_id = p_game_id AND pg.player_id = p_player_id;
END//
DELIMITER ;

-- 5. 获取球员评分统计
DROP PROCEDURE IF EXISTS sp_get_player_rating_summary;
DELIMITER //
CREATE PROCEDURE sp_get_player_rating_summary(
    IN p_game_id INT,
    IN p_player_id INT
)
BEGIN
    SELECT AVG(分数), COUNT(*) FROM Rating
    WHERE game_id = p_game_id AND player_id = p_player_id;
END//
DELIMITER ;

-- 6. 获取球员比赛评论
DROP PROCEDURE IF EXISTS sp_get_player_game_comments;
DELIMITER //
CREATE PROCEDURE sp_get_player_game_comments(
    IN p_game_id INT,
    IN p_player_id INT
)
BEGIN
    SELECT c.comment_id, c.内容, c.创建时间, u.用户名, u.user_id
    FROM Comment c
    JOIN User u ON c.user_id = u.user_id
    WHERE c.game_id = p_game_id AND c.player_id = p_player_id
    ORDER BY c.创建时间 DESC;
END//
DELIMITER ;

-- 7. 创建球员评论
DROP PROCEDURE IF EXISTS sp_create_player_comment;
DELIMITER //
CREATE PROCEDURE sp_create_player_comment(
    IN p_user_id INT,
    IN p_game_id INT,
    IN p_player_id INT,
    IN p_content TEXT,
    IN p_created_at DATETIME
)
BEGIN
    INSERT INTO Comment (user_id, game_id, player_id, 内容, 创建时间)
    VALUES (p_user_id, p_game_id, p_player_id, p_content, p_created_at);
END//
DELIMITER ;

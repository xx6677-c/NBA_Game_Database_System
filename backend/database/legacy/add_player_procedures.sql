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

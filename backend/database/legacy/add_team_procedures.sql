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

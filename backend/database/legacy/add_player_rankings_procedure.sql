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

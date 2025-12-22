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

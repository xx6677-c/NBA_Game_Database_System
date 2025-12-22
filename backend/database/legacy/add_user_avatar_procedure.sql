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

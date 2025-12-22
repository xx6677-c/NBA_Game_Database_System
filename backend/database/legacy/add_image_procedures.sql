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
END//
DELIMITER ;

DROP PROCEDURE IF EXISTS sp_get_image;
DELIMITER //
CREATE PROCEDURE sp_get_image(IN p_image_id INT)
BEGIN
    SELECT 数据, MIME类型 FROM Image WHERE image_id = p_image_id;
END//
DELIMITER ;

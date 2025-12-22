DELIMITER //

CREATE PROCEDURE sp_get_image(
    IN p_image_id INT
)
BEGIN
    SELECT 数据, MIME类型
    FROM Image
    WHERE image_id = p_image_id;
END //

DELIMITER ;

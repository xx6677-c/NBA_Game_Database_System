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

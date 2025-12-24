DROP PROCEDURE IF EXISTS sp_delete_comment;
DELIMITER //
CREATE PROCEDURE sp_delete_comment(
    IN p_comment_id INT
)
BEGIN
    -- 先删除评论的点赞记录
    DELETE FROM Comment_Like WHERE comment_id = p_comment_id;
    -- 再删除评论
    DELETE FROM Comment WHERE comment_id = p_comment_id;
END//
DELIMITER ;

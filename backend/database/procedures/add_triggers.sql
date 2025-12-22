USE h_db23373502;

-- ==========================================
-- 触发器定义
-- ==========================================

-- 1. 自动更新比赛获胜球队 (UPDATE)
DROP TRIGGER IF EXISTS trg_game_update_winner;
DELIMITER //
CREATE TRIGGER trg_game_update_winner
BEFORE UPDATE ON Game
FOR EACH ROW
BEGIN
    IF NEW.状态 = '已结束' AND NEW.主队得分 IS NOT NULL AND NEW.客队得分 IS NOT NULL THEN
        IF NEW.主队得分 > NEW.客队得分 THEN
            SET NEW.获胜球队ID = NEW.主队ID;
        ELSEIF NEW.客队得分 > NEW.主队得分 THEN
            SET NEW.获胜球队ID = NEW.客队ID;
        ELSE
            SIGNAL SQLSTATE '45000' 
            SET MESSAGE_TEXT = '错误：比赛结束时不能平局';
        END IF;
    END IF;
END//
DELIMITER ;

-- 2. 自动更新比赛获胜球队 & 检查主客队 (INSERT)
DROP TRIGGER IF EXISTS trg_game_insert_winner;
DELIMITER //
CREATE TRIGGER trg_game_insert_winner
BEFORE INSERT ON Game
FOR EACH ROW
BEGIN
    -- 自动计算获胜球队
    IF NEW.状态 = '已结束' AND NEW.主队得分 IS NOT NULL AND NEW.客队得分 IS NOT NULL THEN
        IF NEW.主队得分 > NEW.客队得分 THEN
            SET NEW.获胜球队ID = NEW.主队ID;
        ELSEIF NEW.客队得分 > NEW.主队得分 THEN
            SET NEW.获胜球队ID = NEW.客队ID;
        ELSE
            SIGNAL SQLSTATE '45000' 
            SET MESSAGE_TEXT = '错误：比赛结束时不能平局';
        END IF;
    END IF;
    
    -- 检查主客队是否相同
    IF NEW.主队ID = NEW.客队ID THEN
        SIGNAL SQLSTATE '45000' 
        SET MESSAGE_TEXT = '错误：主队和客队不能是同一支球队';
    END IF;
END//
DELIMITER ;

-- 3. 帖子点赞自动计数 (增加)
DROP TRIGGER IF EXISTS trg_post_like_increment;
DELIMITER //
CREATE TRIGGER trg_post_like_increment
AFTER INSERT ON Post_Like
FOR EACH ROW
BEGIN
    UPDATE Post SET 点赞数 = 点赞数 + 1 WHERE post_id = NEW.post_id;
END//
DELIMITER ;

-- 4. 帖子点赞自动计数 (减少)
DROP TRIGGER IF EXISTS trg_post_like_decrement;
DELIMITER //
CREATE TRIGGER trg_post_like_decrement
AFTER DELETE ON Post_Like
FOR EACH ROW
BEGIN
    UPDATE Post SET 点赞数 = GREATEST(点赞数 - 1, 0) WHERE post_id = OLD.post_id;
END//
DELIMITER ;

-- 5. 用户注销清理关联数据
DROP TRIGGER IF EXISTS trg_user_delete_cleanup;
DELIMITER //
CREATE TRIGGER trg_user_delete_cleanup
BEFORE DELETE ON User
FOR EACH ROW
BEGIN
    -- 删除用户相关的帖子
    DELETE FROM Post WHERE user_id = OLD.user_id;
    -- 删除用户相关的评论
    DELETE FROM Comment WHERE user_id = OLD.user_id;
    -- 删除用户相关的评分
    DELETE FROM Rating WHERE user_id = OLD.user_id;
    -- 删除用户相关的竞猜
    DELETE FROM Prediction WHERE user_id = OLD.user_id;
    -- 删除用户头像关联
    DELETE FROM User_Avatar WHERE user_id = OLD.user_id;
    -- 删除用户卡片
    DELETE FROM User_Card WHERE user_id = OLD.user_id;
    
    -- 注意：Post_Like 和 Comment_Like 表已设置 ON DELETE CASCADE，会自动删除
END//
DELIMITER ;

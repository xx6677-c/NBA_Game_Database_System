-- 添加浏览量和点赞功能数据库结构修改
USE h_db23373502;

-- 1. 为Post表添加浏览量和点赞数字段（检查是否已存在）
SET @sql = (SELECT IF(
    (SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS 
     WHERE TABLE_SCHEMA = 'h_db23373502' 
     AND TABLE_NAME = 'Post' 
     AND COLUMN_NAME = '浏览量') > 0,
    'SELECT 1',
    CONCAT('ALTER TABLE Post ADD COLUMN 浏览量 INT DEFAULT 0')
));
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

SET @sql = (SELECT IF(
    (SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS 
     WHERE TABLE_SCHEMA = 'h_db23373502' 
     AND TABLE_NAME = 'Post' 
     AND COLUMN_NAME = '点赞数') > 0,
    'SELECT 1',
    CONCAT('ALTER TABLE Post ADD COLUMN 点赞数 INT DEFAULT 0')
));
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- 2. 为Comment表添加点赞数字段（检查是否已存在）
SET @sql = (SELECT IF(
    (SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS 
     WHERE TABLE_SCHEMA = 'h_db23373502' 
     AND TABLE_NAME = 'Comment' 
     AND COLUMN_NAME = '点赞数') > 0,
    'SELECT 1',
    CONCAT('ALTER TABLE Comment ADD COLUMN 点赞数 INT DEFAULT 0')
));
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- 3. 创建帖子点赞表
CREATE TABLE IF NOT EXISTS Post_Like (
    like_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    post_id INT NOT NULL,
    创建时间 DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY unique_user_post (user_id, post_id),
    FOREIGN KEY (user_id) REFERENCES User(user_id) ON DELETE CASCADE,
    FOREIGN KEY (post_id) REFERENCES Post(post_id) ON DELETE CASCADE
);

-- 4. 创建评论点赞表
CREATE TABLE IF NOT EXISTS Comment_Like (
    like_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    comment_id INT NOT NULL,
    创建时间 DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY unique_user_comment (user_id, comment_id),
    FOREIGN KEY (user_id) REFERENCES User(user_id) ON DELETE CASCADE,
    FOREIGN KEY (comment_id) REFERENCES Comment(comment_id) ON DELETE CASCADE
);

-- 5. 创建索引优化查询性能（检查是否已存在）
SET @sql = (SELECT IF(
    (SELECT COUNT(*) FROM INFORMATION_SCHEMA.STATISTICS 
     WHERE TABLE_SCHEMA = 'h_db23373502' 
     AND TABLE_NAME = 'Post_Like' 
     AND INDEX_NAME = 'idx_post_like_user') > 0,
    'SELECT 1',
    'CREATE INDEX idx_post_like_user ON Post_Like(user_id)'
));
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

SET @sql = (SELECT IF(
    (SELECT COUNT(*) FROM INFORMATION_SCHEMA.STATISTICS 
     WHERE TABLE_SCHEMA = 'h_db23373502' 
     AND TABLE_NAME = 'Post_Like' 
     AND INDEX_NAME = 'idx_post_like_post') > 0,
    'SELECT 1',
    'CREATE INDEX idx_post_like_post ON Post_Like(post_id)'
));
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

SET @sql = (SELECT IF(
    (SELECT COUNT(*) FROM INFORMATION_SCHEMA.STATISTICS 
     WHERE TABLE_SCHEMA = 'h_db23373502' 
     AND TABLE_NAME = 'Comment_Like' 
     AND INDEX_NAME = 'idx_comment_like_user') > 0,
    'SELECT 1',
    'CREATE INDEX idx_comment_like_user ON Comment_Like(user_id)'
));
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

SET @sql = (SELECT IF(
    (SELECT COUNT(*) FROM INFORMATION_SCHEMA.STATISTICS 
     WHERE TABLE_SCHEMA = 'h_db23373502' 
     AND TABLE_NAME = 'Comment_Like' 
     AND INDEX_NAME = 'idx_comment_like_comment') > 0,
    'SELECT 1',
    'CREATE INDEX idx_comment_like_comment ON Comment_Like(comment_id)'
));
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- 6. 更新现有帖子的浏览量（示例数据）
UPDATE Post SET 浏览量 = FLOOR(RAND() * 1000) + 50 WHERE 浏览量 = 0;

-- 7. 更新现有帖子的点赞数（示例数据）
UPDATE Post SET 点赞数 = (
    SELECT COUNT(*) FROM Post_Like WHERE Post_Like.post_id = Post.post_id
) WHERE 点赞数 = 0;

-- 8. 更新现有评论的点赞数（示例数据）
UPDATE Comment SET 点赞数 = (
    SELECT COUNT(*) FROM Comment_Like WHERE Comment_Like.comment_id = Comment.comment_id
) WHERE 点赞数 = 0;

-- 输出修改结果
SELECT '数据库结构修改完成' as '结果', NOW() as '修改时间'
UNION ALL
SELECT 'Post表字段添加完成', COUNT(*) FROM Post WHERE 浏览量 IS NOT NULL AND 点赞数 IS NOT NULL
UNION ALL  
SELECT 'Post_Like表创建完成', COUNT(*) FROM Post_Like
UNION ALL
SELECT 'Comment_Like表创建完成', COUNT(*) FROM Comment_Like
UNION ALL
SELECT 'Comment表字段添加完成', COUNT(*) FROM Comment WHERE 点赞数 IS NOT NULL;
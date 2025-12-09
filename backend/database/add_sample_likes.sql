-- 添加示例点赞数据
USE h_db23373502;

-- 插入一些帖子点赞记录
INSERT IGNORE INTO Post_Like (user_id, post_id, 创建时间) VALUES
(1, 1, NOW()),
(2, 1, NOW()),
(3, 2, NOW()),
(1, 3, NOW()),
(2, 3, NOW()),
(1, 2, NOW()),
(3, 1, NOW());

-- 插入一些评论点赞记录  
INSERT IGNORE INTO Comment_Like (user_id, comment_id, 创建时间) VALUES
(1, 1, NOW()),
(2, 1, NOW()),
(3, 2, NOW()),
(1, 3, NOW()),
(2, 2, NOW()),
(1, 2, NOW()),
(3, 3, NOW());

-- 更新帖子点赞计数
UPDATE Post SET 点赞数 = (
    SELECT COUNT(*) FROM Post_Like WHERE Post_Like.post_id = Post.post_id
);

-- 更新评论点赞计数
UPDATE Comment SET 点赞数 = (
    SELECT COUNT(*) FROM Comment_Like WHERE Comment_Like.comment_id = Comment.comment_id
);

-- 输出结果
SELECT '点赞示例数据添加完成' as '结果', NOW() as '时间'
UNION ALL
SELECT '帖子点赞记录数', COUNT(*) FROM Post_Like
UNION ALL
SELECT '评论点赞记录数', COUNT(*) FROM Comment_Like;
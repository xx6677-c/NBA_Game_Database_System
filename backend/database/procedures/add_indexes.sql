
-- ==========================================
-- 7. 性能优化索引 (新增)
-- ==========================================

-- 用户表：优化按角色筛选
CREATE INDEX idx_user_role ON User(角色);

-- 球员表：优化按姓名搜索和位置筛选
CREATE INDEX idx_player_name ON Player(姓名);
CREATE INDEX idx_player_position ON Player(位置);

-- 比赛表：优化按赛季、状态及球队查询
CREATE INDEX idx_game_season ON Game(赛季);
CREATE INDEX idx_game_status ON Game(状态);
CREATE INDEX idx_game_home_team ON Game(主队ID);
CREATE INDEX idx_game_away_team ON Game(客队ID);

-- 帖子表：优化按用户查询及按热度/时间排序
CREATE INDEX idx_post_user ON Post(user_id);
CREATE INDEX idx_post_created ON Post(创建时间);
CREATE INDEX idx_post_likes ON Post(点赞数);

-- 评论表：优化按用户查询及时间排序
CREATE INDEX idx_comment_user ON Comment(user_id);
CREATE INDEX idx_comment_created ON Comment(创建时间);

-- 球员比赛数据表：优化排行榜查询 (得分、篮板、助攻)
CREATE INDEX idx_pg_points ON Player_Game(得分);
CREATE INDEX idx_pg_rebounds ON Player_Game(篮板);
CREATE INDEX idx_pg_assists ON Player_Game(助攻);
CREATE INDEX idx_pg_game_id ON Player_Game(game_id);

-- 竞猜表：优化按用户和比赛查询
CREATE INDEX idx_prediction_user ON Prediction(user_id);
CREATE INDEX idx_prediction_game ON Prediction(game_id);

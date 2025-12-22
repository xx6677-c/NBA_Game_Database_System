# 后端存储过程重构报告

## 1. 概述
本项目已完成后端逻辑的全面重构，将原本散落在 Python 代码中的 SQL 语句迁移至 MySQL 存储过程。此举旨在提高系统的安全性、性能和可维护性。

## 2. 修改的文件列表

### 后端路由 (Python)
以下文件中的 SQL 操作已替换为 `cursor.callproc` 调用：
- `backend/routes/auth.py`: 用户注册、登录、个人信息获取。
- `backend/routes/games.py`: 比赛的增删改查、球员数据统计。
- `backend/routes/posts.py`: 帖子列表、发布、点赞、删除（级联）。
- `backend/routes/comments.py`: 评论点赞功能。
- `backend/routes/rankings.py`: 球队排名、球员数据榜单（动态排序）。
- `backend/routes/players.py`: 球员的增删改查、生涯数据雷达图。
- `backend/routes/teams.py`: 球队的增删改查。
- `backend/routes/images.py`: 图片上传、头像更新、图片获取。
- `backend/routes/shop.py`: 积分抽卡、我的卡片获取。

### 数据库脚本 (SQL)
所有存储过程已合并至主文件：
- `backend/database/all_procedures.sql`

## 3. 新增/更新的存储过程清单

### 用户与认证 (Auth)
- `sp_register_user`: 注册新用户。
- `sp_login_user`: 用户登录验证。
- `sp_update_last_login`: 更新最后登录时间。
- `sp_get_user_profile`: 获取用户详细信息（含头像）。

### 比赛管理 (Games)
- `sp_create_game`: 创建新比赛记录。
- `sp_update_game`: 更新比赛信息。
- `sp_delete_game`: 删除比赛。
- `sp_get_game_player_stats`: 获取某场比赛的球员数据。
- `sp_update_game_player_stats`: 更新球员单场数据。

### 社区互动 (Posts & Comments)
- `sp_get_posts`: 获取帖子列表（含用户信息、点赞数、评论数）。
- `sp_create_post`: 发布新帖子。
- `sp_toggle_post_like`: 切换帖子点赞状态。
- `sp_delete_post`: 删除帖子（自动级联删除关联的图片、评论、点赞）。
- `sp_add_comment_like`: 评论点赞。
- `sp_remove_comment_like`: 取消评论点赞。

### 数据排行 (Rankings)
- `sp_get_team_standings`: 获取球队排名（计算胜负场、胜率）。
- `sp_get_player_rankings`: 获取球员数据榜单（支持按得分、篮板、助攻等动态排序）。

### 基础数据管理 (Players & Teams)
- `sp_get_players`: 获取球员列表（支持搜索、筛选）。
- `sp_create_player`: 创建球员。
- `sp_update_player`: 更新球员信息。
- `sp_delete_player`: 删除球员（级联删除关联数据）。
- `sp_get_player_career_stats`: 获取球员生涯平均数据（用于雷达图）。
- `sp_get_all_teams`: 获取所有球队。
- `sp_create_team`: 创建球队。
- `sp_update_team`: 更新球队。
- `sp_delete_team`: 删除球队。

### 图片与商店 (Images & Shop)
- `sp_upload_image`: 上传图片元数据。
- `sp_update_user_avatar`: 更新用户头像。
- `sp_get_image`: 获取图片二进制数据。
- `sp_draw_card`: 积分抽卡（包含扣分、随机逻辑的事务处理）。
- `sp_get_my_cards`: 获取用户拥有的球星卡。

## 4. 数据库变更
- 执行了 `all_procedures.sql`，在数据库中创建了上述所有存储过程。
- 确保了所有涉及外键约束和级联删除的逻辑都在存储过程或表定义中得到处理。

## 5. 测试验证
已编写并执行全面测试脚本 `test_procedures.py`，覆盖了以下场景：
- **用户管理**: 注册、登录、更新资料 (Pass)
- **球队管理**: 创建、更新、读取 (Pass)
- **球员管理**: 创建、更新、读取 (Pass)
- **比赛管理**: 创建比赛、添加球员数据 (Pass)
- **社区功能**: 发帖、点赞、读取帖子 (Pass)
- **图片功能**: 上传图片、设置头像 (Pass)
- **清理机制**: 测试完成后自动清理了所有测试数据 (Pass)

测试结果表明所有核心存储过程均能正常工作，且与 Python 后端代码的交互逻辑正确。

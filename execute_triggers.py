#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))
from database import config as db_config

def execute_trigger_script():
    """执行包含触发器的SQL脚本"""
    db = db_config.DatabaseConfig()
    conn = db.get_connection()
    if not conn:
        print('数据库连接失败')
        return
    
    try:
        with conn.cursor() as cursor:
            # 先执行 DROP TRIGGER
            cursor.execute("DROP TRIGGER IF EXISTS trg_game_update_winner")
            cursor.execute("DROP TRIGGER IF EXISTS trg_game_insert_winner")
            cursor.execute("DROP TRIGGER IF EXISTS trg_post_like_increment")
            cursor.execute("DROP TRIGGER IF EXISTS trg_post_like_decrement")
            cursor.execute("DROP TRIGGER IF EXISTS trg_game_check_teams")
            cursor.execute("DROP TRIGGER IF EXISTS trg_user_delete_cleanup")
            
            # 共享的比赛获胜判定逻辑
            game_winner_logic = """
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
            """

            # 定义触发器 SQL
            trg1 = f"""
            CREATE TRIGGER trg_game_update_winner
            BEFORE UPDATE ON Game
            FOR EACH ROW
            BEGIN
                {game_winner_logic}
            END
            """

            trg1_insert = f"""
            CREATE TRIGGER trg_game_insert_winner
            BEFORE INSERT ON Game
            FOR EACH ROW
            BEGIN
                {game_winner_logic}
                
                -- 合并检查主客队是否相同
                IF NEW.主队ID = NEW.客队ID THEN
                    SIGNAL SQLSTATE '45000' 
                    SET MESSAGE_TEXT = '错误：主队和客队不能是同一支球队';
                END IF;
            END
            """
            
            trg2 = """
            CREATE TRIGGER trg_post_like_increment
            AFTER INSERT ON Post_Like
            FOR EACH ROW
            BEGIN
                UPDATE Post SET 点赞数 = 点赞数 + 1 WHERE post_id = NEW.post_id;
            END
            """
            
            trg3 = """
            CREATE TRIGGER trg_post_like_decrement
            AFTER DELETE ON Post_Like
            FOR EACH ROW
            BEGIN
                UPDATE Post SET 点赞数 = GREATEST(点赞数 - 1, 0) WHERE post_id = OLD.post_id;
            END
            """

            trg5 = """
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
            END
            """
            
            print("Creating trg_game_update_winner...")
            cursor.execute(trg1)

            print("Creating trg_game_insert_winner...")
            cursor.execute(trg1_insert)
            
            print("Creating trg_post_like_increment...")
            cursor.execute(trg2)
            
            print("Creating trg_post_like_decrement...")
            cursor.execute(trg3)

            print("Creating trg_user_delete_cleanup...")
            cursor.execute(trg5)
            
            conn.commit()
            print('触发器创建成功！')
            
    except Exception as e:
        print(f'执行SQL脚本时出错: {e}')
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    execute_trigger_script()

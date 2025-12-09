"""帖子管理路由"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

from database.config import DatabaseConfig


posts_bp = Blueprint('posts', __name__)
db_config = DatabaseConfig()


@posts_bp.route('', methods=['GET'])
def get_posts():
    """获取帖子列表"""
    game_id = request.args.get('game_id')
    
    conn = db_config.get_connection()
    if not conn:
        return jsonify({'error': '数据库连接失败'}), 500
    
    try:
        with conn.cursor() as cursor:
            if game_id:
                cursor.execute("""
                    SELECT p.post_id, p.标题, p.内容, p.创建时间, p.浏览量, p.点赞数,
                           u.用户名, g.赛季, ht.名称 as home_team, at.名称 as away_team
                    FROM Post p
                    JOIN User u ON p.user_id = u.user_id
                    LEFT JOIN Game g ON p.game_id = g.game_id
                    LEFT JOIN Team ht ON g.主队ID = ht.team_id
                    LEFT JOIN Team at ON g.客队ID = at.team_id
                    WHERE p.game_id = %s
                    ORDER BY p.创建时间 DESC
                """, (game_id,))
            else:
                cursor.execute("""
                    SELECT p.post_id, p.标题, p.内容, p.创建时间, p.浏览量, p.点赞数,
                           u.用户名, g.赛季, ht.名称 as home_team, at.名称 as away_team
                    FROM Post p
                    JOIN User u ON p.user_id = u.user_id
                    LEFT JOIN Game g ON p.game_id = g.game_id
                    LEFT JOIN Team ht ON g.主队ID = ht.team_id
                    LEFT JOIN Team at ON g.客队ID = at.team_id
                    ORDER BY p.创建时间 DESC
                """)
            
            posts = []
            for row in cursor.fetchall():
                posts.append({
                    'post_id': row[0],
                    'title': row[1],
                    'content': row[2],
                    'create_time': row[3].strftime('%Y-%m-%d %H:%M'),
                    'view_count': row[4],
                    'like_count': row[5],
                    'username': row[6],
                    'season': row[7],
                    'home_team': row[8],
                    'away_team': row[9]
                })
            
            return jsonify(posts), 200
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()


@posts_bp.route('', methods=['POST'])
@jwt_required()
def create_post():
    """创建帖子"""
    data = request.get_json()
    current_user_id = get_jwt_identity()
    
    title = data.get('title')
    content = data.get('content')
    game_id = data.get('game_id')
    
    if not title or not content:
        return jsonify({'error': '标题和内容不能为空'}), 400
    
    if not game_id or game_id == '' or game_id == 0:
        game_id = None
    
    conn = db_config.get_connection()
    if not conn:
        return jsonify({'error': '数据库连接失败'}), 500
    
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO Post (user_id, 标题, 内容, game_id, 创建时间)
                VALUES (%s, %s, %s, %s, %s)
            """, (current_user_id, title, content, game_id, datetime.now()))
            
            conn.commit()
            return jsonify({'message': '帖子创建成功'}), 201
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()


@posts_bp.route('/<int:post_id>/view', methods=['POST'])
def increment_post_view(post_id):
    """增加帖子浏览量"""
    conn = db_config.get_connection()
    if not conn:
        return jsonify({'error': '数据库连接失败'}), 500
    
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                UPDATE Post 
                SET 浏览量 = 浏览量 + 1 
                WHERE post_id = %s
            """, (post_id,))
            
            conn.commit()
            return jsonify({'message': '浏览量增加成功'})
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()


@posts_bp.route('/<int:post_id>/like', methods=['POST', 'DELETE'])
@jwt_required()
def toggle_post_like(post_id):
    """点赞/取消点赞帖子"""
    current_user_id = get_jwt_identity()
    
    conn = db_config.get_connection()
    if not conn:
        return jsonify({'error': '数据库连接失败'}), 500
    
    try:
        with conn.cursor() as cursor:
            if request.method == 'POST':
                cursor.execute("""
                    SELECT COUNT(*) FROM Post_Like 
                    WHERE user_id = %s AND post_id = %s
                """, (current_user_id, post_id))
                
                if cursor.fetchone()[0] == 0:
                    cursor.execute("""
                        INSERT INTO Post_Like (user_id, post_id) 
                        VALUES (%s, %s)
                    """, (current_user_id, post_id))
                    
                    cursor.execute("""
                        UPDATE Post 
                        SET 点赞数 = 点赞数 + 1 
                        WHERE post_id = %s
                    """, (post_id,))
                    
                    conn.commit()
                    return jsonify({'message': '点赞成功', 'liked': True})
                else:
                    return jsonify({'message': '已经点赞过了', 'liked': True})
            
            else:  # DELETE
                cursor.execute("""
                    SELECT COUNT(*) FROM Post_Like 
                    WHERE user_id = %s AND post_id = %s
                """, (current_user_id, post_id))
                
                if cursor.fetchone()[0] > 0:
                    cursor.execute("""
                        DELETE FROM Post_Like 
                        WHERE user_id = %s AND post_id = %s
                    """, (current_user_id, post_id))
                    
                    cursor.execute("""
                        UPDATE Post 
                        SET 点赞数 = 点赞数 - 1 
                        WHERE post_id = %s
                    """, (post_id,))
                    
                    conn.commit()
                    return jsonify({'message': '取消点赞成功', 'liked': False})
                else:
                    return jsonify({'message': '还未点赞', 'liked': False})
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()


@posts_bp.route('/<int:post_id>/like-status', methods=['GET'])
@jwt_required()
def get_post_like_status(post_id):
    """获取帖子点赞状态"""
    current_user_id = get_jwt_identity()
    
    conn = db_config.get_connection()
    if not conn:
        return jsonify({'error': '数据库连接失败'}), 500
    
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT COUNT(*) FROM Post_Like 
                WHERE user_id = %s AND post_id = %s
            """, (current_user_id, post_id))
            
            liked = cursor.fetchone()[0] > 0
            return jsonify({'liked': liked})
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

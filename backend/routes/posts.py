"""帖子管理路由"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

from database.core.config import DatabaseConfig


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
            cursor.callproc('sp_get_posts', (game_id,))
            
            posts = []
            for row in cursor.fetchall():
                image_ids_str = row[10]
                images = []
                if image_ids_str:
                    # GROUP_CONCAT returns string, need to convert to list of urls
                    # Handle potential byte string if returned as such (though usually string in pymysql)
                    if isinstance(image_ids_str, bytes):
                        image_ids_str = image_ids_str.decode('utf-8')
                    images = [f'/api/images/{img_id}' for img_id in image_ids_str.split(',')]

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
                    'away_team': row[9],
                    'images': images,
                    'image_url': images[0] if images else None,
                    'user_id': row[11]
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
    image_ids = data.get('image_ids', [])
    
    # 兼容旧的 image_id 参数
    if 'image_id' in data and data['image_id']:
        if data['image_id'] not in image_ids:
            image_ids.append(data['image_id'])
    
    if not title or not content:
        return jsonify({'error': '标题和内容不能为空'}), 400
    
    if not game_id or game_id == '' or game_id == 0:
        game_id = None
    
    conn = db_config.get_connection()
    if not conn:
        return jsonify({'error': '数据库连接失败'}), 500
    
    try:
        with conn.cursor() as cursor:
            # sp_create_post 有6个参数，最后一个是OUT参数 p_post_id
            # 使用 execute 代替 callproc 以确保正确获取 OUT 参数
            cursor.execute("SET @p_post_id = 0")
            cursor.execute("""
                CALL sp_create_post(%s, %s, %s, %s, %s, @p_post_id)
            """, (current_user_id, title, content, game_id, datetime.now()))
            
            cursor.execute("SELECT @p_post_id")
            result = cursor.fetchone()
            post_id = result[0]
            
            if image_ids:
                for img_id in image_ids:
                    cursor.callproc('sp_add_post_image', (post_id, img_id))
            
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
            cursor.callproc('sp_increment_post_view', (post_id,))
            
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
                cursor.callproc('sp_check_post_like', (current_user_id, post_id))
                
                if cursor.fetchone()[0] == 0:
                    cursor.callproc('sp_add_post_like', (current_user_id, post_id))
                    
                    # 点赞数由触发器 trg_post_like_increment 自动更新
                    
                    conn.commit()
                    return jsonify({'message': '点赞成功', 'liked': True})
                else:
                    return jsonify({'message': '已经点赞过了', 'liked': True})
            
            else:  # DELETE
                cursor.callproc('sp_check_post_like', (current_user_id, post_id))
                
                if cursor.fetchone()[0] > 0:
                    cursor.callproc('sp_remove_post_like', (current_user_id, post_id))
                    
                    # 点赞数由触发器 trg_post_like_decrement 自动更新
                    
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
            cursor.callproc('sp_check_post_like', (current_user_id, post_id))
            
            liked = cursor.fetchone()[0] > 0
            return jsonify({'liked': liked})
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()


@posts_bp.route('/<int:post_id>/comments', methods=['GET'])
def get_post_comments(post_id):
    """获取帖子评论"""
    conn = db_config.get_connection()
    if not conn:
        return jsonify({'error': '数据库连接失败'}), 500
    
    try:
        with conn.cursor() as cursor:
            cursor.callproc('sp_get_post_comments', (post_id,))
            
            comments = []
            for row in cursor.fetchall():
                comments.append({
                    'comment_id': row[0],
                    'content': row[1],
                    'create_time': row[2].strftime('%Y-%m-%d %H:%M'),
                    'username': row[3],
                    'user_id': row[4],
                    'like_count': 0  # 暂不支持评论点赞显示，避免前端报错
                })
            
            return jsonify(comments), 200
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()


@posts_bp.route('/<int:post_id>/comments', methods=['POST'])
@jwt_required()
def create_post_comment(post_id):
    """创建帖子评论"""
    current_user_id = get_jwt_identity()
    data = request.get_json()
    content = data.get('content')
    
    if not content:
        return jsonify({'error': '评论内容不能为空'}), 400
        
    conn = db_config.get_connection()
    if not conn:
        return jsonify({'error': '数据库连接失败'}), 500
    
    try:
        with conn.cursor() as cursor:
            cursor.callproc('sp_create_post_comment', (current_user_id, post_id, content, datetime.now()))
            
            conn.commit()
            return jsonify({'message': '评论发表成功'}), 201
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()


@posts_bp.route('/<int:post_id>', methods=['DELETE'])
@jwt_required()
def delete_post(post_id):
    """删除帖子"""
    current_user_id = get_jwt_identity()
    
    conn = db_config.get_connection()
    if not conn:
        return jsonify({'error': '数据库连接失败'}), 500
    
    try:
        with conn.cursor() as cursor:
            # 检查帖子是否存在以及用户权限
            cursor.execute("""
                SELECT p.user_id, u.角色 
                FROM Post p
                JOIN User u ON u.user_id = %s
                WHERE p.post_id = %s
            """, (current_user_id, post_id))
            
            result = cursor.fetchone()
            if not result:
                # 可能是帖子不存在，或者只是为了获取当前用户角色
                cursor.execute("SELECT 角色 FROM User WHERE user_id = %s", (current_user_id,))
                user_role = cursor.fetchone()
                
                cursor.execute("SELECT user_id FROM Post WHERE post_id = %s", (post_id,))
                post = cursor.fetchone()
                
                if not post:
                    return jsonify({'error': '帖子不存在'}), 404
                
                if user_role and user_role[0] == 'admin':
                    # 管理员可以删除任何帖子
                    pass
                else:
                    return jsonify({'error': '无权删除此帖子'}), 403
            else:
                # 帖子存在，且result包含当前用户是否是作者的信息（如果当前用户是作者，result[0]应该等于post.user_id，但这里逻辑有点绕）
                # 让我们简化逻辑：
                pass

            # 重新清晰的权限检查逻辑
            # 1. 获取帖子作者ID
            cursor.execute("SELECT user_id FROM Post WHERE post_id = %s", (post_id,))
            post = cursor.fetchone()
            if not post:
                return jsonify({'error': '帖子不存在'}), 404
            post_author_id = post[0]
            
            # 2. 获取当前用户角色
            cursor.execute("SELECT 角色 FROM User WHERE user_id = %s", (current_user_id,))
            user_role = cursor.fetchone()[0]
            
            # 3. 验证权限：作者本人 或 管理员
            if str(post_author_id) != str(current_user_id) and user_role != 'admin':
                return jsonify({'error': '无权删除此帖子'}), 403
            
            # 4. 执行删除
            cursor.callproc('sp_delete_post', (post_id,))
            
            conn.commit()
            return jsonify({'message': '帖子删除成功'}), 200
            
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

"""认证相关路由"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity, get_jwt
from datetime import datetime

from database.core.config import DatabaseConfig
from utils.auth import hash_password, check_password
from middlewares.jwt_config import jwt_blacklist


auth_bp = Blueprint('auth', __name__)
db_config = DatabaseConfig()


@auth_bp.route('/register', methods=['POST'])
def register():
    """用户注册"""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    role = data.get('role', 'user')
    secret_key = data.get('secret_key', '')
    
    if not username or not password:
        return jsonify({'error': '用户名和密码不能为空'}), 400
    
    # 验证管理员和数据分析师角色的密钥
    if role == 'admin':
        if not secret_key:
            return jsonify({'error': '管理员注册需要提供管理员密钥'}), 400
        if secret_key != 'NBA_ADMIN_2025':
            return jsonify({'error': '管理员密钥错误'}), 400
    elif role == 'analyst':
        if not secret_key:
            return jsonify({'error': '数据分析师注册需要提供分析师密钥'}), 400
        if secret_key != 'NBA_ANALYST_2025':
            return jsonify({'error': '数据分析师密钥错误'}), 400
    
    conn = db_config.get_connection()
    if not conn:
        return jsonify({'error': '数据库连接失败'}), 500
    
    try:
        with conn.cursor() as cursor:
            # 检查用户名是否已存在
            cursor.execute("SELECT user_id FROM User WHERE 用户名 = %s", (username,))
            if cursor.fetchone():
                return jsonify({'error': '用户名已存在'}), 400
            
            # 创建新用户
            hashed_password = hash_password(password)
            cursor.callproc('sp_register_user', (username, hashed_password, role, datetime.now()))
            
            conn.commit()
            return jsonify({'message': '注册成功'}), 201
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()


@auth_bp.route('/login', methods=['POST'])
def login():
    """用户登录"""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'error': '用户名和密码不能为空'}), 400
    
    conn = db_config.get_connection()
    if not conn:
        return jsonify({'error': '数据库连接失败'}), 500
    
    try:
        with conn.cursor() as cursor:
            cursor.callproc('sp_login_user', (username,))
            
            user = cursor.fetchone()
            # user: (user_id, password_hash, role)
            if not user or not check_password(password, user[1]):
                return jsonify({'error': '用户名或密码错误'}), 401
            
            # 创建JWT token
            access_token = create_access_token(identity=str(user[0]))
            
            # 更新最后登录时间
            cursor.callproc('sp_update_last_login', (user[0], datetime.now()))
            conn.commit()
            
            return jsonify({
                'access_token': access_token,
                'user_id': user[0],
                'username': username,
                'role': user[2]
            }), 200
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()


@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """用户登出"""
    jti = get_jwt()['jti']
    jwt_blacklist.add(jti)
    return jsonify({'message': '登出成功'}), 200


@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """获取当前用户信息"""
    current_user_id = get_jwt_identity()
    
    conn = db_config.get_connection()
    if not conn:
        return jsonify({'error': '数据库连接失败'}), 500
    
    try:
        with conn.cursor() as cursor:
            cursor.callproc('sp_get_user_profile', (current_user_id,))
            
            user_data = cursor.fetchone()
            
            if user_data:
                return jsonify({
                    'user_id': user_data[0],
                    'username': user_data[1],
                    'role': user_data[2],
                    'register_time': user_data[3].strftime('%Y-%m-%d %H:%M') if user_data[3] else None,
                    'last_login': user_data[4].strftime('%Y-%m-%d %H:%M') if user_data[4] else None,
                    'email': user_data[5],
                    'phone': user_data[6],
                    'points': user_data[7] or 0,
                    'avatar_url': f'/api/images/{user_data[8]}' if user_data[8] else None
                }), 200
            else:
                return jsonify({'error': '用户不存在'}), 404
                
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()


@auth_bp.route('/me', methods=['PUT'])
@jwt_required()
def update_user_profile():
    """更新用户信息"""
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    email = data.get('email')
    phone = data.get('phone')
    
    conn = db_config.get_connection()
    if not conn:
        return jsonify({'error': '数据库连接失败'}), 500
    
    try:
        with conn.cursor() as cursor:
            cursor.callproc('sp_update_user_profile', (current_user_id, email, phone))
            
            conn.commit()
            return jsonify({'message': '个人信息更新成功'}), 200
                
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()


@auth_bp.route('/me/posts', methods=['GET'])
@jwt_required()
def get_user_posts():
    """获取当前用户的帖子"""
    current_user_id = get_jwt_identity()
    
    conn = db_config.get_connection()
    if not conn:
        return jsonify({'error': '数据库连接失败'}), 500
    
    try:
        with conn.cursor() as cursor:
            cursor.callproc('sp_get_user_posts', (current_user_id,))
            
            posts = []
            for row in cursor.fetchall():
                posts.append({
                    'post_id': row[0],
                    'title': row[1],
                    'content': row[2],
                    'create_time': row[3].strftime('%Y-%m-%d %H:%M'),
                    'views': row[4],
                    'likes': row[5],
                    'season': row[6],
                    'home_team': row[7],
                    'away_team': row[8]
                })
            
            return jsonify(posts), 200
                
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()


@auth_bp.route('/me/ratings', methods=['GET'])
@jwt_required()
def get_user_ratings():
    """获取当前用户的评分"""
    current_user_id = get_jwt_identity()
    
    conn = db_config.get_connection()
    if not conn:
        return jsonify({'error': '数据库连接失败'}), 500
    
    try:
        with conn.cursor() as cursor:
            cursor.callproc('sp_get_user_ratings', (current_user_id,))
            
            ratings = []
            for row in cursor.fetchall():
                ratings.append({
                    'user_id': row[0],
                    'player_id': row[1],
                    'game_id': row[2],
                    'rating': float(row[3]),
                    'create_time': row[4].strftime('%Y-%m-%d %H:%M'),
                    'player_name': row[5],
                    'position': row[6],
                    'team_name': row[7],
                    'season': row[8],
                    'game_date': row[9].strftime('%Y-%m-%d %H:%M'),
                    'home_team': row[10],
                    'away_team': row[11]
                })
            
            return jsonify(ratings), 200
                
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()


@auth_bp.route('/verify-password', methods=['POST'])
@jwt_required()
def verify_password():
    """验证密码"""
    current_user_id = get_jwt_identity()
    data = request.get_json()
    password = data.get('password')
    
    if not password:
        return jsonify({'error': '密码不能为空'}), 400
    
    conn = db_config.get_connection()
    if not conn:
        return jsonify({'error': '数据库连接失败'}), 500
    
    try:
        with conn.cursor() as cursor:
            cursor.callproc('sp_get_user_password_hash', (current_user_id,))
            user_data = cursor.fetchone()
            
            if not user_data:
                return jsonify({'error': '用户不存在'}), 404
            
            if check_password(password, user_data[0]):
                return jsonify({'success': True, 'message': '密码验证成功'}), 200
            else:
                return jsonify({'success': False, 'message': '密码错误'}), 401
                
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()


@auth_bp.route('/delete-account', methods=['DELETE'])
@jwt_required()
def delete_account():
    """注销账户"""
    current_user_id = get_jwt_identity()
    data = request.get_json()
    password = data.get('password')
    
    if not password:
        return jsonify({'error': '密码不能为空'}), 400
    
    conn = db_config.get_connection()
    if not conn:
        return jsonify({'error': '数据库连接失败'}), 500
    
    try:
        with conn.cursor() as cursor:
            # 验证密码
            cursor.callproc('sp_get_user_password_hash', (current_user_id,))
            user_data = cursor.fetchone()
            
            if not user_data:
                return jsonify({'error': '用户不存在'}), 404
            
            if not check_password(password, user_data[0]):
                return jsonify({'error': '密码错误'}), 401
            
            # 开始事务
            conn.autocommit = False
            
            try:
                # 删除用户相关数据
                cursor.callproc('sp_delete_account', (current_user_id,))
                
                conn.commit()
                
                # 将JWT令牌加入黑名单
                jti = get_jwt()['jti']
                jwt_blacklist.add(jti)
                
                return jsonify({'success': True, 'message': '账户注销成功'}), 200
                
            except Exception as e:
                conn.rollback()
                raise e
                
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()


@auth_bp.route('/me/points-history', methods=['GET'])
@jwt_required()
def get_user_points_history():
    """获取用户积分历史"""
    current_user_id = get_jwt_identity()
    
    conn = db_config.get_connection()
    if not conn:
        return jsonify({'error': '数据库连接失败'}), 500
    
    try:
        with conn.cursor() as cursor:
            # 获取已领取的竞猜奖励记录
            cursor.callproc('sp_get_user_points_history', (current_user_id,))
            
            history = []
            for row in cursor.fetchall():
                history.append({
                    'type': '竞猜奖励',
                    'points': 100,
                    'date': row[0].strftime('%Y-%m-%d %H:%M'),
                    'description': f'竞猜正确：{row[3]} vs {row[4]}',
                    'game_info': {
                        'home_team': row[3],
                        'away_team': row[4],
                        'score': f'{row[5]}-{row[6]}',
                        'game_date': row[7].strftime('%Y-%m-%d')
                    }
                })
            
            return jsonify(history), 200
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

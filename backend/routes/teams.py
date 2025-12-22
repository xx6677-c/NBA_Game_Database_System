"""球队管理路由"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from database.core.config import DatabaseConfig
from utils.permissions import check_admin_permission


teams_bp = Blueprint('teams', __name__)
db_config = DatabaseConfig()


@teams_bp.route('', methods=['GET'])
def get_teams():
    """获取所有球队"""
    conn = db_config.get_connection()
    if not conn:
        return jsonify({'error': '数据库连接失败'}), 500
    
    try:
        with conn.cursor() as cursor:
            cursor.callproc('sp_get_all_teams')
            
            teams = []
            for row in cursor.fetchall():
                teams.append({
                    'team_id': row[0],
                    'name': row[1],
                    'city': row[2],
                    'arena': row[3],
                    'conference': row[4],
                    'founded_year': row[5],
                    'logo_url': f'/api/images/{row[6]}' if row[6] else None
                })
            
            return jsonify(teams), 200
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()


@teams_bp.route('', methods=['POST'])
@jwt_required()
def create_team():
    """创建球队（仅管理员）"""
    current_user_id = get_jwt_identity()
    
    if not check_admin_permission(current_user_id):
        return jsonify({'error': '权限不足，仅管理员可创建球队'}), 403
    
    data = request.get_json()
    name = data.get('name')
    city = data.get('city')
    arena = data.get('arena')
    conference = data.get('conference')
    founded_year = data.get('founded_year')
    
    if not all([name, city, arena, conference, founded_year]):
        return jsonify({'error': '所有字段都必须填写'}), 400
    
    conn = db_config.get_connection()
    if not conn:
        return jsonify({'error': '数据库连接失败'}), 500
    
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT team_id FROM Team WHERE 名称 = %s", (name,))
            if cursor.fetchone():
                return jsonify({'error': '球队名称已存在'}), 400
            
            # sp_create_team 有6个参数，最后一个是OUT参数 p_team_id
            # 使用 execute 代替 callproc 以确保正确获取 OUT 参数
            cursor.execute("SET @p_team_id = 0")
            cursor.execute("""
                CALL sp_create_team(%s, %s, %s, %s, %s, @p_team_id)
            """, (name, city, arena, conference, founded_year))
            
            conn.commit()
            return jsonify({'message': '球队创建成功'}), 201
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()


@teams_bp.route('/<int:team_id>', methods=['PUT'])
@jwt_required()
def update_team(team_id):
    """更新球队（仅管理员）"""
    current_user_id = get_jwt_identity()
    
    if not check_admin_permission(current_user_id):
        return jsonify({'error': '权限不足，仅管理员可更新球队'}), 403
    
    data = request.get_json()
    name = data.get('name')
    city = data.get('city')
    arena = data.get('arena')
    conference = data.get('conference')
    founded_year = data.get('founded_year')
    
    if not all([name, city, arena, conference, founded_year]):
        return jsonify({'error': '所有字段都必须填写'}), 400
    
    conn = db_config.get_connection()
    if not conn:
        return jsonify({'error': '数据库连接失败'}), 500
    
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT team_id FROM Team WHERE team_id = %s", (team_id,))
            if not cursor.fetchone():
                return jsonify({'error': '球队不存在'}), 404
            
            cursor.execute("SELECT team_id FROM Team WHERE 名称 = %s AND team_id != %s", (name, team_id))
            if cursor.fetchone():
                return jsonify({'error': '球队名称已存在'}), 400
            
            cursor.callproc('sp_update_team', (team_id, name, city, arena, conference, founded_year))
            
            conn.commit()
            return jsonify({'message': '球队更新成功'}), 200
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()


@teams_bp.route('/<int:team_id>', methods=['DELETE'])
@jwt_required()
def delete_team(team_id):
    """删除球队（仅管理员）"""
    current_user_id = get_jwt_identity()
    
    if not check_admin_permission(current_user_id):
        return jsonify({'error': '权限不足，仅管理员可删除球队'}), 403
    
    conn = db_config.get_connection()
    if not conn:
        return jsonify({'error': '数据库连接失败'}), 500
    
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT team_id FROM Team WHERE team_id = %s", (team_id,))
            if not cursor.fetchone():
                return jsonify({'error': '球队不存在'}), 404
            
            cursor.callproc('sp_delete_team', (team_id,))
            conn.commit()
            return jsonify({'message': '球队删除成功'}), 200
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@teams_bp.route('/<int:team_id>/logo', methods=['POST'])
@jwt_required()
def upload_team_logo(team_id):
    """上传并设置球队Logo（仅管理员）"""
    current_user_id = get_jwt_identity()
    
    if not check_admin_permission(current_user_id):
        return jsonify({'error': '权限不足，仅管理员可上传球队Logo'}), 403
    
    if 'file' not in request.files:
        return jsonify({'error': '没有文件部分'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': '未选择文件'}), 400
        
    if file and allowed_file(file.filename):
        conn = db_config.get_connection()
        if not conn:
            return jsonify({'error': '数据库连接失败'}), 500
            
        try:
            # 读取文件二进制数据
            file_data = file.read()
            mime_type = file.mimetype
            filename = file.filename
            
            with conn.cursor() as cursor:
                # 1. 检查球队是否存在
                cursor.execute("SELECT team_id FROM Team WHERE team_id = %s", (team_id,))
                if not cursor.fetchone():
                    return jsonify({'error': '球队不存在'}), 404

                # 2. 插入图片到 Image 表
                cursor.execute("""
                    INSERT INTO Image (名称, 数据, MIME类型)
                    VALUES (%s, %s, %s)
                """, (filename, file_data, mime_type))
                
                image_id = cursor.lastrowid
                
                # 3. 更新或插入 Team_Logo 表
                # 先检查是否已有 Logo
                cursor.execute("SELECT image_id FROM Team_Logo WHERE team_id = %s", (team_id,))
                existing_logo = cursor.fetchone()
                
                if existing_logo:
                    # 如果已有 Logo，更新 image_id
                    old_image_id = existing_logo[0]
                    cursor.execute("UPDATE Team_Logo SET image_id = %s WHERE team_id = %s", (image_id, team_id))
                else:
                    # 如果没有，插入新记录
                    cursor.execute("INSERT INTO Team_Logo (team_id, image_id) VALUES (%s, %s)", (team_id, image_id))
                
                conn.commit()
                
                return jsonify({
                    'message': '球队Logo上传成功',
                    'image_id': image_id,
                    'logo_url': f'/api/images/{image_id}'
                }), 201
                
        except Exception as e:
            conn.rollback()
            return jsonify({'error': str(e)}), 500
        finally:
            conn.close()
    
    return jsonify({'error': '不支持的文件类型'}), 400

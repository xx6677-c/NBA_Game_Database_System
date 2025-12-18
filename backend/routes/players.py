"""球员管理路由"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from database.config import DatabaseConfig
from utils.permissions import check_admin_permission


players_bp = Blueprint('players', __name__)
db_config = DatabaseConfig()


@players_bp.route('', methods=['GET'])
def get_players():
    """获取球员列表"""
    team_id = request.args.get('team_id')
    
    conn = db_config.get_connection()
    if not conn:
        return jsonify({'error': '数据库连接失败'}), 500
    
    try:
        with conn.cursor() as cursor:
            if team_id:
                cursor.execute("""
                    SELECT p.player_id, p.姓名, p.位置, p.球衣号, p.身高, p.体重, 
                           p.出生日期, p.国籍, p.当前球队ID, t.名称 as team_name,
                           p.合同到期, p.薪资, pi.image_id
                    FROM Player p 
                    LEFT JOIN Team t ON p.当前球队ID = t.team_id
                    LEFT JOIN Player_Image pi ON p.player_id = pi.player_id
                    WHERE p.当前球队ID = %s
                    ORDER BY p.球衣号
                """, (team_id,))
            else:
                cursor.execute("""
                    SELECT p.player_id, p.姓名, p.位置, p.球衣号, p.身高, p.体重, 
                           p.出生日期, p.国籍, p.当前球队ID, t.名称 as team_name,
                           p.合同到期, p.薪资, pi.image_id
                    FROM Player p 
                    LEFT JOIN Team t ON p.当前球队ID = t.team_id
                    LEFT JOIN Player_Image pi ON p.player_id = pi.player_id
                    ORDER BY t.名称, p.球衣号
                """)
            
            players = []
            for row in cursor.fetchall():
                try:
                    players.append({
                        'player_id': row[0],
                        'name': row[1],
                        'position': row[2],
                        'jersey_number': row[3],
                        'height': row[4],
                        'weight': row[5],
                        'birth_date': row[6].strftime('%Y-%m-%d') if row[6] else None,
                        'nationality': row[7],
                        'current_team_id': row[8],
                        'team_name': row[9],
                        'contract_expiry': row[10].strftime('%Y-%m-%d') if row[10] else None,
                        'salary': float(row[11]) if row[11] else None,
                        'photo_url': f'/api/images/{row[12]}' if row[12] else None
                    })
                except Exception as e:
                    print(f"Error processing player row {row[0]}: {e}")
                    continue
            
            return jsonify(players), 200
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()


@players_bp.route('', methods=['POST'])
@jwt_required()
def create_player():
    """创建球员（仅管理员）"""
    current_user_id = get_jwt_identity()
    
    if not check_admin_permission(current_user_id):
        return jsonify({'error': '权限不足，仅管理员可创建球员'}), 403
    
    data = request.get_json()
    name = data.get('name')
    position = data.get('position')
    jersey_number = data.get('jersey_number')
    height = data.get('height')
    weight = data.get('weight')
    birth_date = data.get('birth_date')
    nationality = data.get('nationality')
    current_team_id = data.get('current_team_id')
    contract_expiry = data.get('contract_expiry')
    salary = data.get('salary')
    
    # 处理空字符串为None
    height = height if height != '' else None
    weight = weight if weight != '' else None
    birth_date = birth_date if birth_date != '' else None
    nationality = nationality if nationality != '' else None
    current_team_id = current_team_id if current_team_id != '' else None
    contract_expiry = contract_expiry if contract_expiry != '' else None
    salary = salary if salary != '' else None
    
    if not name or not position or jersey_number is None:
        return jsonify({'error': '姓名、位置和球衣号是必填字段'}), 400
    
    conn = db_config.get_connection()
    if not conn:
        return jsonify({'error': '数据库连接失败'}), 500
    
    try:
        with conn.cursor() as cursor:
            if current_team_id:
                cursor.execute("""
                    SELECT player_id FROM Player 
                    WHERE 球衣号 = %s AND 当前球队ID = %s
                """, (jersey_number, current_team_id))
                if cursor.fetchone():
                    return jsonify({'error': '该球队中已有球员使用此球衣号'}), 400
            
            cursor.execute("""
                INSERT INTO Player (姓名, 位置, 球衣号, 身高, 体重, 出生日期, 
                                  国籍, 当前球队ID, 合同到期, 薪资) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (name, position, jersey_number, height, weight, 
                  birth_date, nationality, current_team_id, contract_expiry, salary))
            
            conn.commit()
            return jsonify({'message': '球员创建成功'}), 201
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()


@players_bp.route('/<int:player_id>', methods=['PUT'])
@jwt_required()
def update_player(player_id):
    """更新球员（仅管理员）"""
    current_user_id = get_jwt_identity()
    
    if not check_admin_permission(current_user_id):
        return jsonify({'error': '权限不足，仅管理员可更新球员'}), 403
    
    data = request.get_json()
    name = data.get('name')
    position = data.get('position')
    jersey_number = data.get('jersey_number')
    height = data.get('height')
    weight = data.get('weight')
    birth_date = data.get('birth_date')
    nationality = data.get('nationality')
    current_team_id = data.get('current_team_id')
    contract_expiry = data.get('contract_expiry')
    salary = data.get('salary')
    
    # 处理空字符串为None
    height = height if height != '' else None
    weight = weight if weight != '' else None
    birth_date = birth_date if birth_date != '' else None
    nationality = nationality if nationality != '' else None
    current_team_id = current_team_id if current_team_id != '' else None
    contract_expiry = contract_expiry if contract_expiry != '' else None
    salary = salary if salary != '' else None
    
    if not name or not position or jersey_number is None:
        return jsonify({'error': '姓名、位置和球衣号是必填字段'}), 400
    
    conn = db_config.get_connection()
    if not conn:
        return jsonify({'error': '数据库连接失败'}), 500
    
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT player_id FROM Player WHERE player_id = %s", (player_id,))
            if not cursor.fetchone():
                return jsonify({'error': '球员不存在'}), 404
            
            if current_team_id:
                cursor.execute("""
                    SELECT player_id FROM Player 
                    WHERE 球衣号 = %s AND 当前球队ID = %s AND player_id != %s
                """, (jersey_number, current_team_id, player_id))
                if cursor.fetchone():
                    return jsonify({'error': '该球队中已有其他球员使用此球衣号'}), 400
            
            cursor.execute("""
                UPDATE Player 
                SET 姓名 = %s, 位置 = %s, 球衣号 = %s, 身高 = %s, 体重 = %s, 
                    出生日期 = %s, 国籍 = %s, 当前球队ID = %s, 合同到期 = %s, 薪资 = %s
                WHERE player_id = %s
            """, (name, position, jersey_number, height, weight, 
                  birth_date, nationality, current_team_id, contract_expiry, salary, player_id))
            
            conn.commit()
            return jsonify({'message': '球员更新成功'}), 200
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()


@players_bp.route('/<int:player_id>', methods=['DELETE'])
@jwt_required()
def delete_player(player_id):
    """删除球员（仅管理员）"""
    current_user_id = get_jwt_identity()
    
    if not check_admin_permission(current_user_id):
        return jsonify({'error': '权限不足，仅管理员可删除球员'}), 403
    
    conn = db_config.get_connection()
    if not conn:
        return jsonify({'error': '数据库连接失败'}), 500
    
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT player_id FROM Player WHERE player_id = %s", (player_id,))
            if not cursor.fetchone():
                return jsonify({'error': '球员不存在'}), 404
            
            cursor.execute("DELETE FROM Player WHERE player_id = %s", (player_id,))
            conn.commit()
            return jsonify({'message': '球员删除成功'}), 200
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()


@players_bp.route('/<int:player_id>/photo', methods=['POST'])
@jwt_required()
def upload_player_photo(player_id):
    """上传球员照片（仅管理员）"""
    current_user_id = get_jwt_identity()
    
    if not check_admin_permission(current_user_id):
        return jsonify({'error': '权限不足，仅管理员可上传球员照片'}), 403
        
    if 'image' not in request.files:
        return jsonify({'error': '没有上传文件'}), 400
        
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': '未选择文件'}), 400
        
    conn = db_config.get_connection()
    if not conn:
        return jsonify({'error': '数据库连接失败'}), 500
        
    try:
        file_data = file.read()
        mime_type = file.mimetype
        filename = file.filename
        
        with conn.cursor() as cursor:
            # 1. Insert into Image table
            cursor.execute("""
                INSERT INTO Image (user_id, 名称, 数据, MIME类型)
                VALUES (%s, %s, %s, %s)
            """, (current_user_id, filename, file_data, mime_type))
            image_id = cursor.lastrowid
            
            # 2. Insert/Update Player_Image table
            # Use ON DUPLICATE KEY UPDATE to handle existing record
            cursor.execute("""
                INSERT INTO Player_Image (player_id, image_id)
                VALUES (%s, %s)
                ON DUPLICATE KEY UPDATE image_id = VALUES(image_id)
            """, (player_id, image_id))
            
            conn.commit()
            
            return jsonify({
                'message': '球员照片上传成功',
                'image_id': image_id,
                'url': f'/api/images/{image_id}'
            }), 201
            
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

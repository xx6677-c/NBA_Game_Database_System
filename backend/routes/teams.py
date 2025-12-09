"""球队管理路由"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from database.config import DatabaseConfig
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
            cursor.execute("""
                SELECT team_id, 名称, 城市, 场馆, 分区, 成立年份 
                FROM Team ORDER BY 名称
            """)
            
            teams = []
            for row in cursor.fetchall():
                teams.append({
                    'team_id': row[0],
                    'name': row[1],
                    'city': row[2],
                    'arena': row[3],
                    'conference': row[4],
                    'founded_year': row[5]
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
            
            cursor.execute("""
                INSERT INTO Team (名称, 城市, 场馆, 分区, 成立年份) 
                VALUES (%s, %s, %s, %s, %s)
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
            
            cursor.execute("""
                UPDATE Team 
                SET 名称 = %s, 城市 = %s, 场馆 = %s, 分区 = %s, 成立年份 = %s
                WHERE team_id = %s
            """, (name, city, arena, conference, founded_year, team_id))
            
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
            
            cursor.execute("DELETE FROM Team WHERE team_id = %s", (team_id,))
            conn.commit()
            return jsonify({'message': '球队删除成功'}), 200
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

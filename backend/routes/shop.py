"""商店相关路由"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import random

from database.config import DatabaseConfig

shop_bp = Blueprint('shop', __name__)
db_config = DatabaseConfig()

@shop_bp.route('/draw', methods=['POST'])
@jwt_required()
def draw_card():
    """抽取球星卡"""
    current_user_id = get_jwt_identity()
    cost = 50  # 抽卡消耗积分
    
    conn = db_config.get_connection()
    if not conn:
        return jsonify({'error': '数据库连接失败'}), 500
        
    try:
        with conn.cursor() as cursor:
            # 1. 检查积分是否足够
            cursor.execute("SELECT points FROM User WHERE user_id = %s", (current_user_id,))
            user = cursor.fetchone()
            if not user or user[0] < cost:
                return jsonify({'error': '积分不足，需要 50 积分'}), 400
                
            # 2. 随机抽取一名球员
            # 这里使用简单的随机算法，实际生产环境可能需要更复杂的权重算法
            cursor.execute("""
                SELECT p.player_id, p.姓名, p.位置, p.球衣号, t.名称 as team_name, pi.image_id
                FROM Player p
                JOIN Team t ON p.当前球队ID = t.team_id
                LEFT JOIN Player_Image pi ON p.player_id = pi.player_id
                ORDER BY RAND() LIMIT 1
            """)
            player = cursor.fetchone()
            
            if not player:
                return jsonify({'error': '卡池为空'}), 500
                
            player_data = {
                'player_id': player[0],
                'name': player[1],
                'position': player[2],
                'jersey_number': player[3],
                'team_name': player[4],
                'photo_url': f'/api/images/{player[5]}' if player[5] else None
            }
            
            # 3. 扣除积分并添加卡片 (事务处理)
            conn.autocommit = False
            try:
                # 扣积分
                cursor.execute("UPDATE User SET points = points - %s WHERE user_id = %s", (cost, current_user_id))
                
                # 添加卡片
                cursor.execute("""
                    INSERT INTO User_Card (user_id, player_id) VALUES (%s, %s)
                """, (current_user_id, player_data['player_id']))
                
                conn.commit()
                
                return jsonify({
                    'message': '恭喜获得球星卡！',
                    'card': player_data,
                    'remaining_points': user[0] - cost
                }), 200
                
            except Exception as e:
                conn.rollback()
                raise e
                
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

@shop_bp.route('/my-cards', methods=['GET'])
@jwt_required()
def get_my_cards():
    """获取我的球星卡"""
    current_user_id = get_jwt_identity()
    
    conn = db_config.get_connection()
    if not conn:
        return jsonify({'error': '数据库连接失败'}), 500
        
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT uc.id, uc.get_time,
                       p.player_id, p.姓名, p.位置, p.球衣号, t.名称 as team_name, pi.image_id
                FROM User_Card uc
                JOIN Player p ON uc.player_id = p.player_id
                JOIN Team t ON p.当前球队ID = t.team_id
                LEFT JOIN Player_Image pi ON p.player_id = pi.player_id
                WHERE uc.user_id = %s
                ORDER BY uc.get_time DESC
            """, (current_user_id,))
            
            cards = []
            for row in cursor.fetchall():
                cards.append({
                    'card_id': row[0],
                    'get_time': row[1].strftime('%Y-%m-%d %H:%M'),
                    'player_id': row[2],
                    'name': row[3],
                    'position': row[4],
                    'jersey_number': row[5],
                    'team_name': row[6],
                    'photo_url': f'/api/images/{row[7]}' if row[7] else None
                })
            
            return jsonify(cards), 200
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

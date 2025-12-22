"""商店相关路由"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import random

from database.core.config import DatabaseConfig

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
            # 调用存储过程 sp_draw_card
            # 参数: p_user_id, p_cost, OUT p_success, OUT p_message, OUT p_player_id, ...
            # 使用 execute 代替 callproc 以确保正确获取 OUT 参数
            cursor.execute("""
                SET @p_success = FALSE,
                    @p_message = '',
                    @p_player_id = 0,
                    @p_player_name = '',
                    @p_position = '',
                    @p_jersey_number = 0,
                    @p_team_name = '',
                    @p_image_id = 0,
                    @p_remaining_points = 0
            """)
            
            cursor.execute("""
                CALL sp_draw_card(%s, %s, @p_success, @p_message, @p_player_id, 
                                @p_player_name, @p_position, @p_jersey_number, 
                                @p_team_name, @p_image_id, @p_remaining_points)
            """, (current_user_id, cost))
            
            cursor.execute("""
                SELECT @p_success, @p_message, @p_player_id, @p_player_name, 
                       @p_position, @p_jersey_number, @p_team_name, @p_image_id, 
                       @p_remaining_points
            """)
            result = cursor.fetchone()
            
            success = result[0]
            message = result[1]
            
            if not success:
                return jsonify({'error': message}), 400
                
            player_data = {
                'player_id': result[2],
                'name': result[3],
                'position': result[4],
                'jersey_number': result[5],
                'team_name': result[6],
                'photo_url': f'/api/images/{result[7]}' if result[7] else None
            }
            
            remaining_points = result[8]
            
            conn.commit()
            
            return jsonify({
                'message': message,
                'card': player_data,
                'remaining_points': remaining_points
            }), 200
                
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
            cursor.callproc('sp_get_my_cards', (current_user_id,))
            
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

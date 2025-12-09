"""评论管理路由"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from database.config import DatabaseConfig


comments_bp = Blueprint('comments', __name__)
db_config = DatabaseConfig()


@comments_bp.route('/<int:comment_id>/like', methods=['POST', 'DELETE'])
@jwt_required()
def toggle_comment_like(comment_id):
    """点赞/取消点赞评论"""
    current_user_id = get_jwt_identity()
    
    conn = db_config.get_connection()
    if not conn:
        return jsonify({'error': '数据库连接失败'}), 500
    
    try:
        with conn.cursor() as cursor:
            if request.method == 'POST':
                cursor.execute("""
                    SELECT COUNT(*) FROM Comment_Like 
                    WHERE user_id = %s AND comment_id = %s
                """, (current_user_id, comment_id))
                
                if cursor.fetchone()[0] == 0:
                    cursor.execute("""
                        INSERT INTO Comment_Like (user_id, comment_id) 
                        VALUES (%s, %s)
                    """, (current_user_id, comment_id))
                    
                    cursor.execute("""
                        UPDATE Comment 
                        SET 点赞数 = 点赞数 + 1 
                        WHERE comment_id = %s
                    """, (comment_id,))
                    
                    conn.commit()
                    return jsonify({'message': '点赞成功', 'liked': True})
                else:
                    return jsonify({'message': '已经点赞过了', 'liked': True})
            
            else:  # DELETE
                cursor.execute("""
                    SELECT COUNT(*) FROM Comment_Like 
                    WHERE user_id = %s AND comment_id = %s
                """, (current_user_id, comment_id))
                
                if cursor.fetchone()[0] > 0:
                    cursor.execute("""
                        DELETE FROM Comment_Like 
                        WHERE user_id = %s AND comment_id = %s
                    """, (current_user_id, comment_id))
                    
                    cursor.execute("""
                        UPDATE Comment 
                        SET 点赞数 = 点赞数 - 1 
                        WHERE comment_id = %s
                    """, (comment_id,))
                    
                    conn.commit()
                    return jsonify({'message': '取消点赞成功', 'liked': False})
                else:
                    return jsonify({'message': '还未点赞', 'liked': False})
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

"""评论管理路由"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from database.core.config import DatabaseConfig


comments_bp = Blueprint('comments', __name__)
db_config = DatabaseConfig()


@comments_bp.route('/<int:comment_id>', methods=['DELETE'])
@jwt_required()
def delete_comment(comment_id):
    """删除评论"""
    current_user_id = get_jwt_identity()
    
    conn = db_config.get_connection()
    if not conn:
        return jsonify({'error': '数据库连接失败'}), 500
    
    try:
        with conn.cursor() as cursor:
            # 检查评论是否存在并获取评论者ID
            cursor.execute('SELECT user_id FROM Comment WHERE comment_id = %s', (comment_id,))
            result = cursor.fetchone()
            
            if not result:
                return jsonify({'error': '评论不存在'}), 404
            
            comment_user_id = result[0]
            
            # 检查权限：只有评论作者或管理员可以删除
            cursor.execute('SELECT 角色 FROM User WHERE user_id = %s', (current_user_id,))
            user_result = cursor.fetchone()
            user_role = user_result[0] if user_result else 'user'
            
            if comment_user_id != current_user_id and user_role != 'admin':
                return jsonify({'error': '无权删除此评论'}), 403
            
            # 调用存储过程删除评论
            cursor.callproc('sp_delete_comment', (comment_id,))
            conn.commit()
            
            return jsonify({'message': '评论删除成功'})
            
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()


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
                cursor.callproc('sp_check_comment_like', (current_user_id, comment_id))
                
                if cursor.fetchone()[0] == 0:
                    cursor.callproc('sp_add_comment_like', (current_user_id, comment_id))
                    
                    conn.commit()
                    return jsonify({'message': '点赞成功', 'liked': True})
                else:
                    return jsonify({'message': '已经点赞过了', 'liked': True})
            
            else:  # DELETE
                cursor.callproc('sp_check_comment_like', (current_user_id, comment_id))
                
                if cursor.fetchone()[0] > 0:
                    cursor.callproc('sp_remove_comment_like', (current_user_id, comment_id))
                    
                    conn.commit()
                    return jsonify({'message': '取消点赞成功', 'liked': False})
                else:
                    return jsonify({'message': '还未点赞', 'liked': False})
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

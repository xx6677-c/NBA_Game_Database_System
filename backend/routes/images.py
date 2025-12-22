"""图片管理路由"""
from flask import Blueprint, request, jsonify, send_file, Response
from flask_jwt_extended import jwt_required, get_jwt_identity
import io

from database.core.config import DatabaseConfig

images_bp = Blueprint('images', __name__)
db_config = DatabaseConfig()

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@images_bp.route('/upload', methods=['POST'])
@jwt_required()
def upload_image():
    """上传图片"""
    current_user_id = get_jwt_identity()
    
    if 'file' not in request.files:
        return jsonify({'error': '没有文件部分'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': '未选择文件'}), 400
        
    if file and allowed_file(file.filename):
        try:
            # 读取文件二进制数据
            file_data = file.read()
            mime_type = file.mimetype
            filename = file.filename
            
            conn = db_config.get_connection()
            if not conn:
                return jsonify({'error': '数据库连接失败'}), 500
                
            with conn.cursor() as cursor:
                # sp_upload_image 有4个参数，最后一个是OUT参数 p_image_id
                # 使用 execute 代替 callproc 以确保正确获取 OUT 参数
                cursor.execute("SET @p_image_id = 0")
                cursor.execute("CALL sp_upload_image(%s, %s, %s, @p_image_id)", 
                             (filename, file_data, mime_type))
                cursor.execute("SELECT @p_image_id")
                result = cursor.fetchone()
                image_id = result[0]
                
                conn.commit()
                
                return jsonify({
                    'message': '图片上传成功',
                    'image_id': image_id,
                    'url': f'/api/images/{image_id}'
                }), 201
                
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        finally:
            if conn:
                conn.close()
    
    return jsonify({'error': '不支持的文件类型'}), 400


@images_bp.route('/avatar', methods=['POST'])
@jwt_required()
def upload_avatar():
    """上传用户头像"""
    current_user_id = get_jwt_identity()
    
    if 'file' not in request.files:
        return jsonify({'error': '没有文件部分'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': '未选择文件'}), 400
        
    if file and allowed_file(file.filename):
        try:
            file_data = file.read()
            mime_type = file.mimetype
            filename = file.filename
            
            conn = db_config.get_connection()
            if not conn:
                return jsonify({'error': '数据库连接失败'}), 500
                
            with conn.cursor() as cursor:
                # 1. 插入图片到 Image 表
                # 使用 execute 代替 callproc 以确保正确获取 OUT 参数
                cursor.execute("SET @p_image_id = 0")
                cursor.execute("CALL sp_upload_image(%s, %s, %s, @p_image_id)", 
                             (filename, file_data, mime_type))
                cursor.execute("SELECT @p_image_id")
                result = cursor.fetchone()
                image_id = result[0]
                
                # 2. 更新 User_Avatar 表
                cursor.callproc('sp_update_user_avatar', (current_user_id, image_id))
                
                conn.commit()
                
                return jsonify({
                    'message': '头像上传成功',
                    'avatar_url': f'/api/images/{image_id}'
                }), 200
                
        except Exception as e:
            conn.rollback()
            return jsonify({'error': str(e)}), 500
        finally:
            if conn:
                conn.close()
    
    return jsonify({'error': '不支持的文件类型'}), 400


@images_bp.route('/<int:image_id>', methods=['GET'])
def get_image(image_id):
    """获取图片"""
    conn = db_config.get_connection()
    if not conn:
        return jsonify({'error': '数据库连接失败'}), 500
        
    try:
        with conn.cursor() as cursor:
            cursor.callproc('sp_get_image', (image_id,))
            row = cursor.fetchone()
            
            if not row:
                return jsonify({'error': '图片不存在'}), 404
                
            image_data = row[0]
            mime_type = row[1]
            
            return send_file(
                io.BytesIO(image_data),
                mimetype=mime_type
            )
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

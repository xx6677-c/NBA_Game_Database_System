"""SQL查询路由（仅数据分析师）"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from database.config import DatabaseConfig
from utils.permissions import check_analyst_permission


query_bp = Blueprint('query', __name__)
db_config = DatabaseConfig()


@query_bp.route('/execute', methods=['POST'])
@jwt_required()
def execute_query():
    """执行SQL查询（仅数据分析师）"""
    current_user_id = get_jwt_identity()
    
    if not check_analyst_permission(current_user_id):
        return jsonify({'error': '权限不足，仅数据分析师可执行SQL查询'}), 403
    
    data = request.get_json()
    sql_query = data.get('query', '').strip()
    
    if not sql_query:
        return jsonify({'error': 'SQL查询不能为空'}), 400
    
    # 安全检查：只允许SELECT查询
    if not sql_query.upper().startswith('SELECT'):
        return jsonify({'error': '仅允许执行SELECT查询'}), 400
    
    conn = db_config.get_connection()
    if not conn:
        return jsonify({'error': '数据库连接失败'}), 500
    
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql_query)
            
            # 获取列名
            columns = [desc[0] for desc in cursor.description] if cursor.description else []
            
            # 获取查询结果
            rows = cursor.fetchall()
            
            # 转换为字典列表
            results = []
            for row in rows:
                result_dict = {}
                for idx, col in enumerate(columns):
                    value = row[idx]
                    # 处理日期时间类型
                    if hasattr(value, 'strftime'):
                        value = value.strftime('%Y-%m-%d %H:%M:%S')
                    result_dict[col] = value
                results.append(result_dict)
            
            return jsonify({
                'success': True,
                'columns': columns,
                'data': results,
                'row_count': len(results)
            }), 200
            
    except Exception as e:
        return jsonify({'error': f'查询执行失败: {str(e)}'}), 500
    finally:
        conn.close()

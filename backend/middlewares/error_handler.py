"""全局错误处理中间件"""
from flask import jsonify
from werkzeug.exceptions import HTTPException
import traceback


def register_error_handlers(app):
    """注册全局错误处理器"""
    
    @app.errorhandler(HTTPException)
    def handle_http_exception(e):
        """处理HTTP异常"""
        return jsonify({
            'success': False,
            'error': e.description,
            'status_code': e.code
        }), e.code
    
    @app.errorhandler(Exception)
    def handle_exception(e):
        """处理所有未捕获的异常"""
        app.logger.error(f"未处理的异常: {str(e)}\n{traceback.format_exc()}")
        
        # 开发环境返回详细错误信息
        if app.debug:
            return jsonify({
                'success': False,
                'error': str(e),
                'traceback': traceback.format_exc()
            }), 500
        
        # 生产环境返回通用错误信息
        return jsonify({
            'success': False,
            'error': '服务器内部错误'
        }), 500
    
    @app.errorhandler(404)
    def handle_404(e):
        """处理404错误"""
        return jsonify({
            'success': False,
            'error': '请求的资源不存在'
        }), 404
    
    @app.errorhandler(403)
    def handle_403(e):
        """处理403错误"""
        return jsonify({
            'success': False,
            'error': '没有权限访问该资源'
        }), 403
    
    @app.errorhandler(401)
    def handle_401(e):
        """处理401错误"""
        return jsonify({
            'success': False,
            'error': '未授权，请先登录'
        }), 401

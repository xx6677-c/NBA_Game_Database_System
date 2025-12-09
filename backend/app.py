"""Flask应用工厂"""
from flask import Flask
from flask_cors import CORS
import os

from middlewares.jwt_config import configure_jwt
from middlewares.error_handler import register_error_handlers
from routes import register_blueprints


def create_app():
    """创建并配置Flask应用"""
    app = Flask(__name__)
    
    # 基础配置
    app.config['JWT_SECRET'] = os.getenv('JWT_SECRET', 'your-secret-key-change-this-in-production')
    app.config['DEBUG'] = os.getenv('DEBUG', 'False').lower() == 'true'
    
    # 启用CORS
    CORS(app)
    
    # 配置JWT
    configure_jwt(app)
    
    # 注册错误处理器
    register_error_handlers(app)
    
    # 注册蓝图
    register_blueprints(app)
    
    # 健康检查端点
    @app.route('/health')
    def health():
        return {'status': 'healthy', 'message': 'NBA Game Database API is running'}
    
    @app.route('/')
    def index():
        return {
            'name': 'NBA Game Database System API',
            'version': '2.0',
            'description': 'Refactored modular architecture',
            'endpoints': {
                'auth': '/api/auth',
                'teams': '/api/teams',
                'players': '/api/players',
                'games': '/api/games',
                'posts': '/api/posts',
                'comments': '/api/comments',
                'query': '/api/query'
            }
        }
    
    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')

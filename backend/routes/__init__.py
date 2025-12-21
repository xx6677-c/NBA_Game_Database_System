"""路由模块初始化"""
from flask import Blueprint


def register_blueprints(app):
    """注册所有蓝图"""
    from .auth import auth_bp
    from .teams import teams_bp
    from .players import players_bp
    from .games import games_bp
    from .posts import posts_bp
    from .comments import comments_bp
    from .query import query_bp
    from .rankings import rankings_bp
    from .images import images_bp
    from .shop import shop_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(teams_bp, url_prefix='/api/teams')
    app.register_blueprint(players_bp, url_prefix='/api/players')
    app.register_blueprint(games_bp, url_prefix='/api/games')
    app.register_blueprint(posts_bp, url_prefix='/api/posts')
    app.register_blueprint(comments_bp, url_prefix='/api/comments')
    app.register_blueprint(query_bp, url_prefix='/api/query')
    app.register_blueprint(rankings_bp, url_prefix='/api/rankings')
    app.register_blueprint(images_bp, url_prefix='/api/images')
    app.register_blueprint(shop_bp, url_prefix='/api/shop')

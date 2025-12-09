"""JWT配置和黑名单管理"""
from flask_jwt_extended import JWTManager


# JWT令牌黑名单（生产环境应该使用Redis或数据库）
jwt_blacklist = set()


def configure_jwt(app):
    """配置JWT"""
    app.config['JWT_SECRET_KEY'] = app.config.get('JWT_SECRET', 'your-secret-key-change-this-in-production')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 3600  # 1小时过期
    app.config['JWT_TOKEN_LOCATION'] = ['headers']
    app.config['JWT_HEADER_NAME'] = 'Authorization'
    app.config['JWT_HEADER_TYPE'] = 'Bearer'
    app.config['JWT_BLACKLIST_ENABLED'] = True
    app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access']
    
    jwt = JWTManager(app)
    
    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload):
        jti = jwt_payload['jti']
        return jti in jwt_blacklist
    
    return jwt

"""认证相关工具函数"""
import bcrypt


def hash_password(password: str) -> str:
    """对密码进行哈希加密"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


def check_password(password: str, hashed: str) -> bool:
    """验证密码是否正确"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

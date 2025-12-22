"""权限验证工具函数"""
from database.core.config import DatabaseConfig


db_config = DatabaseConfig()


def check_admin_permission(user_id: str) -> bool:
    """
    验证用户是否具有管理员权限
    
    Args:
        user_id: 用户ID
        
    Returns:
        bool: 是否是管理员
    """
    conn = db_config.get_connection()
    if not conn:
        return False
    
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT 角色 FROM User WHERE user_id = %s", (user_id,))
            user_data = cursor.fetchone()
            
            if not user_data or user_data[0] != 'admin':
                return False
            return True
    except Exception as e:
        print(f"权限验证错误: {e}")
        return False
    finally:
        conn.close()


def check_analyst_permission(user_id: str) -> bool:
    """
    验证用户是否具有数据分析师权限
    
    Args:
        user_id: 用户ID
        
    Returns:
        bool: 是否是数据分析师
    """
    conn = db_config.get_connection()
    if not conn:
        return False
    
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT 角色 FROM User WHERE user_id = %s", (user_id,))
            user_data = cursor.fetchone()
            
            if not user_data or user_data[0] != 'analyst':
                return False
            return True
    except Exception as e:
        print(f"权限验证错误: {e}")
        return False
    finally:
        conn.close()

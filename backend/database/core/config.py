import pymysql
import os
from typing import Any, Optional
from dotenv import load_dotenv
import logging

load_dotenv()

logger = logging.getLogger(__name__)


class DatabaseConfig:
    """
    数据库配置类
    支持SSL连接和连接池管理
    """
    
    def __init__(self):
        # 华为云TaurusDB连接配置
        self.host: str = os.getenv('DB_HOST', 'your_host')
        self.port: int = int(os.getenv('DB_PORT', '3306'))
        self.database: str = os.getenv('DB_NAME', 'nba_database')
        self.username: str = os.getenv('DB_USERNAME', '')
        self.password: str = os.getenv('DB_PASSWORD', '')
        
        # 连接池配置
        self.max_connections: int = int(os.getenv('DB_MAX_CONNECTIONS', '10'))
        self.connect_timeout: int = int(os.getenv('DB_CONNECT_TIMEOUT', '10'))
        
        # SSL配置
        ssl_ca_path = os.getenv('SSL_CA_PATH')
        if ssl_ca_path and os.path.exists(ssl_ca_path):
            self.ssl_config = {
                'ca': ssl_ca_path,
                'check_hostname': False
            }
        else:
            self.ssl_config = None
    
    def get_connection(self, retry: int = 3) -> Optional[Any]:
        """
        获取数据库连接，支持重试机制
        
        Args:
            retry: 重试次数
            
        Returns:
            数据库连接对象或None
        """
        for attempt in range(retry):
            try:
                conn_params = {
                    'host': self.host,
                    'port': self.port,
                    'user': self.username,
                    'password': self.password,
                    'database': self.database,
                    'charset': 'utf8mb4',
                    'connect_timeout': self.connect_timeout,
                    'autocommit': True
                }
                
                # 添加SSL配置
                if self.ssl_config:
                    conn_params['ssl'] = self.ssl_config
                
                # 创建连接
                conn = pymysql.connect(**conn_params)
                logger.info(f"数据库连接成功 (尝试 {attempt + 1}/{retry})")
                return conn
                
            except pymysql.OperationalError as e:
                logger.error(f"数据库连接失败 (尝试 {attempt + 1}/{retry}): {e}")
                if attempt == retry - 1:
                    logger.error("数据库连接重试次数已用尽")
                    return None
            except Exception as e:
                logger.error(f"数据库连接异常: {e}")
                return None
        
        return None
        
        # SSL连接失败或没有SSL配置，尝试普通连接
        try:
            conn = pymysql.connect(
                host=self.host,
                port=self.port,
                user=self.username,
                password=self.password,
                database=self.database
            )
            print("普通连接成功")
            return conn
        except Exception as e:
            print(f"数据库连接失败: {e}")
            return None
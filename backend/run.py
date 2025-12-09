#!/usr/bin/env python3
"""
NBA比赛数据库系统 - 后端启动脚本
"""

import os
import sys
from app import app

def main():
    """主函数"""
    print("🏀 NBA比赛数据库系统 - 后端服务")
    print("=" * 50)
    
    # 检查环境变量
    required_env_vars = [
        'DB_HOST',
        'DB_USERNAME', 
        'DB_PASSWORD',
        'DB_NAME'
    ]
    
    missing_vars = []
    for var in required_env_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print("❌ 缺少必要的环境变量:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\n请检查 .env 文件配置")
        sys.exit(1)
    
    print("✅ 环境变量检查通过")
    print("🚀 启动Flask应用...")
    
    # 启动应用
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )

if __name__ == '__main__':
    main()
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NBA比赛数据库系统初始化脚本
执行 init.sql 文件中的 SQL 语句来初始化数据库
"""

import os
import sys
import pymysql
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

def get_database_connection():
    """获取数据库连接"""
    try:
        # 数据库配置
        host = os.getenv('DB_HOST', '124.70.86.207')
        port = int(os.getenv('DB_PORT', 3306))
        database = os.getenv('DB_NAME', 'h_db23373502')
        username = os.getenv('DB_USERNAME', 'u23373502')
        password = os.getenv('DB_PASSWORD', 'Aa243634')
        
        # SSL配置
        ssl_ca_path = os.getenv('SSL_CA_PATH')
        ssl_config = None
        
        if ssl_ca_path and os.path.exists(ssl_ca_path):
            ssl_config = {
                'ssl': {
                    'ca': ssl_ca_path,
                    'check_hostname': False  # 禁用主机名验证
                }
            }
        
        # 尝试SSL连接
        try:
            conn = pymysql.connect(
                host=host,
                port=port,
                user=username,
                password=password,
                database=database,
                ssl=ssl_config['ssl'] if ssl_config else None,
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
            print("SSL连接成功")
            return conn
        except Exception as e:
            print(f"SSL连接失败，尝试非SSL连接: {e}")
            
            # 尝试非SSL连接
            conn = pymysql.connect(
                host=host,
                port=port,
                user=username,
                password=password,
                database=database,
                ssl=None,
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
            print("非SSL连接成功")
            return conn
            
    except Exception as e:
        print(f"数据库连接失败: {e}")
        return None

def read_sql_file(file_path):
    """读取SQL文件并分割成单独的SQL语句"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # 分割SQL语句（以分号结尾）
        statements = []
        current_statement = ""
        
        for line in content.split('\n'):
            # 跳过注释行
            if line.strip().startswith('--') or line.strip().startswith('#'):
                continue
            
            current_statement += line + '\n'
            
            # 如果行以分号结尾，表示一个完整的SQL语句
            if line.strip().endswith(';'):
                statements.append(current_statement.strip())
                current_statement = ""
        
        # 添加最后一个语句（如果没有分号）
        if current_statement.strip():
            statements.append(current_statement.strip())
        
        return statements
    except Exception as e:
        print(f"读取SQL文件失败: {e}")
        return []

def execute_sql_statements(conn, statements):
    """执行SQL语句"""
    if not conn:
        print("数据库连接失败，无法执行SQL语句")
        return False
    
    try:
        with conn.cursor() as cursor:
            success_count = 0
            error_count = 0
            
            for i, statement in enumerate(statements, 1):
                if not statement.strip():
                    continue
                    
                try:
                    cursor.execute(statement)
                    success_count += 1
                    print(f"✓ 执行成功 [{i}/{len(statements)}]: {statement[:50]}...")
                except Exception as e:
                    # 如果是索引重复错误，忽略并继续
                    if "Duplicate key" in str(e) or "already exists" in str(e):
                        success_count += 1
                        print(f"⚠ 索引已存在 [{i}/{len(statements)}]: {statement[:50]}...")
                    else:
                        error_count += 1
                        print(f"✗ 执行失败 [{i}/{len(statements)}]: {e}")
                        print(f"   SQL语句: {statement[:100]}...")
            
            # 提交事务
            conn.commit()
            
            print(f"\n执行结果:")
            print(f"成功: {success_count}")
            print(f"失败: {error_count}")
            print(f"总计: {len(statements)}")
            
            return error_count == 0
            
    except Exception as e:
        print(f"执行SQL语句时发生错误: {e}")
        return False

def main():
    """主函数"""
    print("=== NBA比赛数据库系统初始化 ===")
    print("正在连接数据库...")
    
    # 获取数据库连接
    conn = get_database_connection()
    if not conn:
        print("数据库连接失败，请检查配置")
        sys.exit(1)
    
    print("数据库连接成功")
    
    # 读取SQL文件
    sql_file_path = os.path.join(os.path.dirname(__file__), 'init.sql')
    print(f"正在读取SQL文件: {sql_file_path}")
    
    statements = read_sql_file(sql_file_path)
    if not statements:
        print("没有找到有效的SQL语句")
        conn.close()
        sys.exit(1)
    
    print(f"找到 {len(statements)} 条SQL语句")
    
    # 执行SQL语句
    print("\n开始执行SQL语句...")
    success = execute_sql_statements(conn, statements)
    
    # 关闭连接
    conn.close()
    
    if success:
        print("\n🎉 数据库初始化完成！")
        print("数据库表结构已创建，初始数据已插入")
    else:
        print("\n❌ 数据库初始化失败，请检查错误信息")
        sys.exit(1)

if __name__ == "__main__":
    main()
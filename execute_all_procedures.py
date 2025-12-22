#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import re
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))
from database import config as db_config

def execute_sql_file(file_path):
    """执行包含存储过程的SQL文件"""
    db = db_config.DatabaseConfig()
    conn = db.get_connection()
    if not conn:
        print('数据库连接失败')
        return
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 简单的解析器，用于处理 DELIMITER
        # 1. 移除注释 (简单处理 -- )
        # content = re.sub(r'--.*', '', content) # 这可能会误删内容中的 --，先不处理注释，pymysql应该能处理
        
        # 2. 按 DELIMITER 分割
        # 默认分隔符是 ;
        # 我们主要寻找 DELIMITER // ... // DELIMITER ; 结构
        
        # 策略：手动解析
        statements = []
        current_statement = []
        delimiter = ';'
        
        lines = content.split('\n')
        for line in lines:
            line = line.strip()
            if not line or line.startswith('--'):
                continue
                
            if line.upper().startswith('DELIMITER'):
                new_delimiter = line.split()[1]
                delimiter = new_delimiter
                continue
            
            if line.endswith(delimiter):
                current_statement.append(line[:-len(delimiter)])
                full_statement = '\n'.join(current_statement).strip()
                if full_statement:
                    statements.append(full_statement)
                current_statement = []
            else:
                current_statement.append(line)
                
        with conn.cursor() as cursor:
            for i, sql in enumerate(statements):
                if not sql:
                    continue
                try:
                    # print(f"Executing statement {i+1}...")
                    cursor.execute(sql)
                except Exception as e:
                    print(f"Error executing statement {i+1}: {e}")
                    print(f"SQL: {sql[:100]}...")
                    # Continue executing other statements
            
            conn.commit()
            print(f'成功执行了 {len(statements)} 条SQL语句。存储过程创建完成！')
            
    except Exception as e:
        print(f'执行脚本时出错: {e}')
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    file_path = os.path.join(os.path.dirname(__file__), 'backend', 'database', 'all_procedures.sql')
    execute_sql_file(file_path)

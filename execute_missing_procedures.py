import os
import sys

# 添加项目根目录到 Python 路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backend.database.core.config import DatabaseConfig

def execute_sql_file(filename):
    db_config = DatabaseConfig()
    conn = db_config.get_connection()
    if not conn:
        print("无法连接到数据库")
        return

    try:
        with open(filename, 'r', encoding='utf-8') as f:
            sql_content = f.read()

        # 分割SQL语句
        # 注意：这里简单的分割可能无法处理复杂的存储过程定义
        # 因为存储过程定义中包含分号。
        # 我们需要特殊的逻辑来处理 DELIMITER
        
        statements = []
        current_statement = []
        delimiter = ';'
        
        lines = sql_content.split('\n')
        for line in lines:
            line = line.strip()
            if not line or line.startswith('--'):
                continue
                
            if line.startswith('DELIMITER'):
                delimiter = line.split()[1]
                continue
                
            if line.endswith(delimiter):
                current_statement.append(line[:-len(delimiter)])
                statements.append('\n'.join(current_statement))
                current_statement = []
            else:
                current_statement.append(line)
                
        with conn.cursor() as cursor:
            for sql in statements:
                if not sql.strip():
                    continue
                try:
                    # print(f"Executing: {sql[:50]}...")
                    cursor.execute(sql)
                except Exception as e:
                    print(f"Error executing SQL: {e}")
                    print(f"SQL: {sql}")
            
            conn.commit()
            print(f"成功执行了 {len(statements)} 条SQL语句。补充存储过程创建完成！")

    except Exception as e:
        print(f"发生错误: {e}")
    finally:
        conn.close()

if __name__ == '__main__':
    # 获取当前脚本所在目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    sql_file = os.path.join(current_dir, 'backend', 'database', 'all_procedures.sql')
    
    if os.path.exists(sql_file):
        execute_sql_file(sql_file)
    else:
        print(f"找不到文件: {sql_file}")

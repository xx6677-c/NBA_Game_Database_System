#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据库初始化脚本
用于创建NBA比赛数据库系统的表结构
"""

import pymysql
import os
from dotenv import load_dotenv

def initialize_database():
    """初始化数据库和表结构"""
    
    # 加载环境变量
    load_dotenv()
    
    # 获取数据库配置
    host = os.getenv('DB_HOST', '124.70.86.207')
    port = int(os.getenv('DB_PORT', 3306))
    username = os.getenv('DB_USERNAME', 'u23373502')
    password = os.getenv('DB_PASSWORD', 'Aa243634')
    database = os.getenv('DB_NAME', 'h_db23373502')
    ssl_ca_path = os.getenv('SSL_CA_PATH')
    
    print("🏀 NBA比赛数据库系统 - 数据库初始化")
    print("=" * 50)
    print(f"目标数据库: {database}")
    print(f"连接地址: {host}:{port}")
    print(f"SSL证书路径: {ssl_ca_path}")
    
    # 配置SSL连接
    ssl_config = None
    if ssl_ca_path and os.path.exists(ssl_ca_path):
        ssl_config = {
            'ssl': {
                'ca': ssl_ca_path,
                'check_hostname': False  # 禁用主机名验证
            }
        }
        print("✅ SSL证书配置成功")
    else:
        print("⚠️ 未找到SSL证书，将尝试非SSL连接")
    
    try:
        # 使用SSL连接数据库
        conn = pymysql.connect(
            host=host,
            port=port,
            user=username,
            password=password,
            database=database,
            ssl=ssl_config['ssl'] if ssl_config else None
        )
        
        cursor = conn.cursor()
        print(f"✅ 成功连接到数据库 {database}")
        
        # 检查当前数据库中的表
        cursor.execute("SHOW TABLES")
        existing_tables = [table[0] for table in cursor.fetchall()]
        
        if existing_tables:
            print(f"\n📊 当前数据库中有 {len(existing_tables)} 个表:")
            for table in existing_tables:
                print(f"   - {table}")
            print("\n🔄 将重新创建所有表结构...")
        else:
            print("\n📊 数据库为空，将创建新表结构...")
        
        # 定义表结构SQL语句
        table_sqls = [
            # 用户表
            """
            CREATE TABLE IF NOT EXISTS User (
                user_id INT AUTO_INCREMENT PRIMARY KEY,
                用户名 VARCHAR(50) NOT NULL UNIQUE,
                密码 VARCHAR(255) NOT NULL,
                角色 ENUM('user', 'admin', 'analyst') DEFAULT 'user',
                注册时间 DATETIME DEFAULT CURRENT_TIMESTAMP,
                最后登录时间 DATETIME,
                邮箱 VARCHAR(100),
                手机号 VARCHAR(20)
            )
            """,
            
            # 球队表
            """
            CREATE TABLE IF NOT EXISTS Team (
                team_id INT AUTO_INCREMENT PRIMARY KEY,
                名称 VARCHAR(100) NOT NULL UNIQUE,
                城市 VARCHAR(50),
                场馆 VARCHAR(100),
                分区 ENUM('东部', '西部') NOT NULL,
                成立年份 INT,
            )
            """,
            
            # 球员表
            """
            CREATE TABLE IF NOT EXISTS Player (
                player_id INT AUTO_INCREMENT PRIMARY KEY,
                姓名 VARCHAR(50) NOT NULL,
                位置 ENUM('控球后卫', '得分后卫', '小前锋', '大前锋', '中锋') NOT NULL,
                球衣号 INT,
                身高 DECIMAL(3,2),
                体重 DECIMAL(5,2),
                出生日期 DATE,
                国籍 VARCHAR(50),
                当前球队ID INT,
                合同到期 DATE,
                薪资 DECIMAL(10,2),
                FOREIGN KEY (当前球队ID) REFERENCES Team(team_id) ON DELETE SET NULL
            )
            """,
            
            # 比赛表
            """
            CREATE TABLE IF NOT EXISTS Game (
                game_id INT AUTO_INCREMENT PRIMARY KEY,
                赛季 VARCHAR(20) NOT NULL,
                日期 DATETIME NOT NULL,
                主队ID INT NOT NULL,
                客队ID INT NOT NULL,
                主队得分 INT,
                客队得分 INT,
                状态 ENUM('未开始', '已结束') DEFAULT '未开始',
                获胜球队ID INT,
                场馆 VARCHAR(100),
                观众人数 INT,
                FOREIGN KEY (主队ID) REFERENCES Team(team_id),
                FOREIGN KEY (客队ID) REFERENCES Team(team_id),
                FOREIGN KEY (获胜球队ID) REFERENCES Team(team_id) ON DELETE SET NULL
            )
            """,

            
            # 帖子表
            """
            CREATE TABLE IF NOT EXISTS Post (
                post_id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                game_id INT,
                标题 VARCHAR(200) NOT NULL,
                内容 TEXT NOT NULL,
                创建时间 DATETIME DEFAULT CURRENT_TIMESTAMP,
                浏览量 INT DEFAULT 0,
                点赞数 INT DEFAULT 0,
                FOREIGN KEY (user_id) REFERENCES User(user_id),
                FOREIGN KEY (game_id) REFERENCES Game(game_id) ON DELETE SET NULL
            )
            """,
            
            # 评论表
            """
           CREATE TABLE IF NOT EXISTS Comment (
                comment_id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                player_id INT,
                game_id INT,
                post_id INT,
                内容 TEXT NOT NULL,
                创建时间 DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES User(user_id),
                FOREIGN KEY (player_id) REFERENCES Player(player_id),
                FOREIGN KEY (game_id) REFERENCES Game(game_id),
                FOREIGN KEY (post_id) REFERENCES Post(post_id)
            );
            """,
            
            # 评分表
            """
            CREATE TABLE IF NOT EXISTS Rating (
                user_id INT NOT NULL,
                player_id INT NOT NULL,
                game_id INT NOT NULL,
                分数 DECIMAL(2,0) DEFAULT 0 CHECK(分数 BETWEEN 0 AND 10) NOT NULL,
                创建时间 DATETIME DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (user_id, player_id, game_id),
                FOREIGN KEY (user_id) REFERENCES User(user_id),
                FOREIGN KEY (player_id) REFERENCES Player(player_id),
                FOREIGN KEY (game_id) REFERENCES Game(game_id)
            )
            """
        ]
        
        # 创建索引的SQL语句
        index_sqls = [
            "CREATE INDEX idx_player_team ON Player(当前球队ID)",
            "CREATE INDEX idx_game_home_team ON Game(主队ID)",
            "CREATE INDEX idx_game_away_team ON Game(客队ID)",
            "CREATE INDEX idx_game_date ON Game(日期)",
            "CREATE INDEX idx_post_game ON Post(game_id)",
            "CREATE INDEX idx_post_user ON Post(user_id)",
            "CREATE INDEX idx_comment_post ON Comment(post_id)",
            "CREATE INDEX idx_comment_user ON Comment(user_id)",
            "CREATE INDEX idx_rating_user ON Rating(user_id)",
            "CREATE INDEX idx_rating_player ON Rating(player_id)",
            "CREATE INDEX idx_rating_game ON Rating(game_id)"
        ]
        
        print("\n📋 开始创建表结构...")
        
        # 执行表创建SQL
        for i, sql in enumerate(table_sqls, 1):
            try:
                cursor.execute(sql)
                print(f"✅ 表 {i}/{len(table_sqls)} 创建成功")
            except Exception as e:
                print(f"⚠️ 表 {i}/{len(table_sqls)} 创建失败: {e}")
        
        print("\n📋 开始创建索引...")
        
        # 执行索引创建SQL
        for i, sql in enumerate(index_sqls, 1):
            try:
                cursor.execute(sql)
                print(f"✅ 索引 {i}/{len(index_sqls)} 创建成功")
            except Exception as e:
                print(f"⚠️ 索引 {i}/{len(index_sqls)} 创建失败: {e}")
        
        # 提交事务
        conn.commit()
        
        # 验证表创建结果
        cursor.execute("SHOW TABLES")
        final_tables = [table[0] for table in cursor.fetchall()]
        
        print(f"\n🎉 数据库初始化完成！")
        print(f"📊 当前数据库中有 {len(final_tables)} 个表:")
        for table in final_tables:
            print(f"   - {table}")
        
        cursor.close()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"❌ 数据库初始化失败: {e}")
        return False

if __name__ == "__main__":
    initialize_database()
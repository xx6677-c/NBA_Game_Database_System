"""
CSV数据导入脚本
将CSV文件数据导入数据库，并清空相关表的现有数据
"""
import csv
import os
import sys
from datetime import datetime
from dotenv import load_dotenv

# 获取项目根目录
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 加载backend目录下的.env文件
load_dotenv(os.path.join(BASE_DIR, 'backend', '.env'))

# 添加backend目录到路径
sys.path.insert(0, os.path.join(BASE_DIR, 'backend'))

from backend.database.core.config import DatabaseConfig


def parse_date(date_str):
    """解析日期字符串，支持多种格式"""
    if not date_str or date_str.strip() == '':
        return None
    
    # 尝试解析 "DEC 18, 2001" 格式
    try:
        return datetime.strptime(date_str.strip(), "%b %d, %Y").strftime("%Y-%m-%d")
    except:
        pass
    
    # 尝试解析 "2025-10-22" 格式
    try:
        return datetime.strptime(date_str.strip(), "%Y-%m-%d").strftime("%Y-%m-%d")
    except:
        pass
    
    # 尝试解析 "2025-10-22 07:30:00" 格式
    try:
        return datetime.strptime(date_str.strip(), "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d %H:%M:%S")
    except:
        pass
    
    return None


def clean_value(value, default=None):
    """清理值，处理空字符串"""
    if value is None or value.strip() == '':
        return default
    return value.strip()


def clean_number(value, default=None):
    """清理数字值"""
    if value is None or value.strip() == '':
        return default
    try:
        return float(value.strip())
    except:
        return default


def clean_int(value, default=None):
    """清理整数值"""
    if value is None or value.strip() == '':
        return default
    try:
        return int(float(value.strip()))
    except:
        return default


def import_teams(cursor, csv_path):
    """导入球队数据"""
    print(f"\n正在导入球队数据: {csv_path}")
    
    with open(csv_path, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        count = 0
        for row in reader:
            team_id = clean_int(row.get('team_id'))
            name = clean_value(row.get('名称'))
            city = clean_value(row.get('城市'), '')
            arena = clean_value(row.get('场馆'), '')
            division = clean_value(row.get('分区'))
            founded = clean_int(row.get('成立年份'))
            
            if team_id and name and division:
                cursor.execute("""
                    INSERT INTO Team (team_id, 名称, 城市, 场馆, 分区, 成立年份)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE 
                        名称=VALUES(名称), 城市=VALUES(城市), 场馆=VALUES(场馆), 
                        分区=VALUES(分区), 成立年份=VALUES(成立年份)
                """, (team_id, name, city, arena, division, founded))
                count += 1
        
        print(f"✓ 成功导入 {count} 支球队")
        return count


def import_players(cursor, csv_path):
    """导入球员数据"""
    print(f"\n正在导入球员数据: {csv_path}")
    
    with open(csv_path, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        count = 0
        for row in reader:
            player_id = clean_int(row.get('player_id'))
            name = clean_value(row.get('姓名'))
            position = clean_value(row.get('位置'))
            jersey = clean_int(row.get('球衣号'))
            height = clean_number(row.get('身高'))
            weight = clean_number(row.get('体重'))
            birth_date = parse_date(row.get('出生日期', '').replace('"', ''))
            nationality = clean_value(row.get('国籍'))
            team_id = clean_int(row.get('当前球队ID'))
            
            if player_id and name and position:
                cursor.execute("""
                    INSERT INTO Player (player_id, 姓名, 位置, 球衣号, 身高, 体重, 出生日期, 国籍, 当前球队ID)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE 
                        姓名=VALUES(姓名), 位置=VALUES(位置), 球衣号=VALUES(球衣号),
                        身高=VALUES(身高), 体重=VALUES(体重), 出生日期=VALUES(出生日期),
                        国籍=VALUES(国籍), 当前球队ID=VALUES(当前球队ID)
                """, (player_id, name, position, jersey, height, weight, birth_date, nationality, team_id))
                count += 1
        
        print(f"✓ 成功导入 {count} 名球员")
        return count


def import_games(cursor, csv_path):
    """导入比赛数据"""
    print(f"\n正在导入比赛数据: {csv_path}")
    
    with open(csv_path, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        count = 0
        team_game_records = []
        
        for row in reader:
            game_id = clean_int(row.get('game_id'))
            season = clean_value(row.get('赛季'))
            date = parse_date(row.get('日期'))
            home_team_id = clean_int(row.get('主队ID'))
            away_team_id = clean_int(row.get('客队ID'))
            home_score = clean_int(row.get('主队得分'))
            away_score = clean_int(row.get('客队得分'))
            status = clean_value(row.get('状态'), '未开始')
            winner_id = clean_int(row.get('获胜球队ID'))
            arena = clean_value(row.get('场馆'), '')
            
            if game_id and season and date and home_team_id and away_team_id:
                cursor.execute("""
                    INSERT INTO Game (game_id, 赛季, 日期, 主队ID, 客队ID, 主队得分, 客队得分, 状态, 获胜球队ID, 场馆)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE 
                        赛季=VALUES(赛季), 日期=VALUES(日期), 主队ID=VALUES(主队ID),
                        客队ID=VALUES(客队ID), 主队得分=VALUES(主队得分), 客队得分=VALUES(客队得分),
                        状态=VALUES(状态), 获胜球队ID=VALUES(获胜球队ID), 场馆=VALUES(场馆)
                """, (game_id, season, date, home_team_id, away_team_id, home_score, away_score, status, winner_id, arena))
                count += 1
                
                # 记录Team_Game关系
                team_game_records.append((home_team_id, game_id, '主场'))
                team_game_records.append((away_team_id, game_id, '客场'))
        
        print(f"✓ 成功导入 {count} 场比赛")
        
        # 导入Team_Game关系
        print("\n正在导入球队-比赛关系...")
        tg_count = 0
        for record in team_game_records:
            try:
                cursor.execute("""
                    INSERT INTO Team_Game (team_id, game_id, 主客类型)
                    VALUES (%s, %s, %s)
                    ON DUPLICATE KEY UPDATE 主客类型=VALUES(主客类型)
                """, record)
                tg_count += 1
            except Exception as e:
                pass  # 忽略重复记录
        
        print(f"✓ 成功导入 {tg_count} 条球队-比赛关系")
        return count


def import_player_games(cursor, csv_path):
    """导入球员比赛数据"""
    print(f"\n正在导入球员比赛数据: {csv_path}")
    
    with open(csv_path, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        count = 0
        skipped = 0
        
        for row in reader:
            player_id = clean_int(row.get('player_id'))
            game_id_str = clean_value(row.get('game_id'))
            
            # 处理game_id，可能有前导零
            if game_id_str:
                game_id = int(game_id_str.lstrip('0') or '0')
            else:
                game_id = None
            
            minutes = clean_number(row.get('上场时间'), 0)
            points = clean_int(row.get('得分'), 0)
            rebounds = clean_int(row.get('篮板'), 0)
            assists = clean_int(row.get('助攻'), 0)
            steals = clean_int(row.get('抢断'), 0)
            blocks = clean_int(row.get('盖帽'), 0)
            turnovers = clean_int(row.get('失误'), 0)
            fouls = clean_int(row.get('犯规'), 0)
            plus_minus = clean_int(row.get('正负值'))
            
            if player_id and game_id:
                try:
                    cursor.execute("""
                        INSERT INTO Player_Game (player_id, game_id, 上场时间, 得分, 篮板, 助攻, 抢断, 盖帽, 失误, 犯规, 正负值)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        ON DUPLICATE KEY UPDATE 
                            上场时间=VALUES(上场时间), 得分=VALUES(得分), 篮板=VALUES(篮板),
                            助攻=VALUES(助攻), 抢断=VALUES(抢断), 盖帽=VALUES(盖帽),
                            失误=VALUES(失误), 犯规=VALUES(犯规), 正负值=VALUES(正负值)
                    """, (player_id, game_id, minutes, points, rebounds, assists, steals, blocks, turnovers, fouls, plus_minus))
                    count += 1
                except Exception as e:
                    skipped += 1
                    # 可能是外键约束失败（球员或比赛不存在）
                    pass
        
        print(f"✓ 成功导入 {count} 条球员比赛数据")
        if skipped > 0:
            print(f"  (跳过 {skipped} 条无效记录)")
        return count


def clear_tables(cursor):
    """清空相关表数据（按外键依赖顺序）"""
    print("\n正在清空现有数据...")
    
    # 禁用外键检查以便删除
    cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
    
    tables_to_clear = [
        'Player_Game',
        'Team_Game', 
        'Game',
        'Player',
        'Team'
    ]
    
    for table in tables_to_clear:
        try:
            cursor.execute(f"DELETE FROM {table}")
            print(f"  ✓ 已清空表: {table}")
        except Exception as e:
            print(f"  ✗ 清空表 {table} 失败: {e}")
    
    # 重新启用外键检查
    cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
    print("✓ 数据清空完成")


def main():
    """主函数"""
    print("=" * 60)
    print("NBA数据库CSV数据导入工具")
    print("=" * 60)
    
    # 获取项目根目录
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # CSV文件路径
    csv_files = {
        'team': os.path.join(base_dir, '1_Team.csv'),
        'player': os.path.join(base_dir, '2_Player.csv'),
        'game': os.path.join(base_dir, '3_Game.csv'),
        'player_game': os.path.join(base_dir, '4_Player_Game.csv')
    }
    
    # 检查文件是否存在
    for name, path in csv_files.items():
        if not os.path.exists(path):
            print(f"错误: 找不到文件 {path}")
            return
    
    print("\n所有CSV文件已找到，准备连接数据库...")
    
    # 连接数据库
    db_config = DatabaseConfig()
    conn = db_config.get_connection()
    
    if not conn:
        print("错误: 无法连接到数据库")
        return
    
    try:
        cursor = conn.cursor()
        
        # 清空现有数据
        clear_tables(cursor)
        conn.commit()
        
        # 按顺序导入数据（先导入没有外键依赖的表）
        # 1. 导入球队
        import_teams(cursor, csv_files['team'])
        conn.commit()
        
        # 2. 导入球员
        import_players(cursor, csv_files['player'])
        conn.commit()
        
        # 3. 导入比赛（包含Team_Game关系）
        import_games(cursor, csv_files['game'])
        conn.commit()
        
        # 4. 导入球员比赛数据
        import_player_games(cursor, csv_files['player_game'])
        conn.commit()
        
        print("\n" + "=" * 60)
        print("✓ 所有数据导入完成！")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n错误: {e}")
        conn.rollback()
        raise
    finally:
        cursor.close()
        conn.close()


if __name__ == '__main__':
    main()

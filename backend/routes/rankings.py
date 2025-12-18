"""数据榜单路由"""
from flask import Blueprint, request, jsonify
from database.config import DatabaseConfig


rankings_bp = Blueprint('rankings', __name__)
db_config = DatabaseConfig()


@rankings_bp.route('/teams', methods=['GET'])
def get_team_standings():
    """
    获取球队战绩榜单
    返回东西部球队按胜率排序的榜单
    """
    conn = db_config.get_connection()
    if not conn:
        return jsonify({'error': '数据库连接失败'}), 500
    
    try:
        with conn.cursor() as cursor:
            # 查询每支球队的胜负场次
            cursor.execute("""
                SELECT 
                    t.team_id,
                    t.名称 as name,
                    t.城市 as city,
                    t.分区 as conference,
                    COUNT(CASE WHEN g.获胜球队ID = t.team_id THEN 1 END) as wins,
                    COUNT(CASE WHEN g.状态 = '已结束' AND g.获胜球队ID != t.team_id 
                               AND (g.主队ID = t.team_id OR g.客队ID = t.team_id) THEN 1 END) as losses,
                    COUNT(CASE WHEN g.状态 = '已结束' 
                               AND (g.主队ID = t.team_id OR g.客队ID = t.team_id) THEN 1 END) as games_played
                FROM Team t
                LEFT JOIN Game g ON (g.主队ID = t.team_id OR g.客队ID = t.team_id) AND g.状态 = '已结束'
                GROUP BY t.team_id, t.名称, t.城市, t.分区
                ORDER BY t.分区, 
                    CASE WHEN COUNT(CASE WHEN g.状态 = '已结束' 
                                        AND (g.主队ID = t.team_id OR g.客队ID = t.team_id) THEN 1 END) > 0 
                         THEN COUNT(CASE WHEN g.获胜球队ID = t.team_id THEN 1 END) * 1.0 / 
                              COUNT(CASE WHEN g.状态 = '已结束' 
                                        AND (g.主队ID = t.team_id OR g.客队ID = t.team_id) THEN 1 END)
                         ELSE 0 END DESC
            """)
            
            east_teams = []
            west_teams = []
            
            for row in cursor.fetchall():
                games_played = row[6] or 0
                wins = row[4] or 0
                losses = row[5] or 0
                win_rate = round(wins / games_played * 100, 1) if games_played > 0 else 0
                
                team_data = {
                    'team_id': row[0],
                    'name': row[1],
                    'city': row[2],
                    'conference': row[3],
                    'wins': wins,
                    'losses': losses,
                    'games_played': games_played,
                    'win_rate': win_rate
                }
                
                if row[3] == '东部':
                    east_teams.append(team_data)
                else:
                    west_teams.append(team_data)
            
            # 按胜率排序并添加排名
            east_teams.sort(key=lambda x: x['win_rate'], reverse=True)
            west_teams.sort(key=lambda x: x['win_rate'], reverse=True)
            
            for i, team in enumerate(east_teams, 1):
                team['rank'] = i
            for i, team in enumerate(west_teams, 1):
                team['rank'] = i
            
            return jsonify({
                'east': east_teams,
                'west': west_teams
            }), 200
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()


@rankings_bp.route('/players', methods=['GET'])
def get_player_stats_rankings():
    """
    获取球员数据榜单
    支持按不同数据类型排序：得分、篮板、助攻、抢断、盖帽
    """
    stat_type = request.args.get('stat', 'points')  # 默认得分榜
    limit = request.args.get('limit', 10, type=int)  # 默认前10
    
    # 映射统计类型到数据库字段
    stat_mapping = {
        'points': '得分',
        'rebounds': '篮板',
        'assists': '助攻',
        'steals': '抢断',
        'blocks': '盖帽',
        'minutes': '上场时间'
    }
    
    if stat_type not in stat_mapping:
        return jsonify({'error': '无效的统计类型'}), 400
    
    stat_field = stat_mapping[stat_type]
    
    conn = db_config.get_connection()
    if not conn:
        return jsonify({'error': '数据库连接失败'}), 500
    
    try:
        with conn.cursor() as cursor:
            # 查询球员场均数据
            cursor.execute(f"""
                SELECT 
                    p.player_id,
                    p.姓名 as name,
                    p.位置 as position,
                    t.名称 as team_name,
                    COUNT(pg.game_id) as games_played,
                    ROUND(AVG(COALESCE(pg.得分, 0)), 1) as avg_points,
                    ROUND(AVG(COALESCE(pg.篮板, 0)), 1) as avg_rebounds,
                    ROUND(AVG(COALESCE(pg.助攻, 0)), 1) as avg_assists,
                    ROUND(AVG(COALESCE(pg.抢断, 0)), 1) as avg_steals,
                    ROUND(AVG(COALESCE(pg.盖帽, 0)), 1) as avg_blocks,
                    ROUND(AVG(COALESCE(pg.上场时间, 0)), 1) as avg_minutes
                FROM Player p
                LEFT JOIN Player_Game pg ON p.player_id = pg.player_id
                LEFT JOIN Team t ON p.当前球队ID = t.team_id
                GROUP BY p.player_id, p.姓名, p.位置, t.名称
                ORDER BY AVG(COALESCE(pg.{stat_field}, 0)) DESC, p.player_id
                LIMIT %s
            """, (limit,))
            
            players = []
            for i, row in enumerate(cursor.fetchall(), 1):
                players.append({
                    'rank': i,
                    'player_id': row[0],
                    'name': row[1],
                    'position': row[2],
                    'team_name': row[3] or '自由球员',
                    'games_played': row[4],
                    'avg_points': float(row[5] or 0),
                    'avg_rebounds': float(row[6] or 0),
                    'avg_assists': float(row[7] or 0),
                    'avg_steals': float(row[8] or 0),
                    'avg_blocks': float(row[9] or 0),
                    'avg_minutes': float(row[10] or 0)
                })
            
            return jsonify({
                'stat_type': stat_type,
                'players': players
            }), 200
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()


@rankings_bp.route('/players/leaders', methods=['GET'])
def get_stat_leaders():
    """
    获取各项数据的领跑者（综合榜单）
    返回得分王、篮板王、助攻王等
    """
    conn = db_config.get_connection()
    if not conn:
        return jsonify({'error': '数据库连接失败'}), 500
    
    try:
        with conn.cursor() as cursor:
            leaders = {}
            
            # 各项数据的领跑者
            stats = [
                ('points', '得分', '得分王'),
                ('rebounds', '篮板', '篮板王'),
                ('assists', '助攻', '助攻王'),
                ('steals', '抢断', '抢断王'),
                ('blocks', '盖帽', '盖帽王')
            ]
            
            for stat_key, stat_field, stat_title in stats:
                cursor.execute(f"""
                    SELECT 
                        p.player_id,
                        p.姓名 as name,
                        p.位置 as position,
                        t.名称 as team_name,
                        COUNT(pg.game_id) as games_played,
                        ROUND(AVG(COALESCE(pg.{stat_field}, 0)), 1) as avg_stat
                    FROM Player p
                    LEFT JOIN Player_Game pg ON p.player_id = pg.player_id
                    LEFT JOIN Team t ON p.当前球队ID = t.team_id
                    GROUP BY p.player_id, p.姓名, p.位置, t.名称
                    ORDER BY AVG(COALESCE(pg.{stat_field}, 0)) DESC, p.player_id
                    LIMIT 1
                """)
                
                row = cursor.fetchone()
                if row:
                    leaders[stat_key] = {
                        'title': stat_title,
                        'player_id': row[0],
                        'name': row[1],
                        'position': row[2],
                        'team_name': row[3] or '自由球员',
                        'games_played': row[4],
                        'avg_value': float(row[5]) if row[5] else 0
                    }
            
            return jsonify(leaders), 200
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

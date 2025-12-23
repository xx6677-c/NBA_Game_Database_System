"""数据榜单路由"""
from flask import Blueprint, request, jsonify
from database.core.config import DatabaseConfig


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
            # 先获取球队logo映射 (从Team_Logo表)
            cursor.execute("""
                SELECT team_id, image_id FROM Team_Logo
            """)
            logo_map = {row[0]: row[1] for row in cursor.fetchall()}
            
            # 查询每支球队的胜负场次
            cursor.callproc('sp_get_team_standings', (None,))
            
            east_teams = []
            west_teams = []
            
            for row in cursor.fetchall():
                games_played = row[6] or 0
                wins = row[4] or 0
                losses = row[5] or 0
                win_rate = round(wins / games_played * 100, 1) if games_played > 0 else 0
                team_id = row[0]
                logo_id = logo_map.get(team_id)
                
                team_data = {
                    'team_id': team_id,
                    'name': row[1],
                    'city': row[2],
                    'conference': row[3],
                    'wins': wins,
                    'losses': losses,
                    'games_played': games_played,
                    'win_rate': win_rate,
                    'logo_url': f'/api/images/{logo_id}' if logo_id else None
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
            cursor.callproc('sp_get_player_rankings', (stat_field, limit))
            
            players_data = []
            player_ids = []
            for i, row in enumerate(cursor.fetchall(), 1):
                player_id = row[0]
                player_ids.append(player_id)
                players_data.append({
                    'rank': i,
                    'player_id': player_id,
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
            
            # 清空结果集
            while cursor.nextset():
                pass
            
            # 获取球员照片映射
            if player_ids:
                placeholders = ','.join(['%s'] * len(player_ids))
                cursor.execute(f"""
                    SELECT player_id, image_id FROM Player_Image WHERE player_id IN ({placeholders})
                """, tuple(player_ids))
                photo_map = {row[0]: row[1] for row in cursor.fetchall()}
            else:
                photo_map = {}
            
            # 添加照片URL
            for player in players_data:
                photo_id = photo_map.get(player['player_id'])
                player['photo_url'] = f'/api/images/{photo_id}' if photo_id else None
            
            return jsonify({
                'stat_type': stat_type,
                'players': players_data
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
                ('points', '得分', '得分王', 5),
                ('rebounds', '篮板', '篮板王', 6),
                ('assists', '助攻', '助攻王', 7),
                ('steals', '抢断', '抢断王', 8),
                ('blocks', '盖帽', '盖帽王', 9)
            ]
            
            for stat_key, stat_field, stat_title, index in stats:
                cursor.callproc('sp_get_player_rankings', (stat_field, 1))
                
                row = cursor.fetchone()
                # 清空剩余结果集
                cursor.nextset()
                
                if row:
                    leaders[stat_key] = {
                        'title': stat_title,
                        'player_id': row[0],
                        'name': row[1],
                        'position': row[2],
                        'team_name': row[3] or '自由球员',
                        'games_played': row[4],
                        'avg_value': float(row[index]) if row[index] else 0
                    }
            
            return jsonify(leaders), 200
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

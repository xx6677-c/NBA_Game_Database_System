"""比赛管理路由"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

from database.config import DatabaseConfig
from utils.permissions import check_admin_permission


games_bp = Blueprint('games', __name__)
db_config = DatabaseConfig()


@games_bp.route('', methods=['GET'])
def get_games():
    """获取比赛列表"""
    date_from = request.args.get('date_from')
    date_to = request.args.get('date_to')
    team_id = request.args.get('team_id')
    
    conn = db_config.get_connection()
    if not conn:
        return jsonify({'error': '数据库连接失败'}), 500
    
    try:
        with conn.cursor() as cursor:
            query = """
                SELECT g.game_id, g.赛季, g.日期, g.状态, g.主队得分, g.客队得分,
                       ht.名称 as home_team, at.名称 as away_team,
                       wt.名称 as winner_team, g.场馆,
                       htl.image_id as home_logo_id, atl.image_id as away_logo_id,
                       g.主队ID, g.客队ID
                FROM Game g
                JOIN Team ht ON g.主队ID = ht.team_id
                JOIN Team at ON g.客队ID = at.team_id
                LEFT JOIN Team wt ON g.获胜球队ID = wt.team_id
                LEFT JOIN Team_Logo htl ON ht.team_id = htl.team_id
                LEFT JOIN Team_Logo atl ON at.team_id = atl.team_id
            """
            
            params = []
            conditions = []
            
            if date_from:
                conditions.append("g.日期 >= %s")
                params.append(date_from)
            if date_to:
                conditions.append("g.日期 <= %s")
                params.append(date_to)
            if team_id:
                conditions.append("(g.主队ID = %s OR g.客队ID = %s)")
                params.extend([team_id, team_id])
            
            if conditions:
                query += " WHERE " + " AND ".join(conditions)
            
            query += " ORDER BY g.日期 DESC"
            
            cursor.execute(query, params)
            
            games = []
            for row in cursor.fetchall():
                games.append({
                    'game_id': row[0],
                    'season': row[1],
                    'date': row[2].strftime('%Y-%m-%d %H:%M'),
                    'status': row[3],
                    'home_score': row[4],
                    'away_score': row[5],
                    'home_team': row[6],
                    'away_team': row[7],
                    'winner_team': row[8],
                    'venue': row[9],
                    'home_logo_url': f'/api/images/{row[10]}' if row[10] else None,
                    'away_logo_url': f'/api/images/{row[11]}' if row[11] else None,
                    'home_team_id': row[12],
                    'away_team_id': row[13]
                })
            
            return jsonify(games), 200
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()


@games_bp.route('/<int:game_id>', methods=['GET'])
def get_game_detail(game_id):
    """获取比赛详情"""
    conn = db_config.get_connection()
    if not conn:
        return jsonify({'error': '数据库连接失败'}), 500
    
    try:
        with conn.cursor() as cursor:
            # 获取比赛基本信息
            cursor.execute("""
                SELECT g.game_id, g.赛季, g.日期, g.状态, g.主队得分, g.客队得分,
                       g.主队ID, g.客队ID,
                       ht.名称 as home_team, at.名称 as away_team,
                       wt.名称 as winner_team, g.场馆
                FROM Game g
                JOIN Team ht ON g.主队ID = ht.team_id
                JOIN Team at ON g.客队ID = at.team_id
                LEFT JOIN Team wt ON g.获胜球队ID = wt.team_id
                WHERE g.game_id = %s
            """, (game_id,))
            
            game = cursor.fetchone()
            if not game:
                return jsonify({'error': '比赛不存在'}), 404
            
            game_data = {
                'game_id': game[0],
                'season': game[1],
                'date': game[2].strftime('%Y-%m-%d %H:%M'),
                'status': game[3],
                'home_score': game[4],
                'away_score': game[5],
                'home_team_id': game[6],
                'away_team_id': game[7],
                'home_team': game[8],
                'away_team': game[9],
                'winner_team': game[10],
                'venue': game[11]
            }
            
            # 如果比赛已结束，获取球员比赛数据
            if game[3] == '已结束':
                cursor.execute("""
                    SELECT pg.player_id, pg.上场时间, pg.得分, pg.篮板, pg.助攻, 
                           pg.抢断, pg.盖帽, pg.失误, pg.犯规, pg.正负值,
                           p.姓名, p.位置, p.球衣号, t.名称 as team_name, t.team_id
                    FROM Player_Game pg
                    JOIN Player p ON pg.player_id = p.player_id
                    JOIN Team t ON p.当前球队ID = t.team_id
                    WHERE pg.game_id = %s
                    ORDER BY t.名称, p.球衣号
                """, (game_id,))
                
                player_stats = []
                for row in cursor.fetchall():
                    player_stats.append({
                        'player_id': row[0],
                        'playing_time': float(row[1]) if row[1] else 0,
                        'points': row[2],
                        'rebounds': row[3],
                        'assists': row[4],
                        'steals': row[5],
                        'blocks': row[6],
                        'turnovers': row[7],
                        'fouls': row[8],
                        'plus_minus': row[9],
                        'player_name': row[10],
                        'position': row[11],
                        'jersey_number': row[12],
                        'team_name': row[13],
                        'team_id': row[14]
                    })
                
                game_data['player_stats'] = player_stats
            
            return jsonify(game_data), 200
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()


@games_bp.route('/<int:game_id>/ratings', methods=['GET'])
@jwt_required(optional=True)
def get_game_ratings(game_id):
    """获取比赛球员评分"""
    current_user_id = get_jwt_identity()
    
    conn = db_config.get_connection()
    if not conn:
        return jsonify({'error': '数据库连接失败'}), 500
    
    try:
        with conn.cursor() as cursor:
            # 获取所有参与比赛的球员及其平均评分
            query = """
                SELECT p.player_id, p.姓名, p.当前球队ID, t.名称 as team_name,
                       AVG(r.分数) as avg_rating, COUNT(r.user_id) as rating_count,
                       pi.image_id
                FROM Player_Game pg
                JOIN Player p ON pg.player_id = p.player_id
                JOIN Team t ON p.当前球队ID = t.team_id
                LEFT JOIN Rating r ON p.player_id = r.player_id AND r.game_id = pg.game_id
                LEFT JOIN Player_Image pi ON p.player_id = pi.player_id
                WHERE pg.game_id = %s
                GROUP BY p.player_id
                ORDER BY t.team_id, p.球衣号
            """
            cursor.execute(query, (game_id,))
            
            players = []
            for row in cursor.fetchall():
                player_data = {
                    'player_id': row[0],
                    'name': row[1],
                    'team_id': row[2],
                    'team_name': row[3],
                    'avg_rating': float(row[4]) if row[4] else 0,
                    'rating_count': row[5],
                    'photo_url': f'/api/images/{row[6]}' if row[6] else None,
                    'user_rating': None
                }
                
                # 如果用户已登录，获取用户的评分
                if current_user_id:
                    cursor.execute("""
                        SELECT 分数 FROM Rating 
                        WHERE user_id = %s AND player_id = %s AND game_id = %s
                    """, (current_user_id, row[0], game_id))
                    user_rating = cursor.fetchone()
                    if user_rating:
                        player_data['user_rating'] = float(user_rating[0])
                
                players.append(player_data)
            
            return jsonify(players), 200
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()


@games_bp.route('/<int:game_id>/ratings', methods=['POST'])
@jwt_required()
def submit_rating(game_id):
    """提交球员评分"""
    current_user_id = get_jwt_identity()
    data = request.get_json()
    player_id = data.get('player_id')
    rating = data.get('rating')
    
    if not player_id or rating is None:
        return jsonify({'error': '缺少必要参数'}), 400
        
    if not (0 <= float(rating) <= 10):
        return jsonify({'error': '评分必须在0-10之间'}), 400
        
    conn = db_config.get_connection()
    if not conn:
        return jsonify({'error': '数据库连接失败'}), 500
        
    try:
        with conn.cursor() as cursor:
            # 检查是否已经评分
            cursor.execute("""
                INSERT INTO Rating (user_id, player_id, game_id, 分数)
                VALUES (%s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE 分数 = %s, 创建时间 = CURRENT_TIMESTAMP
            """, (current_user_id, player_id, game_id, rating, rating))
            
            conn.commit()
            return jsonify({'message': '评分成功'}), 200
            
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()


@games_bp.route('/<int:game_id>/players/<int:player_id>', methods=['GET'])
@jwt_required(optional=True)
def get_player_game_detail(game_id, player_id):
    """获取球员单场比赛详情（数据+评论）"""
    current_user_id = get_jwt_identity()
    
    conn = db_config.get_connection()
    if not conn:
        return jsonify({'error': '数据库连接失败'}), 500
        
    try:
        with conn.cursor() as cursor:
            # 1. 获取球员本场数据
            cursor.execute("""
                SELECT pg.上场时间, pg.得分, pg.篮板, pg.助攻, 
                       pg.抢断, pg.盖帽, pg.失误, pg.犯规, pg.正负值,
                       p.姓名, p.位置, p.球衣号, t.名称 as team_name, t.team_id
                FROM Player_Game pg
                JOIN Player p ON pg.player_id = p.player_id
                JOIN Team t ON p.当前球队ID = t.team_id
                WHERE pg.game_id = %s AND pg.player_id = %s
            """, (game_id, player_id))
            
            stats_row = cursor.fetchone()
            if not stats_row:
                return jsonify({'error': '未找到该球员本场数据'}), 404
                
            stats = {
                'playing_time': float(stats_row[0]) if stats_row[0] else 0,
                'points': stats_row[1],
                'rebounds': stats_row[2],
                'assists': stats_row[3],
                'steals': stats_row[4],
                'blocks': stats_row[5],
                'turnovers': stats_row[6],
                'fouls': stats_row[7],
                'plus_minus': stats_row[8],
                'player_name': stats_row[9],
                'position': stats_row[10],
                'jersey_number': stats_row[11],
                'team_name': stats_row[12],
                'team_id': stats_row[13]
            }
            
            # 2. 获取评分信息
            cursor.execute("""
                SELECT AVG(分数), COUNT(*) FROM Rating
                WHERE game_id = %s AND player_id = %s
            """, (game_id, player_id))
            rating_row = cursor.fetchone()
            stats['avg_rating'] = float(rating_row[0]) if rating_row[0] else 0
            stats['rating_count'] = rating_row[1]
            
            if current_user_id:
                cursor.execute("""
                    SELECT 分数 FROM Rating
                    WHERE user_id = %s AND game_id = %s AND player_id = %s
                """, (current_user_id, game_id, player_id))
                user_rating = cursor.fetchone()
                stats['user_rating'] = float(user_rating[0]) if user_rating else None
            
            # 3. 获取评论
            cursor.execute("""
                SELECT c.comment_id, c.内容, c.创建时间, u.用户名, u.user_id
                FROM Comment c
                JOIN User u ON c.user_id = u.user_id
                WHERE c.game_id = %s AND c.player_id = %s
                ORDER BY c.创建时间 DESC
            """, (game_id, player_id))
            
            comments = []
            for row in cursor.fetchall():
                comments.append({
                    'comment_id': row[0],
                    'content': row[1],
                    'created_at': row[2].strftime('%Y-%m-%d %H:%M'),
                    'username': row[3],
                    'user_id': row[4]
                })
                
            return jsonify({
                'stats': stats,
                'comments': comments
            }), 200
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()


@games_bp.route('/<int:game_id>/players/<int:player_id>/comments', methods=['POST'])
@jwt_required()
def submit_player_comment(game_id, player_id):
    """提交球员评论"""
    current_user_id = get_jwt_identity()
    data = request.get_json()
    content = data.get('content')
    
    if not content:
        return jsonify({'error': '评论内容不能为空'}), 400
        
    conn = db_config.get_connection()
    if not conn:
        return jsonify({'error': '数据库连接失败'}), 500
        
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO Comment (user_id, player_id, game_id, 内容)
                VALUES (%s, %s, %s, %s)
            """, (current_user_id, player_id, game_id, content))
            
            conn.commit()
            return jsonify({'message': '评论成功'}), 200
            
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()


@games_bp.route('', methods=['POST'])
@jwt_required()
def create_game():
    """创建比赛（仅管理员）"""
    current_user_id = get_jwt_identity()
    
    if not check_admin_permission(current_user_id):
        return jsonify({'error': '权限不足，仅管理员可创建比赛'}), 403
    
    data = request.get_json()
    season = data.get('season')
    date = data.get('date')
    home_team_id = data.get('home_team_id')
    away_team_id = data.get('away_team_id')
    status = data.get('status', '未开始')
    home_score = data.get('home_score')
    away_score = data.get('away_score')
    venue = data.get('venue')
    player_data = data.get('player_data', [])
    
    if not all([season, date, home_team_id, away_team_id]):
        return jsonify({'error': '赛季、日期、主队和客队ID是必填字段'}), 400
    
    if home_team_id == away_team_id:
        return jsonify({'error': '主队和客队不能相同'}), 400
    
    if status == '已结束':
        if home_score is None or away_score is None:
            return jsonify({'error': '已结束的比赛必须提供比分'}), 400
        if not player_data:
            return jsonify({'error': '已结束的比赛必须提供球员比赛数据'}), 400
    
    conn = db_config.get_connection()
    if not conn:
        return jsonify({'error': '数据库连接失败'}), 500
    
    try:
        with conn.cursor() as cursor:
            conn.autocommit = False
            
            winner_team_id = None
            if status == '已结束':
                if home_score > away_score:
                    winner_team_id = home_team_id
                elif away_score > home_score:
                    winner_team_id = away_team_id
            
            cursor.execute("""
                INSERT INTO Game (赛季, 日期, 主队ID, 客队ID, 主队得分, 客队得分, 状态, 获胜球队ID, 场馆)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (season, date, home_team_id, away_team_id, home_score, away_score, status, winner_team_id, venue))
            
            game_id = cursor.lastrowid
            
            cursor.execute("INSERT INTO Team_Game (team_id, game_id, 主客类型) VALUES (%s, %s, '主场')", (home_team_id, game_id))
            cursor.execute("INSERT INTO Team_Game (team_id, game_id, 主客类型) VALUES (%s, %s, '客场')", (away_team_id, game_id))
            
            if status == '已结束' and player_data:
                for player_stat in player_data:
                    player_id = player_stat.get('player_id')
                    if not player_id:
                        continue
                    
                    cursor.execute("""
                        INSERT INTO Player_Game (player_id, game_id, 上场时间, 得分, 篮板, 助攻, 抢断, 盖帽, 失误, 犯规, 正负值)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """, (
                        player_id, game_id,
                        player_stat.get('上场时间', 0),
                        player_stat.get('得分', 0),
                        player_stat.get('篮板', 0),
                        player_stat.get('助攻', 0),
                        player_stat.get('抢断', 0),
                        player_stat.get('盖帽', 0),
                        player_stat.get('失误', 0),
                        player_stat.get('犯规', 0),
                        player_stat.get('正负值')
                    ))
            
            # 记录管理员操作
            try:
                cursor.execute("""
                    INSERT INTO Admin_Insert (user_id, game_id) 
                    VALUES (%s, %s)
                    ON DUPLICATE KEY UPDATE user_id = VALUES(user_id), 操作时间 = CURRENT_TIMESTAMP
                """, (int(current_user_id), game_id))
            except Exception as e:
                print(f"Warning: Failed to log admin insert in create_game: {e}")
            
            conn.commit()
            return jsonify({'message': '比赛创建成功', 'game_id': game_id}), 201
            
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()


@games_bp.route('/<int:game_id>', methods=['PUT'])
@jwt_required()
def update_game(game_id):
    """更新比赛（仅管理员）"""
    current_user_id = get_jwt_identity()
    
    if not check_admin_permission(current_user_id):
        return jsonify({'error': '权限不足，仅管理员可更新比赛'}), 403
    
    data = request.get_json()
    season = data.get('season')
    date = data.get('date')
    home_team_id = data.get('home_team_id')
    away_team_id = data.get('away_team_id')
    status = data.get('status')
    home_score = data.get('home_score')
    away_score = data.get('away_score')
    venue = data.get('venue')
    player_data = data.get('player_data')
    
    conn = db_config.get_connection()
    if not conn:
        return jsonify({'error': '数据库连接失败'}), 500
    
    try:
        with conn.cursor() as cursor:
            conn.autocommit = False
            
            cursor.execute("SELECT game_id, 状态 FROM Game WHERE game_id = %s", (game_id,))
            existing_game = cursor.fetchone()
            if not existing_game:
                return jsonify({'error': '比赛不存在'}), 404
            
            if status == '已结束':
                if home_score is None or away_score is None:
                    return jsonify({'error': '已结束的比赛必须提供比分'}), 400
                if not player_data:
                    return jsonify({'error': '已结束的比赛必须提供球员比赛数据'}), 400
            
            winner_team_id = None
            if status == '已结束':
                if home_score > away_score:
                    winner_team_id = home_team_id
                elif away_score > home_score:
                    winner_team_id = away_team_id
            
            update_fields = []
            update_values = []
            
            if season is not None:
                update_fields.append("赛季 = %s")
                update_values.append(season)
            if date is not None:
                update_fields.append("日期 = %s")
                update_values.append(date)
            if home_team_id is not None:
                update_fields.append("主队ID = %s")
                update_values.append(home_team_id)
            if away_team_id is not None:
                update_fields.append("客队ID = %s")
                update_values.append(away_team_id)
            if status is not None:
                update_fields.append("状态 = %s")
                update_values.append(status)
            if home_score is not None:
                update_fields.append("主队得分 = %s")
                update_values.append(home_score)
            if away_score is not None:
                update_fields.append("客队得分 = %s")
                update_values.append(away_score)
            if venue is not None:
                update_fields.append("场馆 = %s")
                update_values.append(venue)
            if winner_team_id is not None:
                update_fields.append("获胜球队ID = %s")
                update_values.append(winner_team_id)
            
            if update_fields:
                update_values.append(game_id)
                cursor.execute(f"UPDATE Game SET {', '.join(update_fields)} WHERE game_id = %s", update_values)
            
            if home_team_id is not None:
                cursor.execute("UPDATE Team_Game SET team_id = %s WHERE game_id = %s AND 主客类型 = '主场'", (home_team_id, game_id))
            if away_team_id is not None:
                cursor.execute("UPDATE Team_Game SET team_id = %s WHERE game_id = %s AND 主客类型 = '客场'", (away_team_id, game_id))
            
            if status == '已结束' and player_data and existing_game[1] != '已结束':
                cursor.execute("DELETE FROM Player_Game WHERE game_id = %s", (game_id,))
                
                for player_stat in player_data:
                    player_id = player_stat.get('player_id')
                    if not player_id:
                        continue
                    
                    plus_minus = player_stat.get('正负值')
                    if plus_minus == '' or plus_minus is None:
                        plus_minus = None
                    
                    cursor.execute("""
                        INSERT INTO Player_Game (player_id, game_id, 上场时间, 得分, 篮板, 助攻, 抢断, 盖帽, 失误, 犯规, 正负值)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """, (
                        player_id, game_id,
                        float(player_stat.get('上场时间', 0)),
                        int(player_stat.get('得分', 0)),
                        int(player_stat.get('篮板', 0)),
                        int(player_stat.get('助攻', 0)),
                        int(player_stat.get('抢断', 0)),
                        int(player_stat.get('盖帽', 0)),
                        int(player_stat.get('失误', 0)),
                        int(player_stat.get('犯规', 0)),
                        plus_minus
                    ))
            
            # 记录管理员操作
            if status == '已结束' and existing_game[1] != '已结束':
                try:
                    cursor.execute("""
                        INSERT INTO Admin_Insert (user_id, game_id) 
                        VALUES (%s, %s)
                        ON DUPLICATE KEY UPDATE user_id = VALUES(user_id), 操作时间 = CURRENT_TIMESTAMP
                    """, (int(current_user_id), game_id))
                except Exception as e:
                    print(f"Warning: Failed to log admin insert in update_game: {e}")
            
            conn.commit()
            return jsonify({'message': '比赛更新成功'}), 200
            
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()


@games_bp.route('/<int:game_id>', methods=['DELETE'])
@jwt_required()
def delete_game(game_id):
    """删除比赛（仅管理员）"""
    current_user_id = get_jwt_identity()
    
    if not check_admin_permission(current_user_id):
        return jsonify({'error': '权限不足，仅管理员可删除比赛'}), 403
    
    conn = db_config.get_connection()
    if not conn:
        return jsonify({'error': '数据库连接失败'}), 500
    
    try:
        with conn.cursor() as cursor:
            conn.autocommit = False
            
            cursor.execute("SELECT game_id FROM Game WHERE game_id = %s", (game_id,))
            if not cursor.fetchone():
                return jsonify({'error': '比赛不存在'}), 404
            
            cursor.execute("DELETE FROM Rating WHERE game_id = %s", (game_id,))
            cursor.execute("DELETE FROM Player_Game WHERE game_id = %s", (game_id,))
            cursor.execute("DELETE FROM Team_Game WHERE game_id = %s", (game_id,))
            cursor.execute("DELETE FROM Admin_Insert WHERE game_id = %s", (game_id,))
            cursor.execute("DELETE FROM Post WHERE game_id = %s", (game_id,))
            cursor.execute("DELETE FROM Comment WHERE game_id = %s", (game_id,))
            cursor.execute("DELETE FROM Game WHERE game_id = %s", (game_id,))
            
            conn.commit()
            return jsonify({'message': '比赛删除成功'}), 200
            
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

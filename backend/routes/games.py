"""比赛管理路由"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

from database.core.config import DatabaseConfig
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
            cursor.callproc('sp_get_games', (date_from, date_to, team_id))
            
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


@games_bp.route('/<int:game_id>/claim', methods=['POST'])
@jwt_required()
def claim_reward(game_id):
    """领取竞猜奖励"""
    current_user_id = get_jwt_identity()
    
    conn = db_config.get_connection()
    if not conn:
        return jsonify({'error': '数据库连接失败'}), 500
        
    try:
        with conn.cursor() as cursor:
            # 1. 检查比赛状态和竞猜结果
            cursor.callproc('sp_check_prediction_status', (game_id, current_user_id))
            
            result = cursor.fetchone()
            
            if not result:
                return jsonify({'error': '未找到竞猜记录'}), 404
                
            status, winner_id, predicted_id, is_claimed = result
            
            if status != '已结束':
                return jsonify({'error': '比赛尚未结束'}), 400
                
            if winner_id != predicted_id:
                return jsonify({'error': '竞猜失败，无法领取奖励'}), 400
                
            if is_claimed:
                return jsonify({'error': '奖励已领取'}), 400
                
            # 2. 发放奖励 (更新用户积分和领取状态)
            # 奖励 100 积分
            reward_points = 100
            
            cursor.callproc('sp_claim_reward', (game_id, current_user_id, reward_points))
            
            conn.commit()
            
            return jsonify({'message': f'恭喜！成功领取 {reward_points} 积分', 'points': reward_points}), 200
            
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()


@games_bp.route('/<int:game_id>/predict', methods=['POST'])
@jwt_required()
def predict_game(game_id):
    """比赛竞猜投票"""
    current_user_id = get_jwt_identity()
    data = request.get_json()
    team_id = data.get('team_id')
    
    if not team_id:
        return jsonify({'error': '请选择支持的球队'}), 400
        
    conn = db_config.get_connection()
    if not conn:
        return jsonify({'error': '数据库连接失败'}), 500
        
    try:
        with conn.cursor() as cursor:
            # 1. 检查比赛状态
            cursor.callproc('sp_check_game_status', (game_id,))
            game = cursor.fetchone()
            
            if not game:
                return jsonify({'error': '比赛不存在'}), 404
                
            if game[0] != '未开始':
                return jsonify({'error': '比赛已开始或已结束，无法投票'}), 400
                
            # 2. 插入或更新投票
            cursor.callproc('sp_predict_game', (current_user_id, game_id, team_id))
            
            conn.commit()
            return jsonify({'message': '投票成功'}), 200
            
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()


@games_bp.route('/<int:game_id>', methods=['GET'])
@jwt_required(optional=True)
def get_game_detail(game_id):
    """获取比赛详情"""
    current_user_id = get_jwt_identity()
    conn = db_config.get_connection()
    if not conn:
        return jsonify({'error': '数据库连接失败'}), 500
    
    try:
        with conn.cursor() as cursor:
            # 获取比赛基本信息
            cursor.callproc('sp_get_game_detail', (game_id,))
            
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
                'venue': game[11],
                'winner_team_id': game[12]
            }

            # 获取竞猜数据
            # 1. 统计双方支持数
            cursor.callproc('sp_get_game_prediction_stats', (game_id,))
            
            predictions = cursor.fetchall()
            home_votes = 0
            away_votes = 0
            
            for team_id, count in predictions:
                if team_id == game_data['home_team_id']:
                    home_votes = count
                elif team_id == game_data['away_team_id']:
                    away_votes = count
            
            total_votes = home_votes + away_votes
            game_data['prediction'] = {
                'home_votes': home_votes,
                'away_votes': away_votes,
                'total_votes': total_votes,
                'home_percent': round(home_votes / total_votes * 100) if total_votes > 0 else 50,
                'away_percent': round(away_votes / total_votes * 100) if total_votes > 0 else 50
            }
            
            # 2. 获取当前用户投票状态
            if current_user_id:
                cursor.callproc('sp_get_user_prediction', (game_id, current_user_id))
                user_vote = cursor.fetchone()
                if user_vote:
                    game_data['user_prediction'] = user_vote[0]
                    game_data['is_claimed'] = bool(user_vote[1])
                else:
                    game_data['user_prediction'] = None
                    game_data['is_claimed'] = False
            
            # 如果比赛已结束，获取球员比赛数据
            if game[3] == '已结束':
                cursor.callproc('sp_get_game_player_stats', (game_id,))
                
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
            cursor.callproc('sp_get_game_players_with_ratings', (game_id,))
            
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
                    # 注意：这里在循环中调用存储过程可能效率不高，但为了保持逻辑一致性先这样做
                    # 更好的做法是一次性获取所有评分，或者在 sp_get_game_players_with_ratings 中传入 user_id
                    # 但目前的 sp_get_game_players_with_ratings 没有 user_id 参数
                    cursor.callproc('sp_get_user_player_rating', (current_user_id, row[0], game_id))
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
            cursor.callproc('sp_upsert_rating', (current_user_id, player_id, game_id, rating))
            
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
            cursor.callproc('sp_get_player_game_stats_single', (game_id, player_id))
            
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
            cursor.callproc('sp_get_player_rating_summary', (game_id, player_id))
            rating_row = cursor.fetchone()
            stats['avg_rating'] = float(rating_row[0]) if rating_row[0] else 0
            stats['rating_count'] = rating_row[1]
            
            if current_user_id:
                cursor.callproc('sp_get_user_player_rating', (current_user_id, player_id, game_id))
                user_rating = cursor.fetchone()
                stats['user_rating'] = float(user_rating[0]) if user_rating else None
            
            # 3. 获取评论
            cursor.callproc('sp_get_player_game_comments', (game_id, player_id))
            
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
            cursor.callproc('sp_create_player_comment', (current_user_id, game_id, player_id, content, datetime.now()))
            
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
    
    # 主队和客队不能相同 - 数据库触发器 trg_game_check_teams 会再次检查
    if home_team_id == away_team_id:
        return jsonify({'error': '主队和客队不能相同'}), 400
    
    if status == '已结束':
        if home_score is None or away_score is None:
            return jsonify({'error': '已结束的比赛必须提供比分'}), 400
        if int(home_score) == int(away_score):
            return jsonify({'error': '比赛结束时不能平局'}), 400
        if not player_data:
            return jsonify({'error': '已结束的比赛必须提供球员比赛数据'}), 400
    
    conn = db_config.get_connection()
    if not conn:
        return jsonify({'error': '数据库连接失败'}), 500
    
    try:
        with conn.cursor() as cursor:
            conn.autocommit = False
            
            # 获胜球队ID由触发器 trg_game_update_winner 自动计算
            # 调用存储过程创建比赛
            # sp_create_game 有9个参数，最后一个是OUT参数 p_game_id
            # 使用 execute 代替 callproc 以确保正确获取 OUT 参数
            cursor.execute("SET @p_game_id = 0")
            cursor.execute("""
                CALL sp_create_game(%s, %s, %s, %s, %s, %s, %s, %s, @p_game_id)
            """, (season, date, home_team_id, away_team_id, 
                  home_score, away_score, status, venue))
            
            cursor.execute("SELECT @p_game_id")
            result = cursor.fetchone()
            game_id = result[0]
            
            if status == '已结束' and player_data:
                for player_stat in player_data:
                    player_id = player_stat.get('player_id')
                    if not player_id:
                        continue
                    
                    cursor.callproc('sp_add_player_game_stat', (
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
            
            cursor.callproc('sp_check_game_status', (game_id,))
            existing_game = cursor.fetchone()
            if not existing_game:
                return jsonify({'error': '比赛不存在'}), 404
            
            if status == '已结束':
                if home_score is None or away_score is None:
                    return jsonify({'error': '已结束的比赛必须提供比分'}), 400
                if int(home_score) == int(away_score):
                    return jsonify({'error': '比赛结束时不能平局'}), 400
                if not player_data:
                    return jsonify({'error': '已结束的比赛必须提供球员比赛数据'}), 400
            
            # 获胜球队ID由触发器 trg_game_update_winner 自动计算
            
            cursor.callproc('sp_update_game', (
                game_id, season, date, home_team_id, away_team_id,
                status, home_score, away_score, venue
            ))
            
            if status == '已结束' and player_data:
                cursor.callproc('sp_delete_player_game_stats', (game_id,))
                
                for player_stat in player_data:
                    player_id = player_stat.get('player_id')
                    if not player_id:
                        continue
                    
                    plus_minus = player_stat.get('正负值')
                    if plus_minus == '' or plus_minus is None:
                        plus_minus = None
                    
                    cursor.callproc('sp_add_player_game_stat', (
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
            
            cursor.callproc('sp_check_game_status', (game_id,))
            if not cursor.fetchone():
                return jsonify({'error': '比赛不存在'}), 404
            
            cursor.callproc('sp_delete_game', (game_id,))
            
            conn.commit()
            return jsonify({'message': '比赛删除成功'}), 200
            
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

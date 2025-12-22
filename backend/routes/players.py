"""球员管理路由"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from database.core.config import DatabaseConfig
from utils.permissions import check_admin_permission


players_bp = Blueprint('players', __name__)
db_config = DatabaseConfig()


@players_bp.route('', methods=['GET'])
def get_players():
    """获取球员列表"""
    team_id = request.args.get('team_id')
    
    conn = db_config.get_connection()
    if not conn:
        return jsonify({'error': '数据库连接失败'}), 500
    
    try:
        with conn.cursor() as cursor:
            cursor.callproc('sp_get_players', (team_id,))
            
            players = []
            for row in cursor.fetchall():
                try:
                    players.append({
                        'player_id': row[0],
                        'name': row[1],
                        'position': row[2],
                        'jersey_number': row[3],
                        'height': row[4],
                        'weight': row[5],
                        'birth_date': row[6].strftime('%Y-%m-%d') if row[6] else None,
                        'nationality': row[7],
                        'current_team_id': row[8],
                        'team_name': row[9],
                        'contract_expiry': row[10].strftime('%Y-%m-%d') if row[10] else None,
                        'salary': float(row[11]) if row[11] else None,
                        'photo_url': f'/api/images/{row[12]}' if row[12] else None
                    })
                except Exception as e:
                    print(f"Error processing player row {row[0]}: {e}")
                    continue
            
            return jsonify(players), 200
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()


@players_bp.route('', methods=['POST'])
@jwt_required()
def create_player():
    """创建球员（仅管理员）"""
    current_user_id = get_jwt_identity()
    
    if not check_admin_permission(current_user_id):
        return jsonify({'error': '权限不足，仅管理员可创建球员'}), 403
    
    data = request.get_json()
    name = data.get('name')
    position = data.get('position')
    jersey_number = data.get('jersey_number')
    height = data.get('height')
    weight = data.get('weight')
    birth_date = data.get('birth_date')
    nationality = data.get('nationality')
    current_team_id = data.get('current_team_id')
    contract_expiry = data.get('contract_expiry')
    salary = data.get('salary')
    
    # 处理空字符串为None
    height = height if height != '' else None
    weight = weight if weight != '' else None
    birth_date = birth_date if birth_date != '' else None
    nationality = nationality if nationality != '' else None
    current_team_id = current_team_id if current_team_id != '' else None
    contract_expiry = contract_expiry if contract_expiry != '' else None
    salary = salary if salary != '' else None
    
    if not name or not position or jersey_number is None:
        return jsonify({'error': '姓名、位置和球衣号是必填字段'}), 400
    
    conn = db_config.get_connection()
    if not conn:
        return jsonify({'error': '数据库连接失败'}), 500
    
    try:
        with conn.cursor() as cursor:
            if current_team_id:
                cursor.execute("""
                    SELECT player_id FROM Player 
                    WHERE 球衣号 = %s AND 当前球队ID = %s
                """, (jersey_number, current_team_id))
                if cursor.fetchone():
                    return jsonify({'error': '该球队中已有球员使用此球衣号'}), 400
            
            # sp_create_player 有11个参数，最后一个是OUT参数 p_player_id
            args = cursor.callproc('sp_create_player', (
                name, position, jersey_number, height, weight, 
                birth_date, nationality, current_team_id, contract_expiry, salary, 0
            ))
            
            conn.commit()
            return jsonify({'message': '球员创建成功'}), 201
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()


@players_bp.route('/<int:player_id>', methods=['PUT'])
@jwt_required()
def update_player(player_id):
    """更新球员（仅管理员）"""
    current_user_id = get_jwt_identity()
    
    if not check_admin_permission(current_user_id):
        return jsonify({'error': '权限不足，仅管理员可更新球员'}), 403
    
    data = request.get_json()
    name = data.get('name')
    position = data.get('position')
    jersey_number = data.get('jersey_number')
    height = data.get('height')
    weight = data.get('weight')
    birth_date = data.get('birth_date')
    nationality = data.get('nationality')
    current_team_id = data.get('current_team_id')
    contract_expiry = data.get('contract_expiry')
    salary = data.get('salary')
    
    # 处理空字符串为None
    height = height if height != '' else None
    weight = weight if weight != '' else None
    birth_date = birth_date if birth_date != '' else None
    nationality = nationality if nationality != '' else None
    current_team_id = current_team_id if current_team_id != '' else None
    contract_expiry = contract_expiry if contract_expiry != '' else None
    salary = salary if salary != '' else None
    
    if not name or not position or jersey_number is None:
        return jsonify({'error': '姓名、位置和球衣号是必填字段'}), 400
    
    conn = db_config.get_connection()
    if not conn:
        return jsonify({'error': '数据库连接失败'}), 500
    
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT player_id FROM Player WHERE player_id = %s", (player_id,))
            if not cursor.fetchone():
                return jsonify({'error': '球员不存在'}), 404
            
            if current_team_id:
                cursor.execute("""
                    SELECT player_id FROM Player 
                    WHERE 球衣号 = %s AND 当前球队ID = %s AND player_id != %s
                """, (jersey_number, current_team_id, player_id))
                if cursor.fetchone():
                    return jsonify({'error': '该球队中已有其他球员使用此球衣号'}), 400
            
            cursor.callproc('sp_update_player', (
                player_id, name, position, jersey_number, height, weight, 
                birth_date, nationality, current_team_id, contract_expiry, salary
            ))
            
            conn.commit()
            return jsonify({'message': '球员更新成功'}), 200
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()


@players_bp.route('/<int:player_id>', methods=['GET'])
def get_player(player_id):
    """获取单个球员详情"""
    conn = db_config.get_connection()
    if not conn:
        return jsonify({'error': '数据库连接失败'}), 500
    
    try:
        with conn.cursor() as cursor:
            cursor.callproc('sp_get_player_detail', (player_id,))
            
            row = cursor.fetchone()
            if not row:
                return jsonify({'error': '球员不存在'}), 404
                
            player = {
                'player_id': row[0],
                'name': row[1],
                'position': row[2],
                'jersey_number': row[3],
                'height': row[4],
                'weight': row[5],
                'birth_date': row[6].strftime('%Y-%m-%d') if row[6] else None,
                'nationality': row[7],
                'current_team_id': row[8],
                'team_name': row[9],
                'contract_expiry': row[10].strftime('%Y-%m-%d') if row[10] else None,
                'salary': float(row[11]) if row[11] else None,
                'photo_url': f'/api/images/{row[12]}' if row[12] else None
            }

            # Get average stats
            cursor.callproc('sp_get_player_career_stats', (player_id,))
            
            stats_row = cursor.fetchone()
            # sp_get_player_career_stats returns:
            # games_played, avg_minutes, avg_points, avg_rebounds, avg_assists, avg_steals, avg_blocks, ...
            
            if stats_row and stats_row[0] > 0:
                player['stats'] = {
                    'games_played': stats_row[0],
                    'ppg': round(float(stats_row[2]), 1) if stats_row[2] else 0,
                    'rpg': round(float(stats_row[3]), 1) if stats_row[3] else 0,
                    'apg': round(float(stats_row[4]), 1) if stats_row[4] else 0,
                    'spg': round(float(stats_row[5]), 1) if stats_row[5] else 0,
                    'bpg': round(float(stats_row[6]), 1) if stats_row[6] else 0
                }
            else:
                player['stats'] = {
                    'games_played': 0,
                    'ppg': 0,
                    'rpg': 0,
                    'apg': 0,
                    'spg': 0,
                    'bpg': 0
                }
            
            return jsonify(player), 200
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()


@players_bp.route('/<int:player_id>', methods=['DELETE'])
@jwt_required()
def delete_player(player_id):
    """删除球员（仅管理员）"""
    current_user_id = get_jwt_identity()
    
    if not check_admin_permission(current_user_id):
        return jsonify({'error': '权限不足，仅管理员可删除球员'}), 403
    
    conn = db_config.get_connection()
    if not conn:
        return jsonify({'error': '数据库连接失败'}), 500
    
    try:
        with conn.cursor() as cursor:
            cursor.callproc('sp_get_player_detail', (player_id,))
            if not cursor.fetchone():
                return jsonify({'error': '球员不存在'}), 404
            
            cursor.callproc('sp_delete_player', (player_id,))
            conn.commit()
            return jsonify({'message': '球员删除成功'}), 200
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()


@players_bp.route('/<int:player_id>/photo', methods=['POST'])
@jwt_required()
def upload_player_photo(player_id):
    """上传球员照片（仅管理员）"""
    current_user_id = get_jwt_identity()
    
    if not check_admin_permission(current_user_id):
        return jsonify({'error': '权限不足，仅管理员可上传球员照片'}), 403
        
    if 'image' not in request.files:
        return jsonify({'error': '没有上传文件'}), 400
        
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': '未选择文件'}), 400
        
    conn = db_config.get_connection()
    if not conn:
        return jsonify({'error': '数据库连接失败'}), 500
        
    try:
        file_data = file.read()
        mime_type = file.mimetype
        filename = file.filename
        
        with conn.cursor() as cursor:
            # 1. Insert into Image table
            cursor.execute("""
                INSERT INTO Image (名称, 数据, MIME类型)
                VALUES (%s, %s, %s)
            """, (filename, file_data, mime_type))
            image_id = cursor.lastrowid
            
            # 2. Insert/Update Player_Image table
            # Use ON DUPLICATE KEY UPDATE to handle existing record
            cursor.execute("""
                INSERT INTO Player_Image (player_id, image_id)
                VALUES (%s, %s)
                ON DUPLICATE KEY UPDATE image_id = VALUES(image_id)
            """, (player_id, image_id))
            
            conn.commit()
            
            return jsonify({
                'message': '球员照片上传成功',
                'image_id': image_id,
                'url': f'/api/images/{image_id}'
            }), 201
            
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()


@players_bp.route('/<int:player_id>/stats', methods=['GET'])
def get_player_stats(player_id):
    """获取球员雷达图数据 (基于真实比赛数据)"""
    conn = db_config.get_connection()
    if not conn:
        return jsonify({'error': '数据库连接失败'}), 500
    
    try:
        with conn.cursor() as cursor:
            # 1. 获取真实评分
            cursor.execute("SELECT AVG(分数) FROM Rating WHERE player_id = %s", (player_id,))
            result = cursor.fetchone()
            avg_rating = float(result[0]) if result and result[0] is not None else 5.0
            
            # 2. 获取比赛数据平均值
            cursor.callproc('sp_get_player_career_stats', (player_id,))
            stats_row = cursor.fetchone()
            
            # 默认基础值
            stats = {
                '进攻': 40,
                '防守': 40,
                '篮板': 30,
                '助攻': 30,
                '体力': 40,
                '综合评价': int(avg_rating * 10)
            }
            
            if stats_row and stats_row[0] > 0:
                # 提取数据 (处理 None)
                # sp_get_player_career_stats returns:
                # 0:games_played, 1:avg_minutes, 2:avg_points, 3:avg_rebounds, 
                # 4:avg_assists, 5:avg_steals, 6:avg_blocks
                
                mpg = float(stats_row[1]) if stats_row[1] else 0
                ppg = float(stats_row[2]) if stats_row[2] else 0
                rpg = float(stats_row[3]) if stats_row[3] else 0
                apg = float(stats_row[4]) if stats_row[4] else 0
                spg = float(stats_row[5]) if stats_row[5] else 0
                bpg = float(stats_row[6]) if stats_row[6] else 0
                
                # 计算各项能力值 (0-100)
                # 进攻: 基于得分 (基准: 30分=100)
                stats['进攻'] = min(99, int(40 + (ppg / 30.0) * 60))
                
                # 篮板: 基于篮板 (基准: 12个=100)
                stats['篮板'] = min(99, int(30 + (rpg / 12.0) * 70))
                
                # 助攻: 基于助攻 (基准: 10个=100)
                stats['助攻'] = min(99, int(30 + (apg / 10.0) * 70))
                
                # 防守: 基于抢断+盖帽+篮板 (综合计算)
                # 抢断/盖帽权重高，篮板权重低
                def_score = (spg * 15) + (bpg * 15) + (rpg * 2)
                stats['防守'] = min(99, int(40 + def_score))
                
                # 体力: 基于上场时间 (基准: 40分钟=100)
                stats['体力'] = min(99, int(40 + (mpg / 40.0) * 60))
            
            return jsonify(stats), 200
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()


@players_bp.route('/<int:player_id>/details', methods=['GET'])
def get_player_details(player_id):
    """获取球员详细统计数据 (用于详情页)"""
    conn = db_config.get_connection()
    if not conn:
        return jsonify({'error': '数据库连接失败'}), 500
    
    try:
        with conn.cursor() as cursor:
            # 1. 获取球员基本信息
            cursor.execute("""
                SELECT p.姓名, p.位置, p.球衣号, p.身高, p.体重, p.国籍, 
                       t.名称 as team_name, pi.image_id, p.当前球队ID
                FROM Player p 
                LEFT JOIN Team t ON p.当前球队ID = t.team_id
                LEFT JOIN Player_Image pi ON p.player_id = pi.player_id
                WHERE p.player_id = %s
            """, (player_id,))
            player_info = cursor.fetchone()
            
            if not player_info:
                return jsonify({'error': '球员不存在'}), 404
                
            player_data = {
                'name': player_info[0],
                'position': player_info[1],
                'jersey_number': player_info[2],
                'height': float(player_info[3]) if player_info[3] else None,
                'weight': float(player_info[4]) if player_info[4] else None,
                'nationality': player_info[5],
                'team_name': player_info[6],
                'photo_url': f'/api/images/{player_info[7]}' if player_info[7] else None,
                'team_id': player_info[8]
            }
            
            # 2. 获取比赛数据
            # 简单的对手判断逻辑：如果主队ID不是球员当前球队ID，则主队是对手，否则客队是对手
            cursor.execute("""
                SELECT 
                    g.日期, 
                    CASE 
                        WHEN g.主队ID = %s THEN t_away.名称 
                        ELSE t_home.名称 
                    END as opponent,
                    pg.得分, pg.篮板, pg.助攻, pg.抢断, pg.盖帽, pg.上场时间, pg.正负值,
                    g.game_id
                FROM Player_Game pg
                JOIN Game g ON pg.game_id = g.game_id
                JOIN Team t_home ON g.主队ID = t_home.team_id
                JOIN Team t_away ON g.客队ID = t_away.team_id
                WHERE pg.player_id = %s AND g.状态 = '已结束' AND pg.上场时间 > 0
                ORDER BY g.日期
            """, (player_data['team_id'], player_id))
            
            games = []
            total_stats = {'points': 0, 'rebounds': 0, 'assists': 0, 'steals': 0, 'blocks': 0, 'count': 0}
            
            for row in cursor.fetchall():
                games.append({
                    'date': row[0].strftime('%Y-%m-%d'),
                    'opponent': row[1],
                    'points': row[2],
                    'rebounds': row[3],
                    'assists': row[4],
                    'steals': row[5],
                    'blocks': row[6],
                    'minutes': float(row[7]),
                    'plus_minus': row[8],
                    'game_id': row[9]
                })
                total_stats['points'] += row[2]
                total_stats['rebounds'] += row[3]
                total_stats['assists'] += row[4]
                total_stats['steals'] += row[5]
                total_stats['blocks'] += row[6]
                total_stats['count'] += 1
            
            # 计算平均数据用于雷达图
            averages = {}
            if total_stats['count'] > 0:
                count = total_stats['count']
                averages = {
                    'points': round(total_stats['points'] / count, 1),
                    'rebounds': round(total_stats['rebounds'] / count, 1),
                    'assists': round(total_stats['assists'] / count, 1),
                    'steals': round(total_stats['steals'] / count, 1),
                    'blocks': round(total_stats['blocks'] / count, 1)
                }
            
            return jsonify({
                'player': player_data,
                'games': games,
                'averages': averages
            })
            
    except Exception as e:
        print(f"Error getting player stats: {e}")
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()



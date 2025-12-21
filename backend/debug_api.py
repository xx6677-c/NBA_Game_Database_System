import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database.config import DatabaseConfig

def test_game_detail(game_id):
    print(f"Testing get_game_detail for game_id={game_id}")
    db = DatabaseConfig()
    conn = db.get_connection()
    if not conn:
        print("Failed to connect to DB")
        return

    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT g.game_id, g.赛季, g.日期, g.状态, g.主队得分, g.客队得分,
                       g.主队ID, g.客队ID,
                       ht.名称 as home_team, at.名称 as away_team,
                       wt.名称 as winner_team, g.场馆, g.获胜球队ID
                FROM Game g
                JOIN Team ht ON g.主队ID = ht.team_id
                JOIN Team at ON g.客队ID = at.team_id
                LEFT JOIN Team wt ON g.获胜球队ID = wt.team_id
                WHERE g.game_id = %s
            """, (game_id,))
            game = cursor.fetchone()
            print(f"Game result: {game}")
            
            if game:
                cursor.execute("""
                    SELECT predicted_team_id, COUNT(*) 
                    FROM Prediction 
                    WHERE game_id = %s 
                    GROUP BY predicted_team_id
                """, (game_id,))
                preds = cursor.fetchall()
                print(f"Predictions: {preds}")

    except Exception as e:
        print(f"Error in game detail: {e}")
    finally:
        conn.close()

def test_game_ratings(game_id):
    print(f"Testing get_game_ratings for game_id={game_id}")
    db = DatabaseConfig()
    conn = db.get_connection()
    if not conn:
        print("Failed to connect to DB")
        return

    try:
        with conn.cursor() as cursor:
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
            players = cursor.fetchall()
            print(f"Ratings result count: {len(players)}")
            if len(players) > 0:
                print(f"First player: {players[0]}")

    except Exception as e:
        print(f"Error in game ratings: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    # Try to find a valid game_id first
    db = DatabaseConfig()
    conn = db.get_connection()
    game_id = 1
    if conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT game_id FROM Game LIMIT 1")
            res = cursor.fetchone()
            if res:
                game_id = res[0]
        conn.close()
    
    test_game_detail(game_id)
    test_game_ratings(game_id)

import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from backend.database.core.config import DatabaseConfig

def test_rankings():
    db_config = DatabaseConfig()
    conn = db_config.get_connection()
    
    if not conn:
        print("Failed to connect to database")
        return

    try:
        with conn.cursor() as cursor:
            # 1. Check if there are players
            cursor.execute("SELECT COUNT(*) FROM Player")
            count = cursor.fetchone()[0]
            print(f"Total players in DB: {count}")

            if count == 0:
                print("No players found!")
                return

            # 2. Test the query
            stat_field = '得分'
            limit = 5
            sql = f"""
                SELECT 
                    p.player_id,
                    p.姓名 as name,
                    p.位置 as position,
                    t.名称 as team_name,
                    COUNT(pg.game_id) as games_played,
                    ROUND(AVG(COALESCE(pg.得分, 0)), 1) as avg_points
                FROM Player p
                LEFT JOIN Player_Game pg ON p.player_id = pg.player_id
                LEFT JOIN Team t ON p.当前球队ID = t.team_id
                GROUP BY p.player_id, p.姓名, p.位置, t.名称
                ORDER BY AVG(COALESCE(pg.{stat_field}, 0)) DESC, p.player_id
                LIMIT %s
            """
            print("\nExecuting query...")
            cursor.execute(sql, (limit,))
            results = cursor.fetchall()
            print(f"Query returned {len(results)} rows")
            for row in results:
                print(row)

    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    test_rankings()

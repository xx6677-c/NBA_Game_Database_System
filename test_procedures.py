import sys
import os
import json
import datetime
import random

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backend.database.core.config import DatabaseConfig

def test_procedures():
    print("Starting Comprehensive Stored Procedures Verification...")
    db = DatabaseConfig()
    conn = db.get_connection()
    
    if not conn:
        print("❌ Failed to connect to database.")
        return

    # Variables to store IDs for cleanup
    test_user_id = None
    test_team_id_1 = None
    test_team_id_2 = None
    test_player_id = None
    test_game_id = None
    test_post_id = None
    test_image_id = None

    try:
        with conn.cursor() as cursor:
            # ==========================================
            # 1. Auth & User Management
            # ==========================================
            print("\n--- Testing Auth & User ---")
            
            # Register User
            username = f"test_user_{random.randint(1000, 9999)}"
            print(f"Registering user: {username}")
            cursor.callproc('sp_register_user', (username, 'password123', 'user', datetime.datetime.now()))
            conn.commit()
            
            # Login to get ID
            cursor.callproc('sp_login_user', (username,))
            user_row = cursor.fetchone()
            if user_row:
                test_user_id = user_row[0]
                print(f"✅ User registered and logged in. ID: {test_user_id}")
            else:
                raise Exception("Failed to retrieve registered user.")

            # Update Profile
            cursor.callproc('sp_update_user_profile', (test_user_id, 'test@example.com', '1234567890'))
            conn.commit()
            print("✅ User profile updated.")

            # ==========================================
            # 2. Team Management
            # ==========================================
            print("\n--- Testing Teams ---")
            
            # Debug: Check Team table structure
            # cursor.execute("SHOW CREATE TABLE Team")
            # print(cursor.fetchone()[1])

            # Create Team 1
            team_name_1 = f'Test Team A {random.randint(1000,9999)}'
            args = cursor.callproc('sp_create_team', (team_name_1, 'City A', 'Arena A', 'East', 2020, 0))
            test_team_id_1 = args[5]
            
            # Fallback if OUT param fails (pymysql quirk?)
            if test_team_id_1 == 0:
                print("⚠️ OUT parameter returned 0. Fetching ID manually...")
                cursor.execute("SELECT team_id FROM Team WHERE 名称 = %s", (team_name_1,))
                row = cursor.fetchone()
                if row:
                    test_team_id_1 = row[0]
            
            print(f"✅ Created Team A. ID: {test_team_id_1}")
            
            # Create Team 2
            team_name_2 = f'Test Team B {random.randint(1000,9999)}'
            args = cursor.callproc('sp_create_team', (team_name_2, 'City B', 'Arena B', 'West', 2021, 0))
            test_team_id_2 = args[5]
            
            if test_team_id_2 == 0:
                cursor.execute("SELECT team_id FROM Team WHERE 名称 = %s", (team_name_2,))
                row = cursor.fetchone()
                if row:
                    test_team_id_2 = row[0]

            print(f"✅ Created Team B. ID: {test_team_id_2}")
            
            if test_team_id_1 == 0 or test_team_id_2 == 0:
                raise Exception("Failed to create teams with valid IDs.")

            # Update Team 1
            cursor.callproc('sp_update_team', (test_team_id_1, 'Updated Team A', 'New City A', 'New Arena A', 'East', 2020))
            conn.commit()
            print("✅ Updated Team A.")

            # ==========================================
            # 3. Player Management
            # ==========================================
            print("\n--- Testing Players ---")
            
            # Create Player
            # p_name, p_position, p_jersey_number, p_height, p_weight, p_birth_date, p_nationality, p_current_team_id, p_contract_expiry, p_salary, OUT p_player_id
            player_name = f'Test Player {random.randint(1000,9999)}'
            args = cursor.callproc('sp_create_player', (
                player_name, 'PG', 1, 1.90, 90.0, '2000-01-01', 'USA', test_team_id_1, '2025-01-01', 1000000.00, 0
            ))
            test_player_id = args[10]
            
            if test_player_id == 0:
                cursor.execute("SELECT player_id FROM Player WHERE 姓名=%s", (player_name,))
                row = cursor.fetchone()
                if row:
                    test_player_id = row[0]

            print(f"✅ Created Player. ID: {test_player_id}")
            
            # Update Player
            cursor.callproc('sp_update_player', (
                test_player_id, 'Updated Player', 'SG', 23, 1.95, 95.0, '2000-01-01', 'USA', test_team_id_1, '2026-01-01', 2000000.00
            ))
            conn.commit()
            print("✅ Updated Player.")

            # ==========================================
            # 4. Game Management
            # ==========================================
            print("\n--- Testing Games ---")
            
            # Create Game
            # p_season, p_date, p_home_team_id, p_away_team_id, p_home_score, p_away_score, p_status, p_venue, OUT p_game_id
            args = cursor.callproc('sp_create_game', (
                '2023-24', datetime.datetime.now(), test_team_id_1, test_team_id_2, 100, 90, '已结束', 'Test Arena', 0
            ))
            test_game_id = args[8]
            
            if test_game_id == 0:
                 # Try to find the game we just created
                 cursor.execute("SELECT game_id FROM Game WHERE 主队ID=%s AND 客队ID=%s ORDER BY game_id DESC LIMIT 1", (test_team_id_1, test_team_id_2))
                 row = cursor.fetchone()
                 if row:
                     test_game_id = row[0]

            print(f"✅ Created Game. ID: {test_game_id}")
            
            # Add Player Stats
            # p_player_id, p_game_id, p_minutes, p_points, p_rebounds, p_assists, p_steals, p_blocks, p_turnovers, p_fouls, p_plus_minus
            cursor.callproc('sp_add_player_game_stat', (
                test_player_id, test_game_id, 30.5, 25, 5, 10, 2, 1, 3, 2, 15
            ))
            conn.commit()
            print("✅ Added Player Game Stats.")

            # ==========================================
            # 5. Posts & Community
            # ==========================================
            print("\n--- Testing Posts ---")
            
            # Create Post
            # p_user_id, p_title, p_content, p_game_id, p_created_at, OUT p_post_id
            post_title = f'Test Post {random.randint(1000,9999)}'
            args = cursor.callproc('sp_create_post', (
                test_user_id, post_title, 'Test Content', test_game_id, datetime.datetime.now(), 0
            ))
            test_post_id = args[5]
            
            if test_post_id == 0:
                cursor.execute("SELECT post_id FROM Post WHERE 标题=%s", (post_title,))
                row = cursor.fetchone()
                if row:
                    test_post_id = row[0]

            print(f"✅ Created Post. ID: {test_post_id}")
            
            # Like Post
            cursor.callproc('sp_add_post_like', (test_user_id, test_post_id))
            conn.commit()
            print("✅ Liked Post.")
            
            # Check Like
            cursor.callproc('sp_check_post_like', (test_user_id, test_post_id))
            like_count = cursor.fetchone()[0]
            if like_count > 0:
                print("✅ Verified Post Like.")
            else:
                print("❌ Failed to verify Post Like.")

            # ==========================================
            # 6. Images
            # ==========================================
            print("\n--- Testing Images ---")
            
            # Upload Image (Mock)
            # p_name, p_data, p_mime_type, OUT p_image_id
            dummy_data = b'fake_image_data'
            image_name = f'test_image_{random.randint(1000,9999)}.jpg'
            args = cursor.callproc('sp_upload_image', (
                image_name, dummy_data, 'image/jpeg', 0
            ))
            test_image_id = args[3]
            
            if test_image_id == 0:
                cursor.execute("SELECT image_id FROM Image WHERE 名称=%s", (image_name,))
                row = cursor.fetchone()
                if row:
                    test_image_id = row[0]

            print(f"✅ Uploaded Image. ID: {test_image_id}")
            
            # Set Avatar
            cursor.callproc('sp_update_user_avatar', (test_user_id, test_image_id))
            conn.commit()
            print("✅ Updated User Avatar.")

            # ==========================================
            # 7. Shop & Points
            # ==========================================
            print("\n--- Testing Shop ---")
            
            # Give user points manually for testing
            cursor.execute("UPDATE User SET points = 1000 WHERE user_id = %s", (test_user_id,))
            conn.commit()
            
            # Draw Card
            # p_user_id, p_cost, OUT p_success, OUT p_message, ...
            args = cursor.callproc('sp_draw_card', (
                test_user_id, 50, 0, '', 0, '', '', 0, '', 0, 0
            ))
            success = args[2]
            message = args[3]
            if success:
                print(f"✅ Card Draw Successful: {message}")
                print(f"   Player: {args[5]}, Team: {args[8]}")
            else:
                print(f"⚠️ Card Draw Failed (Expected if no players in DB?): {message}")

            # ==========================================
            # 8. Read Operations (Verification)
            # ==========================================
            print("\n--- Verifying Data ---")
            
            cursor.callproc('sp_get_players', (test_team_id_1,))
            players = cursor.fetchall()
            print(f"✅ Found {len(players)} players in Team A.")
            
            cursor.callproc('sp_get_posts', (test_game_id,))
            posts = cursor.fetchall()
            print(f"✅ Found {len(posts)} posts for the game.")

    except Exception as e:
        print(f"\n❌ Error during testing: {str(e)}")
        import traceback
        traceback.print_exc()
    
    finally:
        # ==========================================
        # Cleanup
        # ==========================================
        print("\n--- Cleaning Up ---")
        try:
            with conn.cursor() as cursor:
                if test_post_id:
                    print(f"Deleting Post {test_post_id}...")
                    cursor.callproc('sp_delete_post', (test_post_id,))
                
                if test_game_id:
                    print(f"Deleting Game {test_game_id}...")
                    cursor.callproc('sp_delete_game', (test_game_id,))
                
                if test_player_id:
                    print(f"Deleting Player {test_player_id}...")
                    cursor.callproc('sp_delete_player', (test_player_id,))
                
                if test_team_id_1:
                    print(f"Deleting Team {test_team_id_1}...")
                    cursor.callproc('sp_delete_team', (test_team_id_1,))
                
                if test_team_id_2:
                    print(f"Deleting Team {test_team_id_2}...")
                    cursor.callproc('sp_delete_team', (test_team_id_2,))
                
                if test_user_id:
                    print(f"Deleting User {test_user_id}...")
                    cursor.callproc('sp_delete_account', (test_user_id,))
                
                conn.commit()
                print("✅ Cleanup complete.")
        except Exception as e:
            print(f"❌ Error during cleanup: {str(e)}")
        
        conn.close()

if __name__ == "__main__":
    test_procedures()

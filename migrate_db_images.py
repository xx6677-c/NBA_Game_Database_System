import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from backend.database.core.config import DatabaseConfig

def migrate_images():
    db_config = DatabaseConfig()
    conn = db_config.get_connection()
    
    if not conn:
        print("Failed to connect to database")
        return

    try:
        with conn.cursor() as cursor:
            print("Migrating Image table...")
            
            # 1. Check if '数据' column exists
            cursor.execute("SHOW COLUMNS FROM Image LIKE '数据'")
            if not cursor.fetchone():
                print("Adding '数据' and 'MIME类型' columns...")
                # We allow NULL initially to avoid errors with existing rows
                cursor.execute("ALTER TABLE Image ADD COLUMN 数据 LONGBLOB")
                cursor.execute("ALTER TABLE Image ADD COLUMN MIME类型 VARCHAR(50)")
            
            # 2. Check if '文件路径' column exists
            cursor.execute("SHOW COLUMNS FROM Image LIKE '文件路径'")
            if cursor.fetchone():
                print("Dropping '文件路径' column...")
                cursor.execute("ALTER TABLE Image DROP COLUMN 文件路径")

            # 3. Create Team_Logo table
            print("Creating Team_Logo table...")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Team_Logo (
                    team_id INT PRIMARY KEY,
                    image_id INT NOT NULL UNIQUE,
                    FOREIGN KEY (team_id) REFERENCES Team(team_id) ON DELETE CASCADE,
                    FOREIGN KEY (image_id) REFERENCES Image(image_id) ON DELETE CASCADE
                )
            """)
            
            conn.commit()
            print("Migration completed successfully!")

    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    migrate_images()

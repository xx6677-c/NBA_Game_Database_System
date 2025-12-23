"""
球员图片上传脚本
将球员图片上传到数据库Image表，并建立与Player的关联（Player_Image表）
图片文件名格式: {player_id}.png
"""
import os
import sys
import mimetypes
from dotenv import load_dotenv

# 获取项目根目录
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 加载backend目录下的.env文件
load_dotenv(os.path.join(BASE_DIR, 'backend', '.env'))

# 添加backend目录到路径
sys.path.insert(0, os.path.join(BASE_DIR, 'backend'))

from backend.database.core.config import DatabaseConfig


def get_player_ids():
    """
    获取数据库中所有球员的player_id
    返回: set of player_ids
    """
    db_config = DatabaseConfig()
    conn = db_config.get_connection()
    
    if not conn:
        print("错误: 无法连接到数据库")
        return set()
    
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT player_id FROM Player")
        ids = {row[0] for row in cursor.fetchall()}
        cursor.close()
        return ids
    finally:
        conn.close()


def upload_player_images(image_dir):
    """
    上传球员图片到数据库
    
    Args:
        image_dir: 球员图片所在目录
    """
    print("=" * 60)
    print("球员图片上传工具")
    print("=" * 60)
    
    # 获取数据库中的球员ID
    player_ids = get_player_ids()
    if not player_ids:
        print("错误: 无法获取球员信息")
        return
    
    print(f"\n数据库中共有 {len(player_ids)} 名球员")
    
    # 获取图片目录中的所有图片
    if not os.path.exists(image_dir):
        print(f"错误: 目录不存在 - {image_dir}")
        return
    
    image_files = [f for f in os.listdir(image_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp'))]
    print(f"发现 {len(image_files)} 个图片文件")
    
    # 连接数据库
    db_config = DatabaseConfig()
    conn = db_config.get_connection()
    
    if not conn:
        print("错误: 无法连接到数据库")
        return
    
    try:
        cursor = conn.cursor()
        
        # 先清空现有的Player_Image关联（避免重复）
        print("\n正在清空现有的球员图片关联...")
        cursor.execute("DELETE FROM Player_Image")
        conn.commit()
        print("✓ 已清空Player_Image表")
        
        success_count = 0
        skipped_count = 0
        failed_count = 0
        
        print("\n开始上传球员图片...")
        print("-" * 60)
        
        for image_file in image_files:
            # 从文件名提取player_id（去除扩展名）
            try:
                player_id = int(os.path.splitext(image_file)[0])
            except ValueError:
                print(f"  ✗ 无效的文件名格式: {image_file}")
                failed_count += 1
                continue
            
            # 检查球员是否存在于数据库
            if player_id not in player_ids:
                skipped_count += 1
                continue  # 静默跳过不存在的球员
            
            # 读取图片文件
            image_path = os.path.join(image_dir, image_file)
            try:
                with open(image_path, 'rb') as f:
                    image_data = f.read()
            except Exception as e:
                print(f"  ✗ 读取文件失败 {image_file}: {e}")
                failed_count += 1
                continue
            
            # 获取MIME类型
            mime_type, _ = mimetypes.guess_type(image_file)
            if mime_type is None:
                mime_type = 'image/png'  # 默认
            
            try:
                # 插入图片到Image表
                cursor.execute("""
                    INSERT INTO Image (名称, 数据, MIME类型)
                    VALUES (%s, %s, %s)
                """, (f"player_{player_id}", image_data, mime_type))
                
                # 获取刚插入的image_id
                image_id = cursor.lastrowid
                
                # 建立Player_Image关联
                cursor.execute("""
                    INSERT INTO Player_Image (player_id, image_id)
                    VALUES (%s, %s)
                    ON DUPLICATE KEY UPDATE image_id = VALUES(image_id)
                """, (player_id, image_id))
                
                conn.commit()
                success_count += 1
                
                # 每50个打印一次进度
                if success_count % 50 == 0:
                    print(f"  已处理 {success_count} 张图片...")
                
            except Exception as e:
                print(f"  ✗ 上传失败 player_id={player_id}: {e}")
                conn.rollback()
                failed_count += 1
        
        print("-" * 60)
        print(f"\n上传完成!")
        print(f"  成功: {success_count}")
        print(f"  跳过 (球员不存在): {skipped_count}")
        print(f"  失败: {failed_count}")
        
        # 验证结果
        print("\n验证已上传的图片...")
        cursor.execute("SELECT COUNT(*) FROM Player_Image")
        total_images = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM Player")
        total_players = cursor.fetchone()[0]
        
        cursor.execute("""
            SELECT COUNT(*) FROM Player p
            LEFT JOIN Player_Image pi ON p.player_id = pi.player_id
            WHERE pi.image_id IS NULL
        """)
        without_image = cursor.fetchone()[0]
        
        print(f"\n球员图片统计:")
        print(f"  有图片的球员: {total_images}/{total_players}")
        print(f"  无图片的球员: {without_image}")
        
    except Exception as e:
        print(f"\n错误: {e}")
        conn.rollback()
        raise
    finally:
        cursor.close()
        conn.close()


def main():
    # 球员图片目录
    image_dir = os.path.join(BASE_DIR, 'player_images')
    upload_player_images(image_dir)


if __name__ == '__main__':
    main()

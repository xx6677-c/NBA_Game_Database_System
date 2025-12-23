"""
球队Logo上传脚本
将球队logo图片上传到数据库Image表，并建立与Team的关联（Team_Logo表）
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


def get_team_name_mapping():
    """
    获取球队名称到team_id的映射
    返回: {球队名称: team_id}
    """
    db_config = DatabaseConfig()
    conn = db_config.get_connection()
    
    if not conn:
        print("错误: 无法连接到数据库")
        return {}
    
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT team_id, 名称 FROM Team")
        mapping = {row[1]: row[0] for row in cursor.fetchall()}
        cursor.close()
        return mapping
    finally:
        conn.close()


def upload_team_logos(logo_dir):
    """
    上传球队logo到数据库
    
    Args:
        logo_dir: 球队logo图片所在目录
    """
    print("=" * 60)
    print("球队Logo上传工具")
    print("=" * 60)
    
    # 获取球队名称到ID的映射
    team_mapping = get_team_name_mapping()
    if not team_mapping:
        print("错误: 无法获取球队信息")
        return
    
    print(f"\n已找到 {len(team_mapping)} 支球队")
    
    # 获取logo目录中的所有图片
    if not os.path.exists(logo_dir):
        print(f"错误: 目录不存在 - {logo_dir}")
        return
    
    logo_files = [f for f in os.listdir(logo_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp'))]
    print(f"发现 {len(logo_files)} 个logo文件")
    
    # 连接数据库
    db_config = DatabaseConfig()
    conn = db_config.get_connection()
    
    if not conn:
        print("错误: 无法连接到数据库")
        return
    
    try:
        cursor = conn.cursor()
        
        # 先清空现有的Team_Logo关联（避免重复）
        print("\n正在清空现有的球队Logo关联...")
        cursor.execute("DELETE FROM Team_Logo")
        conn.commit()
        print("✓ 已清空Team_Logo表")
        
        success_count = 0
        failed_count = 0
        
        print("\n开始上传球队Logo...")
        print("-" * 60)
        
        for logo_file in logo_files:
            # 从文件名提取球队名称（去除扩展名）
            team_name = os.path.splitext(logo_file)[0]
            
            # 查找对应的team_id
            team_id = team_mapping.get(team_name)
            
            if team_id is None:
                print(f"  ✗ 找不到球队: {team_name}")
                failed_count += 1
                continue
            
            # 读取图片文件
            logo_path = os.path.join(logo_dir, logo_file)
            try:
                with open(logo_path, 'rb') as f:
                    image_data = f.read()
            except Exception as e:
                print(f"  ✗ 读取文件失败 {logo_file}: {e}")
                failed_count += 1
                continue
            
            # 获取MIME类型
            mime_type, _ = mimetypes.guess_type(logo_file)
            if mime_type is None:
                mime_type = 'image/jpeg'  # 默认
            
            try:
                # 插入图片到Image表
                cursor.execute("""
                    INSERT INTO Image (名称, 数据, MIME类型)
                    VALUES (%s, %s, %s)
                """, (f"team_logo_{team_name}", image_data, mime_type))
                
                # 获取刚插入的image_id
                image_id = cursor.lastrowid
                
                # 建立Team_Logo关联
                cursor.execute("""
                    INSERT INTO Team_Logo (team_id, image_id)
                    VALUES (%s, %s)
                    ON DUPLICATE KEY UPDATE image_id = VALUES(image_id)
                """, (team_id, image_id))
                
                conn.commit()
                print(f"  ✓ {team_name} (team_id={team_id}, image_id={image_id})")
                success_count += 1
                
            except Exception as e:
                print(f"  ✗ 上传失败 {team_name}: {e}")
                conn.rollback()
                failed_count += 1
        
        print("-" * 60)
        print(f"\n上传完成!")
        print(f"  成功: {success_count}")
        print(f"  失败: {failed_count}")
        
        # 验证结果
        print("\n验证已上传的Logo...")
        cursor.execute("""
            SELECT t.名称, t.team_id, tl.image_id
            FROM Team t
            LEFT JOIN Team_Logo tl ON t.team_id = tl.team_id
            ORDER BY t.名称
        """)
        
        with_logo = 0
        without_logo = 0
        for row in cursor.fetchall():
            if row[2]:
                with_logo += 1
            else:
                without_logo += 1
                print(f"  ! 球队 {row[0]} (id={row[1]}) 没有Logo")
        
        print(f"\n球队Logo统计: {with_logo}/{with_logo + without_logo} 支球队有Logo")
        
    except Exception as e:
        print(f"\n错误: {e}")
        conn.rollback()
        raise
    finally:
        cursor.close()
        conn.close()


def main():
    # 球队logo目录
    logo_dir = os.path.join(BASE_DIR, '球队logo')
    upload_team_logos(logo_dir)


if __name__ == '__main__':
    main()

import pandas as pd
import requests
import os
import time

def download_player_headshots():
    # 1. 创建保存图片的文件夹
    save_dir = 'player_images'
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
        print(f"已创建文件夹: {save_dir}")

    # 2. 读取球员列表
    # 请确保文件名是你最新生成的那个csv
    csv_file = '2_Player.csv' 
    if not os.path.exists(csv_file):
        print(f"错误: 找不到 {csv_file}")
        return

    df = pd.read_csv(csv_file)
    total = len(df)
    print(f"找到 {total} 名球员，准备开始下载...")

    # 3. 设置请求头 (防止被服务器拒绝)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    success_count = 0
    fail_count = 0

    # 4. 循环下载
    for index, row in df.iterrows():
        p_id = row['player_id']
        p_name = row['姓名']
        
        # 构造官方图片 URL
        # 1040x760 是高清大图，如果想要小图可以用 260x190
        url = f"https://cdn.nba.com/headshots/nba/latest/1040x760/{p_id}.png"
        
        file_path = os.path.join(save_dir, f"{p_id}.png")
        
        # 如果文件已存在，跳过（方便断点续传）
        if os.path.exists(file_path):
            print(f"[{index+1}/{total}] {p_name} 已存在，跳过。")
            success_count += 1
            continue

        try:
            print(f"[{index+1}/{total}] 正在下载: {p_name} ...", end="")
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                with open(file_path, 'wb') as f:
                    f.write(response.content)
                print(" 成功")
                success_count += 1
            else:
                print(f" 失败 (HTTP {response.status_code}) - 可能暂无照片")
                fail_count += 1
            
            # 礼貌性延迟，防止请求过快
            time.sleep(0.2)

        except Exception as e:
            print(f" 出错: {e}")
            fail_count += 1

    print("\n" + "="*30)
    print(f"下载完成！")
    print(f"成功: {success_count}")
    print(f"失败: {fail_count} (通常是新秀或双向合同球员暂无官网照片)")
    print(f"图片保存在: {os.getcwd()}/{save_dir}")

if __name__ == "__main__":
    download_player_headshots()
import requests
import os
import time
import sys
# 下载并保存刚刚遗失的 NBA 球员的官方头像图片
# ================= 关键设置 =================
# 强制将标准输出设置为 UTF-8，防止 Windows 控制台因为打印 "ć, š" 等字符报错
sys.stdout.reconfigure(encoding='utf-8')

def download_specific_players():
    save_dir = 'player_images'
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    # 你提供的 19 人名单 (ID: 名字)
    missing_players = {
        203992: "Bogdan Bogdanović",
        1643024: "Chris Mañon",
        203967: "Dario Šarić",
        203471: "Dennis Schröder",
        1642856: "Egor Dëmin",
        202685: "Jonas Valančiūnas",
        203994: "Jusuf Nurkić",
        1631255: "Karlo Matković",
        1642857: "Kasparas Jakučionis",
        204001: "Kristaps Porziņģis",
        1629029: "Luka Dončić",
        1642365: "Nikola Đurišić",
        203999: "Nikola Jokić",
        1631107: "Nikola Jović",
        1642260: "Nikola Topić",
        202696: "Nikola Vučević",
        1642359: "Pacôme Dadiet",
        1630249: "Vít Krejčí",
        1642949: "Yanic Konan Niederhäuser"
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    print(f"开始尝试补全 {len(missing_players)} 名球员的图片...\n")

    success_count = 0
    
    for p_id, p_name in missing_players.items():
        file_path = os.path.join(save_dir, f"{p_id}.png")
        
        # 即使文件存在也强制覆盖下载一遍，确保不是坏文件
        # if os.path.exists(file_path): ... (这里去掉跳过逻辑)

        # 1. 尝试下载高清图 (1040x760)
        url_large = f"https://cdn.nba.com/headshots/nba/latest/1040x760/{p_id}.png"
        # 2. 备用：尝试下载小图 (260x190) - 有些新秀或双向合同球员只有小图
        url_small = f"https://cdn.nba.com/headshots/nba/latest/260x190/{p_id}.png"

        try:
            # 这里的 print 之前可能因为特殊字符导致报错，现在应该没问题了
            print(f"[{p_id}] {p_name} ... ", end="")
            
            # 尝试高清
            res = requests.get(url_large, headers=headers, timeout=10)
            
            if res.status_code == 200:
                with open(file_path, 'wb') as f:
                    f.write(res.content)
                print("成功 (高清)")
                success_count += 1
            else:
                # 尝试小图
                print("高清图缺失，尝试小图...", end="")
                res_small = requests.get(url_small, headers=headers, timeout=10)
                if res_small.status_code == 200:
                    with open(file_path, 'wb') as f:
                        f.write(res_small.content)
                    print("成功 (小图)")
                    success_count += 1
                else:
                    print(f"失败 (无官方图)")
            
            time.sleep(0.3)

        except Exception as e:
            # 捕获错误，防止因为一个人失败导致整个脚本停止
            print(f" 程序错误: {str(e)}")

    print("\n" + "="*30)
    print(f"补漏完成。成功下载: {success_count}/{len(missing_players)}")

if __name__ == "__main__":
    download_specific_players()
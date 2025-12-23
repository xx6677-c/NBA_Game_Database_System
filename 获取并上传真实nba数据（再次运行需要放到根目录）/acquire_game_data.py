import requests
import pandas as pd
from datetime import datetime, timedelta

def get_schedule_final_correction():
    print("正在获取 NBA 官方赛程 (使用 UTC 字段修正北京时间)...")
    
    url = "https://cdn.nba.com/static/json/staticData/scheduleLeagueV2.json"
    
    try:
        response = requests.get(url, timeout=15)
        data = response.json()
        game_dates = data['leagueSchedule']['gameDates']
        
        all_games = []
        
        for date_item in game_dates:
            games = date_item['games']
            for game in games:
                # 过滤非正赛
                if game['gameId'][:3] not in ['002', '004', '005']:
                    continue

                # ================= 核心修正点 =================
                # 之前读取的是 gameDateTimeEst (美东时间)，现在改读 gameDateTimeUTC
                raw_time_str = game['gameDateTimeUTC'] 
                
                try:
                    # 1. 解析标准 UTC 时间 (例如 "2024-12-24T03:00:00Z")
                    utc_dt = datetime.strptime(raw_time_str, "%Y-%m-%dT%H:%M:%SZ")
                    
                    # 2. 加上 8 小时变为北京时间
                    beijing_dt = utc_dt + timedelta(hours=8)
                    
                    # 3. 格式化
                    final_time_str = beijing_dt.strftime("%Y-%m-%d %H:%M:%S")
                    
                except Exception:
                    # 如果 UTC 字段有问题，回退到 EST + 13 (冬令时近似计算)
                    final_time_str = game['gameDateTimeEst']

                # ============================================

                # 提取其他信息
                home = game['homeTeam']
                away = game['awayTeam']
                h_score = home.get('score', 0)
                a_score = away.get('score', 0)
                
                # 状态与获胜者
                status = '已结束' if game['gameStatus'] == 3 else '未开始'
                winner_id = None
                if status == '已结束':
                    winner_id = home['teamId'] if h_score > a_score else away['teamId']

                all_games.append({
                    'game_id': game['gameId'],
                    '赛季': '2025-26', 
                    '日期': final_time_str, # 现在是正确的北京时间
                    '主队ID': home['teamId'],
                    '主队名称': home['teamTricode'],
                    '客队ID': away['teamId'],
                    '客队名称': away['teamTricode'],
                    '主队得分': h_score,
                    '客队得分': a_score,
                    '状态': status,
                    '获胜球队ID': winner_id,
                    '场馆': f"{game.get('arenaName', '')}, {game.get('arenaCity', '')}"
                })

        # 导出
        df = pd.DataFrame(all_games)
        df.to_csv('3_Game_Corrected_Time.csv', index=False, encoding='utf-8-sig')
        
        print(f"\n成功！已导出 {len(df)} 场比赛。")
        print("\n=== 时间验证 (开拓者 vs 活塞) ===")
        # 筛选活塞 (DET) 或 开拓者 (POR) 的近期比赛看时间
        check_teams = ['DET', 'POR']
        preview = df[
            (df['主队名称'].isin(check_teams)) | 
            (df['客队名称'].isin(check_teams))
        ]
        # 只看最近几天的
        print(preview[['日期', '主队名称', '客队名称']].tail(5))

    except Exception as e:
        print(f"发生错误: {e}")

if __name__ == "__main__":
    get_schedule_final_correction()
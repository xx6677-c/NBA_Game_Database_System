import pandas as pd
import time
from nba_api.stats.endpoints import leaguegamelog

# ================= 配置 =================
CURRENT_SEASON = '2025-26'  # 确认赛季
pd.set_option('display.max_columns', None)

def export_player_game_stats_only():
    print(f"正在获取 {CURRENT_SEASON} 赛季所有球员的比赛数据...")
    print("注意：数据量较大（约数万条），请求可能需要几秒到十几秒，请耐心等待...")

    try:
        # 获取球员级别的比赛日志 (player_or_team_abbreviation='P')
        # season_type_all_star 默认为 Regular Season
        log = leaguegamelog.LeagueGameLog(season=CURRENT_SEASON, player_or_team_abbreviation='P')
        df_raw = log.get_data_frames()[0]

        if df_raw.empty:
            print("未获取到数据，请检查网络或赛季设置。")
            return

        # 映射列名 (API -> 数据库字段)
        rename_map = {
            'PLAYER_ID': 'player_id',
            'GAME_ID': 'game_id',
            'MIN': '上场时间',
            'PTS': '得分',
            'REB': '篮板',
            'AST': '助攻',
            'STL': '抢断',
            'BLK': '盖帽',
            'TOV': '失误',
            'PF': '犯规',
            'PLUS_MINUS': '正负值'
        }

        # 提取并重命名
        df_export = df_raw[list(rename_map.keys())].rename(columns=rename_map)

        # ================= 数据清洗 =================
        
        # 1. 强制转 ID 为整数 (去除 .0)
        # 使用 Int64 支持空值，虽然比赛日志里 ID 通常不为空
        df_export['player_id'] = df_export['player_id'].astype('Int64')
        df_export['game_id'] = df_export['game_id'].astype('Int64')

        # 2. 清洗上场时间 ("24:12" -> 24.2)
        def clean_min(x):
            if pd.isna(x): return 0.0
            x_str = str(x)
            if ':' in x_str:
                try:
                    m, s = x_str.split(':')
                    return round(int(m) + int(s)/60, 1)
                except:
                    return 0.0
            try:
                # 应对有些数据可能是纯数字字符串 '24'
                return float(x_str)
            except:
                return 0.0

        df_export['上场时间'] = df_export['上场时间'].apply(clean_min)

        # 3. 填充基础数据的空值为 0 (得分、篮板等)
        stats_cols = ['得分', '篮板', '助攻', '抢断', '盖帽', '失误', '犯规']
        df_export[stats_cols] = df_export[stats_cols].fillna(0)
        
        # 正负值也是整数，但也可能为空
        df_export['正负值'] = df_export['正负值'].fillna(0).astype('Int64')

        # ================= 导出 =================
        filename = '4_Player_Game.csv'
        df_export.to_csv(filename, index=False, encoding='utf-8-sig')
        
        print("\n" + "="*30)
        print(f"成功导出！文件保存在: {filename}")
        print(f"总记录数: {len(df_export)}")
        print("="*30)
        print("数据预览:")
        print(df_export.head())

    except Exception as e:
        print(f"\n发生错误: {e}")
        print("如果是 ConnectionTimeout，请检查 VPN。")

if __name__ == "__main__":
    export_player_game_stats_only()
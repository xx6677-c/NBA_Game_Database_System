import pandas as pd
import time
from nba_api.stats.static import teams
from nba_api.stats.endpoints import commonteamroster, leaguedashplayerbiostats

# ================= 配置 =================
CURRENT_SEASON = '2025-26' 
POS_MAP = {
    'G': '控球后卫', 'G-F': '得分后卫', 'F-G': '得分后卫',
    'F': '小前锋', 'F-C': '大前锋', 'C-F': '大前锋',
    'C': '中锋', '': '控球后卫'
}

# ================= 数据转换工具函数 (带空值保护) =================
def safe_height_to_meters(height_str):
    """
    安全转换身高: '6-6' -> 1.98
    如果为空或格式不对，返回 None
    """
    try:
        if not height_str or not isinstance(height_str, str):
            return None
        if '-' not in height_str:
            return None
        feet, inches = map(int, height_str.split('-'))
        # 1 foot = 12 inches, 1 inch = 0.0254 meters
        total_inches = feet * 12 + inches
        return round(total_inches * 0.0254, 2)
    except Exception:
        return None

def safe_weight_to_kg(weight_lbs):
    """
    安全转换体重: 220 -> 99.8
    如果为空或不是数字，返回 None
    """
    try:
        if weight_lbs is None or weight_lbs == "":
            return None
        # 1 lb = 0.453592 kg
        val = float(weight_lbs)
        return round(val * 0.453592, 1)
    except Exception:
        return None

# ================= 主逻辑 =================
def get_player_country_map():
    """获取国籍映射"""
    print("正在获取全联盟球员国籍信息...")
    try:
        bio = leaguedashplayerbiostats.LeagueDashPlayerBioStats(season=CURRENT_SEASON)
        df_bio = bio.get_data_frames()[0]
        # 建立 {PLAYER_ID: COUNTRY} 字典
        return dict(zip(df_bio['PLAYER_ID'], df_bio['COUNTRY']))
    except Exception as e:
        print(f"获取国籍信息警告: {e}")
        return {}

def export_players_final():
    # 1. 获取国籍字典
    country_map = get_player_country_map()
    
    print("正在获取球员详细数据 (带体重/身高转换)...")
    nba_teams = teams.get_teams()
    all_players_list = []
    
    for i, team in enumerate(nba_teams):
        t_id = team['id']
        t_name = team['full_name']
        print(f"   -> [{i+1}/30] 处理 {t_name}...")
        
        try:
            roster = commonteamroster.CommonTeamRoster(team_id=t_id, season=CURRENT_SEASON)
            df_roster = roster.get_data_frames()[0]
            
            for _, row in df_roster.iterrows():
                p_id = row['PLAYER_ID']
                
                # --- 字段处理 ---
                # 1. 位置
                position = POS_MAP.get(row['POSITION'], '控球后卫')
                
                # 2. 国籍 (优先查Bio库，查不到用默认)
                country = country_map.get(p_id, 'USA')
                
                # 3. 身高 (带保护)
                height_m = safe_height_to_meters(row['HEIGHT'])
                
                # 4. 体重 (带保护)
                weight_kg = safe_weight_to_kg(row['WEIGHT'])

                # 5. 生日 (有些新秀可能生日暂时为空，这里原样保留或处理)
                birth_date = row['BIRTH_DATE'] if row['BIRTH_DATE'] else None

                all_players_list.append({
                    'player_id': p_id,
                    '姓名': row['PLAYER'],
                    '位置': position,
                    '球衣号': row['NUM'],
                    '身高': height_m,
                    '体重': weight_kg,
                    '出生日期': birth_date,
                    '国籍': country,
                    '当前球队ID': t_id
                })
            
            time.sleep(0.5) # 礼貌延迟
            
        except Exception as e:
            print(f"    ! {t_name} 获取失败: {e}")

    # 导出
    if all_players_list:
        df = pd.DataFrame(all_players_list)
        # 去重
        df.drop_duplicates(subset=['player_id'], keep='last', inplace=True)
        
        filename = '2_Player_Final.csv'
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        print(f"\n成功！已导出 {len(df)} 名球员到 {filename}")
        
        # --- 打印几个样本检查转换结果 ---
        print("\n=== 数据样本检查 (验证转换) ===")
        print(df[['姓名', '身高', '体重', '国籍']].head(5))
    else:
        print("未获取到任何数据，请检查网络。")

if __name__ == "__main__":
    export_players_final()
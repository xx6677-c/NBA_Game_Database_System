import pandas as pd

def fix_game_id_format():
    print("正在修正获胜球队ID格式...")
    
    # 读取 CSV
    df = pd.read_csv('3_Game.csv', encoding='utf-8-sig')
    
    # ================= 核心修改 =================
    # astype('Int64') 注意这里 I 是大写
    # 这是 pandas 专用的可空整数类型，它不会因为有空值就变 float
    df['获胜球队ID'] = df['获胜球队ID'].astype('Int64')
    # ==========================================
    
    # 保存
    output_file = '3_Game_Fixed.csv'
    df.to_csv(output_file, index=False, encoding='utf-8-sig')
    
    print(f"修正完成！文件已保存为: {output_file}")
    
    # 预览一下效果
    print("\n=== 预览 (注意 ID 后面没有 .0 了) ===")
    # 选取几行已结束的（有ID）和几行未开始的（无ID）
    print(df[['日期', '状态', '获胜球队ID']].iloc[[0, 1, -1]])

if __name__ == "__main__":
    fix_game_id_format()
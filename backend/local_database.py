"""
本地数据库模拟模块
用于在没有外部数据库连接时提供模拟数据
"""

import json
import os
from datetime import datetime

class LocalDatabase:
    """本地数据库模拟类"""
    
    def __init__(self):
        self.data_file = "local_data.json"
        self.init_sample_data()
    
    def init_sample_data(self):
        """初始化示例数据"""
        if not os.path.exists(self.data_file):
            sample_data = {
                "users": [
                    {
                        "user_id": 1,
                        "username": "admin",
                        "password": "$2b$12$LQv3c1yqBWVHrnG0q9QY0e",  # 密码: admin123
                        "role": "admin",
                        "register_time": "2024-01-01 10:00:00",
                        "last_login": "2024-11-04 15:30:00",
                        "email": "admin@example.com",
                        "phone": "13800138000"
                    },
                    {
                        "user_id": 2,
                        "username": "user1",
                        "password": "$2b$12$LQv3c1yqBWVHrnG0q9QY0e",  # 密码: user123
                        "role": "user",
                        "register_time": "2024-02-01 14:20:00",
                        "last_login": "2024-11-04 16:45:00",
                        "email": "user1@example.com",
                        "phone": "13900139000"
                    }
                ],
                "teams": [
                    {
                        "team_id": 1,
                        "name": "洛杉矶湖人",
                        "city": "洛杉矶",
                        "arena": "Crypto.com球馆",
                        "conference": "西部",
                        "founded_year": 1947
                    },
                    {
                        "team_id": 2,
                        "name": "金州勇士",
                        "city": "旧金山",
                        "arena": "大通中心",
                        "conference": "西部",
                        "founded_year": 1946
                    }
                ],
                "players": [
                    {
                        "player_id": 1,
                        "name": "勒布朗·詹姆斯",
                        "position": "小前锋",
                        "jersey_number": 23,
                        "height": "203cm",
                        "weight": "113kg",
                        "birth_date": "1984-12-30",
                        "nationality": "美国",
                        "team_name": "洛杉矶湖人"
                    },
                    {
                        "player_id": 2,
                        "name": "斯蒂芬·库里",
                        "position": "控球后卫",
                        "jersey_number": 30,
                        "height": "188cm",
                        "weight": "84kg",
                        "birth_date": "1988-03-14",
                        "nationality": "美国",
                        "team_name": "金州勇士"
                    }
                ],
                "games": [
                    {
                        "game_id": 1,
                        "season": "2023-2024",
                        "date": "2024-01-15 19:30:00",
                        "status": "finished",
                        "home_score": 108,
                        "away_score": 105,
                        "home_team": "洛杉矶湖人",
                        "away_team": "金州勇士",
                        "winner_team": "洛杉矶湖人",
                        "venue": "Crypto.com球馆"
                    }
                ],
                "posts": [
                    {
                        "post_id": 1,
                        "user_id": 1,
                        "title": "湖人vs勇士精彩比赛回顾",
                        "content": "这场比赛真是太精彩了！詹姆斯的关键三分决定了比赛胜负。",
                        "create_time": "2024-01-16 10:00:00",
                        "views": 150,
                        "likes": 25,
                        "season": "2023-2024",
                        "home_team": "洛杉矶湖人",
                        "away_team": "金州勇士"
                    }
                ],
                "ratings": [
                    {
                        "rating_id": 1,
                        "user_id": 1,
                        "player_id": 1,
                        "rating": 9.5,
                        "comment": "詹姆斯的表现一如既往的稳定",
                        "create_time": "2024-01-16 11:00:00",
                        "player_name": "勒布朗·詹姆斯",
                        "position": "小前锋",
                        "team_name": "洛杉矶湖人"
                    }
                ]
            }
            
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(sample_data, f, ensure_ascii=False, indent=2)
    
    def get_data(self):
        """获取所有数据"""
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    
    def save_data(self, data):
        """保存数据"""
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    # 用户相关操作
    def get_user_by_username(self, username):
        """根据用户名获取用户"""
        data = self.get_data()
        for user in data.get('users', []):
            if user['username'] == username:
                return user
        return None
    
    def get_user_by_id(self, user_id):
        """根据用户ID获取用户"""
        data = self.get_data()
        for user in data.get('users', []):
            if user['user_id'] == user_id:
                return user
        return None
    
    def update_user(self, user_id, update_data):
        """更新用户信息"""
        data = self.get_data()
        for i, user in enumerate(data.get('users', [])):
            if user['user_id'] == user_id:
                data['users'][i].update(update_data)
                self.save_data(data)
                return True
        return False
    
    # 帖子相关操作
    def get_user_posts(self, user_id):
        """获取用户帖子"""
        data = self.get_data()
        return [post for post in data.get('posts', []) if post['user_id'] == user_id]
    
    # 评分相关操作
    def get_user_ratings(self, user_id):
        """获取用户评分"""
        data = self.get_data()
        return [rating for rating in data.get('ratings', []) if rating['user_id'] == user_id]
    
    # 通用数据获取
    def get_teams(self):
        """获取所有球队"""
        return self.get_data().get('teams', [])
    
    def get_players(self, team_id=None):
        """获取球员列表"""
        players = self.get_data().get('players', [])
        if team_id:
            # 这里简化处理，实际应该根据team_id过滤
            return players
        return players
    
    def get_games(self):
        """获取比赛列表"""
        return self.get_data().get('games', [])
    
    def get_posts(self, game_id=None):
        """获取帖子列表"""
        posts = self.get_data().get('posts', [])
        if game_id:
            # 这里简化处理，实际应该根据game_id过滤
            return posts
        return posts

# 创建全局实例
local_db = LocalDatabase()
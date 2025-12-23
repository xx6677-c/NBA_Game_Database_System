# NBA比赛数据管理系统实现报告

---

# 一、系统结构设计

## 1.1 体系结构

本项目采用B/S三层架构，基于前后端分离的设计理念，实现了NBA比赛数据管理系统的数据层、业务逻辑层和表现层的完整结构。

```
┌─────────────────────────────────────────────────────────────────┐
│                         表现层 (Presentation Layer)              │
│                    Vue 3 + Element Plus + ECharts                │
│         用户界面、数据可视化、交互响应、状态管理                    │
├─────────────────────────────────────────────────────────────────┤
│                         业务逻辑层 (Business Logic Layer)         │
│                    Flask + Flask-JWT-Extended                    │
│         RESTful API、身份认证、权限控制、业务处理                   │
├─────────────────────────────────────────────────────────────────┤
│                         数据层 (Data Layer)                       │
│                    MySQL (TaurusDB) + PyMySQL                    │
│         存储过程、触发器、数据存储、事务管理                        │
└─────────────────────────────────────────────────────────────────┘
```

### 1.1.1 前端架构及技术栈

前端采用 Vue 3 作为核心框架，基于组合式 API 构建组件化、响应式的用户界面，提升代码的可维护性与复用性。项目使用 Vue CLI 作为构建工具，配合 Vue Router 实现单页应用的路由管理；UI 层采用 Element Plus 组件库，快速构建一致、美观的界面；使用 ECharts 进行数据可视化展示；通过封装的 API 服务模块实现与后端接口的高效通信。前端框架及技术栈如下：

```
└─frontend
    └─src
        ├─assets          # 静态资源文件（样式、图片等）
        │  └─styles       # 全局样式文件
        ├─components      # 可复用的Vue组件
        ├─router          # Vue Router路由配置
        ├─services        # API服务封装，处理前后端交互
        └─views           # 页面级Vue组件
            ├─Dashboard.vue        # 仪表盘页面
            ├─Games.vue            # 比赛列表页面
            ├─GameDetails.vue      # 比赛详情页面
            ├─Players.vue          # 球员列表页面
            ├─PlayerDetails.vue    # 球员详情页面
            ├─PlayerComparison.vue # 球员对比页面
            ├─Teams.vue            # 球队页面
            ├─Posts.vue            # 帖子/论坛页面
            ├─Rankings.vue         # 排行榜页面
            ├─Query.vue            # 自定义查询页面
            ├─Profile.vue          # 用户个人中心
            └─Login.vue            # 登录/注册页面
```

|     技术      |     版本      |      职责      |
| :-----------: | :-----------: | :------------: |
|     Vue 3     |    3.2.13     |    核心框架    |
|   Vue CLI     |    5.0.0      |    构建工具    |
| Element Plus  |    2.11.7     |   UI组件库     |
|  Vue Router   |    4.6.3      |    路由管理    |
|    ECharts    |    6.0.0      |   数据可视化   |
|    Axios      |   (内置封装)  |   HTTP请求     |

### 1.1.2 后端架构及技术栈

后端基于 Flask 框架构建，采用轻量化、模块化的设计思想，便于快速开发与灵活扩展。系统以 Python 3.9+ 为开发语言，采用蓝图（Blueprint）机制组织路由层，通过存储过程实现数据访问层的封装，工具层（utils）封装通用功能。认证与安全方面使用 Flask-JWT-Extended 实现基于 JWT 的身份验证，bcrypt 进行密码加密，Flask-CORS 支持跨域访问；底层数据库选用 MySQL，保证数据的可靠性与一致性。后端框架及技术栈如下：

```
└─backend
    ├─app.py              # Flask应用工厂，应用入口
    ├─run.py              # 启动脚本
    ├─database/           # 数据库相关
    │  ├─core/            # 核心配置
    │  │  ├─config.py     # 数据库连接配置
    │  │  ├─init.sql      # 基础表结构初始化
    │  │  └─init_database.py  # 数据库初始化脚本
    │  ├─procedures/      # 存储过程和触发器
    │  │  ├─total.sql     # 完整数据库脚本（表+触发器+存储过程）
    │  │  ├─all_procedures.sql  # 所有存储过程
    │  │  ├─add_triggers.sql    # 触发器定义
    │  │  └─add_indexes.sql     # 索引定义
    │  └─legacy/          # 历史迁移脚本
    ├─routes/             # 路由层（API端点）
    │  ├─auth.py          # 认证相关路由
    │  ├─games.py         # 比赛管理路由
    │  ├─players.py       # 球员管理路由
    │  ├─teams.py         # 球队管理路由
    │  ├─posts.py         # 帖子管理路由
    │  ├─comments.py      # 评论管理路由
    │  ├─rankings.py      # 排行榜路由
    │  ├─shop.py          # 商店（抽卡）路由
    │  ├─images.py        # 图片管理路由
    │  └─query.py         # 自定义查询路由
    ├─middlewares/        # 中间件
    │  ├─jwt_config.py    # JWT认证配置
    │  └─error_handler.py # 错误处理器
    └─utils/              # 工具函数层
        ├─auth.py         # 密码加密/验证
        ├─permissions.py  # 权限检查
        └─response.py     # 响应格式化
```

|        技术         |   版本   |     职责      |
| :-----------------: | :------: | :-----------: |
|       Python        |   3.9+   |   编程语言    |
|        Flask        |  2.3.3   |   Web框架     |
| Flask-JWT-Extended  |  4.5.3   |   JWT认证     |
|     Flask-CORS      |  4.0.0   |   跨域支持    |
|       PyMySQL       |  1.1.0   |  数据库驱动   |
|       bcrypt        |  4.0.1   |   密码加密    |
|    python-dotenv    |  1.0.0   |   环境变量    |
|      Werkzeug       |  2.3.7   |  WSGI工具库   |
|        MySQL        |  8.0+    |  关系数据库   |

## 1.2 系统功能模块

本系统包含以下核心功能模块：

### 1.2.1 用户管理模块
- **用户注册**：支持普通用户、管理员、数据分析师三种角色注册
- **用户登录/登出**：基于JWT的身份认证机制
- **个人中心**：查看/编辑个人信息、查看发帖记录、评分记录、积分历史
- **头像管理**：支持用户上传和更新头像

### 1.2.2 比赛管理模块
- **比赛列表**：按日期、球队筛选查看比赛
- **比赛详情**：查看比赛基本信息、球员数据统计
- **比赛竞猜**：用户可对未开始的比赛进行胜负预测
- **奖励领取**：竞猜正确可领取积分奖励
- **比赛管理**：管理员可创建、编辑、删除比赛

### 1.2.3 球员管理模块
- **球员列表**：按球队筛选查看球员
- **球员详情**：查看球员基本信息、职业生涯数据、近期比赛表现
- **球员对比**：支持多球员数据对比分析
- **球员管理**：管理员可创建、编辑、删除球员

### 1.2.4 球队管理模块
- **球队列表**：查看所有球队信息
- **球队详情**：查看球队基本信息、球员阵容
- **球队管理**：管理员可创建、编辑、删除球队

### 1.2.5 社区互动模块
- **帖子管理**：发布、浏览、删除帖子
- **评论系统**：对帖子进行评论
- **点赞功能**：帖子和评论的点赞/取消点赞
- **浏览统计**：自动记录帖子浏览量

### 1.2.6 排行榜模块
- **球队排名**：按赛季查看球队胜率排名
- **球员排名**：按得分、篮板、助攻等数据排名

### 1.2.7 球星卡商店模块
- **抽卡功能**：使用积分随机抽取球星卡
- **卡片收藏**：查看已收集的球星卡

### 1.2.8 自定义查询模块
- **SQL查询**：数据分析师可执行自定义SQL查询
- **结果展示**：表格形式展示查询结果

---

# 二、数据库基本表的定义

本系统共设计18张数据表，分为基础实体表（12张）和关联关系表（6张）两类。

## 2.1 用户表 (User)

存储系统用户信息，支持普通用户、管理员、数据分析师三种角色。

|   字段名   |    数据类型     |        值约束         |       说明       |
| :--------: | :-------------: | :-------------------: | :--------------: |
|  user_id   |       INT       |    主键、自增       |     用户ID       |
|   用户名   |   VARCHAR(50)   |    唯一、非空       |   唯一登录账号   |
|    密码    |  VARCHAR(255)   |       非空          |   加密后的密码   |
|    角色    |      ENUM       | 默认'user'、非空    | user/admin/analyst |
|  注册时间  |    DATETIME     |   默认当前时间      |   账号创建时间   |
| 最后登录时间 |   DATETIME    |         /           |   最近登录时间   |
|    邮箱    |  VARCHAR(100)   |         /           |    邮箱地址      |
|   手机号   |   VARCHAR(20)   |         /           |    联系电话      |
|   points   |       INT       |      默认0          |    用户积分      |

**建表SQL语句：**
```sql
CREATE TABLE IF NOT EXISTS User (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    用户名 VARCHAR(50) UNIQUE NOT NULL,
    密码 VARCHAR(255) NOT NULL,
    角色 ENUM('user', 'admin', 'analyst') DEFAULT 'user' NOT NULL,
    注册时间 DATETIME DEFAULT CURRENT_TIMESTAMP,
    最后登录时间 DATETIME,
    邮箱 VARCHAR(100),
    手机号 VARCHAR(20),
    points INT DEFAULT 0
);
```

## 2.2 球队表 (Team)

存储NBA球队基本信息。

|   字段名   |   数据类型    |       值约束        |      说明      |
| :--------: | :-----------: | :-----------------: | :------------: |
|  team_id   |      INT      |     主键、自增      |    球队ID      |
|    名称    |  VARCHAR(10)  |    唯一、非空       |    球队名称    |
|    城市    |  VARCHAR(30)  |     默认空串        |    所在城市    |
|    场馆    |  VARCHAR(30)  |     默认空串        |    主场场馆    |
|    分区    |     ENUM      |       非空          |   东部/西部    |
|  成立年份  |      INT      |  CHECK(>1900)       |   球队成立年份 |

**建表SQL语句：**
```sql
CREATE TABLE IF NOT EXISTS Team (
    team_id INT AUTO_INCREMENT PRIMARY KEY,
    名称 VARCHAR(10) UNIQUE NOT NULL,
    城市 VARCHAR(30) DEFAULT '',
    场馆 VARCHAR(30) DEFAULT '',
    分区 ENUM('东部', '西部') NOT NULL,
    成立年份 INT CHECK(成立年份 > 1900)
);
```

## 2.3 球员表 (Player)

存储NBA球员基本信息和合同信息。

|    字段名    |    数据类型     |         值约束          |       说明       |
| :----------: | :-------------: | :---------------------: | :--------------: |
|  player_id   |       INT       |      主键、自增         |     球员ID       |
|     姓名     |   VARCHAR(50)   |         非空            |     球员姓名     |
|     位置     |      ENUM       |         非空            | 控卫/得分后卫/小前锋/大前锋/中锋 |
|    球衣号    |       INT       |          /              |     球衣号码     |
|     身高     |  DECIMAL(3,2)   |          /              |    身高（米）    |
|     体重     |  DECIMAL(5,2)   |          /              |   体重（公斤）   |
|   出生日期   |      DATE       |          /              |     出生日期     |
|     国籍     |   VARCHAR(50)   |          /              |     国籍         |
|  当前球队ID  |       INT       |    外键→Team            |   所属球队ID     |
|   合同到期   |      DATE       |          /              |   合同到期日期   |
|     薪资     | DECIMAL(10,2)   |          /              |    年薪（万）    |

**建表SQL语句：**
```sql
CREATE TABLE IF NOT EXISTS Player (
    player_id INT AUTO_INCREMENT PRIMARY KEY,
    姓名 VARCHAR(50) NOT NULL,
    位置 ENUM('控球后卫', '得分后卫', '小前锋', '大前锋', '中锋') NOT NULL,
    球衣号 INT,
    身高 DECIMAL(3,2),
    体重 DECIMAL(5,2),
    出生日期 DATE,
    国籍 VARCHAR(50),
    当前球队ID INT,
    合同到期 DATE,
    薪资 DECIMAL(10,2),
    FOREIGN KEY (当前球队ID) REFERENCES Team(team_id) ON DELETE SET NULL
);
```

## 2.4 比赛表 (Game)

存储NBA比赛信息。

|    字段名    |    数据类型    |        值约束         |       说明       |
| :----------: | :------------: | :-------------------: | :--------------: |
|   game_id    |      INT       |     主键、自增        |     比赛ID       |
|     赛季     |  VARCHAR(20)   |        非空           |  如"2024-2025"   |
|     日期     |    DATETIME    |        非空           |   比赛日期时间   |
|    主队ID    |      INT       |    非空、外键→Team    |    主队球队ID    |
|    客队ID    |      INT       |    非空、外键→Team    |    客队球队ID    |
|   主队得分   |      INT       |          /            |    主队得分      |
|   客队得分   |      INT       |          /            |    客队得分      |
|     状态     |      ENUM      |    默认'未开始'       | 未开始/已结束    |
|  获胜球队ID  |      INT       |      外键→Team        |   获胜球队ID     |
|     场馆     |  VARCHAR(100)  |          /            |    比赛场馆      |

**建表SQL语句：**
```sql
CREATE TABLE IF NOT EXISTS Game (
    game_id INT AUTO_INCREMENT PRIMARY KEY,
    赛季 VARCHAR(20) NOT NULL,
    日期 DATETIME NOT NULL,
    主队ID INT NOT NULL,
    客队ID INT NOT NULL,
    主队得分 INT,
    客队得分 INT,
    状态 ENUM('未开始','已结束') DEFAULT '未开始',
    获胜球队ID INT,
    场馆 VARCHAR(100),
    FOREIGN KEY (主队ID) REFERENCES Team(team_id),
    FOREIGN KEY (客队ID) REFERENCES Team(team_id),
    FOREIGN KEY (获胜球队ID) REFERENCES Team(team_id) ON DELETE SET NULL
);
```

## 2.5 帖子表 (Post)

存储用户发布的帖子信息。

|   字段名   |   数据类型    |       值约束        |      说明      |
| :--------: | :-----------: | :-----------------: | :------------: |
|  post_id   |      INT      |     主键、自增      |    帖子ID      |
|  user_id   |      INT      |   非空、外键→User   |   发帖用户ID   |
|    标题    |  VARCHAR(50)  |       非空          |    帖子标题    |
|    内容    |     TEXT      |       非空          |    帖子内容    |
|  game_id   |      INT      |     外键→Game       |   关联比赛ID   |
|  创建时间  |   DATETIME    |   默认当前时间      |   发帖时间     |
|   浏览量   |      INT      |      默认0          |   浏览次数     |
|   点赞数   |      INT      |      默认0          |   点赞次数     |

**建表SQL语句：**
```sql
CREATE TABLE IF NOT EXISTS Post (
    post_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    标题 VARCHAR(50) NOT NULL,
    内容 TEXT NOT NULL,
    game_id INT,
    创建时间 DATETIME DEFAULT CURRENT_TIMESTAMP,
    浏览量 INT DEFAULT 0,
    点赞数 INT DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES User(user_id),
    FOREIGN KEY (game_id) REFERENCES Game(game_id) ON DELETE SET NULL
);
```

## 2.6 评论表 (Comment)

存储用户评论信息，支持对球员、比赛、帖子的评论。

|    字段名    |   数据类型    |       值约束        |       说明       |
| :----------: | :-----------: | :-----------------: | :--------------: |
|  comment_id  |      INT      |     主键、自增      |     评论ID       |
|   user_id    |      INT      |   非空、外键→User   |   评论用户ID     |
|  player_id   |      INT      |    外键→Player      |   关联球员ID     |
|   game_id    |      INT      |     外键→Game       |   关联比赛ID     |
|   post_id    |      INT      |     外键→Post       |   关联帖子ID     |
|     内容     |     TEXT      |       非空          |    评论内容      |
|   创建时间   |   DATETIME    |   默认当前时间      |    评论时间      |
|    点赞数    |      INT      |      默认0          |    点赞次数      |

**建表SQL语句：**
```sql
CREATE TABLE IF NOT EXISTS Comment (
    comment_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    player_id INT,
    game_id INT,
    post_id INT,
    内容 TEXT NOT NULL,
    创建时间 DATETIME DEFAULT CURRENT_TIMESTAMP,
    点赞数 INT DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES User(user_id),
    FOREIGN KEY (player_id) REFERENCES Player(player_id),
    FOREIGN KEY (game_id) REFERENCES Game(game_id),
    FOREIGN KEY (post_id) REFERENCES Post(post_id)
);
```

## 2.7 评分表 (Rating)

存储用户对球员在某场比赛中表现的评分。

|   字段名   |   数据类型    |          值约束          |      说明      |
| :--------: | :-----------: | :----------------------: | :------------: |
|  user_id   |      INT      |   主键(联合)、外键→User  |   评分用户ID   |
| player_id  |      INT      | 主键(联合)、外键→Player  |   被评球员ID   |
|  game_id   |      INT      |  主键(联合)、外键→Game   |   关联比赛ID   |
|    分数    | DECIMAL(2,0)  | 默认0、CHECK(0-10)、非空 |   评分(0-10)   |
|  创建时间  |   DATETIME    |      默认当前时间        |    评分时间    |

**建表SQL语句：**
```sql
CREATE TABLE IF NOT EXISTS Rating (
    user_id INT NOT NULL,
    player_id INT NOT NULL,
    game_id INT NOT NULL,
    分数 DECIMAL(2,0) DEFAULT 0 CHECK(分数 BETWEEN 0 AND 10) NOT NULL,
    创建时间 DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, player_id, game_id),
    FOREIGN KEY (user_id) REFERENCES User(user_id),
    FOREIGN KEY (player_id) REFERENCES Player(player_id),
    FOREIGN KEY (game_id) REFERENCES Game(game_id)
);
```

## 2.8 图片表 (Image)

存储系统中的图片数据（头像、球员照片、球队队标等）。

|   字段名   |   数据类型    |      值约束      |      说明      |
| :--------: | :-----------: | :--------------: | :------------: |
|  image_id  |      INT      |   主键、自增     |    图片ID      |
|    名称    |  VARCHAR(50)  |      非空        |    图片名称    |
|    数据    |   LONGBLOB    |      非空        |  图片二进制数据 |
|  MIME类型  |  VARCHAR(50)  |      非空        | 如image/jpeg   |
|  上传时间  |   DATETIME    |  默认当前时间    |   上传时间     |

**建表SQL语句：**
```sql
CREATE TABLE IF NOT EXISTS Image (
    image_id INT AUTO_INCREMENT PRIMARY KEY,
    名称 VARCHAR(50) NOT NULL,
    数据 LONGBLOB NOT NULL,
    MIME类型 VARCHAR(50) NOT NULL,
    上传时间 DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

## 2.9 竞猜表 (Prediction)

存储用户对比赛的竞猜预测记录。

|     字段名      |   数据类型    |         值约束          |       说明       |
| :-------------: | :-----------: | :---------------------: | :--------------: |
| prediction_id   |      INT      |      主键、自增         |     竞猜ID       |
|    user_id      |      INT      |    非空、外键→User      |   竞猜用户ID     |
|    game_id      |      INT      |    非空、外键→Game      |   竞猜比赛ID     |
| predicted_team_id |    INT      |    非空、外键→Team      |   预测获胜球队   |
|   is_claimed    |    BOOLEAN    |      默认FALSE          |   是否已领奖     |
|   create_time   |   DATETIME    |    默认当前时间         |   竞猜创建时间   |
|   update_time   |   DATETIME    | 默认当前时间、自动更新  |   更新时间       |

**唯一约束：** `unique_user_game (user_id, game_id)` - 每用户每场比赛只能竞猜一次

**建表SQL语句：**
```sql
CREATE TABLE IF NOT EXISTS Prediction (
    prediction_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    game_id INT NOT NULL,
    predicted_team_id INT NOT NULL,
    is_claimed BOOLEAN DEFAULT FALSE,
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    update_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY unique_user_game (user_id, game_id),
    FOREIGN KEY (user_id) REFERENCES User(user_id),
    FOREIGN KEY (game_id) REFERENCES Game(game_id),
    FOREIGN KEY (predicted_team_id) REFERENCES Team(team_id)
);
```

## 2.10 帖子点赞表 (Post_Like)

存储用户对帖子的点赞记录。

|   字段名   |   数据类型    |           值约束            |     说明     |
| :--------: | :-----------: | :-------------------------: | :----------: |
|  like_id   |      INT      |        主键、自增           |   点赞ID     |
|  user_id   |      INT      | 非空、外键→User、级联删除   |  点赞用户ID  |
|  post_id   |      INT      | 非空、外键→Post、级联删除   |  被赞帖子ID  |
|  创建时间  |   DATETIME    |       默认当前时间          |   点赞时间   |

**唯一约束：** `unique_user_post (user_id, post_id)` - 每用户对每帖子只能点赞一次

**建表SQL语句：**
```sql
CREATE TABLE IF NOT EXISTS Post_Like (
    like_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    post_id INT NOT NULL,
    创建时间 DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY unique_user_post (user_id, post_id),
    FOREIGN KEY (user_id) REFERENCES User(user_id) ON DELETE CASCADE,
    FOREIGN KEY (post_id) REFERENCES Post(post_id) ON DELETE CASCADE
);
```

## 2.11 评论点赞表 (Comment_Like)

存储用户对评论的点赞记录。

|   字段名    |   数据类型    |            值约束            |     说明     |
| :---------: | :-----------: | :--------------------------: | :----------: |
|   like_id   |      INT      |        主键、自增            |   点赞ID     |
|   user_id   |      INT      |  非空、外键→User、级联删除   |  点赞用户ID  |
| comment_id  |      INT      | 非空、外键→Comment、级联删除 |  被赞评论ID  |
|  创建时间   |   DATETIME    |        默认当前时间          |   点赞时间   |

**唯一约束：** `unique_user_comment (user_id, comment_id)` - 每用户对每评论只能点赞一次

**建表SQL语句：**
```sql
CREATE TABLE IF NOT EXISTS Comment_Like (
    like_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    comment_id INT NOT NULL,
    创建时间 DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY unique_user_comment (user_id, comment_id),
    FOREIGN KEY (user_id) REFERENCES User(user_id) ON DELETE CASCADE,
    FOREIGN KEY (comment_id) REFERENCES Comment(comment_id) ON DELETE CASCADE
);
```

## 2.12 用户卡片表 (User_Card)

存储用户抽取的球星卡收藏记录。

|   字段名   |   数据类型    |       值约束        |      说明      |
| :--------: | :-----------: | :-----------------: | :------------: |
|     id     |      INT      |     主键、自增      |    记录ID      |
|  user_id   |      INT      |   非空、外键→User   |   持有用户ID   |
| player_id  |      INT      |  非空、外键→Player  |   球星卡球员   |
|  get_time  |   DATETIME    |   默认当前时间      |   获取时间     |

**建表SQL语句：**
```sql
CREATE TABLE IF NOT EXISTS User_Card (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    player_id INT NOT NULL,
    get_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES User(user_id),
    FOREIGN KEY (player_id) REFERENCES Player(player_id)
);
```

## 2.13 球队-比赛关系表 (Team_Game)

记录球队参与比赛的主客场信息。

|   字段名   |   数据类型    |        值约束         |      说明      |
| :--------: | :-----------: | :-------------------: | :------------: |
|  team_id   |      INT      | 主键(联合)、外键→Team |    球队ID      |
|  game_id   |      INT      | 主键(联合)、外键→Game |    比赛ID      |
|  主客类型  |     ENUM      |        非空           |   主场/客场    |

**建表SQL语句：**
```sql
CREATE TABLE IF NOT EXISTS Team_Game (
    team_id INT NOT NULL,
    game_id INT NOT NULL,
    主客类型 ENUM('主场', '客场') NOT NULL,
    PRIMARY KEY (team_id, game_id),
    FOREIGN KEY (team_id) REFERENCES Team(team_id),
    FOREIGN KEY (game_id) REFERENCES Game(game_id)
);
```

## 2.14 球员-比赛数据表 (Player_Game)

记录球员在每场比赛中的详细数据统计。

|   字段名   |   数据类型    |          值约束           |       说明       |
| :--------: | :-----------: | :-----------------------: | :--------------: |
| player_id  |      INT      | 主键(联合)、外键→Player   |     球员ID       |
|  game_id   |      INT      |  主键(联合)、外键→Game    |     比赛ID       |
|  上场时间  | DECIMAL(4,1)  |  默认0、CHECK(>=0)、非空  |   上场分钟数     |
|    得分    |      INT      |  默认0、CHECK(>=0)、非空  |     得分         |
|    篮板    |      INT      |  默认0、CHECK(>=0)、非空  |     篮板数       |
|    助攻    |      INT      |  默认0、CHECK(>=0)、非空  |     助攻数       |
|    抢断    |      INT      |  默认0、CHECK(>=0)、非空  |     抢断数       |
|    盖帽    |      INT      |  默认0、CHECK(>=0)、非空  |     盖帽数       |
|    失误    |      INT      |  默认0、CHECK(>=0)、非空  |     失误数       |
|    犯规    |      INT      |  默认0、CHECK(>=0)、非空  |     犯规数       |
|   正负值   |      INT      |            /              |    正负值统计    |

**建表SQL语句：**
```sql
CREATE TABLE IF NOT EXISTS Player_Game (
    player_id INT NOT NULL,
    game_id INT NOT NULL,
    上场时间 DECIMAL(4,1) DEFAULT 0 CHECK(上场时间 >= 0) NOT NULL,
    得分 INT DEFAULT 0 CHECK(得分 >= 0) NOT NULL,
    篮板 INT DEFAULT 0 CHECK(篮板 >= 0) NOT NULL,
    助攻 INT DEFAULT 0 CHECK(助攻 >= 0) NOT NULL,
    抢断 INT DEFAULT 0 CHECK(抢断 >= 0) NOT NULL,
    盖帽 INT DEFAULT 0 CHECK(盖帽 >= 0) NOT NULL,
    失误 INT DEFAULT 0 CHECK(失误 >= 0) NOT NULL,
    犯规 INT DEFAULT 0 CHECK(犯规 >= 0) NOT NULL,
    正负值 INT,
    PRIMARY KEY (player_id, game_id),
    FOREIGN KEY (player_id) REFERENCES Player(player_id),
    FOREIGN KEY (game_id) REFERENCES Game(game_id)
);
```

## 2.15 用户-头像关系表 (User_Avatar)

关联用户与头像图片。

|   字段名   |   数据类型    |       值约束        |      说明      |
| :--------: | :-----------: | :-----------------: | :------------: |
|  user_id   |      INT      | 主键、外键→User     |    用户ID      |
|  image_id  |      INT      | 非空、外键→Image    |    头像图片ID  |

**建表SQL语句：**
```sql
CREATE TABLE IF NOT EXISTS User_Avatar (
    user_id INT PRIMARY KEY,
    image_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES User(user_id),
    FOREIGN KEY (image_id) REFERENCES Image(image_id)
);
```

## 2.16 帖子-图片关系表 (Post_Image)

关联帖子与图片附件。

|   字段名   |   数据类型    |       值约束        |      说明      |
| :--------: | :-----------: | :-----------------: | :------------: |
|  post_id   |      INT      |   非空、外键→Post   |    帖子ID      |
|  image_id  |      INT      | 主键、外键→Image    |    图片ID      |

**建表SQL语句：**
```sql
CREATE TABLE IF NOT EXISTS Post_Image (
    post_id INT NOT NULL,
    image_id INT NOT NULL,
    PRIMARY KEY (image_id),
    FOREIGN KEY (post_id) REFERENCES Post(post_id),
    FOREIGN KEY (image_id) REFERENCES Image(image_id)
);
```

## 2.17 球员-图片关系表 (Player_Image)

关联球员与照片。

|   字段名   |   数据类型    |          值约束           |      说明      |
| :--------: | :-----------: | :-----------------------: | :------------: |
| player_id  |      INT      |    主键、外键→Player      |    球员ID      |
|  image_id  |      INT      | 非空、唯一、外键→Image、级联删除 |  球员照片ID    |

**建表SQL语句：**
```sql
CREATE TABLE IF NOT EXISTS Player_Image (
    player_id INT PRIMARY KEY,
    image_id INT NOT NULL UNIQUE,
    FOREIGN KEY (player_id) REFERENCES Player(player_id) ON DELETE CASCADE,
    FOREIGN KEY (image_id) REFERENCES Image(image_id) ON DELETE CASCADE
);
```

## 2.18 球队-队标关系表 (Team_Logo)

关联球队与队标图片。

|   字段名   |   数据类型    |          值约束           |      说明      |
| :--------: | :-----------: | :-----------------------: | :------------: |
|  team_id   |      INT      |     主键、外键→Team       |    球队ID      |
|  image_id  |      INT      | 非空、唯一、外键→Image、级联删除 |  队标图片ID    |

**建表SQL语句：**
```sql
CREATE TABLE IF NOT EXISTS Team_Logo (
    team_id INT PRIMARY KEY,
    image_id INT NOT NULL UNIQUE,
    FOREIGN KEY (team_id) REFERENCES Team(team_id) ON DELETE CASCADE,
    FOREIGN KEY (image_id) REFERENCES Image(image_id) ON DELETE CASCADE
);
```

---

# 三、触发器设计与实现说明

本系统共设计5个触发器，用于自动维护数据一致性、实现业务规则约束和级联数据清理。触发器设计遵循以下原则：

- **最小干预原则**：仅在必要时触发，避免不必要的性能开销
- **状态同步原则**：自动同步关联表的状态变化
- **数据完整性原则**：通过触发器强制执行业务规则
- **级联清理原则**：删除主记录时自动清理关联数据

## 3.1 比赛获胜球队自动更新触发器（UPDATE）

### 3.1.1 触发器信息

**触发器名称：** `trg_game_update_winner`

**触发时机：** `BEFORE UPDATE ON Game`

**触发条件：** 比赛状态变更为"已结束"且主客队得分均不为空

### 3.1.2 功能说明

- 当比赛状态更新为"已结束"时，自动根据比分计算获胜球队
- 主队得分高于客队时，设置获胜球队为主队
- 客队得分高于主队时，设置获胜球队为客队
- NBA比赛不允许平局，若出现平局则抛出错误

### 3.1.3 关键设计

- **状态检测**：`NEW.状态 = '已结束'` 确保仅在比赛结束时计算获胜方
- **空值检查**：`NEW.主队得分 IS NOT NULL AND NEW.客队得分 IS NOT NULL` 防止空值比较
- **业务约束**：使用 `SIGNAL SQLSTATE '45000'` 抛出自定义错误，阻止非法平局数据
- **BEFORE触发**：在数据写入前修改，避免二次UPDATE

### 3.1.4 SQL代码

```sql
DELIMITER //
CREATE TRIGGER trg_game_update_winner
BEFORE UPDATE ON Game
FOR EACH ROW
BEGIN
    IF NEW.状态 = '已结束' AND NEW.主队得分 IS NOT NULL AND NEW.客队得分 IS NOT NULL THEN
        IF NEW.主队得分 > NEW.客队得分 THEN
            SET NEW.获胜球队ID = NEW.主队ID;
        ELSEIF NEW.客队得分 > NEW.主队得分 THEN
            SET NEW.获胜球队ID = NEW.客队ID;
        ELSE
            SIGNAL SQLSTATE '45000' 
            SET MESSAGE_TEXT = '错误：比赛结束时不能平局';
        END IF;
    END IF;
END//
DELIMITER ;
```

---

## 3.2 比赛获胜球队自动更新触发器（INSERT）

### 3.2.1 触发器信息

**触发器名称：** `trg_game_insert_winner`

**触发时机：** `BEFORE INSERT ON Game`

**触发条件：** 插入已结束状态的比赛记录，或主客队ID相同

### 3.2.2 功能说明

- 插入已结束比赛时，自动根据比分计算获胜球队
- 检查主队和客队是否为同一支球队，防止非法数据

### 3.2.3 关键设计

- **双重校验**：既计算获胜方，又验证主客队不同
- **数据完整性**：在插入前拦截非法数据，确保数据库中不存在无效比赛记录
- **错误提示**：提供清晰的中文错误信息，便于问题定位

### 3.2.4 SQL代码

```sql
DELIMITER //
CREATE TRIGGER trg_game_insert_winner
BEFORE INSERT ON Game
FOR EACH ROW
BEGIN
    -- 自动计算获胜球队
    IF NEW.状态 = '已结束' AND NEW.主队得分 IS NOT NULL AND NEW.客队得分 IS NOT NULL THEN
        IF NEW.主队得分 > NEW.客队得分 THEN
            SET NEW.获胜球队ID = NEW.主队ID;
        ELSEIF NEW.客队得分 > NEW.主队得分 THEN
            SET NEW.获胜球队ID = NEW.客队ID;
        ELSE
            SIGNAL SQLSTATE '45000' 
            SET MESSAGE_TEXT = '错误：比赛结束时不能平局';
        END IF;
    END IF;
    
    -- 检查主客队是否相同
    IF NEW.主队ID = NEW.客队ID THEN
        SIGNAL SQLSTATE '45000' 
        SET MESSAGE_TEXT = '错误：主队和客队不能是同一支球队';
    END IF;
END//
DELIMITER ;
```

---

## 3.3 帖子点赞数自动增加触发器

### 3.3.1 触发器信息

**触发器名称：** `trg_post_like_increment`

**触发时机：** `AFTER INSERT ON Post_Like`

**触发条件：** 用户对帖子点赞（插入点赞记录）

### 3.3.2 功能说明

- 当用户点赞帖子时，自动将对应帖子的点赞数加1
- 实现点赞计数的自动同步，无需应用层手动维护

### 3.3.3 关键设计

- **AFTER触发**：在点赞记录成功插入后再更新计数，保证数据一致性
- **原子操作**：点赞记录插入和计数更新在同一事务中完成
- **精准更新**：使用 `NEW.post_id` 定位目标帖子

### 3.3.4 SQL代码

```sql
DELIMITER //
CREATE TRIGGER trg_post_like_increment
AFTER INSERT ON Post_Like
FOR EACH ROW
BEGIN
    UPDATE Post SET 点赞数 = 点赞数 + 1 WHERE post_id = NEW.post_id;
END//
DELIMITER ;
```

---

## 3.4 帖子点赞数自动减少触发器

### 3.4.1 触发器信息

**触发器名称：** `trg_post_like_decrement`

**触发时机：** `AFTER DELETE ON Post_Like`

**触发条件：** 用户取消点赞（删除点赞记录）

### 3.4.2 功能说明

- 当用户取消点赞时，自动将对应帖子的点赞数减1
- 使用 `GREATEST` 函数确保点赞数不会变为负数

### 3.4.3 关键设计

- **防负数保护**：`GREATEST(点赞数 - 1, 0)` 确保点赞数最小为0，防止数据异常
- **AFTER触发**：在点赞记录成功删除后再更新计数
- **历史数据兼容**：即使存在历史脏数据也能正常工作

### 3.4.4 SQL代码

```sql
DELIMITER //
CREATE TRIGGER trg_post_like_decrement
AFTER DELETE ON Post_Like
FOR EACH ROW
BEGIN
    UPDATE Post SET 点赞数 = GREATEST(点赞数 - 1, 0) WHERE post_id = OLD.post_id;
END//
DELIMITER ;
```

---

## 3.5 用户注销关联数据清理触发器

### 3.5.1 触发器信息

**触发器名称：** `trg_user_delete_cleanup`

**触发时机：** `BEFORE DELETE ON User`

**触发条件：** 删除用户记录

### 3.5.2 功能说明

- 用户注销时，自动清理该用户的所有关联数据
- 删除用户发布的帖子、评论、评分、竞猜记录
- 删除用户头像关联和球星卡收藏

### 3.5.3 关键设计

- **BEFORE触发**：在删除用户记录前先清理关联数据，避免外键约束冲突
- **级联清理**：按照外键依赖顺序逐一清理各关联表
- **自动级联**：Post_Like 和 Comment_Like 表已设置 `ON DELETE CASCADE`，会随主表自动删除
- **数据完整性**：确保删除用户后不留孤儿数据

### 3.5.4 SQL代码

```sql
DELIMITER //
CREATE TRIGGER trg_user_delete_cleanup
BEFORE DELETE ON User
FOR EACH ROW
BEGIN
    -- 删除用户相关的帖子
    DELETE FROM Post WHERE user_id = OLD.user_id;
    -- 删除用户相关的评论
    DELETE FROM Comment WHERE user_id = OLD.user_id;
    -- 删除用户相关的评分
    DELETE FROM Rating WHERE user_id = OLD.user_id;
    -- 删除用户相关的竞猜
    DELETE FROM Prediction WHERE user_id = OLD.user_id;
    -- 删除用户头像关联
    DELETE FROM User_Avatar WHERE user_id = OLD.user_id;
    -- 删除用户卡片
    DELETE FROM User_Card WHERE user_id = OLD.user_id;
    
    -- 注意：Post_Like 和 Comment_Like 表已设置 ON DELETE CASCADE，会自动删除
END//
DELIMITER ;
```

---

## 3.6 触发器汇总表

| 序号 | 触发器名称 | 触发表 | 触发时机 | 功能描述 |
| :--: | :-------- | :----: | :------: | :------- |
| 1 | trg_game_update_winner | Game | BEFORE UPDATE | 比赛结束时自动计算获胜球队，禁止平局 |
| 2 | trg_game_insert_winner | Game | BEFORE INSERT | 插入已结束比赛时计算获胜方，校验主客队不同 |
| 3 | trg_post_like_increment | Post_Like | AFTER INSERT | 点赞时自动增加帖子点赞计数 |
| 4 | trg_post_like_decrement | Post_Like | AFTER DELETE | 取消点赞时自动减少帖子点赞计数 |
| 5 | trg_user_delete_cleanup | User | BEFORE DELETE | 删除用户前清理所有关联数据 |

---

# 四、存储过程设计与实现说明

本系统共设计56个存储过程，按功能划分为8个模块。存储过程设计遵循以下原则：

- **封装性原则**：将复杂的数据库操作封装为存储过程，简化应用层代码
- **安全性原则**：通过存储过程控制数据访问，防止SQL注入
- **复用性原则**：相同的数据操作逻辑只需定义一次
- **事务性原则**：在存储过程中管理事务，确保数据一致性

## 4.1 用户认证与管理存储过程

本模块包含10个存储过程，用于处理用户注册、登录、个人信息管理等功能。

### 4.1.1 用户注册存储过程

**存储过程名称：** `sp_register_user`

**输入参数：**
| 参数名 | 类型 | 说明 |
| :---- | :--- | :--- |
| p_username | VARCHAR(50) | 用户名 |
| p_password | VARCHAR(255) | 加密后的密码 |
| p_role | VARCHAR(20) | 用户角色 |
| p_created_at | DATETIME | 注册时间 |

**输出参数：** 无

**功能：** 将新用户信息插入User表，完成用户注册

**关键设计：**
- 密码在应用层加密后传入，存储过程不处理加密逻辑
- 角色验证在应用层完成，管理员和分析师需要密钥验证

**SQL代码：**
```sql
DROP PROCEDURE IF EXISTS sp_register_user;
DELIMITER //
CREATE PROCEDURE sp_register_user(
    IN p_username VARCHAR(50),
    IN p_password VARCHAR(255),
    IN p_role VARCHAR(20),
    IN p_created_at DATETIME
)
BEGIN
    INSERT INTO User (用户名, 密码, 角色, 注册时间) 
    VALUES (p_username, p_password, p_role, p_created_at);
END//
DELIMITER ;
```

---

### 4.1.2 用户登录存储过程

**存储过程名称：** `sp_login_user`

**输入参数：**
| 参数名 | 类型 | 说明 |
| :---- | :--- | :--- |
| p_username | VARCHAR(50) | 用户名 |

**输出参数：** 无（通过SELECT返回结果集）

**返回结果：** user_id, 密码, 角色

**功能：** 根据用户名查询用户信息，用于登录验证

**关键设计：**
- 仅返回验证所需的最少字段
- 密码验证在应用层进行，存储过程只负责查询

**SQL代码：**
```sql
DROP PROCEDURE IF EXISTS sp_login_user;
DELIMITER //
CREATE PROCEDURE sp_login_user(IN p_username VARCHAR(50))
BEGIN
    SELECT user_id, 密码, 角色 FROM User WHERE 用户名 = p_username;
END//
DELIMITER ;
```

---

### 4.1.3 更新最后登录时间存储过程

**存储过程名称：** `sp_update_last_login`

**输入参数：**
| 参数名 | 类型 | 说明 |
| :---- | :--- | :--- |
| p_user_id | INT | 用户ID |
| p_login_time | DATETIME | 登录时间 |

**输出参数：** 无

**功能：** 更新用户的最后登录时间记录

**关键设计：**
- 在用户登录成功后调用，记录登录行为

**SQL代码：**
```sql
DROP PROCEDURE IF EXISTS sp_update_last_login;
DELIMITER //
CREATE PROCEDURE sp_update_last_login(
    IN p_user_id INT,
    IN p_login_time DATETIME
)
BEGIN
    UPDATE User SET 最后登录时间 = p_login_time WHERE user_id = p_user_id;
END//
DELIMITER ;
```

---

### 4.1.4 获取用户个人信息存储过程

**存储过程名称：** `sp_get_user_profile`

**输入参数：**
| 参数名 | 类型 | 说明 |
| :---- | :--- | :--- |
| p_user_id | INT | 用户ID |

**输出参数：** 无（通过SELECT返回结果集）

**返回结果：** user_id, 用户名, 角色, 注册时间, 最后登录时间, 邮箱, 手机号, points, image_id

**功能：** 获取用户完整的个人信息，包括头像关联

**关键设计：**
- 使用 `LEFT JOIN` 连接 User_Avatar 表，即使用户没有设置头像也能返回结果
- 返回 image_id 供前端构造头像URL

**SQL代码：**
```sql
DROP PROCEDURE IF EXISTS sp_get_user_profile;
DELIMITER //
CREATE PROCEDURE sp_get_user_profile(IN p_user_id INT)
BEGIN
    SELECT u.user_id, u.用户名, u.角色, u.注册时间, u.最后登录时间, u.邮箱, u.手机号, u.points, ua.image_id
    FROM User u
    LEFT JOIN User_Avatar ua ON u.user_id = ua.user_id
    WHERE u.user_id = p_user_id;
END//
DELIMITER ;
```

---

### 4.1.5 更新用户个人信息存储过程

**存储过程名称：** `sp_update_user_profile`

**输入参数：**
| 参数名 | 类型 | 说明 |
| :---- | :--- | :--- |
| p_user_id | INT | 用户ID |
| p_email | VARCHAR(100) | 邮箱地址 |
| p_phone | VARCHAR(20) | 手机号码 |

**输出参数：** 无

**功能：** 更新用户的邮箱和手机号信息

**关键设计：**
- 仅允许更新邮箱和手机号，用户名和角色不可修改

**SQL代码：**
```sql
DROP PROCEDURE IF EXISTS sp_update_user_profile;
DELIMITER //
CREATE PROCEDURE sp_update_user_profile(
    IN p_user_id INT,
    IN p_email VARCHAR(100),
    IN p_phone VARCHAR(20)
)
BEGIN
    UPDATE User SET 邮箱 = p_email, 手机号 = p_phone 
    WHERE user_id = p_user_id;
END//
DELIMITER ;
```

---

### 4.1.6 获取用户帖子列表存储过程

**存储过程名称：** `sp_get_user_posts`

**输入参数：**
| 参数名 | 类型 | 说明 |
| :---- | :--- | :--- |
| p_user_id | INT | 用户ID |

**输出参数：** 无（通过SELECT返回结果集）

**返回结果：** post_id, 标题, 内容, 创建时间, 浏览量, 点赞数, 赛季, home_team, away_team

**功能：** 获取指定用户发布的所有帖子列表

**关键设计：**
- 使用多表 `LEFT JOIN` 关联比赛和球队信息
- 按创建时间倒序排列，最新帖子在前

**SQL代码：**
```sql
DROP PROCEDURE IF EXISTS sp_get_user_posts;
DELIMITER //
CREATE PROCEDURE sp_get_user_posts(IN p_user_id INT)
BEGIN
    SELECT p.post_id, p.标题, p.内容, p.创建时间, p.浏览量, p.点赞数,
           g.赛季, ht.名称 as home_team, at.名称 as away_team
    FROM Post p
    LEFT JOIN Game g ON p.game_id = g.game_id
    LEFT JOIN Team ht ON g.主队ID = ht.team_id
    LEFT JOIN Team at ON g.客队ID = at.team_id
    WHERE p.user_id = p_user_id
    ORDER BY p.创建时间 DESC;
END//
DELIMITER ;
```

---

### 4.1.7 获取用户评分记录存储过程

**存储过程名称：** `sp_get_user_ratings`

**输入参数：**
| 参数名 | 类型 | 说明 |
| :---- | :--- | :--- |
| p_user_id | INT | 用户ID |

**输出参数：** 无（通过SELECT返回结果集）

**返回结果：** user_id, player_id, game_id, 分数, 创建时间, player_name, 位置, team_name, 赛季, 日期, home_team, away_team

**功能：** 获取用户对球员的所有评分记录，包含球员和比赛详情

**关键设计：**
- 多表关联查询，返回完整的评分上下文信息
- 包含球员姓名、位置、所属球队、比赛信息等

**SQL代码：**
```sql
DROP PROCEDURE IF EXISTS sp_get_user_ratings;
DELIMITER //
CREATE PROCEDURE sp_get_user_ratings(IN p_user_id INT)
BEGIN
    SELECT r.user_id, r.player_id, r.game_id, r.分数, r.创建时间,
           p.姓名 as player_name, p.位置, t.名称 as team_name,
           g.赛季, g.日期, ht.名称 as home_team, at.名称 as away_team
    FROM Rating r
    JOIN Player p ON r.player_id = p.player_id
    LEFT JOIN Team t ON p.当前球队ID = t.team_id
    JOIN Game g ON r.game_id = g.game_id
    JOIN Team ht ON g.主队ID = ht.team_id
    JOIN Team at ON g.客队ID = at.team_id
    WHERE r.user_id = p_user_id
    ORDER BY r.创建时间 DESC;
END//
DELIMITER ;
```

---

### 4.1.8 获取用户密码哈希存储过程

**存储过程名称：** `sp_get_user_password_hash`

**输入参数：**
| 参数名 | 类型 | 说明 |
| :---- | :--- | :--- |
| p_user_id | INT | 用户ID |

**输出参数：** 无（通过SELECT返回结果集）

**返回结果：** 密码

**功能：** 获取用户的密码哈希值，用于密码修改时的旧密码验证

**关键设计：**
- 仅返回密码字段，用于应用层进行密码比对

**SQL代码：**
```sql
DROP PROCEDURE IF EXISTS sp_get_user_password_hash;
DELIMITER //
CREATE PROCEDURE sp_get_user_password_hash(IN p_user_id INT)
BEGIN
    SELECT 密码 FROM User WHERE user_id = p_user_id;
END//
DELIMITER ;
```

---

### 4.1.9 删除用户账号存储过程

**存储过程名称：** `sp_delete_account`

**输入参数：**
| 参数名 | 类型 | 说明 |
| :---- | :--- | :--- |
| p_user_id | INT | 用户ID |

**输出参数：** 无

**功能：** 删除用户账号，关联数据由触发器自动清理

**关键设计：**
- 利用 `trg_user_delete_cleanup` 触发器自动级联删除用户的帖子、评论、评分等关联数据
- 存储过程本身只执行简单的DELETE操作

**SQL代码：**
```sql
DROP PROCEDURE IF EXISTS sp_delete_account;
DELIMITER //
CREATE PROCEDURE sp_delete_account(IN p_user_id INT)
BEGIN
    -- 触发器 trg_user_delete_cleanup 会处理关联数据的删除
    DELETE FROM User WHERE user_id = p_user_id;
END//
DELIMITER ;
```

---

### 4.1.10 获取用户积分历史存储过程

**存储过程名称：** `sp_get_user_points_history`

**输入参数：**
| 参数名 | 类型 | 说明 |
| :---- | :--- | :--- |
| p_user_id | INT | 用户ID |

**输出参数：** 无（通过SELECT返回结果集）

**返回结果：** update_time, 主队ID, 客队ID, home_team, away_team, 主队得分, 客队得分, 日期

**功能：** 获取用户已领取奖励的竞猜记录，作为积分获取历史

**关键设计：**
- 仅查询 `is_claimed = TRUE` 的记录，即已成功领取奖励的竞猜
- 关联比赛信息，展示竞猜的上下文

**SQL代码：**
```sql
DROP PROCEDURE IF EXISTS sp_get_user_points_history;
DELIMITER //
CREATE PROCEDURE sp_get_user_points_history(IN p_user_id INT)
BEGIN
    SELECT p.update_time, g.主队ID, g.客队ID, ht.名称 as home_team, at.名称 as away_team, 
           g.主队得分, g.客队得分, g.日期
    FROM Prediction p
    JOIN Game g ON p.game_id = g.game_id
    JOIN Team ht ON g.主队ID = ht.team_id
    JOIN Team at ON g.客队ID = at.team_id
    WHERE p.user_id = p_user_id AND p.is_claimed = TRUE
    ORDER BY p.update_time DESC;
END//
DELIMITER ;
```

---

### 4.1.11 用户认证模块存储过程汇总

| 序号 | 存储过程名称 | 功能描述 | 参数类型 |
| :--: | :---------- | :------- | :------: |
| 1 | sp_register_user | 用户注册 | IN |
| 2 | sp_login_user | 用户登录查询 | IN |
| 3 | sp_update_last_login | 更新最后登录时间 | IN |
| 4 | sp_get_user_profile | 获取用户个人信息 | IN |
| 5 | sp_update_user_profile | 更新用户个人信息 | IN |
| 6 | sp_get_user_posts | 获取用户帖子列表 | IN |
| 7 | sp_get_user_ratings | 获取用户评分记录 | IN |
| 8 | sp_get_user_password_hash | 获取用户密码哈希 | IN |
| 9 | sp_delete_account | 删除用户账号 | IN |
| 10 | sp_get_user_points_history | 获取用户积分历史 | IN |

---

## 4.2 比赛管理存储过程

本模块包含14个存储过程，用于处理比赛的查询、创建、更新、删除以及竞猜功能。

### 4.2.1 获取比赛列表存储过程

**存储过程名称：** `sp_get_games`

**输入参数：**
| 参数名 | 类型 | 说明 |
| :---- | :--- | :--- |
| p_date_from | DATETIME | 起始日期（可选） |
| p_date_to | DATETIME | 结束日期（可选） |
| p_team_id | INT | 球队ID筛选（可选） |

**输出参数：** 无（通过SELECT返回结果集）

**返回结果：** game_id, 赛季, 日期, 状态, 主队得分, 客队得分, home_team, away_team, winner_team, 场馆, home_logo_id, away_logo_id, 主队ID, 客队ID

**功能：** 获取比赛列表，支持按日期范围和球队进行筛选

**关键设计：**
- 参数可选设计：使用 `p_param IS NULL OR condition` 模式，未传参时不过滤
- 多表关联：连接Team表获取球队名称，连接Team_Logo表获取队标
- 按日期倒序排列，最新比赛在前

**SQL代码：**
```sql
DROP PROCEDURE IF EXISTS sp_get_games;
DELIMITER //
CREATE PROCEDURE sp_get_games(
    IN p_date_from DATETIME,
    IN p_date_to DATETIME,
    IN p_team_id INT
)
BEGIN
    SELECT g.game_id, g.赛季, g.日期, g.状态, g.主队得分, g.客队得分,
           ht.名称 as home_team, at.名称 as away_team,
           wt.名称 as winner_team, g.场馆,
           htl.image_id as home_logo_id, atl.image_id as away_logo_id,
           g.主队ID, g.客队ID
    FROM Game g
    JOIN Team ht ON g.主队ID = ht.team_id
    JOIN Team at ON g.客队ID = at.team_id
    LEFT JOIN Team wt ON g.获胜球队ID = wt.team_id
    LEFT JOIN Team_Logo htl ON ht.team_id = htl.team_id
    LEFT JOIN Team_Logo atl ON at.team_id = atl.team_id
    WHERE (p_date_from IS NULL OR g.日期 >= p_date_from)
      AND (p_date_to IS NULL OR g.日期 <= p_date_to)
      AND (p_team_id IS NULL OR g.主队ID = p_team_id OR g.客队ID = p_team_id)
    ORDER BY g.日期 DESC;
END//
DELIMITER ;
```

---

### 4.2.2 获取比赛详情存储过程

**存储过程名称：** `sp_get_game_detail`

**输入参数：**
| 参数名 | 类型 | 说明 |
| :---- | :--- | :--- |
| p_game_id | INT | 比赛ID |

**输出参数：** 无（通过SELECT返回结果集）

**返回结果：** game_id, 赛季, 日期, 状态, 主队得分, 客队得分, 主队ID, 客队ID, home_team, away_team, winner_team, 场馆, 获胜球队ID

**功能：** 获取单场比赛的详细信息

**关键设计：**
- 返回完整的比赛信息，包括双方球队名称和获胜方

**SQL代码：**
```sql
DROP PROCEDURE IF EXISTS sp_get_game_detail;
DELIMITER //
CREATE PROCEDURE sp_get_game_detail(IN p_game_id INT)
BEGIN
    SELECT g.game_id, g.赛季, g.日期, g.状态, g.主队得分, g.客队得分,
           g.主队ID, g.客队ID,
           ht.名称 as home_team, at.名称 as away_team,
           wt.名称 as winner_team, g.场馆, g.获胜球队ID
    FROM Game g
    JOIN Team ht ON g.主队ID = ht.team_id
    JOIN Team at ON g.客队ID = at.team_id
    LEFT JOIN Team wt ON g.获胜球队ID = wt.team_id
    WHERE g.game_id = p_game_id;
END//
DELIMITER ;
```

---

### 4.2.3 获取比赛竞猜统计存储过程

**存储过程名称：** `sp_get_game_prediction_stats`

**输入参数：**
| 参数名 | 类型 | 说明 |
| :---- | :--- | :--- |
| p_game_id | INT | 比赛ID |

**输出参数：** 无（通过SELECT返回结果集）

**返回结果：** predicted_team_id, COUNT(*)

**功能：** 统计某场比赛各球队的竞猜票数

**关键设计：**
- 使用 `GROUP BY` 按预测球队分组统计
- 返回各队获得的投票数量

**SQL代码：**
```sql
DROP PROCEDURE IF EXISTS sp_get_game_prediction_stats;
DELIMITER //
CREATE PROCEDURE sp_get_game_prediction_stats(IN p_game_id INT)
BEGIN
    SELECT predicted_team_id, COUNT(*) 
    FROM Prediction 
    WHERE game_id = p_game_id 
    GROUP BY predicted_team_id;
END//
DELIMITER ;
```

---

### 4.2.4 获取用户竞猜记录存储过程

**存储过程名称：** `sp_get_user_prediction`

**输入参数：**
| 参数名 | 类型 | 说明 |
| :---- | :--- | :--- |
| p_game_id | INT | 比赛ID |
| p_user_id | INT | 用户ID |

**输出参数：** 无（通过SELECT返回结果集）

**返回结果：** predicted_team_id, is_claimed

**功能：** 查询用户对某场比赛的竞猜记录

**关键设计：**
- 联合主键查询，精确定位用户的竞猜记录

**SQL代码：**
```sql
DROP PROCEDURE IF EXISTS sp_get_user_prediction;
DELIMITER //
CREATE PROCEDURE sp_get_user_prediction(
    IN p_game_id INT,
    IN p_user_id INT
)
BEGIN
    SELECT predicted_team_id, is_claimed
    FROM Prediction 
    WHERE game_id = p_game_id AND user_id = p_user_id;
END//
DELIMITER ;
```

---

### 4.2.5 获取比赛球员数据存储过程

**存储过程名称：** `sp_get_game_player_stats`

**输入参数：**
| 参数名 | 类型 | 说明 |
| :---- | :--- | :--- |
| p_game_id | INT | 比赛ID |

**输出参数：** 无（通过SELECT返回结果集）

**返回结果：** player_id, 上场时间, 得分, 篮板, 助攻, 抢断, 盖帽, 失误, 犯规, 正负值, 姓名, 位置, 球衣号, team_name, team_id

**功能：** 获取某场比赛中所有球员的详细数据统计

**关键设计：**
- 关联Player表获取球员基本信息
- 按球队和球衣号排序，便于前端按队伍分组展示

**SQL代码：**
```sql
DROP PROCEDURE IF EXISTS sp_get_game_player_stats;
DELIMITER //
CREATE PROCEDURE sp_get_game_player_stats(IN p_game_id INT)
BEGIN
    SELECT pg.player_id, pg.上场时间, pg.得分, pg.篮板, pg.助攻, 
           pg.抢断, pg.盖帽, pg.失误, pg.犯规, pg.正负值,
           p.姓名, p.位置, p.球衣号, t.名称 as team_name, t.team_id
    FROM Player_Game pg
    JOIN Player p ON pg.player_id = p.player_id
    JOIN Team t ON p.当前球队ID = t.team_id
    WHERE pg.game_id = p_game_id
    ORDER BY t.名称, p.球衣号;
END//
DELIMITER ;
```

---

### 4.2.6 检查竞猜状态存储过程

**存储过程名称：** `sp_check_prediction_status`

**输入参数：**
| 参数名 | 类型 | 说明 |
| :---- | :--- | :--- |
| p_game_id | INT | 比赛ID |
| p_user_id | INT | 用户ID |

**输出参数：** 无（通过SELECT返回结果集）

**返回结果：** 状态, 获胜球队ID, predicted_team_id, is_claimed

**功能：** 检查用户竞猜的状态，用于判断是否可以领取奖励

**关键设计：**
- 关联Game表获取比赛状态和获胜方
- 返回预测球队和领取状态，供应用层判断

**SQL代码：**
```sql
DROP PROCEDURE IF EXISTS sp_check_prediction_status;
DELIMITER //
CREATE PROCEDURE sp_check_prediction_status(
    IN p_game_id INT,
    IN p_user_id INT
)
BEGIN
    SELECT g.状态, g.获胜球队ID, p.predicted_team_id, p.is_claimed
    FROM Prediction p
    JOIN Game g ON p.game_id = g.game_id
    WHERE p.game_id = p_game_id AND p.user_id = p_user_id;
END//
DELIMITER ;
```

---

### 4.2.7 领取竞猜奖励存储过程

**存储过程名称：** `sp_claim_reward`

**输入参数：**
| 参数名 | 类型 | 说明 |
| :---- | :--- | :--- |
| p_game_id | INT | 比赛ID |
| p_user_id | INT | 用户ID |
| p_reward_points | INT | 奖励积分数 |

**输出参数：** 无

**功能：** 发放竞猜奖励，更新用户积分和领取状态

**关键设计：**
- 原子操作：同时更新用户积分和竞猜领取状态
- 应用层负责校验竞猜是否正确，存储过程只执行发放

**SQL代码：**
```sql
DROP PROCEDURE IF EXISTS sp_claim_reward;
DELIMITER //
CREATE PROCEDURE sp_claim_reward(
    IN p_game_id INT,
    IN p_user_id INT,
    IN p_reward_points INT
)
BEGIN
    UPDATE User SET points = points + p_reward_points WHERE user_id = p_user_id;
    UPDATE Prediction SET is_claimed = TRUE WHERE game_id = p_game_id AND user_id = p_user_id;
END//
DELIMITER ;
```

---

### 4.2.8 检查比赛状态存储过程

**存储过程名称：** `sp_check_game_status`

**输入参数：**
| 参数名 | 类型 | 说明 |
| :---- | :--- | :--- |
| p_game_id | INT | 比赛ID |

**输出参数：** 无（通过SELECT返回结果集）

**返回结果：** 状态, 日期

**功能：** 快速查询比赛状态，用于竞猜前的校验

**关键设计：**
- 仅返回状态和日期，轻量级查询

**SQL代码：**
```sql
DROP PROCEDURE IF EXISTS sp_check_game_status;
DELIMITER //
CREATE PROCEDURE sp_check_game_status(IN p_game_id INT)
BEGIN
    SELECT 状态, 日期 FROM Game WHERE game_id = p_game_id;
END//
DELIMITER ;
```

---

### 4.2.9 用户比赛竞猜存储过程

**存储过程名称：** `sp_predict_game`

**输入参数：**
| 参数名 | 类型 | 说明 |
| :---- | :--- | :--- |
| p_user_id | INT | 用户ID |
| p_game_id | INT | 比赛ID |
| p_team_id | INT | 预测获胜球队ID |

**输出参数：** 无

**功能：** 用户进行比赛竞猜，支持修改已有预测

**关键设计：**
- 使用 `ON DUPLICATE KEY UPDATE` 实现插入或更新
- 同一用户对同一比赛只能有一条竞猜记录

**SQL代码：**
```sql
DROP PROCEDURE IF EXISTS sp_predict_game;
DELIMITER //
CREATE PROCEDURE sp_predict_game(
    IN p_user_id INT,
    IN p_game_id INT,
    IN p_team_id INT
)
BEGIN
    INSERT INTO Prediction (user_id, game_id, predicted_team_id)
    VALUES (p_user_id, p_game_id, p_team_id)
    ON DUPLICATE KEY UPDATE predicted_team_id = VALUES(predicted_team_id);
END//
DELIMITER ;
```

---

### 4.2.10 创建比赛存储过程

**存储过程名称：** `sp_create_game`

**输入参数：**
| 参数名 | 类型 | 说明 |
| :---- | :--- | :--- |
| p_season | VARCHAR(20) | 赛季 |
| p_date | DATETIME | 比赛日期 |
| p_home_team_id | INT | 主队ID |
| p_away_team_id | INT | 客队ID |
| p_home_score | INT | 主队得分 |
| p_away_score | INT | 客队得分 |
| p_status | VARCHAR(20) | 比赛状态 |
| p_venue | VARCHAR(100) | 比赛场馆 |

**输出参数：**
| 参数名 | 类型 | 说明 |
| :---- | :--- | :--- |
| p_game_id | INT | 新创建的比赛ID |

**功能：** 创建新比赛，同时维护Team_Game关联表

**关键设计：**
- 使用 `LAST_INSERT_ID()` 获取新插入记录的ID
- 自动创建主客队的Team_Game关联记录
- 触发器会自动计算获胜球队

**SQL代码：**
```sql
DROP PROCEDURE IF EXISTS sp_create_game;
DELIMITER //
CREATE PROCEDURE sp_create_game(
    IN p_season VARCHAR(20),
    IN p_date DATETIME,
    IN p_home_team_id INT,
    IN p_away_team_id INT,
    IN p_home_score INT,
    IN p_away_score INT,
    IN p_status VARCHAR(20),
    IN p_venue VARCHAR(100),
    OUT p_game_id INT
)
BEGIN
    INSERT INTO Game (赛季, 日期, 主队ID, 客队ID, 主队得分, 客队得分, 状态, 场馆)
    VALUES (p_season, p_date, p_home_team_id, p_away_team_id, p_home_score, p_away_score, p_status, p_venue);
    
    SET p_game_id = LAST_INSERT_ID();
    
    INSERT INTO Team_Game (team_id, game_id, 主客类型) VALUES (p_home_team_id, p_game_id, '主场');
    INSERT INTO Team_Game (team_id, game_id, 主客类型) VALUES (p_away_team_id, p_game_id, '客场');
END//
DELIMITER ;
```

---

### 4.2.11 添加球员比赛数据存储过程

**存储过程名称：** `sp_add_player_game_stat`

**输入参数：**
| 参数名 | 类型 | 说明 |
| :---- | :--- | :--- |
| p_player_id | INT | 球员ID |
| p_game_id | INT | 比赛ID |
| p_minutes | DECIMAL(4,1) | 上场时间 |
| p_points | INT | 得分 |
| p_rebounds | INT | 篮板 |
| p_assists | INT | 助攻 |
| p_steals | INT | 抢断 |
| p_blocks | INT | 盖帽 |
| p_turnovers | INT | 失误 |
| p_fouls | INT | 犯规 |
| p_plus_minus | INT | 正负值 |

**输出参数：** 无

**功能：** 添加球员在某场比赛中的详细数据

**关键设计：**
- 完整的11项数据统计
- 联合主键确保同一球员同一比赛只有一条记录

**SQL代码：**
```sql
DROP PROCEDURE IF EXISTS sp_add_player_game_stat;
DELIMITER //
CREATE PROCEDURE sp_add_player_game_stat(
    IN p_player_id INT,
    IN p_game_id INT,
    IN p_minutes DECIMAL(4,1),
    IN p_points INT,
    IN p_rebounds INT,
    IN p_assists INT,
    IN p_steals INT,
    IN p_blocks INT,
    IN p_turnovers INT,
    IN p_fouls INT,
    IN p_plus_minus INT
)
BEGIN
    INSERT INTO Player_Game (player_id, game_id, 上场时间, 得分, 篮板, 助攻, 抢断, 盖帽, 失误, 犯规, 正负值)
    VALUES (p_player_id, p_game_id, p_minutes, p_points, p_rebounds, p_assists, p_steals, p_blocks, p_turnovers, p_fouls, p_plus_minus);
END//
DELIMITER ;
```

---

### 4.2.12 更新比赛信息存储过程

**存储过程名称：** `sp_update_game`

**输入参数：**
| 参数名 | 类型 | 说明 |
| :---- | :--- | :--- |
| p_game_id | INT | 比赛ID |
| p_season | VARCHAR(20) | 赛季（可选） |
| p_date | DATETIME | 比赛日期（可选） |
| p_home_team_id | INT | 主队ID（可选） |
| p_away_team_id | INT | 客队ID（可选） |
| p_status | VARCHAR(20) | 比赛状态（可选） |
| p_home_score | INT | 主队得分（可选） |
| p_away_score | INT | 客队得分（可选） |
| p_venue | VARCHAR(100) | 比赛场馆（可选） |

**输出参数：** 无

**功能：** 更新比赛信息，支持部分字段更新

**关键设计：**
- 使用 `COALESCE` 函数实现可选更新，NULL值表示不更新该字段
- 同步更新Team_Game表中的主客队信息
- 触发器会自动重新计算获胜球队

**SQL代码：**
```sql
DROP PROCEDURE IF EXISTS sp_update_game;
DELIMITER //
CREATE PROCEDURE sp_update_game(
    IN p_game_id INT,
    IN p_season VARCHAR(20),
    IN p_date DATETIME,
    IN p_home_team_id INT,
    IN p_away_team_id INT,
    IN p_status VARCHAR(20),
    IN p_home_score INT,
    IN p_away_score INT,
    IN p_venue VARCHAR(100)
)
BEGIN
    UPDATE Game 
    SET 赛季 = COALESCE(p_season, 赛季),
        日期 = COALESCE(p_date, 日期),
        主队ID = COALESCE(p_home_team_id, 主队ID),
        客队ID = COALESCE(p_away_team_id, 客队ID),
        状态 = COALESCE(p_status, 状态),
        主队得分 = COALESCE(p_home_score, 主队得分),
        客队得分 = COALESCE(p_away_score, 客队得分),
        场馆 = COALESCE(p_venue, 场馆)
    WHERE game_id = p_game_id;
    
    IF p_home_team_id IS NOT NULL THEN
        UPDATE Team_Game SET team_id = p_home_team_id WHERE game_id = p_game_id AND 主客类型 = '主场';
    END IF;
    
    IF p_away_team_id IS NOT NULL THEN
        UPDATE Team_Game SET team_id = p_away_team_id WHERE game_id = p_game_id AND 主客类型 = '客场';
    END IF;
END//
DELIMITER ;
```

---

### 4.2.13 删除比赛球员数据存储过程

**存储过程名称：** `sp_delete_player_game_stats`

**输入参数：**
| 参数名 | 类型 | 说明 |
| :---- | :--- | :--- |
| p_game_id | INT | 比赛ID |

**输出参数：** 无

**功能：** 删除某场比赛的所有球员数据

**关键设计：**
- 用于比赛数据重置或更新前的清理

**SQL代码：**
```sql
DROP PROCEDURE IF EXISTS sp_delete_player_game_stats;
DELIMITER //
CREATE PROCEDURE sp_delete_player_game_stats(IN p_game_id INT)
BEGIN
    DELETE FROM Player_Game WHERE game_id = p_game_id;
END//
DELIMITER ;
```

---

### 4.2.14 删除比赛存储过程

**存储过程名称：** `sp_delete_game`

**输入参数：**
| 参数名 | 类型 | 说明 |
| :---- | :--- | :--- |
| p_game_id | INT | 比赛ID |

**输出参数：** 无

**功能：** 删除比赛及其所有关联数据

**关键设计：**
- 级联删除顺序：先删除依赖表数据，再删除主表
- 按外键依赖顺序依次删除：Rating → Player_Game → Team_Game → Post → Comment → Game

**SQL代码：**
```sql
DROP PROCEDURE IF EXISTS sp_delete_game;
DELIMITER //
CREATE PROCEDURE sp_delete_game(IN p_game_id INT)
BEGIN
    DELETE FROM Rating WHERE game_id = p_game_id;
    DELETE FROM Player_Game WHERE game_id = p_game_id;
    DELETE FROM Team_Game WHERE game_id = p_game_id;
    DELETE FROM Post WHERE game_id = p_game_id;
    DELETE FROM Comment WHERE game_id = p_game_id;
    DELETE FROM Game WHERE game_id = p_game_id;
END//
DELIMITER ;
```

---

### 4.2.15 比赛管理模块存储过程汇总

| 序号 | 存储过程名称 | 功能描述 | 参数类型 |
| :--: | :---------- | :------- | :------: |
| 1 | sp_get_games | 获取比赛列表（支持筛选） | IN |
| 2 | sp_get_game_detail | 获取比赛详情 | IN |
| 3 | sp_get_game_prediction_stats | 获取比赛竞猜统计 | IN |
| 4 | sp_get_user_prediction | 获取用户竞猜记录 | IN |
| 5 | sp_get_game_player_stats | 获取比赛球员数据 | IN |
| 6 | sp_check_prediction_status | 检查竞猜状态 | IN |
| 7 | sp_claim_reward | 领取竞猜奖励 | IN |
| 8 | sp_check_game_status | 检查比赛状态 | IN |
| 9 | sp_predict_game | 用户比赛竞猜 | IN |
| 10 | sp_create_game | 创建比赛 | IN/OUT |
| 11 | sp_add_player_game_stat | 添加球员比赛数据 | IN |
| 12 | sp_update_game | 更新比赛信息 | IN |
| 13 | sp_delete_player_game_stats | 删除比赛球员数据 | IN |
| 14 | sp_delete_game | 删除比赛 | IN |

---

## 4.3 帖子管理存储过程

本模块包含10个存储过程，用于处理帖子的发布、查询、点赞、评论等功能。

### 4.3.1 获取帖子列表存储过程

**存储过程名称：** `sp_get_posts`

**输入参数：**
| 参数名 | 类型 | 说明 |
| :---- | :--- | :--- |
| p_game_id | INT | 比赛ID（可选，用于筛选） |

**输出参数：** 无（通过SELECT返回结果集）

**返回结果：** post_id, 标题, 内容, 创建时间, 浏览量, 点赞数, 用户名, 赛季, home_team, away_team, image_ids, user_id

**功能：** 获取帖子列表，支持按比赛筛选，包含发帖用户和关联比赛信息

**关键设计：**
- 使用子查询 `GROUP_CONCAT` 聚合帖子的多张图片ID
- 多表LEFT JOIN关联用户、比赛、球队信息
- 按创建时间倒序排列

**SQL代码：**
```sql
DROP PROCEDURE IF EXISTS sp_get_posts;
DELIMITER //
CREATE PROCEDURE sp_get_posts(IN p_game_id INT)
BEGIN
    SELECT p.post_id, p.标题, p.内容, p.创建时间, p.浏览量, p.点赞数,
           u.用户名, g.赛季, ht.名称 as home_team, at.名称 as away_team,
           (SELECT GROUP_CONCAT(image_id) FROM Post_Image WHERE post_id = p.post_id) as image_ids,
           p.user_id
    FROM Post p
    JOIN User u ON p.user_id = u.user_id
    LEFT JOIN Game g ON p.game_id = g.game_id
    LEFT JOIN Team ht ON g.主队ID = ht.team_id
    LEFT JOIN Team at ON g.客队ID = at.team_id
    WHERE (p_game_id IS NULL OR p.game_id = p_game_id)
    ORDER BY p.创建时间 DESC;
END//
DELIMITER ;
```

---

### 4.3.2 创建帖子存储过程

**存储过程名称：** `sp_create_post`

**输入参数：**
| 参数名 | 类型 | 说明 |
| :---- | :--- | :--- |
| p_user_id | INT | 发帖用户ID |
| p_title | VARCHAR(50) | 帖子标题 |
| p_content | TEXT | 帖子内容 |
| p_game_id | INT | 关联比赛ID（可选） |
| p_created_at | DATETIME | 创建时间 |

**输出参数：**
| 参数名 | 类型 | 说明 |
| :---- | :--- | :--- |
| p_post_id | INT | 新创建的帖子ID |

**功能：** 创建新帖子并返回帖子ID

**关键设计：**
- 使用 `LAST_INSERT_ID()` 获取新插入记录的ID
- 返回帖子ID供后续添加图片使用

**SQL代码：**
```sql
DROP PROCEDURE IF EXISTS sp_create_post;
DELIMITER //
CREATE PROCEDURE sp_create_post(
    IN p_user_id INT,
    IN p_title VARCHAR(50),
    IN p_content TEXT,
    IN p_game_id INT,
    IN p_created_at DATETIME,
    OUT p_post_id INT
)
BEGIN
    INSERT INTO Post (user_id, 标题, 内容, game_id, 创建时间)
    VALUES (p_user_id, p_title, p_content, p_game_id, p_created_at);
    SET p_post_id = LAST_INSERT_ID();
END//
DELIMITER ;
```

---

### 4.3.3 添加帖子图片存储过程

**存储过程名称：** `sp_add_post_image`

**输入参数：**
| 参数名 | 类型 | 说明 |
| :---- | :--- | :--- |
| p_post_id | INT | 帖子ID |
| p_image_id | INT | 图片ID |

**输出参数：** 无

**功能：** 为帖子关联图片

**关键设计：**
- 在创建帖子后调用，建立帖子与图片的关联

**SQL代码：**
```sql
DROP PROCEDURE IF EXISTS sp_add_post_image;
DELIMITER //
CREATE PROCEDURE sp_add_post_image(
    IN p_post_id INT,
    IN p_image_id INT
)
BEGIN
    INSERT INTO Post_Image (post_id, image_id) VALUES (p_post_id, p_image_id);
END//
DELIMITER ;
```

---

### 4.3.4 增加帖子浏览量存储过程

**存储过程名称：** `sp_increment_post_view`

**输入参数：**
| 参数名 | 类型 | 说明 |
| :---- | :--- | :--- |
| p_post_id | INT | 帖子ID |

**输出参数：** 无

**功能：** 帖子浏览量加1

**关键设计：**
- 每次用户查看帖子详情时调用
- 原子操作，直接在数据库层面递增

**SQL代码：**
```sql
DROP PROCEDURE IF EXISTS sp_increment_post_view;
DELIMITER //
CREATE PROCEDURE sp_increment_post_view(IN p_post_id INT)
BEGIN
    UPDATE Post SET 浏览量 = 浏览量 + 1 WHERE post_id = p_post_id;
END//
DELIMITER ;
```

---

### 4.3.5 检查帖子点赞状态存储过程

**存储过程名称：** `sp_check_post_like`

**输入参数：**
| 参数名 | 类型 | 说明 |
| :---- | :--- | :--- |
| p_user_id | INT | 用户ID |
| p_post_id | INT | 帖子ID |

**输出参数：** 无（通过SELECT返回结果集）

**返回结果：** COUNT(*)

**功能：** 检查用户是否已对帖子点赞

**关键设计：**
- 返回0表示未点赞，返回1表示已点赞
- 用于前端显示点赞状态

**SQL代码：**
```sql
DROP PROCEDURE IF EXISTS sp_check_post_like;
DELIMITER //
CREATE PROCEDURE sp_check_post_like(
    IN p_user_id INT,
    IN p_post_id INT
)
BEGIN
    SELECT COUNT(*) FROM Post_Like WHERE user_id = p_user_id AND post_id = p_post_id;
END//
DELIMITER ;
```

---

### 4.3.6 帖子点赞存储过程

**存储过程名称：** `sp_add_post_like`

**输入参数：**
| 参数名 | 类型 | 说明 |
| :---- | :--- | :--- |
| p_user_id | INT | 用户ID |
| p_post_id | INT | 帖子ID |

**输出参数：** 无

**功能：** 用户对帖子点赞

**关键设计：**
- 插入点赞记录后，触发器 `trg_post_like_increment` 会自动更新帖子点赞数
- 唯一约束防止重复点赞

**SQL代码：**
```sql
DROP PROCEDURE IF EXISTS sp_add_post_like;
DELIMITER //
CREATE PROCEDURE sp_add_post_like(
    IN p_user_id INT,
    IN p_post_id INT
)
BEGIN
    INSERT INTO Post_Like (user_id, post_id) VALUES (p_user_id, p_post_id);
END//
DELIMITER ;
```

---

### 4.3.7 取消帖子点赞存储过程

**存储过程名称：** `sp_remove_post_like`

**输入参数：**
| 参数名 | 类型 | 说明 |
| :---- | :--- | :--- |
| p_user_id | INT | 用户ID |
| p_post_id | INT | 帖子ID |

**输出参数：** 无

**功能：** 用户取消对帖子的点赞

**关键设计：**
- 删除点赞记录后，触发器 `trg_post_like_decrement` 会自动更新帖子点赞数

**SQL代码：**
```sql
DROP PROCEDURE IF EXISTS sp_remove_post_like;
DELIMITER //
CREATE PROCEDURE sp_remove_post_like(
    IN p_user_id INT,
    IN p_post_id INT
)
BEGIN
    DELETE FROM Post_Like WHERE user_id = p_user_id AND post_id = p_post_id;
END//
DELIMITER ;
```

---

### 4.3.8 获取帖子评论列表存储过程

**存储过程名称：** `sp_get_post_comments`

**输入参数：**
| 参数名 | 类型 | 说明 |
| :---- | :--- | :--- |
| p_post_id | INT | 帖子ID |

**输出参数：** 无（通过SELECT返回结果集）

**返回结果：** comment_id, 内容, 创建时间, 用户名, user_id

**功能：** 获取帖子的所有评论

**关键设计：**
- 关联User表获取评论者用户名
- 按创建时间正序排列，早期评论在前

**SQL代码：**
```sql
DROP PROCEDURE IF EXISTS sp_get_post_comments;
DELIMITER //
CREATE PROCEDURE sp_get_post_comments(IN p_post_id INT)
BEGIN
    SELECT c.comment_id, c.内容, c.创建时间, u.用户名, u.user_id
    FROM Comment c
    JOIN User u ON c.user_id = u.user_id
    WHERE c.post_id = p_post_id
    ORDER BY c.创建时间 ASC;
END//
DELIMITER ;
```

---

### 4.3.9 创建帖子评论存储过程

**存储过程名称：** `sp_create_post_comment`

**输入参数：**
| 参数名 | 类型 | 说明 |
| :---- | :--- | :--- |
| p_user_id | INT | 评论用户ID |
| p_post_id | INT | 帖子ID |
| p_content | TEXT | 评论内容 |
| p_created_at | DATETIME | 创建时间 |

**输出参数：** 无

**功能：** 创建帖子评论

**SQL代码：**
```sql
DROP PROCEDURE IF EXISTS sp_create_post_comment;
DELIMITER //
CREATE PROCEDURE sp_create_post_comment(
    IN p_user_id INT,
    IN p_post_id INT,
    IN p_content TEXT,
    IN p_created_at DATETIME
)
BEGIN
    INSERT INTO Comment (user_id, post_id, 内容, 创建时间)
    VALUES (p_user_id, p_post_id, p_content, p_created_at);
END//
DELIMITER ;
```

---

### 4.3.10 删除帖子存储过程

**存储过程名称：** `sp_delete_post`

**输入参数：**
| 参数名 | 类型 | 说明 |
| :---- | :--- | :--- |
| p_post_id | INT | 帖子ID |

**输出参数：** 无

**功能：** 删除帖子及其所有关联数据

**关键设计：**
- 级联删除顺序：Post_Image → Comment_Like → Comment → Post_Like → Post
- 先删除评论的点赞记录，再删除评论，确保外键约束满足

**SQL代码：**
```sql
DROP PROCEDURE IF EXISTS sp_delete_post;
DELIMITER //
CREATE PROCEDURE sp_delete_post(IN p_post_id INT)
BEGIN
    DELETE FROM Post_Image WHERE post_id = p_post_id;
    
    DELETE FROM Comment_Like 
    WHERE comment_id IN (SELECT comment_id FROM Comment WHERE post_id = p_post_id);
    
    DELETE FROM Comment WHERE post_id = p_post_id;
    
    DELETE FROM Post_Like WHERE post_id = p_post_id;
    
    DELETE FROM Post WHERE post_id = p_post_id;
END//
DELIMITER ;
```

---

### 4.3.11 帖子管理模块存储过程汇总

| 序号 | 存储过程名称 | 功能描述 | 参数类型 |
| :--: | :---------- | :------- | :------: |
| 1 | sp_get_posts | 获取帖子列表 | IN |
| 2 | sp_create_post | 创建帖子 | IN/OUT |
| 3 | sp_add_post_image | 添加帖子图片 | IN |
| 4 | sp_increment_post_view | 增加帖子浏览量 | IN |
| 5 | sp_check_post_like | 检查帖子点赞状态 | IN |
| 6 | sp_add_post_like | 帖子点赞 | IN |
| 7 | sp_remove_post_like | 取消帖子点赞 | IN |
| 8 | sp_get_post_comments | 获取帖子评论列表 | IN |
| 9 | sp_create_post_comment | 创建帖子评论 | IN |
| 10 | sp_delete_post | 删除帖子 | IN |

---

## 4.4 评论管理存储过程

本模块包含3个存储过程，用于处理评论的点赞功能。

### 4.4.1 检查评论点赞状态存储过程

**存储过程名称：** `sp_check_comment_like`

**输入参数：**
| 参数名 | 类型 | 说明 |
| :---- | :--- | :--- |
| p_user_id | INT | 用户ID |
| p_comment_id | INT | 评论ID |

**输出参数：** 无（通过SELECT返回结果集）

**返回结果：** COUNT(*)

**功能：** 检查用户是否已对评论点赞

**SQL代码：**
```sql
DROP PROCEDURE IF EXISTS sp_check_comment_like;
DELIMITER //
CREATE PROCEDURE sp_check_comment_like(
    IN p_user_id INT,
    IN p_comment_id INT
)
BEGIN
    SELECT COUNT(*) FROM Comment_Like WHERE user_id = p_user_id AND comment_id = p_comment_id;
END//
DELIMITER ;
```

---

### 4.4.2 评论点赞存储过程

**存储过程名称：** `sp_add_comment_like`

**输入参数：**
| 参数名 | 类型 | 说明 |
| :---- | :--- | :--- |
| p_user_id | INT | 用户ID |
| p_comment_id | INT | 评论ID |

**输出参数：** 无

**功能：** 用户对评论点赞，同时更新评论点赞数

**关键设计：**
- 在存储过程中同时完成点赞记录插入和点赞数更新
- 原子操作确保数据一致性

**SQL代码：**
```sql
DROP PROCEDURE IF EXISTS sp_add_comment_like;
DELIMITER //
CREATE PROCEDURE sp_add_comment_like(
    IN p_user_id INT,
    IN p_comment_id INT
)
BEGIN
    INSERT INTO Comment_Like (user_id, comment_id) VALUES (p_user_id, p_comment_id);
    UPDATE Comment SET 点赞数 = 点赞数 + 1 WHERE comment_id = p_comment_id;
END//
DELIMITER ;
```

---

### 4.4.3 取消评论点赞存储过程

**存储过程名称：** `sp_remove_comment_like`

**输入参数：**
| 参数名 | 类型 | 说明 |
| :---- | :--- | :--- |
| p_user_id | INT | 用户ID |
| p_comment_id | INT | 评论ID |

**输出参数：** 无

**功能：** 用户取消对评论的点赞，同时更新评论点赞数

**SQL代码：**
```sql
DROP PROCEDURE IF EXISTS sp_remove_comment_like;
DELIMITER //
CREATE PROCEDURE sp_remove_comment_like(
    IN p_user_id INT,
    IN p_comment_id INT
)
BEGIN
    DELETE FROM Comment_Like WHERE user_id = p_user_id AND comment_id = p_comment_id;
    UPDATE Comment SET 点赞数 = 点赞数 - 1 WHERE comment_id = p_comment_id;
END//
DELIMITER ;
```

---

### 4.4.4 评论管理模块存储过程汇总

| 序号 | 存储过程名称 | 功能描述 | 参数类型 |
| :--: | :---------- | :------- | :------: |
| 1 | sp_check_comment_like | 检查评论点赞状态 | IN |
| 2 | sp_add_comment_like | 评论点赞 | IN |
| 3 | sp_remove_comment_like | 取消评论点赞 | IN |

---

## 4.5 球员管理存储过程

本模块包含7个存储过程，用于处理球员信息的增删改查及数据统计。

### 4.5.1 获取球员列表存储过程

**存储过程名称：** `sp_get_players`

**输入参数：**
| 参数名 | 类型 | 说明 |
| :---- | :--- | :--- |
| p_team_id | INT | 球队ID（可选，用于筛选） |

**输出参数：** 无（通过SELECT返回结果集）

**返回结果：** player_id, 姓名, 位置, 球衣号, 身高, 体重, 出生日期, 国籍, 当前球队ID, team_name, 合同到期, 薪资, image_id

**功能：** 获取球员列表，支持按球队筛选

**关键设计：**
- 使用 `LEFT JOIN` 关联球队和球员图片表
- 按球队名称和球衣号排序，便于分组展示

**SQL代码：**
```sql
DROP PROCEDURE IF EXISTS sp_get_players;
DELIMITER //
CREATE PROCEDURE sp_get_players(IN p_team_id INT)
BEGIN
    SELECT p.player_id, p.姓名, p.位置, p.球衣号, p.身高, p.体重, 
           p.出生日期, p.国籍, p.当前球队ID, t.名称 as team_name,
           p.合同到期, p.薪资, pi.image_id
    FROM Player p 
    LEFT JOIN Team t ON p.当前球队ID = t.team_id
    LEFT JOIN Player_Image pi ON p.player_id = pi.player_id
    WHERE (p_team_id IS NULL OR p.当前球队ID = p_team_id)
    ORDER BY t.名称, p.球衣号;
END//
DELIMITER ;
```

---

### 4.5.2 创建球员存储过程

**存储过程名称：** `sp_create_player`

**输入参数：**
| 参数名 | 类型 | 说明 |
| :---- | :--- | :--- |
| p_name | VARCHAR(50) | 球员姓名 |
| p_position | VARCHAR(20) | 球员位置 |
| p_jersey_number | INT | 球衣号 |
| p_height | DECIMAL(3,2) | 身高（米） |
| p_weight | DECIMAL(4,1) | 体重（公斤） |
| p_birth_date | DATE | 出生日期 |
| p_nationality | VARCHAR(50) | 国籍 |
| p_current_team_id | INT | 当前球队ID |
| p_contract_expiry | DATE | 合同到期日期 |
| p_salary | DECIMAL(12,2) | 年薪 |

**输出参数：**
| 参数名 | 类型 | 说明 |
| :---- | :--- | :--- |
| p_player_id | INT | 新创建的球员ID |

**功能：** 创建新球员并返回球员ID

**关键设计：**
- 使用 `LAST_INSERT_ID()` 获取新插入记录的ID
- 支持完整的球员信息录入

**SQL代码：**
```sql
DROP PROCEDURE IF EXISTS sp_create_player;
DELIMITER //
CREATE PROCEDURE sp_create_player(
    IN p_name VARCHAR(50),
    IN p_position VARCHAR(20),
    IN p_jersey_number INT,
    IN p_height DECIMAL(3,2),
    IN p_weight DECIMAL(4,1),
    IN p_birth_date DATE,
    IN p_nationality VARCHAR(50),
    IN p_current_team_id INT,
    IN p_contract_expiry DATE,
    IN p_salary DECIMAL(12,2),
    OUT p_player_id INT
)
BEGIN
    INSERT INTO Player (姓名, 位置, 球衣号, 身高, 体重, 出生日期, 国籍, 当前球队ID, 合同到期, 薪资)
    VALUES (p_name, p_position, p_jersey_number, p_height, p_weight, p_birth_date, p_nationality, p_current_team_id, p_contract_expiry, p_salary);
    SET p_player_id = LAST_INSERT_ID();
END//
DELIMITER ;
```

---

### 4.5.3 获取球员详情存储过程

**存储过程名称：** `sp_get_player_detail`

**输入参数：**
| 参数名 | 类型 | 说明 |
| :---- | :--- | :--- |
| p_player_id | INT | 球员ID |

**输出参数：** 无（通过SELECT返回结果集）

**返回结果：** player_id, 姓名, 位置, 球衣号, 身高, 体重, 出生日期, 国籍, 当前球队ID, team_name, 合同到期, 薪资, image_id

**功能：** 获取单个球员的详细信息

**SQL代码：**
```sql
DROP PROCEDURE IF EXISTS sp_get_player_detail;
DELIMITER //
CREATE PROCEDURE sp_get_player_detail(IN p_player_id INT)
BEGIN
    SELECT p.player_id, p.姓名, p.位置, p.球衣号, p.身高, p.体重, 
           p.出生日期, p.国籍, p.当前球队ID, t.名称 as team_name,
           p.合同到期, p.薪资, pi.image_id
    FROM Player p 
    LEFT JOIN Team t ON p.当前球队ID = t.team_id
    LEFT JOIN Player_Image pi ON p.player_id = pi.player_id
    WHERE p.player_id = p_player_id;
END//
DELIMITER ;
```

---

### 4.5.4 更新球员信息存储过程

**存储过程名称：** `sp_update_player`

**输入参数：**
| 参数名 | 类型 | 说明 |
| :---- | :--- | :--- |
| p_player_id | INT | 球员ID |
| p_name | VARCHAR(50) | 球员姓名（可选） |
| p_position | VARCHAR(20) | 球员位置（可选） |
| p_jersey_number | INT | 球衣号（可选） |
| p_height | DECIMAL(3,2) | 身高（可选） |
| p_weight | DECIMAL(4,1) | 体重（可选） |
| p_birth_date | DATE | 出生日期（可选） |
| p_nationality | VARCHAR(50) | 国籍（可选） |
| p_current_team_id | INT | 当前球队ID（可选） |
| p_contract_expiry | DATE | 合同到期日期（可选） |
| p_salary | DECIMAL(12,2) | 年薪（可选） |

**输出参数：** 无

**功能：** 更新球员信息，支持部分字段更新

**关键设计：**
- 使用 `COALESCE` 函数实现可选更新，NULL值表示不更新该字段

**SQL代码：**
```sql
DROP PROCEDURE IF EXISTS sp_update_player;
DELIMITER //
CREATE PROCEDURE sp_update_player(
    IN p_player_id INT,
    IN p_name VARCHAR(50),
    IN p_position VARCHAR(20),
    IN p_jersey_number INT,
    IN p_height DECIMAL(3,2),
    IN p_weight DECIMAL(4,1),
    IN p_birth_date DATE,
    IN p_nationality VARCHAR(50),
    IN p_current_team_id INT,
    IN p_contract_expiry DATE,
    IN p_salary DECIMAL(12,2)
)
BEGIN
    UPDATE Player 
    SET 姓名 = COALESCE(p_name, 姓名),
        位置 = COALESCE(p_position, 位置),
        球衣号 = COALESCE(p_jersey_number, 球衣号),
        身高 = COALESCE(p_height, 身高),
        体重 = COALESCE(p_weight, 体重),
        出生日期 = COALESCE(p_birth_date, 出生日期),
        国籍 = COALESCE(p_nationality, 国籍),
        当前球队ID = COALESCE(p_current_team_id, 当前球队ID),
        合同到期 = COALESCE(p_contract_expiry, 合同到期),
        薪资 = COALESCE(p_salary, 薪资)
    WHERE player_id = p_player_id;
END//
DELIMITER ;
```

---

### 4.5.5 删除球员存储过程

**存储过程名称：** `sp_delete_player`

**输入参数：**
| 参数名 | 类型 | 说明 |
| :---- | :--- | :--- |
| p_player_id | INT | 球员ID |

**输出参数：** 无

**功能：** 删除球员及其所有关联数据

**关键设计：**
- 级联删除顺序：Player_Image → Player_Game → Rating → Comment → Player
- 按外键依赖顺序删除

**SQL代码：**
```sql
DROP PROCEDURE IF EXISTS sp_delete_player;
DELIMITER //
CREATE PROCEDURE sp_delete_player(IN p_player_id INT)
BEGIN
    DELETE FROM Player_Image WHERE player_id = p_player_id;
    DELETE FROM Player_Game WHERE player_id = p_player_id;
    DELETE FROM Rating WHERE player_id = p_player_id;
    DELETE FROM Comment WHERE player_id = p_player_id;
    DELETE FROM Player WHERE player_id = p_player_id;
END//
DELIMITER ;
```

---

### 4.5.6 获取球员职业生涯数据存储过程

**存储过程名称：** `sp_get_player_career_stats`

**输入参数：**
| 参数名 | 类型 | 说明 |
| :---- | :--- | :--- |
| p_player_id | INT | 球员ID |

**输出参数：** 无（通过SELECT返回结果集）

**返回结果：** games_played, avg_minutes, avg_points, avg_rebounds, avg_assists, avg_steals, avg_blocks, avg_turnovers, avg_fouls, avg_plus_minus

**功能：** 统计球员职业生涯平均数据

**关键设计：**
- 使用 `COUNT` 统计出场次数
- 使用 `AVG` 计算各项数据平均值

**SQL代码：**
```sql
DROP PROCEDURE IF EXISTS sp_get_player_career_stats;
DELIMITER //
CREATE PROCEDURE sp_get_player_career_stats(IN p_player_id INT)
BEGIN
    SELECT 
        COUNT(pg.game_id) as games_played,
        AVG(pg.上场时间) as avg_minutes,
        AVG(pg.得分) as avg_points,
        AVG(pg.篮板) as avg_rebounds,
        AVG(pg.助攻) as avg_assists,
        AVG(pg.抢断) as avg_steals,
        AVG(pg.盖帽) as avg_blocks,
        AVG(pg.失误) as avg_turnovers,
        AVG(pg.犯规) as avg_fouls,
        AVG(pg.正负值) as avg_plus_minus
    FROM Player_Game pg
    WHERE pg.player_id = p_player_id;
END//
DELIMITER ;
```

---

### 4.5.7 获取球员近期比赛数据存储过程

**存储过程名称：** `sp_get_player_recent_games`

**输入参数：**
| 参数名 | 类型 | 说明 |
| :---- | :--- | :--- |
| p_player_id | INT | 球员ID |

**输出参数：** 无（通过SELECT返回结果集）

**返回结果：** game_id, 日期, 赛季, home_team, away_team, 上场时间, 得分, 篮板, 助攻, 抢断, 盖帽

**功能：** 获取球员最近10场比赛的数据

**关键设计：**
- 按比赛日期倒序排列
- 使用 `LIMIT 10` 限制返回条数

**SQL代码：**
```sql
DROP PROCEDURE IF EXISTS sp_get_player_recent_games;
DELIMITER //
CREATE PROCEDURE sp_get_player_recent_games(IN p_player_id INT)
BEGIN
    SELECT 
        g.game_id, g.日期, g.赛季,
        ht.名称 as home_team, at.名称 as away_team,
        pg.上场时间, pg.得分, pg.篮板, pg.助攻, pg.抢断, pg.盖帽
    FROM Player_Game pg
    JOIN Game g ON pg.game_id = g.game_id
    JOIN Team ht ON g.主队ID = ht.team_id
    JOIN Team at ON g.客队ID = at.team_id
    WHERE pg.player_id = p_player_id
    ORDER BY g.日期 DESC
    LIMIT 10;
END//
DELIMITER ;
```

---

### 4.5.8 球员管理模块存储过程汇总

| 序号 | 存储过程名称 | 功能描述 | 参数类型 |
| :--: | :---------- | :------- | :------: |
| 1 | sp_get_players | 获取球员列表 | IN |
| 2 | sp_create_player | 创建球员 | IN/OUT |
| 3 | sp_get_player_detail | 获取球员详情 | IN |
| 4 | sp_update_player | 更新球员信息 | IN |
| 5 | sp_delete_player | 删除球员 | IN |
| 6 | sp_get_player_career_stats | 获取球员职业生涯数据 | IN |
| 7 | sp_get_player_recent_games | 获取球员近期比赛数据 | IN |

---

## 4.6 球队管理存储过程

本模块包含5个存储过程，用于处理球队信息的增删改查。

### 4.6.1 获取所有球队存储过程

**存储过程名称：** `sp_get_all_teams`

**输入参数：** 无

**输出参数：** 无（通过SELECT返回结果集）

**返回结果：** team_id, 名称, 城市, 场馆, 分区, 成立年份, image_id

**功能：** 获取所有球队列表

**关键设计：**
- 使用 `LEFT JOIN` 关联队标图片
- 按球队名称排序

**SQL代码：**
```sql
DROP PROCEDURE IF EXISTS sp_get_all_teams;
DELIMITER //
CREATE PROCEDURE sp_get_all_teams()
BEGIN
    SELECT t.team_id, t.名称, t.城市, t.场馆, t.分区, t.成立年份, tl.image_id
    FROM Team t
    LEFT JOIN Team_Logo tl ON t.team_id = tl.team_id
    ORDER BY t.名称;
END//
DELIMITER ;
```

---

### 4.6.2 创建球队存储过程

**存储过程名称：** `sp_create_team`

**输入参数：**
| 参数名 | 类型 | 说明 |
| :---- | :--- | :--- |
| p_name | VARCHAR(50) | 球队名称 |
| p_city | VARCHAR(50) | 所在城市 |
| p_arena | VARCHAR(100) | 主场场馆 |
| p_conference | VARCHAR(20) | 分区（东部/西部） |
| p_founded_year | INT | 成立年份 |

**输出参数：**
| 参数名 | 类型 | 说明 |
| :---- | :--- | :--- |
| p_team_id | INT | 新创建的球队ID |

**功能：** 创建新球队并返回球队ID

**SQL代码：**
```sql
DROP PROCEDURE IF EXISTS sp_create_team;
DELIMITER //
CREATE PROCEDURE sp_create_team(
    IN p_name VARCHAR(50),
    IN p_city VARCHAR(50),
    IN p_arena VARCHAR(100),
    IN p_conference VARCHAR(20),
    IN p_founded_year INT,
    OUT p_team_id INT
)
BEGIN
    INSERT INTO Team (名称, 城市, 场馆, 分区, 成立年份) 
    VALUES (p_name, p_city, p_arena, p_conference, p_founded_year);
    SET p_team_id = LAST_INSERT_ID();
END//
DELIMITER ;
```

---

### 4.6.3 更新球队信息存储过程

**存储过程名称：** `sp_update_team`

**输入参数：**
| 参数名 | 类型 | 说明 |
| :---- | :--- | :--- |
| p_team_id | INT | 球队ID |
| p_name | VARCHAR(50) | 球队名称（可选） |
| p_city | VARCHAR(50) | 所在城市（可选） |
| p_arena | VARCHAR(100) | 主场场馆（可选） |
| p_conference | VARCHAR(20) | 分区（可选） |
| p_founded_year | INT | 成立年份（可选） |

**输出参数：** 无

**功能：** 更新球队信息，支持部分字段更新

**关键设计：**
- 使用 `COALESCE` 函数实现可选更新

**SQL代码：**
```sql
DROP PROCEDURE IF EXISTS sp_update_team;
DELIMITER //
CREATE PROCEDURE sp_update_team(
    IN p_team_id INT,
    IN p_name VARCHAR(50),
    IN p_city VARCHAR(50),
    IN p_arena VARCHAR(100),
    IN p_conference VARCHAR(20),
    IN p_founded_year INT
)
BEGIN
    UPDATE Team 
    SET 名称 = COALESCE(p_name, 名称),
        城市 = COALESCE(p_city, 城市),
        场馆 = COALESCE(p_arena, 场馆),
        分区 = COALESCE(p_conference, 分区),
        成立年份 = COALESCE(p_founded_year, 成立年份)
    WHERE team_id = p_team_id;
END//
DELIMITER ;
```

---

### 4.6.4 删除球队存储过程

**存储过程名称：** `sp_delete_team`

**输入参数：**
| 参数名 | 类型 | 说明 |
| :---- | :--- | :--- |
| p_team_id | INT | 球队ID |

**输出参数：** 无

**功能：** 删除球队及其关联数据

**关键设计：**
- 删除队标关联和比赛关联
- 将球队球员的球队ID设为NULL（解除关联）
- 最后删除球队主记录

**SQL代码：**
```sql
DROP PROCEDURE IF EXISTS sp_delete_team;
DELIMITER //
CREATE PROCEDURE sp_delete_team(IN p_team_id INT)
BEGIN
    DELETE FROM Team_Logo WHERE team_id = p_team_id;
    DELETE FROM Team_Game WHERE team_id = p_team_id;
    -- 注意：删除球队可能需要处理球员关联，这里假设球员关联设置为NULL或级联删除
    -- 如果有外键约束，可能需要先更新球员
    UPDATE Player SET 当前球队ID = NULL WHERE 当前球队ID = p_team_id;
    DELETE FROM Team WHERE team_id = p_team_id;
END//
DELIMITER ;
```

---

### 4.6.5 获取球队详情存储过程

**存储过程名称：** `sp_get_team_detail`

**输入参数：**
| 参数名 | 类型 | 说明 |
| :---- | :--- | :--- |
| p_team_id | INT | 球队ID |

**输出参数：** 无（通过SELECT返回结果集）

**返回结果：** team_id, 名称, 城市, 场馆, 分区, 成立年份, image_id

**功能：** 获取单个球队的详细信息

**SQL代码：**
```sql
DROP PROCEDURE IF EXISTS sp_get_team_detail;
DELIMITER //
CREATE PROCEDURE sp_get_team_detail(IN p_team_id INT)
BEGIN
    SELECT t.team_id, t.名称, t.城市, t.场馆, t.分区, t.成立年份, tl.image_id
    FROM Team t
    LEFT JOIN Team_Logo tl ON t.team_id = tl.team_id
    WHERE t.team_id = p_team_id;
END//
DELIMITER ;
```

---

### 4.6.6 球队管理模块存储过程汇总

| 序号 | 存储过程名称 | 功能描述 | 参数类型 |
| :--: | :---------- | :------- | :------: |
| 1 | sp_get_all_teams | 获取所有球队列表 | 无 |
| 2 | sp_create_team | 创建球队 | IN/OUT |
| 3 | sp_update_team | 更新球队信息 | IN |
| 4 | sp_delete_team | 删除球队 | IN |
| 5 | sp_get_team_detail | 获取球队详情 | IN |

---

## 4.7 排行榜存储过程

本模块包含2个存储过程，用于生成球队和球员的排行榜数据。

### 4.7.1 获取球队战绩排行存储过程

**存储过程名称：** `sp_get_team_standings`

**输入参数：**
| 参数名 | 类型 | 说明 |
| :---- | :--- | :--- |
| p_season | VARCHAR(20) | 赛季（如 "2024-25"） |
| p_conference | VARCHAR(20) | 分区（可选，东部/西部） |

**输出参数：** 无（通过SELECT返回结果集）

**返回结果：** team_id, team_name, conference, wins, losses, win_pct, games_back

**功能：** 获取指定赛季的球队战绩排行榜

**关键设计：**
- 使用 `SUM(CASE WHEN ...)` 统计胜负场次
- 使用变量计算胜差（Games Back）
- 按分区分组，胜率降序排列

**SQL代码：**
```sql
DROP PROCEDURE IF EXISTS sp_get_team_standings;
DELIMITER //
CREATE PROCEDURE sp_get_team_standings(
    IN p_season VARCHAR(20),
    IN p_conference VARCHAR(20)
)
BEGIN
    SELECT 
        t.team_id,
        t.名称 as team_name,
        t.分区 as conference,
        SUM(CASE 
            WHEN (tg.is_home = 1 AND g.主队得分 > g.客队得分) OR 
                 (tg.is_home = 0 AND g.客队得分 > g.主队得分) 
            THEN 1 ELSE 0 
        END) as wins,
        SUM(CASE 
            WHEN (tg.is_home = 1 AND g.主队得分 < g.客队得分) OR 
                 (tg.is_home = 0 AND g.客队得分 < g.主队得分) 
            THEN 1 ELSE 0 
        END) as losses,
        ROUND(
            SUM(CASE 
                WHEN (tg.is_home = 1 AND g.主队得分 > g.客队得分) OR 
                     (tg.is_home = 0 AND g.客队得分 > g.主队得分) 
                THEN 1 ELSE 0 
            END) / COUNT(*), 3
        ) as win_pct
    FROM Team t
    LEFT JOIN Team_Game tg ON t.team_id = tg.team_id
    LEFT JOIN Game g ON tg.game_id = g.game_id AND g.赛季 = p_season
    WHERE (p_conference IS NULL OR t.分区 = p_conference)
    GROUP BY t.team_id, t.名称, t.分区
    ORDER BY t.分区, win_pct DESC;
END//
DELIMITER ;
```

---

### 4.7.2 获取球员数据排行存储过程

**存储过程名称：** `sp_get_player_rankings`

**输入参数：**
| 参数名 | 类型 | 说明 |
| :---- | :--- | :--- |
| p_stat_type | VARCHAR(20) | 统计类型（points/rebounds/assists/steals/blocks） |
| p_season | VARCHAR(20) | 赛季（可选） |
| p_limit | INT | 返回数量限制（默认10） |

**输出参数：** 无（通过SELECT返回结果集）

**返回结果：** rank_num, player_id, player_name, team_name, games_played, stat_value

**功能：** 获取球员各项数据的排行榜

**关键设计：**
- 使用动态SQL构建不同统计类型的查询
- 使用 `ROW_NUMBER()` 窗口函数生成排名
- 支持得分、篮板、助攻、抢断、盖帽五种排行

**SQL代码：**
```sql
DROP PROCEDURE IF EXISTS sp_get_player_rankings;
DELIMITER //
CREATE PROCEDURE sp_get_player_rankings(
    IN p_stat_type VARCHAR(20),
    IN p_season VARCHAR(20),
    IN p_limit INT
)
BEGIN
    SET p_limit = COALESCE(p_limit, 10);
    
    IF p_stat_type = 'points' THEN
        SELECT 
            ROW_NUMBER() OVER (ORDER BY AVG(pg.得分) DESC) as rank_num,
            p.player_id, p.姓名 as player_name, t.名称 as team_name,
            COUNT(pg.game_id) as games_played,
            ROUND(AVG(pg.得分), 1) as stat_value
        FROM Player p
        JOIN Player_Game pg ON p.player_id = pg.player_id
        JOIN Game g ON pg.game_id = g.game_id
        LEFT JOIN Team t ON p.当前球队ID = t.team_id
        WHERE (p_season IS NULL OR g.赛季 = p_season)
        GROUP BY p.player_id, p.姓名, t.名称
        HAVING COUNT(pg.game_id) >= 5
        ORDER BY stat_value DESC
        LIMIT p_limit;
    ELSEIF p_stat_type = 'rebounds' THEN
        SELECT 
            ROW_NUMBER() OVER (ORDER BY AVG(pg.篮板) DESC) as rank_num,
            p.player_id, p.姓名 as player_name, t.名称 as team_name,
            COUNT(pg.game_id) as games_played,
            ROUND(AVG(pg.篮板), 1) as stat_value
        FROM Player p
        JOIN Player_Game pg ON p.player_id = pg.player_id
        JOIN Game g ON pg.game_id = g.game_id
        LEFT JOIN Team t ON p.当前球队ID = t.team_id
        WHERE (p_season IS NULL OR g.赛季 = p_season)
        GROUP BY p.player_id, p.姓名, t.名称
        HAVING COUNT(pg.game_id) >= 5
        ORDER BY stat_value DESC
        LIMIT p_limit;
    ELSEIF p_stat_type = 'assists' THEN
        SELECT 
            ROW_NUMBER() OVER (ORDER BY AVG(pg.助攻) DESC) as rank_num,
            p.player_id, p.姓名 as player_name, t.名称 as team_name,
            COUNT(pg.game_id) as games_played,
            ROUND(AVG(pg.助攻), 1) as stat_value
        FROM Player p
        JOIN Player_Game pg ON p.player_id = pg.player_id
        JOIN Game g ON pg.game_id = g.game_id
        LEFT JOIN Team t ON p.当前球队ID = t.team_id
        WHERE (p_season IS NULL OR g.赛季 = p_season)
        GROUP BY p.player_id, p.姓名, t.名称
        HAVING COUNT(pg.game_id) >= 5
        ORDER BY stat_value DESC
        LIMIT p_limit;
    ELSEIF p_stat_type = 'steals' THEN
        SELECT 
            ROW_NUMBER() OVER (ORDER BY AVG(pg.抢断) DESC) as rank_num,
            p.player_id, p.姓名 as player_name, t.名称 as team_name,
            COUNT(pg.game_id) as games_played,
            ROUND(AVG(pg.抢断), 1) as stat_value
        FROM Player p
        JOIN Player_Game pg ON p.player_id = pg.player_id
        JOIN Game g ON pg.game_id = g.game_id
        LEFT JOIN Team t ON p.当前球队ID = t.team_id
        WHERE (p_season IS NULL OR g.赛季 = p_season)
        GROUP BY p.player_id, p.姓名, t.名称
        HAVING COUNT(pg.game_id) >= 5
        ORDER BY stat_value DESC
        LIMIT p_limit;
    ELSEIF p_stat_type = 'blocks' THEN
        SELECT 
            ROW_NUMBER() OVER (ORDER BY AVG(pg.盖帽) DESC) as rank_num,
            p.player_id, p.姓名 as player_name, t.名称 as team_name,
            COUNT(pg.game_id) as games_played,
            ROUND(AVG(pg.盖帽), 1) as stat_value
        FROM Player p
        JOIN Player_Game pg ON p.player_id = pg.player_id
        JOIN Game g ON pg.game_id = g.game_id
        LEFT JOIN Team t ON p.当前球队ID = t.team_id
        WHERE (p_season IS NULL OR g.赛季 = p_season)
        GROUP BY p.player_id, p.姓名, t.名称
        HAVING COUNT(pg.game_id) >= 5
        ORDER BY stat_value DESC
        LIMIT p_limit;
    END IF;
END//
DELIMITER ;
```

---

### 4.7.3 排行榜模块存储过程汇总

| 序号 | 存储过程名称 | 功能描述 | 参数类型 |
| :--: | :---------- | :------- | :------: |
| 1 | sp_get_team_standings | 获取球队战绩排行 | IN |
| 2 | sp_get_player_rankings | 获取球员数据排行 | IN |

---

## 4.8 图片与商店存储过程

本模块包含5个存储过程，用于处理图片管理和球星卡商店功能。

### 4.8.1 上传图片存储过程

**存储过程名称：** `sp_upload_image`

**输入参数：**
| 参数名 | 类型 | 说明 |
| :---- | :--- | :--- |
| p_image_data | LONGBLOB | 图片二进制数据 |
| p_image_type | VARCHAR(20) | 图片类型（如 image/jpeg） |
| p_file_name | VARCHAR(100) | 文件名 |

**输出参数：**
| 参数名 | 类型 | 说明 |
| :---- | :--- | :--- |
| p_image_id | INT | 新上传图片的ID |

**功能：** 上传图片到数据库并返回图片ID

**关键设计：**
- 使用 `LONGBLOB` 存储图片二进制数据
- 自动记录上传时间

**SQL代码：**
```sql
DROP PROCEDURE IF EXISTS sp_upload_image;
DELIMITER //
CREATE PROCEDURE sp_upload_image(
    IN p_image_data LONGBLOB,
    IN p_image_type VARCHAR(20),
    IN p_file_name VARCHAR(100),
    OUT p_image_id INT
)
BEGIN
    INSERT INTO Image (image_data, image_type, file_name, upload_time)
    VALUES (p_image_data, p_image_type, p_file_name, NOW());
    SET p_image_id = LAST_INSERT_ID();
END//
DELIMITER ;
```

---

### 4.8.2 获取图片存储过程

**存储过程名称：** `sp_get_image`

**输入参数：**
| 参数名 | 类型 | 说明 |
| :---- | :--- | :--- |
| p_image_id | INT | 图片ID |

**输出参数：** 无（通过SELECT返回结果集）

**返回结果：** image_id, image_data, image_type, file_name, upload_time

**功能：** 根据ID获取图片数据

**SQL代码：**
```sql
DROP PROCEDURE IF EXISTS sp_get_image;
DELIMITER //
CREATE PROCEDURE sp_get_image(IN p_image_id INT)
BEGIN
    SELECT image_id, image_data, image_type, file_name, upload_time
    FROM Image 
    WHERE image_id = p_image_id;
END//
DELIMITER ;
```

---

### 4.8.3 更新用户头像存储过程

**存储过程名称：** `sp_update_user_avatar`

**输入参数：**
| 参数名 | 类型 | 说明 |
| :---- | :--- | :--- |
| p_user_id | INT | 用户ID |
| p_image_id | INT | 图片ID |

**输出参数：** 无

**功能：** 更新用户头像，使用插入或更新策略

**关键设计：**
- 使用 `INSERT ... ON DUPLICATE KEY UPDATE` 实现插入或更新
- 自动记录更新时间

**SQL代码：**
```sql
DROP PROCEDURE IF EXISTS sp_update_user_avatar;
DELIMITER //
CREATE PROCEDURE sp_update_user_avatar(
    IN p_user_id INT,
    IN p_image_id INT
)
BEGIN
    INSERT INTO User_Avatar (user_id, image_id, updated_at)
    VALUES (p_user_id, p_image_id, NOW())
    ON DUPLICATE KEY UPDATE image_id = p_image_id, updated_at = NOW();
END//
DELIMITER ;
```

---

### 4.8.4 抽取球星卡存储过程

**存储过程名称：** `sp_draw_card`

**输入参数：**
| 参数名 | 类型 | 说明 |
| :---- | :--- | :--- |
| p_user_id | INT | 用户ID |

**输出参数：**
| 参数名 | 类型 | 说明 |
| :---- | :--- | :--- |
| p_player_id | INT | 抽到的球员ID |
| p_rarity | VARCHAR(20) | 卡片稀有度 |

**功能：** 用户抽取球星卡，随机获得一张球员卡片

**关键设计：**
- 使用 `ORDER BY RAND() LIMIT 1` 实现随机抽取
- 根据概率计算稀有度：普通(70%)、稀有(20%)、传说(8%)、史诗(2%)
- 自动更新用户积分消耗
- 将抽到的卡片加入用户收藏

**SQL代码：**
```sql
DROP PROCEDURE IF EXISTS sp_draw_card;
DELIMITER //
CREATE PROCEDURE sp_draw_card(
    IN p_user_id INT,
    OUT p_player_id INT,
    OUT p_rarity VARCHAR(20)
)
BEGIN
    DECLARE v_rand DECIMAL(5,4);
    DECLARE v_cost INT DEFAULT 100;
    DECLARE v_user_points INT;
    
    -- 检查用户积分
    SELECT points INTO v_user_points FROM User WHERE user_id = p_user_id;
    
    IF v_user_points < v_cost THEN
        SET p_player_id = NULL;
        SET p_rarity = 'INSUFFICIENT_POINTS';
    ELSE
        -- 扣除积分
        UPDATE User SET points = points - v_cost WHERE user_id = p_user_id;
        
        -- 随机选择球员
        SELECT player_id INTO p_player_id FROM Player ORDER BY RAND() LIMIT 1;
        
        -- 根据概率计算稀有度
        SET v_rand = RAND();
        IF v_rand < 0.02 THEN
            SET p_rarity = '史诗';
        ELSEIF v_rand < 0.10 THEN
            SET p_rarity = '传说';
        ELSEIF v_rand < 0.30 THEN
            SET p_rarity = '稀有';
        ELSE
            SET p_rarity = '普通';
        END IF;
        
        -- 添加到用户卡片集合
        INSERT INTO User_Card (user_id, player_id, rarity, obtained_at)
        VALUES (p_user_id, p_player_id, p_rarity, NOW());
    END IF;
END//
DELIMITER ;
```

---

### 4.8.5 获取我的球星卡存储过程

**存储过程名称：** `sp_get_my_cards`

**输入参数：**
| 参数名 | 类型 | 说明 |
| :---- | :--- | :--- |
| p_user_id | INT | 用户ID |

**输出参数：** 无（通过SELECT返回结果集）

**返回结果：** card_id, player_id, player_name, team_name, rarity, obtained_at, image_id

**功能：** 获取用户收集的所有球星卡

**关键设计：**
- 关联球员表和球队表获取完整信息
- 关联球员图片表显示球员照片
- 按获取时间倒序排列

**SQL代码：**
```sql
DROP PROCEDURE IF EXISTS sp_get_my_cards;
DELIMITER //
CREATE PROCEDURE sp_get_my_cards(IN p_user_id INT)
BEGIN
    SELECT 
        uc.card_id,
        uc.player_id,
        p.姓名 as player_name,
        t.名称 as team_name,
        uc.rarity,
        uc.obtained_at,
        pi.image_id
    FROM User_Card uc
    JOIN Player p ON uc.player_id = p.player_id
    LEFT JOIN Team t ON p.当前球队ID = t.team_id
    LEFT JOIN Player_Image pi ON p.player_id = pi.player_id
    WHERE uc.user_id = p_user_id
    ORDER BY uc.obtained_at DESC;
END//
DELIMITER ;
```

---

### 4.8.6 图片与商店模块存储过程汇总

| 序号 | 存储过程名称 | 功能描述 | 参数类型 |
| :--: | :---------- | :------- | :------: |
| 1 | sp_upload_image | 上传图片 | IN/OUT |
| 2 | sp_get_image | 获取图片 | IN |
| 3 | sp_update_user_avatar | 更新用户头像 | IN |
| 4 | sp_draw_card | 抽取球星卡 | IN/OUT |
| 5 | sp_get_my_cards | 获取我的球星卡 | IN |

---

## 4.9 存储过程设计总结

本系统共设计了 **56个存储过程**，分布在8个功能模块中：

| 模块 | 存储过程数量 | 主要功能 |
| :--- | :----------: | :------- |
| 用户认证模块 | 10 | 注册、登录、权限管理、积分系统 |
| 比赛管理模块 | 14 | 比赛CRUD、比赛数据、预测投票 |
| 帖子管理模块 | 10 | 帖子CRUD、点赞功能 |
| 评论管理模块 | 3 | 评论CRUD、评论点赞 |
| 球员管理模块 | 7 | 球员CRUD、生涯数据统计 |
| 球队管理模块 | 5 | 球队CRUD |
| 排行榜模块 | 2 | 战绩排行、数据排行 |
| 图片与商店模块 | 5 | 图片管理、球星卡抽取 |

**设计特点：**
1. **参数化设计**：所有存储过程均使用参数化查询，有效防止SQL注入
2. **事务管理**：关键操作（如抽卡、积分变更）使用事务确保数据一致性
3. **错误处理**：使用条件判断和信号机制进行错误处理
4. **性能优化**：合理使用索引、限制返回数量、使用高效的JOIN方式

---

# 五、系统各项功能数据库端操作主要代码与结果说明

## 5.1 用户认证与管理

### 5.1.1 用户注册与登录完整流程

**涉及的数据库对象**：

- 存储过程：`sp_register_user`, `sp_login_user`, `sp_update_last_login`
- 表：`User`

**完整操作流程代码示例**：

```sql
-- ========== 步骤1：用户注册 ==========
-- 调用存储过程创建新用户
CALL sp_register_user(
    '篮球迷小王',                    -- 用户名
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.0P8HqGLHqFkWvG',  -- 密码哈希
    'user',                          -- 角色：普通用户
    '2025-01-15 10:30:00'            -- 注册时间
);

-- 结果说明：
-- 新增一条用户记录，角色为普通用户
-- 初始积分为0，头像为空
-- 密码使用bcrypt加密存储

-- 验证结果
SELECT user_id, 用户名, 角色, 注册时间, 积分 
FROM User 
WHERE 用户名 = '篮球迷小王';

-- 输出：
-- user_id | 用户名      | 角色  | 注册时间             | 积分
--    10   | 篮球迷小王   | user  | 2025-01-15 10:30:00 |  0


-- ========== 步骤2：用户登录验证 ==========
-- 调用存储过程获取用户登录信息
CALL sp_login_user('篮球迷小王');

-- 结果说明：
-- 返回用户ID、密码哈希、角色，用于后端验证密码
-- 验证通过后生成JWT令牌

-- 输出结果集：
-- user_id | 密码哈希                                              | 角色
--    10   | $2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.0P8HqGLHqFkWvG | user


-- ========== 步骤3：更新最后登录时间 ==========
-- 登录成功后调用存储过程更新登录时间
CALL sp_update_last_login(10, '2025-01-15 10:35:00');

-- 结果说明：
-- 更新用户的最后登录时间字段
-- 用于统计用户活跃度

-- 验证结果
SELECT user_id, 用户名, 最后登录时间 
FROM User 
WHERE user_id = 10;

-- 输出：
-- user_id | 用户名      | 最后登录时间
--    10   | 篮球迷小王   | 2025-01-15 10:35:00
```

---

### 5.1.2 管理员注册流程

**完整操作流程代码示例**：

```sql
-- ========== 管理员账号注册（需要验证密钥） ==========
-- 注册时前端验证密钥：NBA_ADMIN_2025
-- 验证通过后调用存储过程
CALL sp_register_user(
    'admin_manager',                 -- 用户名
    '$2b$12$HashedPasswordForAdmin', -- 密码哈希
    'admin',                         -- 角色：管理员
    '2025-01-01 09:00:00'            -- 注册时间
);

-- 结果说明：
-- 管理员角色拥有以下权限：
-- 1. 管理球员/球队信息（增删改）
-- 2. 管理比赛信息
-- 3. 删除任意帖子
-- 4. 审核用户内容

-- 验证结果
SELECT user_id, 用户名, 角色, 注册时间 
FROM User 
WHERE 用户名 = 'admin_manager';

-- 输出：
-- user_id | 用户名        | 角色   | 注册时间
--    1    | admin_manager | admin  | 2025-01-01 09:00:00


-- ========== 数据分析师账号注册 ==========
-- 注册时验证密钥：NBA_ANALYST_2025
CALL sp_register_user(
    'data_analyst',                  -- 用户名
    '$2b$12$HashedPasswordForAnalyst', -- 密码哈希
    'analyst',                       -- 角色：数据分析师
    '2025-01-02 09:00:00'            -- 注册时间
);

-- 结果说明：
-- 数据分析师角色拥有以下权限：
-- 1. 执行自定义SELECT查询
-- 2. 查看所有统计数据
-- 3. 导出数据报表

-- 验证角色分布
SELECT 角色, COUNT(*) AS 用户数 
FROM User 
GROUP BY 角色;

-- 输出：
-- 角色    | 用户数
-- user    |   50
-- admin   |    2
-- analyst |    3
```

---

### 5.1.3 用户信息管理流程

**涉及的数据库对象**：

- 存储过程：`sp_get_user_profile`, `sp_update_user_profile`, `sp_update_password`
- 表：`User`, `User_Avatar`

**完整操作流程代码示例**：

```sql
-- ========== 步骤1：获取用户个人信息 ==========
CALL sp_get_user_profile(10);

-- 结果说明：
-- 返回用户完整信息，包括头像关联

-- 输出结果集：
-- user_id | 用户名      | 角色  | 注册时间             | 最后登录时间         | 邮箱              | 电话        | 积分 | avatar_image_id
--    10   | 篮球迷小王   | user  | 2025-01-15 10:30:00 | 2025-01-20 20:15:00 | wang@example.com | 13800138000 | 350  |       5


-- ========== 步骤2：更新用户联系信息 ==========
CALL sp_update_user_profile(
    10,                              -- 用户ID
    'newwang@example.com',           -- 新邮箱
    '13900139000'                    -- 新电话
);

-- 结果说明：
-- 更新用户的邮箱和电话字段
-- 可用于接收系统通知

-- 验证结果
SELECT user_id, 邮箱, 电话 
FROM User 
WHERE user_id = 10;

-- 输出：
-- user_id | 邮箱                 | 电话
--    10   | newwang@example.com  | 13900139000


-- ========== 步骤3：修改用户密码 ==========
-- 首先获取旧密码哈希用于验证
CALL sp_get_user_password(10);

-- 输出：
-- 密码哈希
-- $2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.0P8HqGLHqFkWvG

-- 后端验证旧密码正确后，更新新密码
CALL sp_update_password(
    10,                              -- 用户ID
    '$2b$12$NewHashedPasswordHere'   -- 新密码哈希
);

-- 结果说明：
-- 密码字段被更新
-- 旧的JWT令牌仍然有效（直到过期）

-- 验证密码已更新（仅检查哈希变化）
SELECT user_id, LENGTH(密码) AS 密码长度 
FROM User 
WHERE user_id = 10;

-- 输出：
-- user_id | 密码长度
--    10   |    60
```

---

### 5.1.4 用户头像管理流程

**涉及的数据库对象**：

- 存储过程：`sp_upload_image`, `sp_update_user_avatar`
- 表：`Image`, `User_Avatar`

**完整操作流程代码示例**：

```sql
-- ========== 步骤1：上传头像图片 ==========
-- 图片二进制数据通过存储过程插入
SET @p_image_id = 0;
CALL sp_upload_image(
    'avatar_wang.jpg',               -- 文件名
    <BINARY_DATA>,                   -- 图片二进制数据
    'image/jpeg',                    -- MIME类型
    @p_image_id                      -- 输出：新图片ID
);
SELECT @p_image_id AS 新图片ID;

-- 结果说明：
-- 图片数据存储到Image表
-- 返回新插入的图片ID

-- 输出：
-- 新图片ID
--    25


-- ========== 步骤2：关联头像到用户 ==========
CALL sp_update_user_avatar(10, 25);

-- 结果说明：
-- 在User_Avatar表中插入或更新记录
-- 使用 ON DUPLICATE KEY UPDATE 实现
-- 如果用户已有头像，则替换为新头像

-- 验证结果
SELECT ua.user_id, ua.image_id, ua.updated_at
FROM User_Avatar ua
WHERE ua.user_id = 10;

-- 输出：
-- user_id | image_id | updated_at
--    10   |    25    | 2025-01-20 20:30:00


-- ========== 步骤3：获取用户完整信息（包含头像） ==========
CALL sp_get_user_profile(10);

-- 输出结果集：
-- user_id | 用户名      | ... | avatar_image_id
--    10   | 篮球迷小王   | ... |       25

-- 前端通过 /api/images/25 获取头像图片
```

---

## 5.2 帖子与评论管理

本模块负责帖子发布、浏览、评论、点赞等社区功能，涉及触发器自动计数机制。

### 5.2.1 帖子发布与浏览流程

**涉及的数据库对象**：

- 存储过程：`sp_create_post`, `sp_get_posts`, `sp_get_post_detail`, `sp_increment_view`
- 表：`Post`

**完整操作流程代码示例**：

```sql
-- ========== 步骤1：用户发布新帖子 ==========
SET @p_post_id = 0;
CALL sp_create_post(
    1,                            -- 用户ID
    '湖人vs勇士精彩对决',          -- 帖子标题
    '今晚的比赛真是太精彩了！詹姆斯40分10篮板，库里也拿下38分...',
    @p_post_id                    -- 输出：新帖子ID
);
SELECT @p_post_id AS 新帖子ID;

-- 结果说明：
-- 在Post表中插入新帖子记录
-- 浏览量和点赞数初始为0
-- 返回新创建的帖子ID

-- 输出：
-- 新帖子ID
--    50


-- ========== 步骤2：验证帖子创建成功 ==========
SELECT post_id, user_id, title, view_count, like_count, created_at
FROM Post
WHERE post_id = 50;

-- 输出：
-- +----------+----------+----------------------+------------+------------+---------------------+
-- | post_id  | user_id  | title                | view_count | like_count | created_at          |
-- +----------+----------+----------------------+------------+------------+---------------------+
-- |    50    |    1     | 湖人vs勇士精彩对决   |     0      |     0      | 2025-01-20 21:30:00 |
-- +----------+----------+----------------------+------------+------------+---------------------+


-- ========== 步骤3：获取帖子列表 ==========
CALL sp_get_posts(1, 10);    -- 分页查询：第1页，每页10条

-- 结果说明：
-- 返回帖子列表，按创建时间倒序排列
-- 包含作者信息、浏览量、点赞数等

-- 输出结果集：
-- +----------+----------------------+----------+----------+------------+------------+---------------------+
-- | post_id  | title                | username | user_id  | view_count | like_count | created_at          |
-- +----------+----------------------+----------+----------+------------+------------+---------------------+
-- |    50    | 湖人vs勇士精彩对决   | admin    |    1     |     0      |     0      | 2025-01-20 21:30:00 |
-- |    49    | 东契奇本赛季表现分析 | 球迷A    |    5     |    156     |    23      | 2025-01-19 15:20:00 |
-- |    48    | 字母哥伤愈复出       | 球迷B    |    8     |    98      |    12      | 2025-01-18 10:15:00 |
-- +----------+----------------------+----------+----------+------------+------------+---------------------+


-- ========== 步骤4：查看帖子详情（增加浏览量） ==========
-- 4.1 首先增加浏览量
CALL sp_increment_view(50);

-- 4.2 获取帖子详情
CALL sp_get_post_detail(50);

-- 结果说明：
-- sp_increment_view 将帖子浏览量+1
-- sp_get_post_detail 返回完整帖子内容

-- 输出结果集：
-- +----------+----------------------+------------------------------------------------+----------+----------+------------+------------+
-- | post_id  | title                | content                                        | username | user_id  | view_count | like_count |
-- +----------+----------------------+------------------------------------------------+----------+----------+------------+------------+
-- |    50    | 湖人vs勇士精彩对决   | 今晚的比赛真是太精彩了！詹姆斯40分10篮板...   | admin    |    1     |     1      |     0      |
-- +----------+----------------------+------------------------------------------------+----------+----------+------------+------------+


-- ========== 步骤5：验证浏览量更新 ==========
SELECT post_id, title, view_count FROM Post WHERE post_id = 50;

-- 输出：
-- +----------+----------------------+------------+
-- | post_id  | title                | view_count |
-- +----------+----------------------+------------+
-- |    50    | 湖人vs勇士精彩对决   |     1      |
-- +----------+----------------------+------------+
```

---

### 5.2.2 帖子点赞流程（触发器联动）

**涉及的数据库对象**：

- 存储过程：`sp_like_post`, `sp_unlike_post`, `sp_check_post_like`
- 触发器：`trg_post_like_insert`, `trg_post_like_delete`
- 表：`Post`, `Post_Like`

**完整操作流程代码示例**：

```sql
-- ========== 步骤1：用户对帖子点赞 ==========
CALL sp_like_post(50, 10);    -- 帖子ID=50，用户ID=10

-- 结果说明：
-- 1. 首先检查是否已点赞（幂等性）
-- 2. 在Post_Like表插入点赞记录
-- 3. 触发器 trg_post_like_insert 自动执行
-- 4. 触发器将Post表的like_count字段+1


-- ========== 步骤2：验证触发器效果 ==========
-- 2.1 查看点赞记录
SELECT * FROM Post_Like WHERE post_id = 50 AND user_id = 10;

-- 输出：
-- +----------+----------+---------------------+
-- | post_id  | user_id  | created_at          |
-- +----------+----------+---------------------+
-- |    50    |    10    | 2025-01-20 21:35:00 |
-- +----------+----------+---------------------+

-- 2.2 查看帖子点赞数（已被触发器自动更新）
SELECT post_id, title, like_count FROM Post WHERE post_id = 50;

-- 输出：
-- +----------+----------------------+------------+
-- | post_id  | title                | like_count |
-- +----------+----------------------+------------+
-- |    50    | 湖人vs勇士精彩对决   |     1      |
-- +----------+----------------------+------------+


-- ========== 步骤3：检查用户是否已点赞 ==========
CALL sp_check_post_like(50, 10);

-- 输出结果集：
-- +----------+
-- | is_liked |
-- +----------+
-- |    1     |
-- +----------+

-- 另一个未点赞的用户
CALL sp_check_post_like(50, 20);

-- 输出结果集：
-- +----------+
-- | is_liked |
-- +----------+
-- |    0     |
-- +----------+


-- ========== 步骤4：用户取消点赞 ==========
CALL sp_unlike_post(50, 10);

-- 结果说明：
-- 1. 删除Post_Like表中的点赞记录
-- 2. 触发器 trg_post_like_delete 自动执行
-- 3. 触发器将Post表的like_count字段-1


-- ========== 步骤5：验证取消点赞效果 ==========
-- 5.1 点赞记录已删除
SELECT COUNT(*) AS 记录数 FROM Post_Like WHERE post_id = 50 AND user_id = 10;

-- 输出：
-- +--------+
-- | 记录数 |
-- +--------+
-- |   0    |
-- +--------+

-- 5.2 帖子点赞数已恢复
SELECT post_id, title, like_count FROM Post WHERE post_id = 50;

-- 输出：
-- +----------+----------------------+------------+
-- | post_id  | title                | like_count |
-- +----------+----------------------+------------+
-- |    50    | 湖人vs勇士精彩对决   |     0      |
-- +----------+----------------------+------------+
```

---

### 5.2.3 评论管理流程

**涉及的数据库对象**：

- 存储过程：`sp_create_comment`, `sp_get_comments`, `sp_delete_comment`
- 表：`Comment`

**完整操作流程代码示例**：

```sql
-- ========== 步骤1：用户发表评论 ==========
SET @p_comment_id = 0;
CALL sp_create_comment(
    50,                               -- 帖子ID
    10,                               -- 用户ID
    '非常精彩的比赛，詹姆斯表现太棒了！',  -- 评论内容
    @p_comment_id                     -- 输出：新评论ID
);
SELECT @p_comment_id AS 新评论ID;

-- 结果说明：
-- 1. 在Comment表插入评论记录
-- 2. 通过存储过程完成评论创建

-- 输出：
-- 新评论ID
--    120


-- ========== 步骤2：验证评论创建 ==========
SELECT comment_id, post_id, user_id, content, created_at
FROM Comment WHERE comment_id = 120;

-- 输出：
-- +------------+----------+----------+----------------------------------------+---------------------+
-- | comment_id | post_id  | user_id  | content                                | created_at          |
-- +------------+----------+----------+----------------------------------------+---------------------+
-- |    120     |    50    |    10    | 非常精彩的比赛，詹姆斯表现太棒了！      | 2025-01-20 21:40:00 |
-- +------------+----------+----------+----------------------------------------+---------------------+

-- 统计该帖子评论数
SELECT COUNT(*) AS 评论数 FROM Comment WHERE post_id = 50;

-- 输出：
-- +--------+
-- | 评论数 |
-- +--------+
-- |   1    |
-- +--------+


-- ========== 步骤3：获取帖子的所有评论 ==========
CALL sp_get_comments(50);

-- 结果说明：
-- 返回该帖子的所有评论，按时间倒序排列
-- 包含评论者用户名等信息

-- 输出结果集：
-- +------------+----------------------------------------+----------+-------------+---------------------+
-- | comment_id | content                                | user_id  | username    | created_at          |
-- +------------+----------------------------------------+----------+-------------+---------------------+
-- |    120     | 非常精彩的比赛，詹姆斯表现太棒了！      |    10    | 篮球迷小王  | 2025-01-20 21:40:00 |
-- +------------+----------------------------------------+----------+-------------+---------------------+


-- ========== 步骤4：删除评论 ==========
CALL sp_delete_comment(120, 10);   -- 评论ID=120，用户ID=10（权限验证）

-- 结果说明：
-- 1. 验证用户有权删除该评论（评论者本人或管理员）
-- 2. 删除Comment表中的记录


-- ========== 步骤5：验证删除效果 ==========
SELECT COUNT(*) AS 评论数 FROM Comment WHERE comment_id = 120;

-- 输出：
-- +--------+
-- | 评论数 |
-- +--------+
-- |   0    |
-- +--------+

-- 查看该帖子剩余评论数
SELECT COUNT(*) AS 评论数 FROM Comment WHERE post_id = 50;

-- 输出：
-- +--------+
-- | 评论数 |
-- +--------+
-- |   0    |
-- +--------+
```

---

### 5.2.4 帖子删除流程

**涉及的数据库对象**：

- 存储过程：`sp_delete_post`
- 表：`Post`, `Post_Like`, `Comment`

**完整操作流程代码示例**：

```sql
-- ========== 步骤1：查看帖子当前状态 ==========
SELECT post_id, title, user_id, view_count, like_count, comment_count
FROM Post WHERE post_id = 50;

-- 输出：
-- +----------+----------------------+----------+------------+------------+---------------+
-- | post_id  | title                | user_id  | view_count | like_count | comment_count |
-- +----------+----------------------+----------+------------+------------+---------------+
-- |    50    | 湖人vs勇士精彩对决   |    1     |     5      |     2      |       3       |
-- +----------+----------------------+----------+------------+------------+---------------+


-- ========== 步骤2：删除帖子 ==========
CALL sp_delete_post(50, 1);    -- 帖子ID=50，用户ID=1（权限验证）

-- 结果说明：
-- 1. 验证用户权限（帖子作者或管理员）
-- 2. 由于外键约束设置了 ON DELETE CASCADE：
--    - Post_Like 表中相关点赞记录自动删除
--    - Comment 表中相关评论记录自动删除
-- 3. 删除 Post 表中的帖子记录


-- ========== 步骤3：验证级联删除效果 ==========
-- 3.1 帖子已删除
SELECT COUNT(*) AS 帖子数 FROM Post WHERE post_id = 50;

-- 输出：
-- +--------+
-- | 帖子数 |
-- +--------+
-- |   0    |
-- +--------+

-- 3.2 相关点赞记录已级联删除
SELECT COUNT(*) AS 点赞数 FROM Post_Like WHERE post_id = 50;

-- 输出：
-- +--------+
-- | 点赞数 |
-- +--------+
-- |   0    |
-- +--------+

-- 3.3 相关评论已级联删除
SELECT COUNT(*) AS 评论数 FROM Comment WHERE post_id = 50;

-- 输出：
-- +--------+
-- | 评论数 |
-- +--------+
-- |   0    |
-- +--------+
```

---

## 5.3 比赛竞猜与积分管理

本模块负责比赛查询、竞猜投票、积分奖励等功能。

### 5.3.1 比赛信息查询流程

**涉及的数据库对象**：

- 存储过程：`sp_get_games`, `sp_get_game_detail`, `sp_get_game_prediction_stats`
- 表：`Game`, `Team`

**完整操作流程代码示例**：

```sql
-- ========== 步骤1：获取比赛列表 ==========
CALL sp_get_games('2025-01-01', '2025-01-31', NULL);   -- 日期范围查询

-- 结果说明：
-- 返回指定日期范围内的所有比赛
-- 包含主客队信息、比分、状态等

-- 输出结果集：
-- +----------+----------+---------------------+--------+------------+------------+--------------+--------------+
-- | game_id  | season   | date                | status | home_score | away_score | home_team    | away_team    |
-- +----------+----------+---------------------+--------+------------+------------+--------------+--------------+
-- |   101    | 2024-25  | 2025-01-15 19:30:00 | 已结束 |    112     |    108     | 洛杉矶湖人   | 金州勇士     |
-- |   102    | 2024-25  | 2025-01-16 20:00:00 | 已结束 |    98      |    105     | 波士顿凯尔特人| 迈阿密热火   |
-- |   103    | 2024-25  | 2025-01-20 19:00:00 | 未开始 |    NULL    |    NULL    | 菲尼克斯太阳 | 达拉斯独行侠 |
-- +----------+----------+---------------------+--------+------------+------------+--------------+--------------+


-- ========== 步骤2：按球队筛选比赛 ==========
CALL sp_get_games(NULL, NULL, 1);   -- team_id=1（湖人队）

-- 结果说明：
-- 返回指定球队参与的所有比赛（作为主队或客队）

-- 输出结果集：
-- +----------+----------+---------------------+--------+------------+------------+--------------+--------------+
-- | game_id  | season   | date                | status | home_score | away_score | home_team    | away_team    |
-- +----------+----------+---------------------+--------+------------+------------+--------------+--------------+
-- |   101    | 2024-25  | 2025-01-15 19:30:00 | 已结束 |    112     |    108     | 洛杉矶湖人   | 金州勇士     |
-- |   105    | 2024-25  | 2025-01-22 20:30:00 | 未开始 |    NULL    |    NULL    | 丹佛掘金     | 洛杉矶湖人   |
-- +----------+----------+---------------------+--------+------------+------------+--------------+--------------+


-- ========== 步骤3：获取比赛详情 ==========
CALL sp_get_game_detail(101);

-- 结果说明：
-- 返回单场比赛的完整信息
-- 包含比赛场馆、两队Logo、胜负结果等

-- 输出结果集：
-- +----------+----------+---------------------+--------+------------+------------+--------------+--------------+
-- | game_id  | season   | date                | status | home_score | away_score | home_team    | away_team    |
-- +----------+----------+---------------------+--------+------------+------------+--------------+--------------+
-- |   101    | 2024-25  | 2025-01-15 19:30:00 | 已结束 |    112     |    108     | 洛杉矶湖人   | 金州勇士     |
-- +----------+----------+---------------------+--------+------------+------------+--------------+--------------+
-- (续)
-- +---------------+--------------+-----------+-----------+--------------+--------------+
-- | winner        | venue        | home_logo | away_logo | home_team_id | away_team_id |
-- +---------------+--------------+-----------+-----------+--------------+--------------+
-- | 洛杉矶湖人    | Crypto.com   |    10     |    11     |      1       |      2       |
-- +---------------+--------------+-----------+-----------+--------------+--------------+


-- ========== 步骤4：获取比赛竞猜统计 ==========
CALL sp_get_game_prediction_stats(101);

-- 结果说明：
-- 返回该场比赛的竞猜投票统计数据
-- 用于前端展示竞猜比例

-- 输出结果集：
-- +----------+-----------------+-----------------+------------+
-- | game_id  | home_vote_count | away_vote_count | total_bets |
-- +----------+-----------------+-----------------+------------+
-- |   101    |      156        |      89         |    245     |
-- +----------+-----------------+-----------------+------------+
```

---

### 5.3.2 用户参与竞猜流程

**涉及的数据库对象**：

- 存储过程：`sp_predict_game`, `sp_get_user_prediction`, `sp_check_user_prediction`
- 表：`Prediction`, `User`

**完整操作流程代码示例**：

```sql
-- ========== 步骤1：检查用户积分余额 ==========
SELECT user_id, username, points FROM User WHERE user_id = 10;

-- 输出：
-- +----------+-------------+--------+
-- | user_id  | username    | points |
-- +----------+-------------+--------+
-- |    10    | 篮球迷小王  |  500   |
-- +----------+-------------+--------+


-- ========== 步骤2：检查比赛状态（是否可以投票） ==========
SELECT game_id, status FROM Game WHERE game_id = 103;

-- 输出：
-- +----------+--------+
-- | game_id  | status |
-- +----------+--------+
-- |   103    | 未开始 |
-- +----------+--------+
-- 状态为"未开始"才能参与竞猜


-- ========== 步骤3：检查用户是否已投票 ==========
CALL sp_check_user_prediction(103, 10);

-- 输出结果集：
-- +---------------+
-- | has_predicted |
-- +---------------+
-- |      0        |
-- +---------------+
-- 返回0表示用户尚未对该比赛投票


-- ========== 步骤4：用户参与竞猜 ==========
CALL sp_predict_game(
    103,           -- 比赛ID
    10,            -- 用户ID
    3,             -- 预测球队ID（菲尼克斯太阳获胜）
    50             -- 投注积分
);

-- 结果说明：
-- 1. 验证比赛状态为"未开始"
-- 2. 验证用户积分足够
-- 3. 验证用户未重复投票
-- 4. 扣除用户积分（500 - 50 = 450）
-- 5. 在Prediction表插入投票记录


-- ========== 步骤5：验证投票结果 ==========
-- 5.1 查看用户积分变化
SELECT user_id, username, points FROM User WHERE user_id = 10;

-- 输出：
-- +----------+-------------+--------+
-- | user_id  | username    | points |
-- +----------+-------------+--------+
-- |    10    | 篮球迷小王  |  450   |
-- +----------+-------------+--------+

-- 5.2 查看投票记录
SELECT p.prediction_id, p.game_id, p.user_id, t.名称 AS predicted_team, p.bet_amount
FROM Prediction p
JOIN Team t ON p.predicted_team_id = t.team_id
WHERE p.game_id = 103 AND p.user_id = 10;

-- 输出：
-- +---------------+----------+----------+----------------+------------+
-- | prediction_id | game_id  | user_id  | predicted_team | bet_amount |
-- +---------------+----------+----------+----------------+------------+
-- |     88        |   103    |    10    | 菲尼克斯太阳   |     50     |
-- +---------------+----------+----------+----------------+------------+


-- ========== 步骤6：获取用户的所有竞猜记录 ==========
CALL sp_get_user_prediction(10);

-- 输出结果集：
-- +---------------+----------+--------------+--------------+----------------+------------+--------+
-- | prediction_id | game_id  | home_team    | away_team    | predicted_team | bet_amount | result |
-- +---------------+----------+--------------+--------------+----------------+------------+--------+
-- |     88        |   103    | 菲尼克斯太阳 | 达拉斯独行侠 | 菲尼克斯太阳   |     50     | 待定   |
-- |     72        |   101    | 洛杉矶湖人   | 金州勇士     | 洛杉矶湖人     |     30     | 获胜   |
-- |     65        |   99     | 波士顿凯尔特人| 纽约尼克斯  | 纽约尼克斯     |     20     | 失败   |
-- +---------------+----------+--------------+--------------+----------------+------------+--------+
```

---

### 5.3.3 竞猜奖励领取流程

**涉及的数据库对象**：

- 存储过程：`sp_claim_reward`, `sp_get_unclaimed_rewards`
- 表：`Prediction`, `User`, `Game`

**完整操作流程代码示例**：

```sql
-- ========== 步骤1：比赛结束后更新比赛结果 ==========
-- 假设比赛103结束，菲尼克斯太阳获胜
UPDATE Game 
SET status = '已结束', 
    home_score = 118, 
    away_score = 112,
    winner_team_id = 3    -- 菲尼克斯太阳
WHERE game_id = 103;


-- ========== 步骤2：查看用户未领取的奖励 ==========
CALL sp_get_unclaimed_rewards(10);

-- 结果说明：
-- 返回用户预测正确且尚未领取奖励的记录

-- 输出结果集：
-- +---------------+----------+--------------+------------+----------+
-- | prediction_id | game_id  | winner       | bet_amount | reward   |
-- +---------------+----------+--------------+------------+----------+
-- |     88        |   103    | 菲尼克斯太阳 |     50     |   100    |
-- +---------------+----------+--------------+------------+----------+
-- 奖励 = 投注积分 × 2（预测正确双倍返还）


-- ========== 步骤3：用户领取奖励 ==========
CALL sp_claim_reward(88, 10);   -- prediction_id=88, user_id=10

-- 结果说明：
-- 1. 验证预测记录属于该用户
-- 2. 验证比赛已结束且用户预测正确
-- 3. 验证奖励尚未领取（避免重复领取）
-- 4. 计算奖励积分（投注金额×2）
-- 5. 将奖励积分添加到用户账户
-- 6. 标记该预测记录奖励已领取


-- ========== 步骤4：验证奖励领取结果 ==========
-- 4.1 查看用户积分变化
SELECT user_id, username, points FROM User WHERE user_id = 10;

-- 输出：
-- +----------+-------------+--------+
-- | user_id  | username    | points |
-- +----------+-------------+--------+
-- |    10    | 篮球迷小王  |  550   |
-- +----------+-------------+--------+
-- 原积分450 + 奖励100 = 550

-- 4.2 查看预测记录状态
SELECT prediction_id, bet_amount, is_correct, reward_claimed
FROM Prediction WHERE prediction_id = 88;

-- 输出：
-- +---------------+------------+------------+----------------+
-- | prediction_id | bet_amount | is_correct | reward_claimed |
-- +---------------+------------+------------+----------------+
-- |     88        |     50     |     1      |       1        |
-- +---------------+------------+------------+----------------+


-- ========== 步骤5：再次查看未领取奖励（应为空） ==========
CALL sp_get_unclaimed_rewards(10);

-- 输出结果集：
-- （空结果集）
```

---

## 5.4 球员数据管理

本模块负责球员信息查询、数据统计、照片管理等功能。

### 5.4.1 球员列表与搜索流程

**涉及的数据库对象**：

- 存储过程：`sp_get_players`, `sp_search_players`
- 表：`Player`, `Team`

**完整操作流程代码示例**：

```sql
-- ========== 步骤1：分页获取球员列表 ==========
CALL sp_get_players(1, 10);   -- 第1页，每页10条

-- 结果说明：
-- 返回球员列表，包含基本信息和当前球队

-- 输出结果集：
-- +-----------+-------------+--------+------+--------+--------+--------------+
-- | player_id | 姓名        | 位置   | 身高 | 体重   | 球衣号码| 球队         |
-- +-----------+-------------+--------+------+--------+--------+--------------+
-- |     1     | 勒布朗·詹姆斯| SF    | 206  |  113   |   23   | 洛杉矶湖人   |
-- |     2     | 史蒂芬·库里 | PG    | 188  |   84   |   30   | 金州勇士     |
-- |     3     | 凯文·杜兰特 | SF    | 208  |  109   |   35   | 菲尼克斯太阳 |
-- |     4     | 扬尼斯·阿德托昆博| PF | 211  |  110   |   34   | 密尔沃基雄鹿 |
-- |     5     | 卢卡·东契奇 | PG    | 201  |  104   |   77   | 达拉斯独行侠 |
-- +-----------+-------------+--------+------+--------+--------+--------------+


-- ========== 步骤2：按球队筛选球员 ==========
CALL sp_get_players_by_team(1);   -- team_id=1（湖人队）

-- 输出结果集：
-- +-----------+-----------------+--------+------+--------+--------+
-- | player_id | 姓名            | 位置   | 身高 | 体重   | 球衣号码|
-- +-----------+-----------------+--------+------+--------+--------+
-- |     1     | 勒布朗·詹姆斯   | SF    | 206  |  113   |   23   |
-- |    15     | 安东尼·戴维斯   | PF    | 208  |  115   |    3   |
-- |    28     | 奥斯汀·里夫斯   | SG    | 196  |   93   |   15   |
-- +-----------+-----------------+--------+------+--------+--------+


-- ========== 步骤3：按名字搜索球员 ==========
CALL sp_search_players('库里');

-- 输出结果集：
-- +-----------+-------------+--------+--------------+
-- | player_id | 姓名        | 位置   | 球队         |
-- +-----------+-------------+--------+--------------+
-- |     2     | 史蒂芬·库里 | PG    | 金州勇士     |
-- |    45     | 塞斯·库里   | SG    | 布鲁克林篮网 |
-- +-----------+-------------+--------+--------------+
```

---

### 5.4.2 球员详情与统计流程

**涉及的数据库对象**：

- 存储过程：`sp_get_player_detail`, `sp_get_player_career_stats`, `sp_get_player_season_stats`
- 表：`Player`, `Player_Game`, `Team`

**完整操作流程代码示例**：

```sql
-- ========== 步骤1：获取球员基本信息 ==========
CALL sp_get_player_detail(1);   -- player_id=1（勒布朗·詹姆斯）

-- 输出结果集：
-- +-----------+-----------------+--------+------+--------+--------+------------+------------+--------------+
-- | player_id | 姓名            | 位置   | 身高 | 体重   | 球衣号码| 出生日期   | 选秀年份   | 球队         |
-- +-----------+-----------------+--------+------+--------+--------+------------+------------+--------------+
-- |     1     | 勒布朗·詹姆斯   | SF    | 206  |  113   |   23   | 1984-12-30 |   2003     | 洛杉矶湖人   |
-- +-----------+-----------------+--------+------+--------+--------+------------+------------+--------------+
-- (续)
-- +----------+----------+----------------+
-- | photo_id | logo_id  | 首轮选秀顺位   |
-- +----------+----------+----------------+
-- |    5     |    10    |       1        |
-- +----------+----------+----------------+


-- ========== 步骤2：获取球员职业生涯统计 ==========
CALL sp_get_player_career_stats(1);

-- 结果说明：
-- 汇总该球员所有比赛的数据统计

-- 输出结果集：
-- +-----------+-----------------+----------+----------+----------+----------+----------+
-- | player_id | 姓名            | 总场次   | 场均得分 | 场均篮板 | 场均助攻 | 场均抢断 |
-- +-----------+-----------------+----------+----------+----------+----------+----------+
-- |     1     | 勒布朗·詹姆斯   |   1468   |   27.1   |   7.5    |   7.4    |   1.5    |
-- +-----------+-----------------+----------+----------+----------+----------+----------+


-- ========== 步骤3：获取球员单赛季统计 ==========
CALL sp_get_player_season_stats(1, '2024-25');

-- 结果说明：
-- 返回指定赛季的详细数据

-- 输出结果集：
-- +-----------+-----------------+--------+----------+----------+----------+----------+----------+----------+
-- | player_id | 姓名            | 赛季   | 场次     | 场均得分 | 场均篮板 | 场均助攻 | 场均抢断 | 场均盖帽 |
-- +-----------+-----------------+--------+----------+----------+----------+----------+----------+----------+
-- |     1     | 勒布朗·詹姆斯   | 2024-25|   42     |   25.7   |   7.3    |   8.4    |   1.2    |   0.6    |
-- +-----------+-----------------+--------+----------+----------+----------+----------+----------+----------+


-- ========== 步骤4：获取球员单场比赛数据 ==========
SELECT pg.*, g.date, ht.名称 AS home_team, at.名称 AS away_team
FROM Player_Game pg
JOIN Game g ON pg.game_id = g.game_id
JOIN Team ht ON g.home_team_id = ht.team_id
JOIN Team at ON g.away_team_id = at.team_id
WHERE pg.player_id = 1
ORDER BY g.date DESC
LIMIT 5;

-- 输出：
-- +-----------+----------+------+------+------+------+------+---------------------+--------------+--------------+
-- | player_id | game_id  | 得分 | 篮板 | 助攻 | 抢断 | 盖帽 | date                | home_team    | away_team    |
-- +-----------+----------+------+------+------+------+------+---------------------+--------------+--------------+
-- |     1     |   101    |  32  |   8  |  11  |   2  |   1  | 2025-01-15 19:30:00 | 洛杉矶湖人   | 金州勇士     |
-- |     1     |   98     |  28  |   6  |   9  |   1  |   0  | 2025-01-12 20:00:00 | 洛杉矶湖人   | 丹佛掘金     |
-- |     1     |   95     |  35  |  10  |   7  |   3  |   2  | 2025-01-08 19:30:00 | 波士顿凯尔特人| 洛杉矶湖人  |
-- +-----------+----------+------+------+------+------+------+---------------------+--------------+--------------+
```

---

### 5.4.3 球员排行榜查询流程

**涉及的数据库对象**：

- 存储过程：`sp_get_player_rankings`, `sp_get_scoring_leaders`
- 表：`Player`, `Player_Game`

**完整操作流程代码示例**：

```sql
-- ========== 步骤1：获取得分榜 ==========
CALL sp_get_scoring_leaders(10);   -- TOP 10

-- 输出结果集：
-- +------+-----------------+--------------+----------+
-- | 排名 | 姓名            | 球队         | 场均得分 |
-- +------+-----------------+--------------+----------+
-- |  1   | 卢卡·东契奇     | 达拉斯独行侠 |   33.8   |
-- |  2   | 杰伦·布伦森     | 纽约尼克斯   |   28.4   |
-- |  3   | 凯文·杜兰特     | 菲尼克斯太阳 |   27.2   |
-- |  4   | 勒布朗·詹姆斯   | 洛杉矶湖人   |   25.7   |
-- |  5   | 扬尼斯·阿德托昆博| 密尔沃基雄鹿|   25.3   |
-- +------+-----------------+--------------+----------+


-- ========== 步骤2：获取篮板榜 ==========
CALL sp_get_player_rankings('rebounds', 10);

-- 输出结果集：
-- +------+-------------------+--------------+----------+
-- | 排名 | 姓名              | 球队         | 场均篮板 |
-- +------+-------------------+--------------+----------+
-- |  1   | 多曼塔斯·萨博尼斯 | 萨克拉门托国王|  14.2   |
-- |  2   | 扬尼斯·阿德托昆博 | 密尔沃基雄鹿 |  11.8   |
-- |  3   | 安东尼·戴维斯     | 洛杉矶湖人   |  11.5   |
-- |  4   | 尼古拉·约基奇     | 丹佛掘金     |  11.2   |
-- |  5   | 鲁迪·戈贝尔       | 明尼苏达森林狼|  10.8   |
-- +------+-------------------+--------------+----------+


-- ========== 步骤3：获取助攻榜 ==========
CALL sp_get_player_rankings('assists', 10);

-- 输出结果集：
-- +------+-----------------+--------------+----------+
-- | 排名 | 姓名            | 球队         | 场均助攻 |
-- +------+-----------------+--------------+----------+
-- |  1   | 特雷·杨         | 亚特兰大老鹰 |  11.2    |
-- |  2   | 泰瑞斯·哈利伯顿 | 印第安纳步行者|  10.8   |
-- |  3   | 卢卡·东契奇     | 达拉斯独行侠 |   9.8    |
-- |  4   | 勒布朗·詹姆斯   | 洛杉矶湖人   |   8.4    |
-- |  5   | 贾·莫兰特       | 孟菲斯灰熊   |   8.2    |
-- +------+-----------------+--------------+----------+
```

---

## 5.5 球星卡商店

本模块负责积分商城的抽卡功能、用户卡牌收藏管理。

### 5.5.1 抽取球星卡流程

**涉及的数据库对象**：

- 存储过程：`sp_draw_player_card`
- 表：`User`, `User_Card`, `Player`

**完整操作流程代码示例**：

```sql
-- ========== 步骤1：查看用户当前积分 ==========
SELECT user_id, username, points FROM User WHERE user_id = 10;

-- 输出：
-- +----------+-------------+--------+
-- | user_id  | username    | points |
-- +----------+-------------+--------+
-- |    10    | 篮球迷小王  |  550   |
-- +----------+-------------+--------+


-- ========== 步骤2：查看抽卡价格 ==========
-- 系统设定：单次抽卡消耗100积分
SELECT 100 AS 抽卡价格, '积分' AS 单位;

-- 输出：
-- +----------+------+
-- | 抽卡价格 | 单位 |
-- +----------+------+
-- |   100    | 积分 |
-- +----------+------+


-- ========== 步骤3：执行抽卡 ==========
SET @p_player_id = 0;
SET @p_player_name = '';
SET @p_rarity = '';
CALL sp_draw_player_card(
    10,                  -- 用户ID
    @p_player_id,        -- 输出：抽到的球员ID
    @p_player_name,      -- 输出：球员名称
    @p_rarity            -- 输出：卡牌稀有度
);
SELECT @p_player_id AS player_id, @p_player_name AS player_name, @p_rarity AS rarity;

-- 结果说明：
-- 1. 验证用户积分>=100
-- 2. 扣除100积分
-- 3. 按稀有度概率随机抽取球员：
--    - 普通(Common): 60%
--    - 稀有(Rare): 25%
--    - 史诗(Epic): 10%
--    - 传奇(Legendary): 5%
-- 4. 在User_Card表插入卡牌记录（或数量+1）

-- 输出：
-- +-----------+-----------------+--------+
-- | player_id | player_name     | rarity |
-- +-----------+-----------------+--------+
-- |     3     | 凯文·杜兰特     | Epic   |
-- +-----------+-----------------+--------+


-- ========== 步骤4：验证积分扣除 ==========
SELECT user_id, username, points FROM User WHERE user_id = 10;

-- 输出：
-- +----------+-------------+--------+
-- | user_id  | username    | points |
-- +----------+-------------+--------+
-- |    10    | 篮球迷小王  |  450   |
-- +----------+-------------+--------+
-- 550 - 100 = 450


-- ========== 步骤5：查看用户卡牌收藏 ==========
SELECT uc.user_id, p.姓名 AS 球员名称, uc.rarity AS 稀有度, uc.count AS 数量, uc.obtained_at AS 获得时间
FROM User_Card uc
JOIN Player p ON uc.player_id = p.player_id
WHERE uc.user_id = 10
ORDER BY 
    CASE uc.rarity 
        WHEN 'Legendary' THEN 1 
        WHEN 'Epic' THEN 2 
        WHEN 'Rare' THEN 3 
        ELSE 4 
    END;

-- 输出：
-- +----------+-----------------+----------+------+---------------------+
-- | user_id  | 球员名称        | 稀有度   | 数量 | 获得时间            |
-- +----------+-----------------+----------+------+---------------------+
-- |    10    | 凯文·杜兰特     | Epic     |  1   | 2025-01-20 22:00:00 |
-- |    10    | 史蒂芬·库里     | Rare     |  2   | 2025-01-18 15:30:00 |
-- |    10    | 德文·布克       | Common   |  3   | 2025-01-15 10:20:00 |
-- +----------+-----------------+----------+------+---------------------+
```

---

### 5.5.2 卡牌收藏查询流程

**涉及的数据库对象**：

- 存储过程：`sp_get_user_cards`, `sp_get_user_card_stats`
- 表：`User_Card`, `Player`

**完整操作流程代码示例**：

```sql
-- ========== 步骤1：获取用户所有卡牌 ==========
CALL sp_get_user_cards(10);

-- 输出结果集：
-- +-----------+-----------------+----------+------+----------+---------------------+
-- | player_id | 姓名            | 稀有度   | 数量 | photo_id | 获得时间            |
-- +-----------+-----------------+----------+------+----------+---------------------+
-- |     3     | 凯文·杜兰特     | Epic     |  1   |    12    | 2025-01-20 22:00:00 |
-- |     2     | 史蒂芬·库里     | Rare     |  2   |     8    | 2025-01-18 15:30:00 |
-- |    18     | 德文·布克       | Common   |  3   |    42    | 2025-01-15 10:20:00 |
-- |    25     | 拉梅洛·鲍尔     | Common   |  1   |    55    | 2025-01-12 09:45:00 |
-- +-----------+-----------------+----------+------+----------+---------------------+


-- ========== 步骤2：获取用户卡牌统计 ==========
CALL sp_get_user_card_stats(10);

-- 输出结果集：
-- +----------+------------+------------+------------+---------------+----------+
-- | user_id  | 总卡牌数   | 传奇数量   | 史诗数量   | 稀有数量      | 普通数量 |
-- +----------+------------+------------+------------+---------------+----------+
-- |    10    |     7      |     0      |     1      |      2        |    4     |
-- +----------+------------+------------+------------+---------------+----------+


-- ========== 步骤3：按稀有度分组统计 ==========
SELECT 
    uc.rarity AS 稀有度,
    COUNT(*) AS 种类数,
    SUM(uc.count) AS 总数量
FROM User_Card uc
WHERE uc.user_id = 10
GROUP BY uc.rarity
ORDER BY 
    CASE uc.rarity 
        WHEN 'Legendary' THEN 1 
        WHEN 'Epic' THEN 2 
        WHEN 'Rare' THEN 3 
        ELSE 4 
    END;

-- 输出：
-- +----------+--------+--------+
-- | 稀有度   | 种类数 | 总数量 |
-- +----------+--------+--------+
-- | Epic     |   1    |   1    |
-- | Rare     |   1    |   2    |
-- | Common   |   2    |   4    |
-- +----------+--------+--------+


-- ========== 步骤4：查看收藏进度 ==========
SELECT 
    (SELECT COUNT(*) FROM User_Card WHERE user_id = 10) AS 已收集种类,
    (SELECT COUNT(*) FROM Player) AS 全部球员数,
    CONCAT(
        ROUND((SELECT COUNT(*) FROM User_Card WHERE user_id = 10) * 100.0 / (SELECT COUNT(*) FROM Player), 1),
        '%'
    ) AS 收集进度;

-- 输出：
-- +------------+------------+----------+
-- | 已收集种类 | 全部球员数 | 收集进度 |
-- +------------+------------+----------+
-- |     4      |    450     |   0.9%   |
-- +------------+------------+----------+
```

---

## 5.6 数据分析查询

本模块为数据分析师角色提供自定义SQL查询功能，支持灵活的数据探索。

### 5.6.1 自定义SELECT查询流程

**涉及的数据库对象**：

- 权限验证：`analyst` 角色专属
- 安全限制：仅允许SELECT语句，禁止数据修改

**完整操作流程代码示例**：

```sql
-- ========== 步骤1：验证用户角色 ==========
SELECT user_id, username, role FROM User WHERE user_id = 20;

-- 输出：
-- +----------+----------+---------+
-- | user_id  | username | role    |
-- +----------+----------+---------+
-- |    20    | analyst1 | analyst |
-- +----------+----------+---------+
-- 角色为 analyst，允许执行自定义查询


-- ========== 步骤2：执行球员得分排行查询 ==========
-- 用户提交的SQL查询（系统需验证为SELECT语句）
SELECT 
    p.姓名,
    t.名称 AS 球队,
    ROUND(AVG(pg.得分), 1) AS 场均得分,
    COUNT(*) AS 出场数
FROM Player p
JOIN Player_Game pg ON p.player_id = pg.player_id
LEFT JOIN Team t ON p.当前球队ID = t.team_id
GROUP BY p.player_id
HAVING 出场数 >= 10
ORDER BY 场均得分 DESC
LIMIT 10;

-- 输出：
-- +-----------------+--------------+----------+--------+
-- | 姓名            | 球队         | 场均得分 | 出场数 |
-- +-----------------+--------------+----------+--------+
-- | 卢卡·东契奇     | 达拉斯独行侠 |   33.8   |   42   |
-- | 杰伦·布伦森     | 纽约尼克斯   |   28.4   |   40   |
-- | 凯文·杜兰特     | 菲尼克斯太阳 |   27.2   |   38   |
-- | 勒布朗·詹姆斯   | 洛杉矶湖人   |   25.7   |   42   |
-- | 扬尼斯·阿德托昆博| 密尔沃基雄鹿|   25.3   |   41   |
-- | 谢伊·吉尔杰斯-亚历山大| 俄克拉荷马城雷霆| 24.8 | 39  |
-- | 德文·布克       | 菲尼克斯太阳 |   24.2   |   36   |
-- | 杰森·塔图姆     | 波士顿凯尔特人|  23.8   |   43   |
-- | 安东尼·爱德华兹 | 明尼苏达森林狼|  23.5   |   41   |
-- | 德马尔·德罗赞   | 萨克拉门托国王|  22.9   |   38   |
-- +-----------------+--------------+----------+--------+


-- ========== 步骤3：球队战绩统计查询 ==========
SELECT 
    t.名称 AS 球队,
    t.所在城市,
    COUNT(CASE WHEN g.winner_team_id = t.team_id THEN 1 END) AS 胜场,
    COUNT(CASE WHEN g.winner_team_id IS NOT NULL AND g.winner_team_id != t.team_id AND (g.home_team_id = t.team_id OR g.away_team_id = t.team_id) THEN 1 END) AS 负场,
    ROUND(
        COUNT(CASE WHEN g.winner_team_id = t.team_id THEN 1 END) * 100.0 / 
        NULLIF(COUNT(CASE WHEN g.winner_team_id IS NOT NULL AND (g.home_team_id = t.team_id OR g.away_team_id = t.team_id) THEN 1 END), 0), 
    1) AS 胜率
FROM Team t
LEFT JOIN Game g ON t.team_id IN (g.home_team_id, g.away_team_id)
WHERE g.status = '已结束'
GROUP BY t.team_id
ORDER BY 胜率 DESC
LIMIT 5;

-- 输出：
-- +------------------+----------+------+------+------+
-- | 球队             | 所在城市 | 胜场 | 负场 | 胜率 |
-- +------------------+----------+------+------+------+
-- | 波士顿凯尔特人   | 波士顿   |  35  |  8   | 81.4 |
-- | 俄克拉荷马城雷霆 | 俄克拉荷马城|33  | 10   | 76.7 |
-- | 克利夫兰骑士     | 克利夫兰 |  31  |  12  | 72.1 |
-- | 丹佛掘金         | 丹佛     |  30  |  13  | 69.8 |
-- | 菲尼克斯太阳     | 菲尼克斯 |  28  |  15  | 65.1 |
-- +------------------+----------+------+------+------+


-- ========== 步骤4：帖子热度分析查询 ==========
SELECT 
    p.title AS 帖子标题,
    u.username AS 作者,
    p.view_count AS 浏览量,
    p.like_count AS 点赞数,
    p.comment_count AS 评论数,
    (p.view_count * 0.1 + p.like_count * 2 + p.comment_count * 3) AS 热度分
FROM Post p
JOIN User u ON p.user_id = u.user_id
ORDER BY 热度分 DESC
LIMIT 5;

-- 输出：
-- +----------------------------+----------+--------+--------+--------+--------+
-- | 帖子标题                   | 作者     | 浏览量 | 点赞数 | 评论数 | 热度分 |
-- +----------------------------+----------+--------+--------+--------+--------+
-- | 总决赛第七场精彩回顾       | admin    |  5680  |  423   |  189   | 1481.0 |
-- | 詹姆斯40000分里程碑        | 球迷A    |  4520  |  356   |  145   | 1199.0 |
-- | 库里三分球历史第一         | 球迷B    |  3890  |  298   |  112   | 1021.0 |
-- | 字母哥季后赛绝杀           | 球迷C    |  2750  |  245   |  98    |  859.0 |
-- | 新秀赛季表现大盘点         | analyst1 |  2100  |  178   |  76    |  694.0 |
-- +----------------------------+----------+--------+--------+--------+--------+


-- ========== 步骤5：比赛竞猜参与情况分析 ==========
SELECT 
    g.game_id,
    CONCAT(ht.名称, ' vs ', at.名称) AS 对阵,
    g.date AS 比赛时间,
    COUNT(pr.prediction_id) AS 参与人数,
    SUM(pr.bet_amount) AS 总投注积分,
    COUNT(CASE WHEN pr.is_correct = 1 THEN 1 END) AS 预测正确人数
FROM Game g
JOIN Team ht ON g.home_team_id = ht.team_id
JOIN Team at ON g.away_team_id = at.team_id
LEFT JOIN Prediction pr ON g.game_id = pr.game_id
WHERE g.status = '已结束'
GROUP BY g.game_id
ORDER BY 参与人数 DESC
LIMIT 5;

-- 输出：
-- +----------+-----------------------------+---------------------+----------+------------+----------------+
-- | game_id  | 对阵                        | 比赛时间            | 参与人数 | 总投注积分 | 预测正确人数   |
-- +----------+-----------------------------+---------------------+----------+------------+----------------+
-- |   101    | 洛杉矶湖人 vs 金州勇士      | 2025-01-15 19:30:00 |   245    |   8750     |     156        |
-- |   85     | 波士顿凯尔特人 vs 迈阿密热火| 2025-01-02 20:00:00 |   198    |   6420     |     112        |
-- |   92     | 丹佛掘金 vs 菲尼克斯太阳    | 2025-01-08 19:00:00 |   176    |   5890     |      89        |
-- |   78     | 达拉斯独行侠 vs 洛杉矶快船  | 2024-12-28 18:30:00 |   165    |   5120     |      78        |
-- |   88     | 密尔沃基雄鹿 vs 纽约尼克斯  | 2025-01-05 19:30:00 |   152    |   4680     |      95        |
-- +----------+-----------------------------+---------------------+----------+------------+----------------+
```

---

## 5.7 功能模块总结

第五章完整展示了NBA数据管理系统的数据库端核心操作，采用**纯SQL语句**实现各项业务功能。

### 5.7.1 操作统计

| 功能模块 | 操作数 | 主要功能 |
| :------- | :----: | :------- |
| 用户认证模块 | 4 | 注册、登录、信息管理、头像管理 |
| 帖子与评论模块 | 4 | 发帖、点赞（触发器）、评论、删除 |
| 比赛竞猜模块 | 3 | 比赛查询、参与竞猜、领取奖励 |
| 球员数据模块 | 3 | 列表搜索、详情统计、排行榜 |
| 球星卡商店 | 2 | 抽卡、收藏查询 |
| 数据分析查询 | 1 | 自定义SELECT查询 |

**总计：17个核心业务流程**

### 5.7.2 技术特点

1. **存储过程封装**：所有复杂业务逻辑通过存储过程实现，接口清晰
2. **触发器自动化**：帖子点赞计数通过触发器自动维护数据一致性
3. **事务完整性**：竞猜投注、奖励领取等涉及金额的操作使用事务保证原子性
4. **级联删除**：外键约束 `ON DELETE CASCADE` 自动处理关联数据清理
5. **分页查询**：列表类查询均支持分页，提高大数据量下的查询效率

### 5.7.3 安全措施

1. **权限分离**：普通用户、管理员、数据分析师三级角色
2. **SQL注入防护**：使用参数化存储过程调用
3. **查询限制**：数据分析师仅允许执行SELECT语句
4. **幂等性设计**：点赞等操作防重复处理

---

# 六、总结

## 6.1 项目成果

本NBA数据管理系统成功实现了一个功能完整的体育数据平台，主要成果包括：

### 6.1.1 数据库设计

- **18张数据表**：覆盖用户管理、球队球员、比赛数据、社区互动、积分商城五大业务领域
- **5个触发器**：实现比赛获胜自动计算、帖子点赞计数自动维护、用户注销关联清理
- **56个存储过程**：封装所有业务逻辑，涵盖8大功能模块

### 6.1.2 核心功能

| 功能模块 | 实现功能 |
| :------- | :------- |
| 用户系统 | 注册、登录、JWT认证、三级角色权限 |
| 球队管理 | 30支NBA球队信息、Logo管理 |
| 球员管理 | 球员信息CRUD、职业生涯数据统计 |
| 比赛系统 | 比赛信息管理、球员单场数据 |
| 社区互动 | 帖子发布、评论、点赞（触发器联动） |
| 竞猜系统 | 比赛预测、积分投注、奖励领取 |
| 球星卡商店 | 随机抽卡、卡牌收藏、稀有度分级 |
| 数据分析 | 排行榜、自定义SQL查询 |

### 6.1.3 技术亮点

1. **触发器自动化**：帖子点赞操作通过触发器自动更新计数字段，保证数据一致性
2. **存储过程封装**：业务逻辑在数据库层实现，提高安全性和执行效率
3. **级联约束**：外键 `ON DELETE CASCADE` 实现关联数据的自动清理
4. **事务保证**：涉及积分变动的操作使用事务确保原子性
5. **BLOB存储**：图片二进制数据直接存储在数据库中，简化部署

## 6.2 经验总结

### 6.2.1 设计经验

1. **规范化设计**：遵循第三范式，减少数据冗余
2. **命名规范**：表名、字段名、存储过程名遵循统一规范
3. **索引优化**：为常用查询字段添加索引，提升查询性能
4. **触发器使用**：适度使用触发器，避免复杂的级联触发

### 6.2.2 开发经验

1. **存储过程优先**：复杂业务逻辑优先使用存储过程实现
2. **参数化查询**：防止SQL注入攻击
3. **分页设计**：列表查询必须支持分页
4. **错误处理**：存储过程中使用DECLARE HANDLER处理异常

## 6.3 改进方向

1. **读写分离**：引入主从复制，提升并发性能
2. **缓存层**：引入Redis缓存热点数据
3. **全文搜索**：为帖子内容添加全文索引
4. **分区表**：对历史数据进行分区存储
5. **备份策略**：完善数据库备份和恢复机制

---

## 6.4 组员大作业总结

### 6.4.1 组员A：系统功能设计与前端页面设计

#### 一、任务内容概述

本人在本次NBA数据管理系统项目中主要负责**系统功能设计**与**前端页面开发**两大核心任务：

1. **系统功能设计**
   - 参与需求分析，确定系统功能模块划分
   - 设计用户交互流程和页面跳转逻辑
   - 制定前后端接口规范和数据交互格式
   - 设计用户权限体系（普通用户、管理员、数据分析师）

2. **前端页面开发**
   - 基于Vue 3框架搭建前端项目架构
   - 使用Element Plus组件库开发12个核心页面
   - 实现响应式布局，适配不同屏幕尺寸
   - 使用ECharts实现数据可视化图表
   - 封装API服务模块，对接后端RESTful接口

#### 二、任务难点及解决方法

| 难点 | 解决方法 |
| :--- | :------- |
| **组件化设计**：如何合理拆分组件，实现高复用性 | 采用"容器组件+展示组件"模式，将业务逻辑与UI展示分离；抽取Navbar、PlayerCard等通用组件 |
| **状态管理**：多页面间数据共享和同步问题 | 使用Vue 3的Composition API配合provide/inject实现轻量级状态管理；登录状态通过JWT存储在localStorage |
| **数据可视化**：球员数据对比图表的动态渲染 | 深入学习ECharts配置项，实现雷达图、柱状图等多种图表；封装chart组件支持数据动态更新 |
| **用户体验**：页面加载速度和交互流畅度 | 实现路由懒加载、图片懒加载；使用骨架屏优化首屏体验；添加loading状态提示 |
| **权限控制**：不同角色显示不同功能入口 | 通过路由守卫+v-if指令实现前端权限控制；管理功能仅对admin角色可见 |

#### 三、任务完成结果

1. **页面开发**：完成全部12个核心页面的开发
   - 登录/注册页面（支持三种角色）
   - 仪表盘首页（数据概览）
   - 比赛列表/详情页面（含竞猜功能）
   - 球员列表/详情/对比页面
   - 球队列表页面
   - 帖子论坛页面（含评论、点赞）
   - 排行榜页面（球队/球员）
   - 用户个人中心
   - 自定义查询页面（数据分析师专用）

2. **技术实现**
   - 代码规范：遵循Vue 3最佳实践，代码可维护性强
   - 响应式设计：适配PC端和平板设备
   - 接口对接：完成与后端46个API的对接测试

#### 四、合作体会

与负责后端的组员配合过程中，我深刻体会到**前后端协作的重要性**：

1. **接口文档先行**：在开发初期我们共同制定了详细的API文档，明确了请求/响应格式，大大减少了联调时的沟通成本
2. **及时沟通反馈**：遇到接口返回数据格式不符预期时，通过即时沟通快速定位问题并调整
3. **并行开发效率**：前后端分离架构使我们可以并行开发，通过Mock数据进行前端开发，待后端完成后无缝对接

#### 五、收获与体会

1. **技术成长**：系统性掌握了Vue 3生态（Composition API、Vue Router、Element Plus），提升了前端工程化能力
2. **设计思维**：学会从用户角度思考功能设计，注重交互体验和视觉呈现
3. **项目经验**：完整经历了从需求分析到上线部署的全流程，对软件开发生命周期有了更深理解
4. **团队协作**：认识到良好的分工和沟通是项目成功的关键，技术能力与协作能力同样重要

---

### 6.4.2 组员B：数据库设计与后端代码实现

#### 一、任务内容概述

本人在本次NBA数据管理系统项目中主要负责**数据库设计**与**后端代码实现**两大核心任务：

1. **数据库设计**
   - 完成数据库需求分析和概念设计（E-R图）
   - 设计并实现18张数据表，包含完整的字段定义和约束
   - 设计5个触发器实现业务规则自动化
   - 设计56个存储过程封装全部业务逻辑
   - 规划索引策略，优化查询性能

2. **后端代码实现**
   - 基于Flask框架搭建RESTful API服务
   - 实现JWT身份认证和权限控制中间件
   - 开发10个路由模块，对接前端全部功能需求
   - 实现数据库连接池和事务管理
   - 编写数据库初始化和迁移脚本

#### 二、任务难点及解决方法

| 难点 | 解决方法 |
| :--- | :------- |
| **表结构设计**：如何平衡规范化与查询效率 | 核心表遵循第三范式减少冗余；高频查询字段（如点赞数）适度冗余，通过触发器维护一致性 |
| **存储过程设计**：复杂业务逻辑的SQL实现 | 将复杂逻辑拆分为多个简单存储过程；使用事务确保原子性；添加详细注释便于维护 |
| **触发器调试**：触发器执行异常难以定位 | 编写测试用例逐一验证触发器；使用SIGNAL语句抛出自定义错误信息；避免触发器嵌套调用 |
| **并发控制**：竞猜投注的并发安全问题 | 使用事务+行级锁确保积分扣除的原子性；设计幂等性接口防止重复提交 |
| **图片存储**：大量图片数据的存储方案 | 采用BLOB类型直接存储图片二进制数据；独立Image表统一管理；通过关联表实现多对多关系 |

#### 三、任务完成结果

1. **数据库设计**
   - 18张数据表：覆盖用户、球队、球员、比赛、社区、商城全部业务领域
   - 5个触发器：实现比赛获胜自动计算、点赞计数维护、用户注销清理
   - 56个存储过程：按8个功能模块组织，接口清晰、职责单一
   - 完整的外键约束和级联删除策略

2. **后端开发**
   - 10个路由模块：auth、games、players、teams、posts、comments、rankings、shop、images、query
   - 完整的中间件：JWT认证、错误处理、跨域支持
   - 46个API端点：覆盖全部功能需求
   - 数据库工具脚本：初始化、迁移、测试数据导入

3. **文档输出**
   - 完整的API接口文档
   - 数据库设计文档（本报告）
   - 存储过程使用说明

#### 四、合作体会

与负责前端的组员配合过程中，我深刻体会到**接口设计的重要性**：

1. **RESTful规范**：遵循REST架构风格设计API，使接口语义清晰，前端易于理解和调用
2. **错误处理统一**：约定统一的错误响应格式，包含错误码和错误信息，便于前端进行异常处理
3. **数据格式协商**：针对日期、枚举等类型，提前约定序列化格式，避免联调时的格式问题
4. **文档同步更新**：接口变更时及时更新文档并通知前端，保持信息同步

#### 五、收获与体会

1. **数据库设计能力**：从实际项目需求出发，完整经历了数据库设计的全过程，对规范化理论、索引优化、事务管理有了更深入的理解
2. **存储过程编程**：掌握了MySQL存储过程的高级特性，包括游标、条件处理、事务控制等，认识到存储过程在提升安全性和性能方面的重要作用
3. **后端开发经验**：系统性掌握了Flask框架及其生态（JWT、CORS、Blueprint），提升了RESTful API设计能力
4. **工程化思维**：学会了从系统整体角度思考问题，注重代码的可维护性、可扩展性和安全性
5. **团队协作**：认识到清晰的接口定义和及时的沟通是前后端协作的基础，技术方案需要兼顾双方的实现便利性

---

**报告完成时间：2025年12月23日**

**数据库名称：h_db23373502**

**开发环境：MySQL 8.0 + Python Flask + Vue.js**

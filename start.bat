@echo off
setlocal enabledelayedexpansion

title NBA比赛数据库系统 - 启动脚本
echo ===================================================
echo      🏀 NBA比赛数据库系统 - 一键启动脚本
echo ===================================================
echo.

REM 1. 环境检查
echo [1/4] 正在检查环境...

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ 错误: 未检测到 Python，请先安装 Python 3.8+ 并添加到 PATH。
    pause
    exit /b 1
)
echo ✅ Python 已安装

node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ 错误: 未检测到 Node.js，请先安装 Node.js 14+。
    pause
    exit /b 1
)
echo ✅ Node.js 已安装

REM 2. 后端配置与启动
echo.
echo [2/4] 正在配置后端服务...
cd backend

REM 检查 .env
if not exist ".env" (
    echo ⚠️  未检测到 .env 文件，正在从模板复制...
    copy .env.example .env >nul
    echo ⚠️  请注意: 您可能需要编辑 backend\.env 文件以配置正确的数据库连接信息。
)

REM 虚拟环境检查
if not exist "venv" (
    echo 📦 正在创建 Python 虚拟环境...
    python -m venv venv
)

REM 激活虚拟环境并安装依赖
call venv\Scripts\activate
echo 📦 正在检查/安装后端依赖...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ❌ 后端依赖安装失败，请检查网络或 pip 配置。
    pause
    exit /b 1
)

echo 🚀 正在启动后端服务 (新窗口)...
start "NBA System - Backend" cmd /k "call venv\Scripts\activate && python run.py"

cd ..

REM 3. 前端配置与启动
echo.
echo [3/4] 正在配置前端服务...
cd frontend

if not exist "node_modules" (
    echo 📦 检测到首次运行，正在安装前端依赖 (这可能需要几分钟)...
    call npm install
    if %errorlevel% neq 0 (
        echo ❌ 前端依赖安装失败。
        pause
        exit /b 1
    )
)

echo 🚀 正在启动前端服务 (新窗口)...
start "NBA System - Frontend" cmd /k "echo Starting Frontend... && npm run serve"

cd ..

REM 4. 完成
echo.
echo [4/4] ✅ 所有服务已启动！
echo.
echo ===================================================
echo    请等待几秒钟，前端启动完成后访问:
echo    http://localhost:8080
echo ===================================================
echo.
pause


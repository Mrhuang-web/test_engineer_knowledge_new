#!/bin/bash
# 功能：后台启动、停止、查看 main.py 进程，启动前自动 SVN 更新（交互式认证），日志超过50M自动清理
# 依赖：确保 Python 环境已配置、SVN 客户端已安装且仓库已 checkout

# ============= 配置参数（可根据实际需求修改）=============
# Python 解释器路径（虚拟环境需替换为对应路径，如 ~/venv/bin/python3）
PYTHON_PATH="python3"
# 程序入口文件
APP_FILE="main.py"
# 日志输出路径（自动创建，追加模式）
LOG_FILE="main.log"
# 进程PID存储文件（用于快速停止程序）
PID_FILE="main.pid"
# 程序启动参数（无则留空，如 --port 8080）
APP_ARGS=""
# SVN 仓库工作目录（当前目录为 SVN 工作副本，保持 "." 即可）
SVN_WORK_DIR="."
# 日志清理阈值（单位：M）
LOG_MAX_SIZE=50

# ============= 工具函数定义 =============
# 1. 日志清理函数（超过阈值则删除旧日志）
clean_log() {
    # 检查日志文件是否存在
    if [ -f "$LOG_FILE" ]; then
        # 获取日志文件大小（单位：字节），转换为 M（除以 1024*1024）
        LOG_SIZE=$(du -b "$LOG_FILE" | awk '{print $1}')
        LOG_SIZE_M=$((LOG_SIZE / 1024 / 1024))

        # 对比阈值，超过则删除旧日志
        if [ $LOG_SIZE_M -ge $LOG_MAX_SIZE ]; then
            echo "🗑️  日志文件大小已达 $LOG_SIZE_M M（阈值 $LOG_MAX_SIZE M），开始清理..."
            rm -f "$LOG_FILE"
            echo "✅ 旧日志已删除，将生成新日志文件"
        fi
    fi
}

# 2. SVN 更新函数（交互式输入账号密码）
svn_update() {
    echo "🔄 开始执行 SVN 更新..."
    # 交互式执行 SVN 更新，自动提示输入账号密码（避免明文泄露）
    svn update "$SVN_WORK_DIR" >> "$LOG_FILE" 2>&1
    # 检查更新结果
    if [ $? -eq 0 ]; then
        echo "✅ SVN 更新成功！"
    else
        echo "⚠️ SVN 更新失败！详细日志请查看：$LOG_FILE"
        read -p "是否继续启动程序？(y/n，默认n)：" CONTINUE
        CONTINUE=${CONTINUE:-n}
        if [ "$CONTINUE" != "y" ] && [ "$CONTINUE" != "Y" ]; then
            exit 1
        fi
    fi
}

# 3. 启动程序函数
start_app() {
    # 第一步：清理超大日志
    clean_log

    # 第二步：执行 SVN 交互式更新
    svn_update

    # 第三步：检测并停止监听在 10101-10130 端口的进程
    echo "正在结束监听在 10101-10130 的进程..."
    for p in $(seq 10101 10130); do 
        PIDS=$(ss -Hlpn "sport = :$p" | awk -F, '{print $2}' | awk -F= '{print $2}') 
        [ -n "$PIDS" ] && kill -9 $PIDS 2>/dev/null 
    done 
    echo "完成。"

    # 第四步：检查程序是否已运行
    if [ -f "$PID_FILE" ] && ps -p $(cat "$PID_FILE") > /dev/null 2>&1; then
        echo "⚠️  程序已在运行！PID: $(cat "$PID_FILE")"
        echo "📜 log 日志：$(pwd)/$LOG_FILE"
        exit 0
    fi

    # 检查入口文件是否存在
    if [ ! -f "$APP_FILE" ]; then
        echo "❌ 错误：当前目录未找到 $APP_FILE 文件，请确认执行路径！"
        exit 1
    fi

    # 后台启动程序（nohup 忽略挂断信号，& 后台运行）
    nohup $PYTHON_PATH $APP_FILE $APP_ARGS >> $LOG_FILE 2>&1 &
    # 记录进程PID
    echo $! > $PID_FILE

    # 验证启动结果
    sleep 1
    if ps -p $(cat "$PID_FILE") > /dev/null 2>&1; then
        echo "✅ 程序启动成功！"
        echo "📌 PID: $(cat "$PID_FILE")"
        echo "📜 log 日志：$(pwd)/$LOG_FILE"
        echo "🔍 查看实时日志：tail -f $LOG_FILE"
        echo "📏 当前日志阈值：$LOG_MAX_SIZE M（超过自动清理）"
    else
        echo "❌ 程序启动失败！请查看日志：$LOG_FILE"
        rm -f $PID_FILE  # 清理无效PID文件
        exit 1
    fi
}

# 4. 停止程序函数
stop_app() {
    # 检查程序是否在运行
    if [ ! -f "$PID_FILE" ] || ! ps -p $(cat "$PID_FILE") > /dev/null 2>&1; then
        echo "⚠️  程序未运行或PID文件无效！"
        exit 0
    fi

    # 优雅停止进程（先尝试正常终止，失败则强制杀死）
    echo "🛑 正在停止程序（PID: $(cat "$PID_FILE")）..."
    kill -15 $(cat "$PID_FILE") > /dev/null 2>&1
    sleep 2

    # 检查是否停止成功
    if ps -p $(cat "$PID_FILE") > /dev/null 2>&1; then
        echo "⚠️  正常停止失败，尝试强制终止..."
        kill -9 $(cat "$PID_FILE") > /dev/null 2>&1
        sleep 1
    fi

    # 清理PID文件
    rm -f $PID_FILE
    echo "✅ 程序已停止！"
}

# 5. 查看程序状态函数
status_app() {
    if [ -f "$PID_FILE" ] && ps -p $(cat "$PID_FILE") > /dev/null 2>&1; then
        echo "📊 程序运行中"
        echo "PID: $(cat "$PID_FILE")"
        echo "日志路径：$(pwd)/$LOG_FILE"
        # 显示当前日志大小
        if [ -f "$LOG_FILE" ]; then
            LOG_SIZE=$(du -b "$LOG_FILE" | awk '{print $1}')
            LOG_SIZE_M=$((LOG_SIZE / 1024 / 1024))
            echo "当前日志大小：$LOG_SIZE_M M（阈值 $LOG_MAX_SIZE M）"
        fi
        echo "启动时间：$(ps -p $(cat "$PID_FILE") -o lstart=)"
    else
        echo "📊 程序未运行"
        rm -f $PID_FILE  # 清理无效PID文件
    fi
}

# 6. 查看实时日志函数
log_app() {
    if [ ! -f "$LOG_FILE" ]; then
        echo "⚠️  日志文件未生成（程序可能未启动）！"
        exit 1
    fi
    # 显示当前日志大小
    LOG_SIZE=$(du -b "$LOG_FILE" | awk '{print $1}')
    LOG_SIZE_M=$((LOG_SIZE / 1024 / 1024))
    echo "📜 实时日志（当前大小：$LOG_SIZE_M M，阈值 $LOG_MAX_SIZE M，按 Ctrl+C 退出）："
    tail -f $LOG_FILE
}

# ============= 命令分发 =============
case "$1" in
    start)
        start_app
        ;;
    stop)
        stop_app
        ;;
    restart)
        stop_app
        sleep 2
        start_app
        ;;
    status)
        status_app
        ;;
    log)
        log_app
        ;;
    svn-update)
        svn_update  # 单独执行 SVN 交互式更新
        ;;
    clean-log)
        clean_log  # 手动清理日志（无论大小）
        ;;
    *)
        echo "📚 用法：$0 [命令]"
        echo "命令列表："
        echo "  start      - 清理超大日志 → SVN 交互式更新 → 后台启动程序"
        echo "  stop       - 停止程序"
        echo "  restart    - 停止程序 → 清理超大日志 → SVN 交互式更新 → 重启程序"
        echo "  status     - 查看程序运行状态（含当前日志大小）"
        echo "  log        - 查看实时日志（含当前日志大小）"
        echo "  svn-update - 单独执行 SVN 交互式更新（不启动程序）"
        echo "  clean-log  - 手动清理日志文件（无论大小）"
        exit 1
        ;;
esac
tail -400f main.log
#exit 0


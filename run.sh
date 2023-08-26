#!/bin/bash

# 使用 ps -aux 命令查找匹配的进程并使用 grep 过滤
# 注意，如果存在多个匹配的进程，可能需要进一步处理
process_info=$(ps -aux | grep "python server.py" | grep -v "grep")

if [ -n "$process_info" ]; then
    # 获取进程的 PID
    pid=$(echo "$process_info" | awk '{print $2}')
    
    # 终止进程
    echo "Terminating process with PID: $pid"
    kill -9 $pid
    
    echo "Process terminated."
else
    echo "No matching process found."
fi

nohup python server.py &
tail -f nohup.out

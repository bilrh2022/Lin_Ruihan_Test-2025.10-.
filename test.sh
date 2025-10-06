#!/bin/bash

# 切换到脚本所在目录
cd "$(dirname "$0")"

# 直接使用 python3 或 python
if command -v python3 >/dev/null 2>&1; then
    python3 "Robot's Morning Routine.py"
elif command -v python >/dev/null 2>&1; then
    python "Robot's Morning Routine.py"
else
    echo "错误：未找到 Python 解释器"
    exit 1
fi

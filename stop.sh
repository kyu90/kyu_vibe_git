#!/bin/bash

echo "🛑 차트봇 종료"

stopped=false

if [[ -d "logs" ]]; then
    for service in backend frontend ollama; do
        if [[ -f "logs/$service.pid" ]]; then
            pid=$(cat logs/$service.pid)
            if kill -0 $pid 2>/dev/null; then
                kill $pid && stopped=true
            fi
            rm -f logs/$service.pid
        fi
    done
fi

pkill -f "python.*main.py" 2>/dev/null && stopped=true
pkill -f "python.*http.server.*3000" 2>/dev/null && stopped=true

for port in 8000 3000; do
    pid=$(lsof -ti :$port 2>/dev/null)
    [[ -n "$pid" ]] && kill -9 $pid 2>/dev/null && stopped=true
done

[[ "$stopped" == "true" ]] && echo "✅ 서비스 종료됨" || echo "⚠️ 실행 중인 서비스 없음"
echo "🚀 시작: ./start.sh"

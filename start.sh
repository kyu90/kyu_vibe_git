#!/bin/bash

echo "🚀 차트봇 시작"

mkdir -p logs

# 기존 프로세스 정리
pkill -f "ollama serve" 2>/dev/null || true
pkill -f "python.*main.py" 2>/dev/null || true  
pkill -f "python.*http.server.*3000" 2>/dev/null || true

for port in 8000 3000 11434; do
    pid=$(lsof -ti :$port 2>/dev/null)
    [[ -n "$pid" ]] && kill -9 $pid 2>/dev/null || true
done

sleep 1

# Ollama 시작
echo "🦙 Ollama 시작..."
nohup ollama serve > logs/ollama.log 2>&1 &
echo $! > logs/ollama.pid
sleep 3

[[ ! $(ollama list | grep -q "llama3") ]] && ollama pull llama3:latest

# 백엔드 시작
echo "📦 백엔드 시작..."
cd backend

[[ ! -d "venv" ]] && python3 -m venv venv

if ! ./venv/bin/python -c "import fastapi" 2>/dev/null; then
    echo "📥 의존성 설치..."
    ./venv/bin/pip install --upgrade pip
    ./venv/bin/pip install -r requirements.txt
fi

[[ ! -f ".env" && -f ".env.example" ]] && cp .env.example .env

nohup ./venv/bin/python main.py > ../logs/backend.log 2>&1 &
echo $! > ../logs/backend.pid
cd ..

# 프론트엔드 시작
echo "🌐 프론트엔드 시작..."
cd frontend
nohup python3 -m http.server 3000 > ../logs/frontend.log 2>&1 &
echo $! > ../logs/frontend.pid
cd ..

sleep 5

# 상태 확인
echo "🔍 상태 확인..."
curl -s http://localhost:11434/api/tags >/dev/null 2>&1 && echo "✅ Ollama (11434)" || echo "❌ Ollama"
curl -s http://localhost:8000/ >/dev/null 2>&1 && echo "✅ 백엔드 (8000)" || echo "❌ 백엔드"
curl -s http://localhost:3000/ >/dev/null 2>&1 && echo "✅ 프론트엔드 (3000)" || echo "❌ 프론트엔드"

echo ""
echo "🌐 접속: http://localhost:3000"
echo "🛑 종료: ./stop.sh"

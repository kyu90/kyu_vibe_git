#!/bin/bash

echo "🚀 차트봇 환경 설정"
echo "==================="

# 현재 디렉토리 확인
if [[ ! "$(basename $(pwd))" == "backend" ]]; then
    echo "❌ backend 디렉토리에서 실행해주세요!"
    echo "   cd backend"
    exit 1
fi

# 기존 가상환경 제거
echo "🧹 기존 환경 정리..."
rm -rf venv

# Python 확인
echo "🐍 Python 확인..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3가 설치되지 않았습니다!"
    echo "   macOS: brew install python"
    exit 1
fi

# 가상환경 생성
echo "📦 가상환경 생성..."
python3 -m venv venv
source venv/bin/activate

# 라이브러리 설치
echo "📚 라이브러리 설치..."
pip install --upgrade pip
pip install -r requirements.txt

# 환경 파일 설정
echo "⚙️  환경 설정..."
if [ ! -f ".env" ]; then
    cp .env.example .env
fi

# Ollama 연결 테스트
echo "🦙 Ollama 테스트..."
if curl -s http://localhost:11434/api/tags >/dev/null 2>&1; then
    echo "✅ Ollama 연결 성공"
else
    echo "⚠️  Ollama 시작 필요: ollama serve"
fi

echo ""
echo "🎉 설정 완료!"
echo "============="
echo "서버 시작: python main.py"

# 🤖📊 차트봇

로컬 AI 기반 데이터 시각화 도구

## 실행

```bash
# 사전 준비
brew install ollama
ollama pull llama3:latest

# 실행
chmod +x start.sh stop.sh
./start.sh

# 접속
open http://localhost:3000

# 종료
./stop.sh
```

## 테스트

웹페이지에서 입력:
- `1월 100, 2월 200, 3월 300을 차트로`
- `사과 30, 바나나 20을 파이차트로`

## 로컬 테스트

```bash
# API 테스트
curl http://localhost:8000/

# 프론트엔드 테스트
curl http://localhost:3000/

# 로그 확인
tail -f logs/*.log

# 수동 백엔드 실행
cd backend
./venv/bin/python main.py
```

## 구조

```
├── start.sh      # 시작
├── stop.sh       # 종료
├── backend/      # FastAPI 서버
├── frontend/     # 웹 인터페이스
└── logs/         # 로그
```

## Github 배포

```bash
# 정리 후 배포
./cleanup.sh
git add .
git commit -m "차트봇 최적화"
git push
```

**실행: `./start.sh` → 접속: `http://localhost:3000`**

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any
import os
from dotenv import load_dotenv

from chart_generator import ChartGenerator

# 환경 변수 로드
load_dotenv()

app = FastAPI(title="간단한 차트봇")

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 차트 생성기 초기화 (llama3 모델 사용)
chart_generator = ChartGenerator(model_name="llama3:latest")

class ChatMessage(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str
    chart_data: Optional[Dict[str, Any]] = None

@app.get("/")
def read_root():
    ollama_status = chart_generator.test_connection()
    return {
        "message": "간단한 차트봇 API 실행중! 🤖📊",
        "ollama_connected": ollama_status,
        "model": "llama3:latest"
    }

@app.post("/chat")
def chat_endpoint(chat_message: ChatMessage):
    """간단한 채팅 엔드포인트"""
    
    try:
        # Ollama 연결 확인
        if not chart_generator.test_connection():
            return ChatResponse(
                response="Ollama가 연결되지 않았습니다. 'ollama serve' 명령어로 시작해주세요."
            )
        
        # AI 분석
        response_text, chart_config, chart_meta = chart_generator.analyze_user_request(chat_message.message)
        
        chart_data = None
        
        # 차트 생성이 필요한 경우
        if chart_config and chart_meta:
            extracted_data = chart_generator.parse_data_from_text(chat_message.message)
            if extracted_data:
                chart_data = chart_generator.generate_chart_config(
                    chart_meta["type"], 
                    extracted_data, 
                    chart_config
                )
        
        return ChatResponse(
            response=response_text,
            chart_data=chart_data
        )
        
    except Exception as e:
        return ChatResponse(
            response=f"오류가 발생했습니다: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    
    print("🚀 간단한 차트봇 서버 시작!")
    print("🦙 Ollama 연결 상태:", chart_generator.test_connection())
    print("📡 사용 모델: llama3:latest")
    print("🌐 서버 주소: http://localhost:8000")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)

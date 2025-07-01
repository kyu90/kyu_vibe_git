import requests
import json
import re
from typing import Dict, Any, Optional, Tuple

class ChartGenerator:
    def __init__(self, ollama_host: str = "http://localhost:11434", model_name: str = "llama2"):
        self.ollama_host = ollama_host.rstrip('/')
        self.model_name = model_name
        
    def _call_ollama(self, prompt: str) -> str:
        """Ollama API 호출 (에러 처리 강화)"""
        try:
            # 먼저 연결 테스트
            test_url = f"{self.ollama_host}/api/tags"
            test_response = requests.get(test_url, timeout=5)
            test_response.raise_for_status()
            
            # 실제 생성 요청
            url = f"{self.ollama_host}/api/generate"
            payload = {
                "model": self.model_name,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "num_predict": 100
                }
            }
            
            print(f"Ollama 요청: {url}")
            print(f"모델: {self.model_name}")
            
            response = requests.post(url, json=payload, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            return result.get("response", "").strip()
            
        except requests.exceptions.ConnectionError:
            return "Ollama 서비스가 실행되지 않았습니다. 'ollama serve' 명령어로 시작해주세요."
        except requests.exceptions.HTTPError as e:
            if "404" in str(e):
                return f"Ollama API 엔드포인트를 찾을 수 없습니다. Ollama가 올바르게 설치되었는지 확인해주세요. ({e})"
            return f"Ollama HTTP 오류: {e}"
        except requests.exceptions.Timeout:
            return "Ollama 응답 시간 초과. 다시 시도해주세요."
        except Exception as e:
            return f"Ollama 오류: {e}"
    
    def analyze_user_request(self, message: str) -> Tuple[str, Optional[Dict], Optional[Dict]]:
        """사용자 메시지 분석"""
        
        # 숫자 데이터가 있는지 확인
        numbers = re.findall(r'\d+', message)
        
        if len(numbers) >= 2:  # 최소 2개 이상의 숫자가 있으면 차트 생성
            # 간단한 프롬프트로 Ollama 호출
            prompt = f"""
사용자가 "{message}"라고 말했습니다.

차트를 만들어달라고 요청하고 있나요? 
간단히 "예" 또는 "아니오"로 답하고, 친근한 한국어 응답을 해주세요.

예시:
예, 차트를 만들어드릴게요!
"""
            
            ai_response = self._call_ollama(prompt)
            
            # 오류 메시지인 경우 그대로 반환
            if "오류" in ai_response or "실행되지" in ai_response:
                return ai_response, None, None
            
            if "예" in ai_response or "차트" in ai_response:
                # 차트 설정
                chart_config = {
                    "title": "데이터 차트",
                    "x_label": "항목",
                    "y_label": "값"
                }
                
                # 차트 타입 결정
                chart_type = "bar"
                if "선" in message or "line" in message.lower():
                    chart_type = "line"
                elif "파이" in message or "pie" in message.lower():
                    chart_type = "pie"
                
                response_text = ai_response if ai_response else "차트를 만들어드릴게요! 📊"
                
                return response_text, chart_config, {"type": chart_type}
            
        # 일반 대화
        prompt = f"사용자가 '{message}'라고 말했습니다. 친근하게 한국어로 간단히 답해주세요."
        response = self._call_ollama(prompt)
        
        return response, None, None
    
    def parse_data_from_text(self, text: str) -> Optional[Dict[str, Any]]:
        """텍스트에서 숫자와 라벨 추출"""
        
        data = {}
        
        # 패턴 1: 라벨 숫자 (예: "1월 100")
        pattern1 = re.findall(r'(\w+)\s*(\d+)', text)
        for label, value in pattern1:
            data[label] = float(value)
        
        # 패턴 2: 숫자 라벨 (예: "100 매출")
        if not data:
            pattern2 = re.findall(r'(\d+)\s*(\w+)', text)
            for value, label in pattern2:
                data[label] = float(value)
        
        if data:
            return {
                "labels": list(data.keys()),
                "datasets": [{
                    "label": "데이터",
                    "data": list(data.values()),
                    "backgroundColor": ["#FF6384", "#36A2EB", "#FFCE56", "#4BC0C0", "#9966FF"][:len(data)]
                }]
            }
        
        return None
    
    def generate_chart_config(self, chart_type: str, data: Dict, config: Dict = None) -> Dict:
        """Chart.js 설정 생성"""
        return {
            "type": chart_type,
            "data": data,
            "options": {
                "responsive": True,
                "plugins": {
                    "title": {
                        "display": True,
                        "text": config.get("title", "데이터 차트") if config else "데이터 차트"
                    }
                }
            }
        }
    
    def test_connection(self) -> bool:
        """Ollama 연결 테스트 (상세 로깅)"""
        try:
            url = f"{self.ollama_host}/api/tags"
            print(f"Ollama 연결 테스트: {url}")
            
            response = requests.get(url, timeout=5)
            print(f"응답 상태: {response.status_code}")
            
            if response.status_code == 200:
                models = response.json().get("models", [])
                print(f"사용 가능한 모델: {[m.get('name', 'unknown') for m in models]}")
                return True
            return False
            
        except Exception as e:
            print(f"Ollama 연결 실패: {e}")
            return False

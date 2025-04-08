import streamlit as st
from groq import Client

# 페이지 기본 설정
st.set_page_config(
 page_title="AI 챗봇",
 page_icon="🤖",
 layout="wide"
)

# API 키 설정 (환경 변수에서 가져오기 또는 하드코딩)
API_KEY = "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"
if not API_KEY:
 st.error("API 키가 설정되지 않았습니다.")
 st.stop()

# Groq 클라이언트 초기화
try:
 client = Client(api_key=API_KEY)
except Exception as e:
 st.error(f"Groq 클라이언트 초기화 중 문제가 발생했습니다: {e}")
 st.stop()

# 지원 모델 리스트
AVAILABLE_MODELS = {
 "Qwen 2.5 표준": "qwen-2.5-32b",
 "Qwen QWQ 고급": "qwen-qwq-32b",
 "Qwen 2.5 코더": "qwen-2.5-coder-32b"
}

# 세션 초기화 - 대화 기록 관리
if "chat_history" not in st.session_state:
 st.session_state['chat_history'] = []

# 사이드바 설정
with st.sidebar:
 st.title("설정")
 st.markdown("---")
 
 # 사용자가 모델 선택
 selected_model = st.selectbox(
 "사용할 모델을 선택하세요",
 list(AVAILABLE_MODELS.keys())
 )
 
 # 대화 기록 초기화 버튼
 if st.button("대화 초기화"):
 st.session_state['chat_history'] = []
 st.experimental_rerun()

# Groq API를 사용하여 질문에 대한 응답 생성
def get_response(question, model_name):
 try:
 model_id = AVAILABLE_MODELS[model_name]
 response = client.model(model_id).generate(prompt=question)
 return response.text
 except Exception as e:
 st.error(f"응답 생성 중 문제가 발생했습니다: {e}")
 return None

# 메인 UI
st.title("🤖 Groq AI 챗봇")
st.markdown("Groq AI 모델을 사용하여 질문에 응답하는 챗봇입니다. 질문을 입력하고 응답을 확인하세요.")

# 사용자 입력
question = st.text_input("질문을 입력하세요:")

if st.button("질문 보내기"):
 if question.strip(): # 공백만 포함된 질문 방지
 # Groq 모델을 사용하여 응답 생성
 response = get_response(question, selected_model)
 
 if response:
 # 대화 기록 업데이트
 st.session_state['chat_history'].append({"role": "user", "content": question})
 st.session_state['chat_history'].append({"role": "assistant", "content": response})
else:
 st.warning("응답을 생성할 수 없습니다. 다시 시도하세요.")
else:
 st.warning("질문을 입력하세요.")

# 대화 내용 표시
st.markdown("### 💬 대화 기록")
for chat in st.session_state['chat_history']:
 role = "🙋‍♂️ 사용자" if chat['role'] == "user" else "🤖 어시스턴트"
 st.markdown(f"**{role}:** {chat['content']}")
import streamlit as st
from groq import Client  # Groq 라이브러리

# 🌟 Streamlit 기본 설정
st.set_page_config(
    page_title="AI 챗봇",
    page_icon="🤖",
    layout="wide"
)

# 🔑 API 키 설정
API_KEY = "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"

if not API_KEY:
    st.error("API 키가 설정되지 않았습니다. 환경 변수를 확인하세요.")
    st.stop()

# 🌐 Groq 클라이언트 초기화
try:
    client = Client(api_key=API_KEY)
except Exception as e:
    st.error(f"Groq 클라이언트 초기화 중 문제가 발생했습니다: {e}")
    st.stop()

# 📚 지원 모델 목록
AVAILABLE_MODELS = {
    "GEMMA2-9B-IT": "gemma2-9b-it",
    "DEEPSeek-R1-Distill-Qwen-32B": "deepseek-r1-distill-qwen-32b",
    "Llama-3.3-70B-StecdEC": "llama-3.3-70b-stecdec"
}

# 📂 세션 상태 초기화 (대화 기록 관리)
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

# 🖋️ 사이드바 UI (설정)
with st.sidebar:
    st.title("챗봇 설정")
    st.markdown("---")
    
    # 모델 선택
    selected_model = st.selectbox(
        "사용할 모델을 선택하세요",
        list(AVAILABLE_MODELS.keys())
    )
    
    # 대화 초기화 버튼
    if st.button("대화 초기화"):  # 버튼 클릭 처리 함수 실행
        st.session_state["chat_history"] = []  # 대화 기록 초기화
        st.experimental_rerun()  # 페이지 새로고침


# 🤖 Groq의 모델 API를 호출해 대답 생성
def get_response(question, model_name):
    try:
        model_id = AVAILABLE_MODELS[model_name]  # 선택된 모델 ID 가져오기
        response = client.model(model_id).generate(prompt=question)  # Groq 호출
        return response.text
    except Exception as e:
        st.error(f"응답 생성 중 문제가 발생했습니다: {e}")
        return None


# 🏠 메인 UI
st.title("🤖 인공지능 챗봇")
st.markdown("Groq 기반 모델을 사용하여 사용자 질문에 응답하는 챗봇입니다.")

# 사용자 질문 입력
user_input = st.text_input("챗봇과 대화하세요! 질문을 입력하세요:")

# 질문 처리 및 답변 생성
if st.button("질문하기"):  # 버튼 클릭 시 실행
    if user_input.strip():  # 입력이 비어있는지 확인
        # Groq 모델 응답 생성
        bot_response = get_response(user_input, selected_model)
        
        if bot_response:  # 응답 성공 시
            # 대화 기록 업데이트
            st.session_state["chat_history"].append({"role": "user", "content": user_input})
            st.session_state["chat_history"].append({"role": "assistant", "content": bot_response})
        else:
            st.warning("응답을 생성하지 못했습니다. 다시 시도해 주세요.")
    else:
        st.warning("질문을 입력하세요.")

# 💬 대화 기록 UI
st.markdown("### 💬 대화 기록")
for chat in st.session_state["chat_history"]:
    role = "🙋 사용자" if chat["role"] == "user" else "🤖 챗봇"
    st.markdown(f"**{role}:** {chat['content']}")
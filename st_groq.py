import streamlit as st
from groq import Client

# Streamlit 기본 설정
st.set_page_config(
    page_title="AI 챗봇",
    page_icon="🤖",
    layout="wide"
)

# Groq API 키 설정
API_KEY = "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"  # Groq API 키를 입력하세요
if not API_KEY:
    st.error("API 키가 설정되지 않았습니다.")
    st.stop()

# Groq 클라이언트 초기화
try:
    client = Client(api_key=API_KEY)
except Exception as e:
    st.error(f"Groq 클라이언트 초기화 중 문제가 발생했습니다: {e}")
    st.stop()

# 모델 목록
AVAILABLE_MODELS = {
    "GEMMA2-9B-IT": "gemma2-9b-it",
    "DEEPSeek-R1-Distill-Qwen-32B": "deepseek-r1-distill-qwen-32b",
    "Llama-3.3-70B-StecdEC": "llama-3.3-70b-stecdec"
}

# 세션 상태 초기화
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

# 사이드바 설정
with st.sidebar:
    st.title("AI 챗봇 설정")
    selected_model = st.selectbox(
        "사용할 모델을 선택하세요",
        list(AVAILABLE_MODELS.keys())
    )
    if st.button("대화 초기화"):
        st.session_state["chat_history"] = []
        # 페이지 상태를 초기화
        st.query_params.clear()

# Groq API 응답 생성
def get_response(question, model_name):
    # Groq API를 호출하여 응답 생성
    try:
        response = client.generate(
            model=model_name,
            prompt=question,
            max_tokens=100
        )
        return response.get("text", "").strip()
    except Exception as e:
        st.error(f"응답 생성 중 오류가 발생했습니다: {e}")
        return None

# 메인 UI
st.title("🤖 Groq AI 챗봇")
user_input = st.text_input("질문 입력: ")

if st.button("질문하기"):
    if user_input.strip():
        bot_response = get_response(user_input, AVAILABLE_MODELS[selected_model])
        if bot_response:
            st.session_state["chat_history"].append({"role": "user", "content": user_input})
            st.session_state["chat_history"].append({"role": "assistant", "content": bot_response})
        else:
            st.warning("응답을 생성할 수 없습니다.")
    else:
        st.warning("질문을 입력하세요.")

# 대화 기록 출력
st.markdown("### 대화 기록")
for chat in st.session_state["chat_history"]:
    role = "🙋 사용자" if chat["role"] == "user" else "🤖 챗봇"
    st.markdown(f"**{role}:** {chat['content']}")
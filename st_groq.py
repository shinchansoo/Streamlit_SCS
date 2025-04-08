import streamlit as st
import os
from groq import Groq

# 페이지 기본 설정
st.set_page_config(
    page_title="AI 어시스턴트",
    page_icon="🌸",
    layout="wide"
)

# CSS 스타일은 이전과 동일

# Groq API 키 설정 (환경 변수에서 가져오기)
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    st.error("API 키가 설정되지 않았습니다. 환경 변수 'GROQ_API_KEY'를 설정하세요.")
    st.stop()

# Groq 클라이언트 초기화
client = Groq(api_key=api_key)

# Qwen 모델 리스트
AVAILABLE_MODELS = {
    "Qwen 2.5 표준": "qwen-2.5-32b",
    "Qwen QWQ 고급": "qwen-qwq-32b",
    "Qwen 2.5 코더": "qwen-2.5-coder-32b"
}

# 사이드바 설정
with st.sidebar:
    st.title("설정")
    st.markdown("---")
    
    # 모델 선택
    selected_model = st.selectbox(
        "모델 선택",
        list(AVAILABLE_MODELS.keys())
    )
    
    if st.button("대화 내용 지우기", key="clear"):
        st.session_state['chat_history'] = []
        st.rerun()

def get_response(question, model_name, temp, max_tok):
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "user", "content": question}
            ],
            model=AVAILABLE_MODELS[model_name],
            temperature=temp,
            max_tokens=max_tok
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"오류가 발생했습니다: {str(e)}"

# 메인 UI
st.title('AI 어시스턴트')
st.markdown(f"**현재 모델: {selected_model}**")

# 채팅 히스토리 초기화
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# 사용자 입력
user_input = st.text_input("메시지를 입력하세요", key="user_input")

col1, col2, col3 = st.columns([1,1,4])
with col1:
    if st.button('전송', key="send"):
        if user_input:
            with st.spinner('처리 중...'):
                st.session_state.chat_history.append(("사용자", user_input))
                response = get_response(user_input, selected_model, temp=0.7, max_tok=100)
                st.session_state.chat_history.append(("어시스턴트", response))

# 채팅 기록 표시
st.markdown("### 대화 내용")
for role, message in st.session_state.chat_history:
    if role == "사용자":
        st.markdown(f"""<div class="user-message">
            {role}: {message}</div>""", unsafe_allow_html=True)
    else:
        st.markdown(f"""<div class="ai-message">
            {role}: {message}</div>""", unsafe_allow_html=True)

# 사이드바 하단 정보
st.sidebar.markdown("---")
st.sidebar.markdown("""
### 모델 정보
- **Qwen 2.5 표준**: 다양한 작업에 적합한 범용 모델
- **Qwen QWQ 고급**: 자연스러운 대화에 최적화된 모델
- **Qwen 2.5 코더**: 프로그래밍과 기술적 작업에 특화된 모델
""")
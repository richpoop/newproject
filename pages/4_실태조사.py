import streamlit as st
from database import init_db, save_survey

st.set_page_config(page_title="AI 및 AX 전환 실태조사", layout="wide")
init_db()

if not st.session_state.get("logged_in", False):
    st.warning("🔒 '실태조사' 페이지는 로그인 후 접근할 수 있습니다. 메인 페이지(run)에서 먼저 로그인해주세요.")
    st.stop()

user_info = st.session_state.user_info

with st.sidebar:
    st.success(f"로그인: **{user_info['username']}**님")

st.title("📋 AI와 AX(AI 전환)에 따른 학생 인식 실태조사")
st.markdown('''
본 조사는 **인공지능(AI) 기술 발전 및 AX(AI Transformation, 인공지능 전환)** 시대에 대한 학생들의 인식을 파악하기 위한 설문입니다.  
각 문항을 읽고 본인의 생각과 가장 일치하는 척도를 선택해 주세요. (1: 전혀 그렇지 않다 ~ 5: 매우 그렇다)
''')
st.divider()

questions = [
    "Q1. 나는 인공지능(AI)과 AX(AI 전환)의 기본 개념과 원리에 대해 잘 이해하고 있다.",
    "Q2. 나는 학업이나 과제 수행 시 생성형 AI 등 AI 도구를 적극적으로 활용하는 편이다.",
    "Q3. AI와 AX 전환은 나의 전공 분야 및 미래 진로에 매우 큰 영향을 미칠 것이라고 생각한다.",
    "Q4. 앞으로의 사회에서는 AI 활용 역량이 개인의 핵심 경쟁력이 될 것이라고 인식한다.",
    "Q5. 현재 학교 교육과정에서 AI 및 AX 전환 관련 교육이 충분히 제공되고 있다고 생각한다.",
    "Q6. 나는 AI가 생성한 결과물의 정확성과 신뢰성을 비판적으로 검증하려고 노력한다.",
    "Q7. AI 기술의 확산으로 인해 기존 일자리가 대체되거나 변화하는 것에 대해 위기감을 느낀다.",
    "Q8. AI 활용 과정에서 발생하는 저작권, 개인정보 침해, 데이터 편향 등 윤리적 문제를 중요하게 인식한다.",
    "Q9. 나는 향후 AI 및 AX 전환과 관련된 심화 학습이나 실습 프로그램에 참여할 의향이 높다.",
    "Q10. 전반적으로 AI와 AX 전환은 우리 사회와 나의 삶에 긍정적인 변화를 가져올 것이라고 기대한다."
]

likert_options = {
    1: "1 - 전혀 그렇지 않다",
    2: "2 - 그렇지 않다",
    3: "3 - 보통이다",
    4: "4 - 그렇다",
    5: "5 - 매우 그렇다"
}

with st.form("ax_survey_form"):
    answers = []
    for idx, q_text in enumerate(questions):
        st.markdown(f"**{q_text}**")
        ans = st.radio(
            label=f"문항 {idx+1}",
            options=[1, 2, 3, 4, 5],
            format_func=lambda x: likert_options[x],
            index=2,
            horizontal=True,
            key=f"q_{idx+1}",
            label_visibility="collapsed"
        )
        answers.append(ans)
        st.write("")
        
    submitted = st.form_submit_button("실태조사 제출하기", use_container_width=True)
    
    if submitted:
        success, msg = save_survey(user_info["userid"], answers)
        if success:
            st.success(msg)
            st.balloons()
        else:
            st.error(msg)

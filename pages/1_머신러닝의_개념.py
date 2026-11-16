import streamlit as st

st.set_page_config(page_title="머신러닝의 개념", layout="wide")

if not st.session_state.get("logged_in", False):
    st.warning("🔒 이 페이지는 로그인 후 접근할 수 있습니다. 메인 페이지(run)에서 먼저 로그인해주세요.")
    st.stop()

with st.sidebar:
    st.success(f"로그인: **{st.session_state.user_info['username']}**님")

st.subheader('머신러닝의 개념')
st.write("여기에 머신러닝의 개념에 대한 학습 내용을 작성하세요.")

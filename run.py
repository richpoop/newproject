import os
import streamlit as st
import pandas as pd
from database import init_db, register_user, authenticate_user

st.set_page_config(page_title="AI & AX 학습 웹앱", layout="wide")

# DB 초기화
init_db()

# 세션 상태 초기화
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_info" not in st.session_state:
    st.session_state.user_info = None

# 사이드바 상태 표시 및 로그아웃 버튼
with st.sidebar:
    if st.session_state.logged_in and st.session_state.user_info:
        st.success(f"환영합니다, **{st.session_state.user_info['username']}**님!")
        st.caption(f"아이디: {st.session_state.user_info['userid']}")
        if st.button("로그아웃", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.user_info = None
            st.rerun()
    else:
        st.warning("로그인이 필요합니다.")
        st.info("사이드바의 하위 페이지들은 로그인 후 이용할 수 있습니다.")

st.title("This is my first webapp")

# 로그인 여부에 따른 화면 분기
if not st.session_state.logged_in:
    st.markdown("### 서비스 이용을 위해 로그인하거나 신규 등록을 진행해주세요.")
    tab_login, tab_register = st.tabs(["로그인", "신규등록"])
    
    with tab_login:
        with st.form("login_form"):
            login_id = st.text_input("아이디 (User ID)")
            login_pw = st.text_input("비밀번호 (Password)", type="password")
            submit_login = st.form_submit_button("로그인", use_container_width=True)
            
            if submit_login:
                if not login_id or not login_pw:
                    st.error("아이디와 비밀번호를 모두 입력해주세요.")
                else:
                    user = authenticate_user(login_id, login_pw)
                    if user:
                        st.session_state.logged_in = True
                        st.session_state.user_info = {
                            "id_num": user[0],
                            "username": user[1],
                            "userid": user[2],
                            "created_at": user[3]
                        }
                        st.success("로그인에 성공했습니다!")
                        st.rerun()
                    else:
                        st.error("아이디 또는 비밀번호가 일치하지 않습니다.")
                        
    with tab_register:
        with st.form("register_form"):
            reg_name = st.text_input("이름 (Username)")
            reg_id = st.text_input("사용할 아이디 (User ID)")
            reg_pw = st.text_input("비밀번호 (Password)", type="password")
            reg_pw_confirm = st.text_input("비밀번호 확인", type="password")
            submit_reg = st.form_submit_button("신규 등록하기", use_container_width=True)
            
            if submit_reg:
                if not reg_name or not reg_id or not reg_pw:
                    st.error("모든 필드를 입력해주세요.")
                elif reg_pw != reg_pw_confirm:
                    st.error("비밀번호가 일치하지 않습니다.")
                else:
                    success, msg = register_user(reg_name, reg_id, reg_pw)
                    if success:
                        st.success(msg)
                    else:
                        st.error(msg)

else:
    # 로그인 완료 시 기존 run.py 랜딩페이지 콘텐츠 표시
    urls = [
        'https://www.youtube.com/watch?v=KR8ddnPjCtk', 
        'https://www.youtube.com/watch?v=CgSvahZkJmc', 
        'https://www.youtube.com/watch?v=CgSvahZkJmc'
    ]
    images = ['https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRfzxCnuTzUej2aNC9oXVxwLr313a7dgc5o1X6QHNNcWQ&s=10']

    con1, con2 = st.columns((4, 1))
    with con1:
        with st.expander('Content....', expanded=True):
            for url in urls:
                st.video(url)
    with con2:
        with st.expander('Tips....', expanded=True):
            st.image(images[0])

    con3, con4 = st.columns((4, 1))
    with con3:
        with st.expander('Content....', expanded=True):
            if os.path.exists('./data.csv'):
                df = pd.read_csv('./data.csv')
                st.write(df)
            else:
                st.info("'./data.csv' 파일이 현재 경로에 없습니다. 샘플 데이터를 표시합니다.")
                sample_df = pd.DataFrame({"항목": ["샘플1", "샘플2"], "값": [100, 200]})
                st.write(sample_df)
    with con4:
        with st.expander('Tips...', expanded=True):
            if os.path.exists('./ml.txt'):
                with open('./ml.txt', 'r', encoding='utf-8') as f:
                    mytxt = f.read()
                    st.markdown(mytxt)
            else:
                st.info("'./ml.txt' 파일이 현재 경로에 없습니다.")
            st.image(images[0])

import sqlite3
import hashlib
from datetime import datetime, timezone, timedelta

DB_NAME = "myproject.db"
KST = timezone(timedelta(hours=9))

def get_connection():
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    return conn

def get_kst_now():
    return datetime.now(KST).strftime("%Y-%m-%d %H:%M:%S")

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    # 사용자 테이블 생성
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id_num INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            username TEXT NOT NULL,
            userid TEXT UNIQUE NOT NULL,
            passward TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    ''')
    
    # 실태조사(inventory) 테이블 생성
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS inventory (
            id_num INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            userid TEXT NOT NULL,
            q1 INTEGER NOT NULL,
            q2 INTEGER NOT NULL,
            q3 INTEGER NOT NULL,
            q4 INTEGER NOT NULL,
            q5 INTEGER NOT NULL,
            q6 INTEGER NOT NULL,
            q7 INTEGER NOT NULL,
            q8 INTEGER NOT NULL,
            q9 INTEGER NOT NULL,
            q10 INTEGER NOT NULL,
            created_at TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def register_user(username: str, userid: str, passwd: str) -> tuple[bool, str]:
    conn = get_connection()
    cursor = conn.cursor()
    try:
        hashed_pw = hash_password(passwd)
        created_at = get_kst_now()
        cursor.execute(
            "INSERT INTO users (username, userid, passward, created_at) VALUES (?, ?, ?, ?)",
            (username, userid, hashed_pw, created_at)
        )
        conn.commit()
        return True, "회원가입이 완료되었습니다. 로그인 탭에서 로그인해주세요."
    except sqlite3.IntegrityError:
        return False, "이미 존재하는 아이디(userid)입니다. 다른 아이디를 사용해주세요."
    except Exception as e:
        return False, f"오류가 발생했습니다: {e}"
    finally:
        conn.close()

def authenticate_user(userid: str, passwd: str):
    conn = get_connection()
    cursor = conn.cursor()
    hashed_pw = hash_password(passwd)
    cursor.execute(
        "SELECT id_num, username, userid, created_at FROM users WHERE userid = ? AND passward = ?",
        (userid, hashed_pw)
    )
    user = cursor.fetchone()
    conn.close()
    return user

def save_survey(userid: str, answers: list[int]) -> tuple[bool, str]:
    conn = get_connection()
    cursor = conn.cursor()
    try:
        created_at = get_kst_now()
        cursor.execute('''
            INSERT INTO inventory (userid, q1, q2, q3, q4, q5, q6, q7, q8, q9, q10, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (userid, *answers, created_at))
        conn.commit()
        return True, "실태조사 응답이 성공적으로 저장되었습니다. 참여해주셔서 감사합니다!"
    except Exception as e:
        return False, f"저장 중 오류가 발생했습니다: {e}"
    finally:
        conn.close()

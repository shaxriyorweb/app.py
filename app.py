import streamlit as st
import sqlite3
import requests
from datetime import datetime

# ============ Telegram bot sozlamalari ============
BOT_TOKEN = "7899690264:AAH14dhEGOlvRoc4CageMH6WYROMEE5NmkY"
CHAT_ID = "-1002671611327"

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "HTML"
    }
    try:
        response = requests.post(url, data=payload)
        return response.ok
    except Exception as e:
        return False

# ============ Ma'lumotlar bazasi ============
DB_NAME = "users.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        firstname TEXT,
        lastname TEXT,
        category TEXT
    )''')

    users = [
        ("admin", "admin123", "Admin", "Superuser", "Admin"),
        ("jsmith", "pass123", "John", "Smith", "Ishchi"),
        ("adoe", "hello123", "Alice", "Doe", "Texnik"),
        ("bbrown", "welcome1", "Bob", "Brown", "Boshqaruvchi"),
        ("cjones", "abc123", "Charlie", "Jones", "Ishchi"),
        ("dlee", "test321", "David", "Lee", "Mehmon"),
        ("eclark", "pass321", "Eva", "Clark", "Ishchi"),
        ("fmartin", "qwerty1", "Frank", "Martin", "Texnik"),
        ("gwhite", "letmein", "Grace", "White", "Boshqaruvchi"),
        ("hyoung", "123456", "Helen", "Young", "Mehmon")
    ]

    c.execute("SELECT COUNT(*) FROM users")
    if c.fetchone()[0] == 0:
        for u in users:
            c.execute("INSERT INTO users (username, password, firstname, lastname, category) VALUES (?, ?, ?, ?, ?)", u)
        conn.commit()
    conn.close()

def check_user(username, password):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT firstname, lastname, category FROM users WHERE username=? AND password=?", (username, password))
    result = c.fetchone()
    conn.close()
    return result

# ============ Streamlit UI ============
st.set_page_config(page_title="Xodim Kirish Tizimi", layout="centered")
st.markdown("""
    <style>
        body, .stApp { background-color: #f5f5f5; }
        .stTextInput>div>div>input {
            background-color: #fff; color: #000;
        }
    </style>
""", unsafe_allow_html=True)

st.title("🔐 Xodim Kirish Tizimi")

init_db()

login = st.text_input("Login")
password = st.text_input("Parol", type="password")

if st.button("Kirish"):
    user = check_user(login, password)
    if user:
        firstname, lastname, category = user
        vaqt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.success(f"Xush kelibsiz, {firstname} {lastname}!")

        message = (
            f"\u2705 <b>Kirish:</b>\n"
            f"Ism: <b>{firstname}</b>\n"
            f"Familiya: <b>{lastname}</b>\n"
            f"Kategoriya: <b>{category}</b>\n"
            f"Login: <b>{login}</b>\n"
            f"Vaqti: <b>{vaqt}</b>"
        )

        if send_telegram_message(message):
            st.info("Telegramga yuborildi!")
        else:
            st.warning("Telegram yuborilmadi.")

        if category.lower() == "admin":
            st.subheader("🔧 Admin Panel")
            st.info("Bu yerda foydalanuvchilar ro'yxatini ko'rish mumkin.")
            conn = sqlite3.connect(DB_NAME)
            c = conn.cursor()
            c.execute("SELECT firstname, lastname, category FROM users")
            rows = c.fetchall()
            conn.close()
            for r in rows:
                st.write(f"👤 {r[0]} {r[1]} - [{r[2]}]")
    else:
        st.error("❌ Login yoki parol noto‘g‘ri.")

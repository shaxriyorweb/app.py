import streamlit as st
import sqlite3
from datetime import datetime
import requests

BOT_TOKEN = "7899690264:AAH14dhEGOlvRoc4CageMH6WYROMEE5NmkY"
CHAT_ID = "-1002671611327"
DB_NAME = "users.db"

def send_telegram_message(text: str):
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
        st.error(f"Telegramga yuborishda xatolik: {e}")
        return False

def check_user(username, password):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT firstname, lastname, category FROM users WHERE username=? AND password=?", (username, password))
    result = c.fetchone()
    conn.close()
    return result

st.set_page_config(page_title="Xodim Kirish Tizimi", layout="centered")

st.markdown("""
    <style>
        body {
            background-color: #f6f6f6;
        }
        .stButton button {
            background-color: #4CAF50;
            color: white;
        }
    </style>
""", unsafe_allow_html=True)

st.title("🔐 Xodim Kirish Tizimi")

login = st.text_input("Login")
password = st.text_input("Parol", type="password")

if st.button("Kirish"):
    user = check_user(login, password)
    if user:
        firstname, lastname, category = user
        vaqt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        st.success(f"Xush kelibsiz, {firstname} {lastname}! ({category})")

        msg = (
            f"🟢 <b>Xodim kirishi</b>\n"
            f"👤 Ism: <b>{firstname}</b>\n"
            f"👥 Familiya: <b>{lastname}</b>\n"
            f"🏷 Kategoriya: <b>{category}</b>\n"
            f"🕒 Vaqt: <b>{vaqt}</b>\n"
            f"🖥 Login: <code>{login}</code>"
        )

        if send_telegram_message(msg):
            st.info("✅ Telegramga yuborildi.")
        else:
            st.error("❌ Telegramga yuborilmadi.")
        
        if login == "admin":
            st.subheader("🛠️ Admin Panel")
            st.write("Hozircha: Foydalanuvchilarni ko‘rish yoki tahrirlash funksiyasi mavjud emas.")
    else:
        st.error("❌ Login yoki parol noto‘g‘ri.")

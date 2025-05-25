import streamlit as st
import sqlite3
from datetime import datetime
import requests

# Telegram bot sozlamalari
BOT_TOKEN = "YOUR_BOT_TOKE"  # O'zingizning bot tokeningizni yozing
CHAT_ID = "YOUR_CHAT_ID"      # Guruh yoki foydalanuvchi chat ID

# Telegramga matnli xabar yuborish
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
        st.error(f"Telegram yuborishda xatolik: {e}")
        return False

# Foydalanuvchini tekshirish
def check_user(username, password):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT firstname, lastname, category FROM users WHERE username=? AND password=?", (username, password))
    result = c.fetchone()
    conn.close()
    return result

# Streamlit sahifasi konfiguratsiyasi
st.set_page_config(page_title="Xodim Kirish", layout="centered")
st.markdown("""
    <style>
        body {
            background-color: #f8f9fa;
        }
        .stButton button {
            background-color: #2b8a3e;
            color: white;
        }
    </style>
""", unsafe_allow_html=True)

st.title("🔐 Xodim Kirish Tizimi")

# Kirish formasi
login = st.text_input("Login")
password = st.text_input("Parol", type="password")

if st.button("Kirish"):
    user = check_user(login, password)
    if user:
        firstname, lastname, category = user
        vaqt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        st.success(f"Xush kelibsiz, {firstname} {lastname} ({category})!")

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
    else:
        st.error("❌ Login yoki parol noto‘g‘ri.")

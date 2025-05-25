import streamlit as st
import requests
from datetime import datetime
import sqlite3
import os

# ================= Telegram bot sozlamalari ==================
BOT_TOKEN = "7899690264:AAH14dhEGOlvRoc4CageMH6WYROMEE5NmkY"   # Bu yerga Telegram bot tokeningizni yozing
CHAT_ID = "-1002671611327"       # Bu yerga chat yoki guruh ID sini yozing

def send_telegram_message(text: str) -> bool:
    """Telegramga matnli xabar yuboradi"""
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
        st.error(f"Telegramga xabar yuborishda xatolik: {e}")
        return False

# ================= SQLite bilan ishlash =======================
DB_PATH = 'users.db'

def init_db():
    """Bazani yaratadi va agar bo‘lmasa, boshlang‘ich foydalanuvchini qo‘shadi"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        firstname TEXT,
        lastname TEXT
    )''')
    # Agar users bo‘sh bo‘lsa, birinchi foydalanuvchini qo‘shamiz
    c.execute("SELECT COUNT(*) FROM users")
    count = c.fetchone()[0]
    if count == 0:
        c.execute("INSERT INTO users (username, password, firstname, lastname) VALUES (?, ?, ?, ?)",
                  ('testuser', '1234', 'Ali', 'Valiyev'))
        conn.commit()
    conn.close()

def check_user(username, password):
    """Foydalanuvchini bazadan tekshiradi"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT firstname, lastname FROM users WHERE username=? AND password=?", (username, password))
    result = c.fetchone()
    conn.close()
    return result  # (firstname, lastname) yoki None

# ================= Streamlit UI ==============================
st.set_page_config(page_title="Xodim Kirish Tizimi", layout="centered")
st.title("🔐 Xodim Kirish Tizimi")

# Bazani ishga tushirish
init_db()

login = st.text_input("Login")
password = st.text_input("Parol", type="password")

if st.button("Kirish"):
    user = check_user(login, password)
    if user:
        firstname, lastname = user
        vaqt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        st.success(f"Xush kelibsiz, {firstname} {lastname}!")

        message = (
            f"🟢 <b>Xodim kirishi</b>:\n"
            f"Login: <b>{login}</b>\n"
            f"Ism: <b>{firstname}</b>\n"
            f"Familiya: <b>{lastname}</b>\n"
            f"Kirish vaqti: <b>{vaqt}</b>"
        )

        if send_telegram_message(message):
            st.info("Telegramga muvaffaqiyatli yuborildi!")
        else:
            st.error("Telegramga yuborishda xatolik yuz berdi.")
    else:
        st.error("❌ Login yoki parol noto‘g‘ri.")

import streamlit as st
import requests
from datetime import datetime

# ================= Telegram bot sozlamalari ==================
BOT_TOKEN = "YOUR_BOT_TOKEN"   # Telegram bot tokeningizni shu yerga yozing
CHAT_ID = "YOUR_CHAT_ID"       # Chat yoki guruh ID sini shu yerga yozing

def send_telegram_message(text: str) -> bool:
    """Telegramga matnli xabar yuboradi"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "HTML"  # HTML formatida yuborish uchun
    }
    try:
        response = requests.post(url, data=payload)
        return response.ok
    except Exception as e:
        st.error(f"Telegram xabar yuborishda xatolik: {e}")
        return False

# ================= Xodimlar ma'lumotlari ===================
# login : (parol, ism, familiya)
users = {
    "user1": ("1234", "Ali", "Valiyev"),
    "user2": ("abcd", "Gulnoza", "Sultonova"),
    "user3": ("pass123", "Jasur", "Karimov"),
    # Istalgancha qo‘shishingiz mumkin
}

# ================= Streamlit UI ===========================
st.set_page_config(page_title="Xodim Kirish Tizimi", layout="centered")
st.title("🔐 Xodim Kirish Tizimi")

login = st.text_input("Login")
password = st.text_input("Parol", type="password")

if st.button("Kirish"):
    if login in users and users[login][0] == password:
        ism = users[login][1]
        familiya = users[login][2]
        vaqt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Foydalanuvchiga xush kelibsiz xabari
        st.success(f"Xush kelibsiz, {ism} {familiya}!")

        # Telegram uchun xabar tayyorlash
        message = (
            f"🟢 <b>Xodim kirishi</b>:\n"
            f"Login: <b>{login}</b>\n"
            f"Ism: <b>{ism}</b>\n"
            f"Familiya: <b>{familiya}</b>\n"
            f"Kirish vaqti: <b>{vaqt}</b>"
        )

        # Telegramga yuborish
        if send_telegram_message(message):
            st.info("Telegramga muvaffaqiyatli yuborildi!")
        else:
            st.error("Telegramga yuborishda xatolik yuz berdi.")
    else:
        st.error("❌ Login yoki parol noto‘g‘ri.")

import streamlit as st
import requests
from datetime import datetime
import pytz

# Telegram bot token va chat ID
BOT_TOKEN = "7899690264:AAH14dhEGOlvRoc4CageMH6WYROMEE5NmkY"
CHAT_ID = "-1002671611327"

# Telegramga xabar yuborish funksiyasi
def send_to_telegram(firstname, lastname):
    tz = pytz.timezone("Asia/Tashkent")
    time_now = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")

    message = (
        f"📥 <b>Xodim tizimga kirdi</b>\n"
        f"👤 Ismi: <b>{firstname}</b>\n"
        f"👤 Familiyasi: <b>{lastname}</b>\n"
        f"🕒 Vaqti: <b>{time_now}</b>"
    )

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }

    try:
        response = requests.post(url, data=payload)
        if response.status_code != 200:
            st.error("❌ Telegramga yuborishda muammo yuz berdi.")
    except Exception as e:
        st.error(f"❌ Telegram xatosi: {e}")

# Foydalanuvchilar ro'yxati (qattiq kodlangan)
users = {
    "testuser": ("1234", "Ali", "Valiyev"),
    "johndoe": ("abcd", "John", "Doe"),
    "janedoe": ("pass", "Jane", "Doe"),
    "anvarbek": ("qwerty", "Anvar", "Beknazarov"),
    "nilufar": ("12345", "Nilufar", "Karimova"),
    "asadbek": ("asdf", "Asadbek", "Rasulov"),
    "dilnoza": ("xyz", "Dilnoza", "Islomova"),
    "temurbek": ("temur123", "Temurbek", "Xolmatov"),
    "aziza": ("aziza12", "Aziza", "G‘aniyeva"),
    "olim": ("olim999", "Olim", "Murodov")
}

# Streamlit interfeysi
st.set_page_config(page_title="Kirish", layout="centered")
st.title("🔐 Xodim tizimiga kirish")

login = st.text_input("Login")
password = st.text_input("Parol", type="password")

if st.button("Kirish"):
    if login in users and users[login][0] == password:
        firstname, lastname = users[login][1], users[login][2]
        st.success(f"Xush kelibsiz, {firstname} {lastname}!")

        # Telegramga yuborish
        send_to_telegram(firstname, lastname)
    else:
        st.error("❌ Login yoki parol noto‘g‘ri.")

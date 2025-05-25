import streamlit as st
import sqlite3
import datetime
import requests

# Telegram bot sozlamalari
BOT_TOKEN = "YOUR_BOT_TOKEN"
CHAT_ID = "YOUR_CHAT_ID"

def send_to_telegram(firstname, lastname):
    time_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message = f"📌 Yangi kirish:\n👤 {firstname} {lastname}\n🕒 {time_now}"
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    try:
        requests.post(url, data={"chat_id": CHAT_ID, "text": message})
    except Exception as e:
        st.error("❌ Telegramga yuborishda muammo yuz berdi.")
        print(e)

# Oddiy foydalanuvchilar ro'yxati (bazasiz)
users = {
    "testuser": ("1234", "Ali", "Valiyev"),
    "johndoe": ("abcd", "John", "Doe"),
    "janedoe": ("pass", "Jane", "Doe")
}

def check_user(username, password):
    if username in users and users[username][0] == password:
        return users[username][1], users[username][2]
    return None

# Streamlit UI
st.set_page_config(page_title="Xodim Kirish Tizimi", layout="centered")
st.title("🔐 Xodim Kirish")

login = st.text_input("Login")
password = st.text_input("Parol", type="password")

if st.button("Kirish"):
    result = check_user(login, password)
    if result:
        firstname, lastname = result
        st.success(f"Xush kelibsiz, {firstname} {lastname}!")
        send_to_telegram(firstname, lastname)
    else:
        st.error("Login yoki parol noto‘g‘ri.")

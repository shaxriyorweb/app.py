import streamlit as st
import requests
from datetime import datetime

# ================= Telegram bot sozlamalari ==================
BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"   # <-- bu yerga o'zingizning bot tokeningizni yozing
CHAT_ID = "YOUR_CHAT_ID_OR_GROUP_ID"    # <-- bu yerga chat yoki guruh ID ni yozing

def send_telegram_message(firstname: str, lastname: str, category: str) -> bool:
    """Telegramga xodim kirishi haqida matnli xabar yuboradi"""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    text = (
        f"📥 *Xodim tizimga kirdi!*\n\n"
        f"👤 Ism: {firstname} {lastname}\n"
        f"🏷 Kategoriya: {category}\n"
        f"⏰ Vaqti: {now}"
    )
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "Markdown"
    }
    try:
        resp = requests.post(url, data=payload, timeout=5)
        return resp.ok
    except Exception:
        return False

# ================= Foydalanuvchilar ma'lumotlari ==================
users = {
    "testuser": {"password": "1234", "firstname": "Ali", "lastname": "Valiyev", "category": "Admin"},
    "johndoe":  {"password": "abcd", "firstname": "John", "lastname": "Doe",     "category": "Staff"},
    "janedoe":  {"password": "pass", "firstname": "Jane", "lastname": "Doe",     "category": "HR"},
    "anvarbek": {"password": "qwerty", "firstname": "Anvar", "lastname": "Beknazarov", "category": "IT"},
    "nilufar":  {"password": "12345","firstname": "Nilufar","lastname": "Karimova",   "category": "Finance"},
    "asadbek":  {"password": "asdf", "firstname": "Asadbek","lastname": "Rasulov",    "category": "Manager"},
    "dilnoza":  {"password": "xyz",  "firstname": "Dilnoza","lastname": "Islomova",   "category": "HR"},
    "temurbek":{"password":"temur123","firstname":"Temurbek","lastname":"Xolmatov",  "category":"Support"},
    "aziza":    {"password":"aziza12","firstname":"Aziza","lastname":"G‘aniyeva",     "category":"Developer"},
    "olim":     {"password":"olim999","firstname":"Olim","lastname":"Murodov",        "category":"Logistics"}
}

def check_user(username: str, password: str):
    """Login/parol to'g'ri bo'lsa (firstname, lastname, category) qaytaradi, aks holda None."""
    user = users.get(username)
    if user and user["password"] == password:
        return user["firstname"], user["lastname"], user["category"]
    return None

# ================= Streamlit UI ==============================
st.set_page_config(page_title="Xodim Kirish Tizimi", layout="centered")
st.markdown("""
    <style>
        body { background-color: #f8f9fa; }
        .stButton>button { background-color: #2b8a3e; color: white; }
        .stTextInput>div>div>input { border-radius: 5px; padding: 8px; }
    </style>
""", unsafe_allow_html=True)

st.title("🔐 Xodim Kirish Tizimi")

login = st.text_input("Login")
password = st.text_input("Parol", type="password")

if st.button("Kirish"):
    result = check_user(login, password)
    if result:
        firstname, lastname, category = result
        st.success(f"Xush kelibsiz, {firstname} {lastname}! ({category})")
        if send_telegram_message(firstname, lastname, category):
            st.info("✅ Telegramga yuborildi.")
        else:
            st.error("❌ Telegramga yuborishda muammo yuz berdi.")
    else:
        st.error("❌ Login yoki parol noto‘g‘ri.")

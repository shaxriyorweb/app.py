import streamlit as st
import sqlite3
from datetime import datetime
import requests

# ================= Telegram bot sozlamalari ==================
BOT_TOKEN = "7899690264:AAH14dhEGOlvRoc4CageMH6WYROMEE5NmkY"  # <-- o'zingizning bot tokeningiz
CHAT_ID = "-1002671611327"      # <-- o'zingizning chat ID yoki guruh ID

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
        st.error(f"Telegramga yuborishda xatolik: {e}")
        return False

# ================== SQLite bazasi ============================
DB_NAME = "users.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            firstname TEXT,
            lastname TEXT,
            category TEXT
        )
    ''')

    # 10 ta foydalanuvchi qo‘shamiz
    users = [
        ("admin", "admin123", "Admin", "Superuser", "Admin"),
        ("jsmith", "pass123", "John", "Smith", "Ishchi"),
        ("adoe", "hello123", "Alice", "Doe", "Boshqaruvchi"),
        ("bbrown", "welcome1", "Bob", "Brown", "Ishchi"),
        ("cjones", "abc123", "Charlie", "Jones", "Texnik"),
        ("dlee", "test321", "David", "Lee", "Ishchi"),
        ("eclark", "pass321", "Eva", "Clark", "Mehmon"),
        ("fmartin", "qwerty1", "Frank", "Martin", "Ishchi"),
        ("gwhite", "letmein", "Grace", "White", "Texnik"),
        ("hyoung", "123456", "Helen", "Young", "Boshqaruvchi")
    ]

    for u in users:
        try:
            c.execute("INSERT INTO users (username, password, firstname, lastname, category) VALUES (?, ?, ?, ?, ?)", u)
        except sqlite3.IntegrityError:
            continue  # foydalanuvchi mavjud

    conn.commit()
    conn.close()

def check_user(username, password):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT firstname, lastname, category FROM users WHERE username=? AND password=?", (username, password))
    result = c.fetchone()
    conn.close()
    return result

# ================= Streamlit UI =============================
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

# Bazani ishga tushurish
init_db()

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
            st.write("Hozircha: Foydalanuvchilarni ko‘rish yoki tahrirlash funksiyasi mavjud emas. Qo‘shamizmi?")
    else:
        st.error("❌ Login yoki parol noto‘g‘ri.")

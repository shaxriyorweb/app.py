import streamlit as st
import telegram
from datetime import datetime

# Telegram bot token va chat id
BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN_HERE"
CHAT_ID = "YOUR_CHAT_ID_HERE"

bot = telegram.Bot(token=BOT_TOKEN)

# Foydalanuvchilar ma'lumotlari
users = {
    "testuser": {"password": "1234", "firstname": "Ali", "lastname": "Valiyev", "category": "Admin"},
    "johndoe": {"password": "abcd", "firstname": "John", "lastname": "Doe", "category": "Staff"},
    "janedoe": {"password": "pass", "firstname": "Jane", "lastname": "Doe", "category": "HR"},
    "anvarbek": {"password": "qwerty", "firstname": "Anvar", "lastname": "Beknazarov", "category": "IT"},
    "nilufar": {"password": "12345", "firstname": "Nilufar", "lastname": "Karimova", "category": "Finance"},
    "asadbek": {"password": "asdf", "firstname": "Asadbek", "lastname": "Rasulov", "category": "Manager"},
    "dilnoza": {"password": "xyz", "firstname": "Dilnoza", "lastname": "Islomova", "category": "HR"},
    "temurbek": {"password": "temur123", "firstname": "Temurbek", "lastname": "Xolmatov", "category": "Support"},
    "aziza": {"password": "aziza12", "firstname": "Aziza", "lastname": "G‘aniyeva", "category": "Developer"},
    "olim": {"password": "olim999", "firstname": "Olim", "lastname": "Murodov", "category": "Logistics"}
}

def check_user(username, password):
    user = users.get(username)
    if user and user["password"] == password:
        return user["firstname"], user["lastname"], user["category"]
    return None

def send_telegram_message(firstname, lastname, category):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message = (
        f"📥 *Xodim tizimga kirdi!*\n\n"
        f"👤 Ism: {firstname} {lastname}\n"
        f"🏷 Kategoriya: {category}\n"
        f"⏰ Vaqti: {now}"
    )
    try:
        bot.send_message(chat_id=CHAT_ID, text=message, parse_mode=telegram.ParseMode.MARKDOWN)
    except Exception as e:
        print(f"Telegramga xabar yuborishda xatolik: {e}")

def main():
    st.title("Xodimlar tizimiga kirish")

    login = st.text_input("Login")
    password = st.text_input("Parol", type="password")

    if st.button("Kirish"):
        result = check_user(login, password)
        if result:
            firstname, lastname, category = result
            st.success(f"Xush kelibsiz, {firstname} {lastname}!\nKategoriya: {category}")
            send_telegram_message(firstname, lastname, category)
        else:
            st.error("Login yoki parol noto‘g‘ri.")

if __name__ == "__main__":
    main()

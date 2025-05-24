import streamlit as st
import sqlite3
import os
import time
import cv2
import requests

# Telegram sozlamalari
BOT_TOKEN = '7899690264:AAH14dhEGOlvRoc4CageMH6WYROMEE5NmkY'     # <-- bu yerga bot tokeningizni yozing
CHAT_ID = 'YOUR_CHAT_ID'                  # <-- bu yerga adminning chat_id sini yozing

# Rasmlar saqlanadigan joy
if not os.path.exists("images"):
    os.makedirs("images")

# Login tekshirish
def check_login(username, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    data = c.fetchone()
    conn.close()
    return data

# Surat olish funksiyasi
def take_picture(filename):
    cap = cv2.VideoCapture(0)
    time.sleep(1)
    ret, frame = cap.read()
    if ret:
        filepath = os.path.join("images", filename)
        cv2.imwrite(filepath, frame)
        cap.release()
        return filepath
    cap.release()
    return None

# Telegramga yuborish funksiyasi
def send_to_telegram(image_path, full_name):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
    with open(image_path, 'rb') as photo:
        files = {'photo': photo}
        data = {'chat_id': CHAT_ID, 'caption': f"🟢 Kirish: {full_name}"}
        r = requests.post(url, files=files, data=data)
        return r.ok

# Streamlit ilova
st.set_page_config(page_title="Xodim Kirish Nazorati", layout="centered")
st.title("🔐 Xodim Kirish Tizimi")

username = st.text_input("Login")
password = st.text_input("Parol", type="password")

if st.button("Kirish"):
    user = check_login(username, password)
    if user:
        full_name = f"{user[3]} {user[4]}"
        st.success(f"Xush kelibsiz, {full_name}!")

        st.info("📷 Surat olinmoqda...")

        filename = f"{username}_{int(time.time())}.jpg"
        img_path = take_picture(filename)

        if img_path:
            st.image(img_path, caption="Yuzingiz", use_column_width=True)
            success = send_to_telegram(img_path, full_name)
            if success:
                st.success("✅ Telegramga yuborildi.")
            else:
                st.error("❌ Telegramga yuborilmadi.")
        else:
            st.error("❌ Rasm olinmadi.")
    else:
        st.error("❌ Login yoki parol noto‘g‘ri.")

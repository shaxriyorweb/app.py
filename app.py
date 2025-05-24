import streamlit as st
from streamlit_webrtc import webrtc_streamer
import cv2
import numpy as np
import sqlite3
import requests
import av
import threading

# Telegram sozlamalari
BOT_TOKEN = "7899690264:AAH14dhEGOlvRoc4CageMH6WYROMEE5NmkY"
CHAT_ID = "-1002671611327"

# SQLite DB bilan bog'lanish va foydalanuvchi tekshirish
def check_login(username, password):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    data = c.fetchone()
    conn.close()
    return data

# Telegramga rasm va matn yuborish
def send_photo_to_telegram(photo_bytes, caption):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
    files = {"photo": ("image.jpg", photo_bytes, "image/jpeg")}
    data = {"chat_id": CHAT_ID, "caption": caption}
    response = requests.post(url, files=files, data=data)
    return response.ok

# Webcam kadrlarini qayta ishlash uchun sinf
class VideoProcessor:
    def __init__(self):
        self.frame = None
        self.lock = threading.Lock()
        self.captured_image = None

    def recv(self, frame):
        img = frame.to_ndarray(format="bgr24")
        with self.lock:
            self.frame = img
        return av.VideoFrame.from_ndarray(img, format="bgr24")

    def capture(self):
        with self.lock:
            if self.frame is not None:
                # Rasmni JPG formatida qaytarish
                ret, buf = cv2.imencode(".jpg", self.frame)
                if ret:
                    return buf.tobytes()
        return None

def main():
    st.title("🔐 Xodim Kirish Tizimi")

    username = st.text_input("Login")
    password = st.text_input("Parol", type="password")
    
    # Foydalanuvchi login bo‘lgan holatda webcamni ko‘rsatamiz va rasm olishni boshlaymiz
    if st.button("Kirish"):
        user = check_login(username, password)
        if user:
            full_name = f"{user[3]} {user[4]}"
            st.success(f"Xush kelibsiz, {full_name}!")

            st.write("📷 Iltimos, kamerangiz yoqilganligini tekshiring va rasm olish tugmasini bosing.")

            ctx = webrtc_streamer(key="example", video_processor_factory=VideoProcessor)

            if ctx.video_processor:
                if st.button("Rasm olish va Telegramga yuborish"):
                    img_bytes = ctx.video_processor.capture()
                    if img_bytes:
                        st.image(img_bytes, caption="Olingan rasm", use_column_width=True)
                        success = send_photo_to_telegram(img_bytes, f"🟢 Kirish: {full_name}")
                        if success:
                            st.success("✅ Rasm Telegramga yuborildi.")
                        else:
                            st.error("❌ Telegramga yuborishda xatolik yuz berdi.")
                    else:
                        st.error("❌ Rasm olinmadi, iltimos kamerani tekshiring.")
        else:
            st.error("❌ Login yoki parol noto‘g‘ri.")

if __name__ == "__main__":
    main()

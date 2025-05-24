import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase
import sqlite3
import cv2
import numpy as np
import av
import os
import requests
import time

BOT_TOKEN = '7899690264:AAH14dhEGOlvRoc4CageMH6WYROMEE5NmkY'
CHAT_ID = '-1002671611327'

class VideoProcessor(VideoProcessorBase):
    def __init__(self):
        self.frame = None

    def recv(self, frame: av.VideoFrame) -> av.VideoFrame:
        img = frame.to_ndarray(format="bgr24")
        self.frame = img
        return av.VideoFrame.from_ndarray(img, format="bgr24")

def check_login(username, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    data = c.fetchone()
    conn.close()
    return data

def save_frame(img, filename):
    filepath = os.path.join("images", filename)
    cv2.imwrite(filepath, img)
    return filepath

def send_to_telegram(image_path, full_name):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
    with open(image_path, 'rb') as photo:
        files = {'photo': photo}
        data = {'chat_id': CHAT_ID, 'caption': f"🟢 Kirish: {full_name}"}
        r = requests.post(url, files=files, data=data)
        return r.ok

st.set_page_config(page_title="Xodim Kirish", layout="centered")
st.title("🔐 Xodim Kirish Tizimi")

username = st.text_input("Login")
password = st.text_input("Parol", type="password")

if st.button("Kirish"):
    user = check_login(username, password)
    if user:
        full_name = f"{user[3]} {user[4]}"
        st.success(f"Xush kelibsiz, {full_name}")
        st.info("📷 Kamerani yoqing va surat oling:")

        ctx = webrtc_streamer(key="camera", video_processor_factory=VideoProcessor)

        if ctx.video_processor and ctx.video_processor.frame is not None:
            if st.button("📸 Suratni Olish"):
                if not os.path.exists("images"):
                    os.makedirs("images")
                img = ctx.video_processor.frame
                filename = f"{username}_{int(time.time())}.jpg"
                path = save_frame(img, filename)
                st.image(img, caption="Olingan surat", channels="BGR")

                if send_to_telegram(path, full_name):
                    st.success("✅ Telegramga yuborildi.")
                else:
                    st.error("❌ Telegramga yuborilmadi.")
    else:
        st.error("❌ Login yoki parol noto‘g‘ri.")

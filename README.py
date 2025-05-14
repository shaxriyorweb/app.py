import streamlit as st
import pandas as pd
import sqlite3
from db import init_db, insert_result, get_all_results

# Dastlabki sozlamalar
st.set_page_config(page_title="Psixologik Test", layout="centered")

# Fon rasmi
st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] {
        background-image: url("background.jpg");
        background-size: cover;
        background-position: center;
    }
    </style>
    """, unsafe_allow_html=True)

# Viloyatlar
regions = [
    "Toshkent", "Samarqand", "Buxoro", "Farg‘ona", "Andijon", "Namangan",
    "Xorazm", "Surxondaryo", "Qashqadaryo", "Jizzax", "Sirdaryo", "Navoiy"
]

# 30 ta savol
questions = [
    "Sinfda yangi odam bilan tanishishga tayyorman:",
    "Men xatolik qilsam nima qilaman?",
    "Do‘stlarim meni qanday tasvirlaydi?",
    "Men uchun maktabdagi eng yaxshi narsa:",
    "Agar sinfdoshim yig‘lasa...",
    "Darsdan keyin nima qilganni yoqtirasiz?",
    "Ko‘p hollarda men o‘zimni qanday his qilaman?",
    "Men yangi narsalarni:",
    "Guruhda ishlash men uchun:",
    "Tanbeh eshitsam:",
    "Men uchun dam olish degani:",
    "Men darsda:",
    "Men stress holatida:",
    "Ota-onam bilan munosabatim:",
    "Men tushkunlikka tushsam:",
    "Sinfda biror narsa noto‘g‘ri bo‘lsa:",
    "Men orzularim haqida:",
    "Men o‘zimni qanday ko‘raman?",
    "Yolg‘izlik siz uchun:",
    "Musobaqalarda qatnashish:",
    "Jamoaviy ishda:",
    "Men fikr bildirayotganda:",
    "Ertalab uyg‘onish:",
    "Yangi joylar:",
    "Men his-tuyg‘ularimni:",
    "Agar kimgadir yordam kerak bo‘lsa:",
    "Yutuqqa erishsam:",
    "Baholar siz uchun:",
    "Tushunmovchilik yuz bersa:",
    "O‘zimni eng baxtli his qilaman:"
]

options = {
    "A": "Ijtimoiy, ochiq, faol",
    "B": "O‘ylovchi, ehtiyotkor, diqqatli",
    "C": "Yakkaxol, mustaqil, ichki dunyoga ega"
}

# Ma'lumotlar bazasini ishga tushirish
init_db()

st.title("🧠 Maktab O‘quvchilari Uchun Psixologik Test")

menu = st.sidebar.selectbox("Bo‘limni tanlang", ["Testni boshlash", "Admin ko‘rish"])

# TEST BO'LIMI
if menu == "Testni boshlash":
    with st.form("user_form"):
        st.subheader("Shaxsiy Ma'lumotlar")
        name = st.text_input("Ism")
        surname = st.text_input("Familiya")
        age = st.number_input("Yosh", min_value=6, max_value=22)
        gender = st.radio("Jins", ["Erkak", "Ayol"])
        region = st.selectbox("Viloyat", regions)
        submit_info = st.form_submit_button("Testni boshlash")

    if submit_info:
        answers = []
        with st.form("quiz_form"):
            st.subheader("📝 Test Savollari")
            for i, question in enumerate(questions):
                answer = st.radio(f"{i+1}. {question}", ["A", "B", "C"], key=f"q{i}")
                answers.append(answer)
            submit_test = st.form_submit_button("Natijani ko‘rish")

        if submit_test:
            a_count = answers.count("A")
            b_count = answers.count("B")
            c_count = answers.count("C")
            total = len(answers)

            st.subheader("📊 Natijalar:")
            st.write(f"A ({options['A']}): {a_count} ta ({a_count/total*100:.1f}%)")
            st.write(f"B ({options['B']}): {b_count} ta ({b_count/total*100:.1f}%)")
            st.write(f"C ({options['C']}): {c_count} ta ({c_count/total*100:.1f}%)")

            st.subheader("🧠 Maslahat:")
            if a_count > b_count and a_count > c_count:
                st.info("Siz ijtimoiy va faol odamsiz. Jamoaviy ishlarda qatnashing.")
            elif b_count > a_count and b_count > c_count:
                st.info("Siz ehtiyotkor va mulohazalisiz. O‘zingizga ishonchni kuchaytiring.")
            elif c_count > a_count and c_count > b_count:
                st.info("Siz mustaqilsiz. Biroq jamoa bilan ishlashni ham unutmang.")
            else:
                st.info("Sizda har xil fazilatlar uyg‘unlashgan. Bu juda yaxshi.")

            insert_result(name, surname, age, gender, region, a_count, b_count, c_count)

            st.success("Natijangiz saqlandi ✅")

# ADMIN PANEL
elif menu == "Admin ko‘rish":
    st.subheader("📋 Barcha Foydalanuvchilar Natijalari")
    df = get_all_results()
    st.dataframe(df)

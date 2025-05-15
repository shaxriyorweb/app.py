import streamlit as st
import pandas as pd
import sqlite3
import random

st.set_page_config(page_title="Psixologik Test", page_icon="🧠")

# Viloyatlar ro‘yxati
regions = [
    "Toshkent", "Samarqand", "Buxoro", "Farg‘ona", "Andijon", "Namangan",
    "Xorazm", "Surxondaryo", "Qashqadaryo", "Jizzax", "Sirdaryo", "Navoiy"
]

# 30 ta savol
original_questions = [
    ("Sinfda yangi odam bilan tanishishga tayyorman:", ["A. Ha, xursand bo‘laman", "B. Biroz uyalaman", "C. Yolg‘iz qolishni afzal ko‘raman"]),
    ("Men xatolik qilsam nima qilaman?", ["A. O‘rganaman va davom etaman", "B. Biroz xafa bo‘laman", "C. O‘zimni juda aybdor his qilaman"]),
    # ... (yana 28 ta savol — siz ilgari taqdim etgan savollar to‘liq shu yerga qo‘shiladi)
    ("O‘zimni eng baxtli his qilaman:", ["A. Do‘stlar orasida", "B. O‘zim yoqtirgan ish bilan band bo‘lsam", "C. O‘zim bilan yolg‘iz qolganda"]),
]

# Ma'lumot kiritish formasi
st.title("🧠 Psixologik Test (Maktab o‘quvchilari uchun)")

if "started" not in st.session_state:
    with st.form("user_form"):
        st.subheader("👤 Shaxsiy Ma'lumotlar")
        name = st.text_input("Ismingiz")
        surname = st.text_input("Familiyangiz")
        age = st.number_input("Yoshingiz", min_value=6, max_value=28, step=1)
        gender = st.radio("Jinsingiz", ["Erkak", "Ayol"])
        region = st.selectbox("Qaysi viloyatdan siz?", regions)
        submit_info = st.form_submit_button("Testni boshlash")

        if submit_info:
            if not name or not surname or not region or not gender:
                st.warning("Iltimos, barcha ma'lumotlarni to‘liq kiriting.")
            else:
                st.session_state["user"] = {
                    "name": name,
                    "surname": surname,
                    "age": age,
                    "gender": gender,
                    "region": region
                }
                st.session_state["questions"] = random.sample(original_questions, len(original_questions))
                st.session_state["started"] = True

# Test
if st.session_state.get("started"):
    st.header("📋 30 ta Savol")
    answers = []

    with st.form("quiz_form"):
        for i, (question, options) in enumerate(st.session_state["questions"]):
            answer = st.radio(f"{i+1}. {question}", options, key=f"q{i}", index=None)
            answers.append(answer[0] if answer else None)

        submit_answers = st.form_submit_button("✅ Natijani ko‘rish")

    if submit_answers:
        if None in answers:
            st.error("Iltimos, barcha savollarga javob bering.")
        else:
            a_count = answers.count("A")
            b_count = answers.count("B")
            c_count = answers.count("C")
            total = len(answers)

            a_percent = round(a_count / total * 100, 1)
            b_percent = round(b_count / total * 100, 1)
            c_percent = round(c_count / total * 100, 1)

            st.subheader("📊 Sizning Natijangiz")
            st.write(f"A javoblari: {a_count} ta ({a_percent}%)")
            st.write(f"B javoblari: {b_count} ta ({b_percent}%)")
            st.write(f"C javoblari: {c_count} ta ({c_percent}%)")

            st.subheader("🧠 Maslahat")
            if a_count > b_count and a_count > c_count:
                st.info("Siz do‘stona, ochiq va ijtimoiy odamsiz.")
            elif b_count > a_count and b_count > c_count:
                st.info("Siz diqqatli va mulohazali odamsiz.")
            elif c_count > a_count and c_count > b_count:
                st.info("Siz mustaqil va ichki dunyoga ega odamsiz.")
            else:
                st.info("Sizda turli fazilatlar uyg‘unlashgan.")

            # Bazaga saqlash
            conn = sqlite3.connect("results.db")
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS results (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    surname TEXT,
                    age INTEGER,
                    gender TEXT,
                    region TEXT,
                    a_percent REAL,
                    b_percent REAL,
                    c_percent REAL
                )""")
            user = st.session_state["user"]
            cursor.execute("""
                INSERT INTO results (name, surname, age, gender, region, a_percent, b_percent, c_percent)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (user["name"], user["surname"], user["age"], user["gender"], user["region"],
                  a_percent, b_percent, c_percent))
            conn.commit()
            conn.close()
            st.success("✅ Natijangiz saqlandi!")

# Admin panel
st.sidebar.markdown("🔐 Admin panel")
if st.sidebar.button("📊 Barcha natijalarni ko‘rish"):
    conn = sqlite3.connect("results.db")
    df = pd.read_sql_query("SELECT * FROM results", conn)
    conn.close()

    st.subheader("📋 Foydalanuvchilar natijalari")
    st.dataframe(df)

    st.subheader("📊 Viloyat bo‘yicha o‘rtacha foizlar")
    region_data = df.groupby('region').agg(
        a_avg=('a_percent', 'mean'),
        b_avg=('b_percent', 'mean'),
        c_avg=('c_percent', 'mean')
    ).reset_index()
    st.write(region_data)

    st.subheader("📊 Yosh bo‘yicha o‘rtacha foizlar")
    age_data = df.groupby('age').agg(
        a_avg=('a_percent', 'mean'),
        b_avg=('b_percent', 'mean'),
        c_avg=('c_percent', 'mean')
    ).reset_index()
    st.write(age_data)

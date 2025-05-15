import streamlit as st
import random
import sqlite3
import pandas as pd

st.set_page_config(page_title="Psychology Quiz", layout="centered")

# Test savollari
test_questions = [
    ("Do‘stlaringiz bilan bo‘lishish siz uchun qanchalik muhim?", ["A. Juda muhim", "B. O‘rtacha", "C. Kamdan-kam"]),
    ("Yangi odamlar bilan tanishish sizga yoqadimi?", ["A. Ha, juda yoqadi", "B. Vaziyatga qarab", "C. Unchalik emas"]),
    ("Ishni yakunlash siz uchun qanchalik muhim?", ["A. Har doim tugataman", "B. Ba'zida tugataman", "C. Ko‘p holatda yarim yo‘lda qoldiraman"]),
    ("Stressli vaziyatlarda qanday harakat qilasiz?", ["A. Hissiyotimni ifodalayman", "B. Ichimga yutaman", "C. Maslahatlasha boshlayman"]),
    ("Yolg‘izlik sizga qanday ta’sir qiladi?", ["A. Tinchlik beradi", "B. Ko‘nikkanman", "C. Bezovta qiladi"]),
    ("Yangi topshiriqlarni bajarishda siz qanday harakat qilasiz?", ["A. Darhol kirishaman", "B. O‘ylab ko‘rib kirishaman", "C. Kechiktiraman"]),
    ("Do‘stlaringiz sizni qanday ta’riflaydi?", ["A. Ochiq va ijtimoiy", "B. Tinch va xotirjam", "C. Fikrlovchi va mustaqil"]),
    ("Muammoga duch kelsangiz, nima qilasiz?", ["A. Boshqalardan yordam so‘rayman", "B. Mustaqil hal qilaman", "C. Vaziyatga qarab"]),
    ("Dam olish kunlaringizni qanday o‘tkazasiz?", ["A. Do‘stlar bilan", "B. Oila davrasida", "C. Yolg‘iz kitob o‘qib"]),
    ("O‘zingizga bo‘lgan ishonchingiz qanchalik yuqori?", ["A. Yuqori", "B. O‘rtacha", "C. Kam"]),
    ("Hayotdagi maqsadingiz aniqmi?", ["A. Ha, juda aniq", "B. Taxminan bilaman", "C. Hali aniqlamadim"]),
    ("Yutuqlaringizni boshqalar bilan bo‘lishasizmi?", ["A. Ha", "B. Ba'zida", "C. Yo‘q"]),
    ("Tanqidni qanday qabul qilasiz?", ["A. Ijobiy", "B. Xafa bo‘laman", "C. E’tibor bermayman"]),
    ("Do‘stlaringiz soni qancha?", ["A. Juda ko‘p", "B. O‘rtacha", "C. Kam"]),
    ("Yangi ish boshlashdan oldin nima qilasiz?", ["A. Rejalashtiraman", "B. Darhol boshlayman", "C. O‘ylab yuraman"]),
    ("Stressni qanday yengasiz?", ["A. Sport bilan", "B. Suhbat orqali", "C. Yolg‘izlikda"]),
    ("Siz uchun muhim narsa nima?", ["A. Aloqalar", "B. Xavfsizlik", "C. Mustaqillik"]),
    ("Mas'uliyatli vazifalarda o‘zingizni qanday his qilasiz?", ["A. Ishonchli", "B. Biroz hayajon", "C. Qiyinchilik bilan"]),
    ("Ijtimoiy tadbirlarda siz...", ["A. Markazda bo‘laman", "B. Chekkada turaman", "C. Umuman qatnashmayman"]),
    ("O‘qish va o‘rganishga bo‘lgan munosabatingiz qanday?", ["A. Juda ijobiy", "B. Qiziqishga qarab", "C. Majburiyat sifatida"]),
    ("Muammoni boshqalarga aytish sizga osonmi?", ["A. Ha", "B. Vaziyatga qarab", "C. Yo‘q"]),
    ("O‘zingizni boshqalarga taqqoslaysizmi?", ["A. Kamdan-kam", "B. Ba'zida", "C. Tez-tez"]),
    ("Maqsad sari harakat qanday bo‘ladi?", ["A. Rejali", "B. Har xil", "C. Sekin"]),
    ("Ish jarayonida siz...", ["A. Hamma bilan ishlay olaman", "B. Tanlanganlar bilan", "C. Yolg‘iz yaxshi ishlayman"]),
    ("Qiyin vaziyatda siz...", ["A. Hal qilishga urinaman", "B. Qochaman", "C. Boshqalarga yuklayman"]),
    ("Sizning hayotiy qadriyatlaringiz...", ["A. Aniq va qat'iy", "B. Vaqtga qarab o‘zgaradi", "C. Hali shakllanmagan"]),
    ("Tashqi ko‘rinishingiz siz uchun...", ["A. Muhim", "B. Ortiqcha", "C. E’tibor bermayman"]),
    ("Tuyg‘ularingizni boshqarasizmi?", ["A. Ha", "B. Har doim emas", "C. Qiyin"]),
    ("Dushmanlik holatida...", ["A. Murosaga boraman", "B. Indamayman", "C. Qarshi chiqaman"]),
    ("Yangi g‘oyalarga ochiqmisiz?", ["A. Ha", "B. O‘ylab ko‘raman", "C. Shubha bilan qarayman"])
]

# Foydalanuvchi ma’lumotlari
if "started" not in st.session_state:
    st.title("🧠 Psixologik Test")
    st.write("Iltimos, quyidagi ma’lumotlarni to‘ldiring:")
    name = st.text_input("Ism")
    surname = st.text_input("Familiya")
    age = st.number_input("Yosh", min_value=7, max_value=25, step=1)
    gender = st.selectbox("Jinsi", ["Erkak", "Ayol"])
    region = st.selectbox("Hudud", [
        "Toshkent", "Toshkent viloyati", "Andijon", "Farg‘ona", "Namangan",
        "Samarqand", "Buxoro", "Navoiy", "Xorazm", "Qashqadaryo", "Surxondaryo", "Jizzax"
    ])

    if st.button("Testni boshlash"):
        if not name or not surname or not region or not gender:
            st.warning("Iltimos, barcha ma’lumotlarni to‘liq kiriting.")
        else:
            st.session_state["user"] = {
                "name": name,
                "surname": surname,
                "age": age,
                "gender": gender,
                "region": region
            }
            st.session_state["started"] = True

# Test boshlangan bo‘lsa
if st.session_state.get("started"):
    st.header("📋 30 ta Savol")
    random.shuffle(test_questions)
    answers = []

    with st.form("quiz_form"):
        for i, (question, options) in enumerate(test_questions):
            answer = st.radio(f"{i+1}. {question}", options, key=f"q{i}", index=None)
            answers.append(answer[0] if answer else "")
        submit_answers = st.form_submit_button("✅ Natijani ko‘rish")

    if submit_answers:
        a_count = answers.count("A")
        b_count = answers.count("B")
        c_count = answers.count("C")
        total = len([a for a in answers if a in ["A", "B", "C"]])

        if total == 0:
            st.error("Iltimos, hech bo‘lmaganda bitta savolga javob bering.")
        else:
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
                st.info("Sizda turli fazilatlar uyg‘unlashgan. Bu yaxshi.")

            # Natijalarni saqlash
            conn = sqlite3.connect("results.db")
            cursor = conn.cursor()
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT, surname TEXT, age INTEGER,
                gender TEXT, region TEXT,
                a_percent REAL, b_percent REAL, c_percent REAL
            )
            """)
            user = st.session_state["user"]
            cursor.execute("""
            INSERT INTO results (name, surname, age, gender, region, a_percent, b_percent, c_percent)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                user["name"], user["surname"], user["age"], user["gender"], user["region"],
                a_percent, b_percent, c_percent
            ))
            conn.commit()
            conn.close()
            st.success("✅ Natijangiz saqlandi!")

# Admin paneli
st.sidebar.title("🔐 Admin Panel")
if st.sidebar.button("📊 Barcha natijalarni ko‘rish"):
    conn = sqlite3.connect("results.db")
    df = pd.read_sql_query("SELECT * FROM results", conn)
    conn.close()

    st.subheader("📊 Viloyat bo‘yicha natijalar")
    st.write(df.groupby("region").agg({
        "a_percent": "mean",
        "b_percent": "mean",
        "c_percent": "mean"
    }).round(1))

    st.subheader("📊 Yosh bo‘yicha natijalar")
    st.write(df.groupby("age").agg({
        "a_percent": "mean",
        "b_percent": "mean",
        "c_percent": "mean"
    }).round(1))

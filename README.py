import streamlit as st
import pandas as pd
import sqlite3

# Viloyatlar ro'yxati
regions = [
    "Toshkent", "Samarqand", "Buxoro", "Farg‘ona", "Andijon", "Namangan",
    "Xorazm", "Surxondaryo", "Qashqadaryo", "Jizzax", "Sirdaryo", "Navoiy"
]

# 30 ta savol va har biriga mos A/B/C variantlari
test_questions = [
    ("Sinfda yangi odam bilan tanishishga tayyorman:", ["A. Ha, xursand bo‘laman", "B. Biroz uyalaman", "C. Yolg‘iz qolishni afzal ko‘raman"]),
    ("Men xatolik qilsam nima qilaman?", ["A. O‘rganaman va davom etaman", "B. Biroz xafa bo‘laman", "C. O‘zimni juda aybdor his qilaman"]),
    ("Do‘stlarim meni qanday tasvirlaydi?", ["A. Do‘stona va ochiq", "B. Jiddiy va ishonchli", "C. Tinch va yolg‘onchi emas"]),
    ("Men uchun maktabdagi eng yaxshi narsa:", ["A. Do‘stlar bilan suhbat", "B. Yangi bilim olish", "C. Mustaqil ish qilish imkoni"]),
    ("Agar sinfdoshim yig‘lasa...", ["A. Darhol yordam beraman", "B. Kuzataman, keyin yordam beraman", "C. Aralashmayman"]),
    ("Darsdan keyin nima qilganni yoqtirasiz?", ["A. Do‘stlar bilan ko‘chada yurish", "B. Uyga borib kitob o‘qish", "C. Kompyuter o‘yinlari bilan vaqt o‘tkazish"]),
    ("Ko‘p hollarda men o‘zimni qanday his qilaman?", ["A. Xursand va faol", "B. Tinch va o‘ylovchan", "C. Hafsalasi pir bo‘lgan"]),
    ("Men yangi narsalarni:", ["A. Qiziqish bilan sinab ko‘raman", "B. Ehtiyot bilan yondashaman", "C. Yolg‘iz o‘rganishni yoqtiraman"]),
    ("Guruhda ishlash men uchun:", ["A. Juda maroqli", "B. O‘rtacha", "C. Qiyin"]),
    ("Tanbeh eshitsam:", ["A. Xulosa chiqaraman", "B. O‘zimga tanqid qilaman", "C. Juda xafa bo‘laman"]),
    ("Men uchun dam olish degani:", ["A. Do‘stlar bilan vaqt o‘tkazish", "B. Kitob o‘qish yoki rasm chizish", "C. YolG‘iz qolib orom olish"]),
    ("Men darsda:", ["A. Faol qatnashaman", "B. O‘rtacha qatnashaman", "C. Ko‘proq kuzatuvchiman"]),
    ("Men stress holatida:", ["A. Kim bilandir suhbatlashaman", "B. Ichimda saqlayman", "C. Yolg‘iz qolishni xohlayman"]),
    ("Ota-onam bilan munosabatim:", ["A. Ochiq va do‘stona", "B. Hurmatli va masofali", "C. Juda ko‘p gaplashmaymiz"]),
    ("Men tushkunlikka tushsam:", ["A. Do‘stlarim bilan vaqt o‘tkazaman", "B. Musiqa eshitaman", "C. Yolg‘iz qolaman"]),
    ("Sinfda biror narsa noto‘g‘ri bo‘lsa:", ["A. Aytilishini xohlayman", "B. Ichimda saqlayman", "C. Aralashmayman"]),
    ("Men orzularim haqida:", ["A. Ochiqchasiga gaplashaman", "B. Faqat yaqinlarimga aytaman", "C. Hech kimga aytmayman"]),
    ("Men o‘zimni qanday ko‘raman?", ["A. Faol va ijtimoiy", "B. O‘rtacha", "C. Tinch va mustaqil"]),
    ("Yolg‘izlik siz uchun:", ["A. Zerikarli", "B. Foydali", "C. Zarur"]),
    ("Musobaqalarda qatnashish:", ["A. Juda xush ko‘raman", "B. Ba'zida qatnashaman", "C. Yo‘q, yoqtirmayman"]),
    ("Jamoaviy ishda:", ["A. Boshchilik qilishni yoqtiraman", "B. O‘rtada bo‘laman", "C. Chetda qolishni afzal ko‘raman"]),
    ("Men fikr bildirayotganda:", ["A. Bemalol fikr bildiraman", "B. Oldin boshqalarga quloq solaman", "C. Kamdan-kam fikr bildiraman"]),
    ("Ertalab uyg‘onish:", ["A. Yengil", "B. Biroz qiynalaman", "C. Juda qiyin"]),
    ("Yangi joylar:", ["A. Qiziqarli", "B. G‘alati lekin chiroyli", "C. Notanish va noqulay"]),
    ("Men his-tuyg‘ularimni:", ["A. Oson bildiraman", "B. Faqat yaqinlarim bilan bo‘lishaman", "C. Ko‘rsatmayman"]),
    ("Agar kimgadir yordam kerak bo‘lsa:", ["A. Birinchi bo‘lib yordam beraman", "B. Kutib turaman, so‘rasa yordam beraman", "C. Aralashmayman"]),
    ("Yutuqqa erishsam:", ["A. Boshqalar bilan bo‘lishaman", "B. Ichimda xursand bo‘laman", "C. Oddiy narsa deb o‘ylayman"]),
    ("Baholar siz uchun:", ["A. Muhim", "B. Foydali lekin muhim emas", "C. Zarur emas"]),
    ("Tushunmovchilik yuz bersa:", ["A. Gaplashib hal qilaman", "B. Kutaman, o‘zi o‘tadi", "C. Uzoqlashaman"]),
    ("O‘zimni eng baxtli his qilaman:", ["A. Do‘stlar orasida", "B. O‘zim yoqtirgan ish bilan band bo‘lsam", "C. O‘zim bilan yolg‘iz qolganda"]),
]

st.title("🧠 Psixologik Test (Maktab o‘quvchilari uchun)")

# Foydalanuvchi ma'lumotlari formasi (Majburiy maydonlar bilan)
with st.form("user_form"):
    st.subheader("👤 Shaxsiy Ma'lumotlar")
    name = st.text_input("Ismingiz")
    surname = st.text_input("Familiyangiz")
    age = st.number_input("Yoshingiz", min_value=6, max_value=22, step=1)
    gender = st.radio("Jinsingiz", ["Erkak", "Ayol"])
    region = st.selectbox("Qaysi viloyatdan siz?", regions)
    submit_info = st.form_submit_button("Testni boshlash")

    if submit_info:
        # Majburiy maydonlarni tekshirish
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
            st.session_state["started"] = True

# Test savollari boshlangan bo‘lsa
if st.session_state.get("started"):
    st.header("📋 30 ta Savol")
    answers = []
    with st.form("quiz_form"):
        for i, (question, options) in enumerate(test_questions):
            answer = st.radio(f"{i+1}. {question}", options, key=f"q{i}")
            answers.append(answer[0])  # A, B, C ni oladi
        submit_answers = st.form_submit_button("✅ Natijani ko‘rish")

    if submit_answers:
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
            st.info("Siz do‘stona, ochiq va ijtimoiy odamsiz. Ijtimoiy faolligingizni qo‘llab-quvvatlang.")
        elif b_count > a_count and b_count > c_count:
            st.info("Siz diqqatli va mulohazali odamsiz. O‘zingizga ishonchingizni oshiring.")
        elif c_count > a_count and c_count > b_count:
            st.info("Siz mustaqil va ichki dunyoga ega odamsiz. Boshqalar bilan hamkorlikni ko‘paytiring.")
        else:
            st.info("Sizda turli fazilatlar uyg‘unlashgan. Bu ijobiy jihat.")

        # Natijalarni SQLite bazaga saqlash
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
        conn.commit()

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

# Admin panel - barcha natijalarni ko‘rish
st.sidebar.markdown("🔐 **Admin panel**")
if st.sidebar.button("📊 Barcha natijalarni ko‘rish"):
    conn = sqlite3.connect("results.db")
    df = pd.read_sql_query("SELECT * FROM results", conn)
    conn.close()
    st.subheader("📋 Foydalanuvchilar natijalari")
    st.dataframe(df)

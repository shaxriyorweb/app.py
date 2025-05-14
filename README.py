import streamlit as st
import pandas as pd

# Viloyatlar
regions = [
    "Toshkent", "Samarqand", "Buxoro", "Farg‘ona", "Andijon", "Namangan",
    "Xorazm", "Surxondaryo", "Qashqadaryo", "Jizzax", "Sirdaryo", "Navoiy"
]

# 30 ta savol (har biri A/B/C)
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

# Savollarni boshlashdan oldingi forma
st.title("Psixologik Test (Maktab O‘quvchilari Uchun)")

with st.form("user_form"):
    st.subheader("Shaxsiy Ma'lumotlar")
    name = st.text_input("Ism")
    surname = st.text_input("Familiya")
    age = st.number_input("Yosh", min_value=6, max_value=18)
    gender = st.radio("Jins", ["Erkak", "Ayol"])
    region = st.selectbox("Viloyatni tanlang", regions)
    submit_info = st.form_submit_button("Testni boshlash")

if submit_info:
    st.session_state["user"] = {
        "name": name,
        "surname": surname,
        "age": age,
        "gender": gender,
        "region": region
    }
    st.session_state["started"] = True

# Test savollari
if st.session_state.get("started"):
    st.header("Test Savollari")

    answers = []
    with st.form("quiz_form"):
        for i, question in enumerate(questions):
            answer = st.radio(question, ["A", "B", "C"], key=f"q{i}")
            answers.append(answer)

        submit_answers = st.form_submit_button("Natijani ko‘rish")

    if submit_answers:
        # Natijalarni hisoblash
        a_count = answers.count("A")
        b_count = answers.count("B")
        c_count = answers.count("C")
        total = len(answers)

        st.subheader("📊 Natijalar:")
        st.write(f"A javoblari: {a_count} ta ({a_count/total*100:.1f}%)")
        st.write(f"B javoblari: {b_count} ta ({b_count/total*100:.1f}%)")
        st.write(f"C javoblari: {c_count} ta ({c_count/total*100:.1f}%)")

        st.subheader("🧠 Maslahat:")
        if a_count > b_count and a_count > c_count:
            st.info("Siz do‘stona, ochiq va ijtimoiy odamsiz. Ijtimoiy faolligingizni qo‘llab-quvvatlang.")
        elif b_count > a_count and b_count > c_count:
            st.info("Siz diqqatli va mulohazali odamsiz. O‘zingizga ishonchingizni oshirish foydali bo‘ladi.")
        elif c_count > a_count and c_count > b_count:
            st.info("Siz mustaqil va o‘z dunyosiga ega odamsiz. Boshqalar bilan hamkorlik qilishga harakat qiling.")
        else:
            st.info("Sizda har xil jihatlar uyg‘unlashgan. Bu yaxshi holat.")

        # Statistikani saqlash
        user_data = st.session_state["user"]
        result_df = pd.DataFrame([{
            "Ism": user_data["name"],
            "Familiya": user_data["surname"],
            "Yosh": user_data["age"],
            "Jins": user_data["gender"],
            "Viloyat": user_data["region"],
            "A foizi": round(a_count/total*100, 1),
            "B foizi": round(b_count/total*100, 1),
            "C foizi": round(c_count/total*100, 1)
        }])

        try:
            existing = pd.read_csv("results.csv")
            final = pd.concat([existing, result_df], ignore_index=True)
        except FileNotFoundError:
            final = result_df

        final.to_csv("results.csv", index=False)
        st.success("Natijangiz saqlandi!")

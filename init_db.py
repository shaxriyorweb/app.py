import streamlit as st

# Foydalanuvchilar ma'lumotlari dict ko'rinishida
users = {
    "testuser": {"password": "1234", "firstname": "Ali", "lastname": "Valiyev", "category": "Admin"},
    "johndoe": {"password": "abcd", "firstname": "John", "lastname": "Doe", "category": "Staff"},
    "janedoe": {"password": "pass", "firstname": "Jane", "lastname": "Doe", "category": "HR"},
    "anvarbek": {"password": "qwerty", "firstname": "Anvar", "lastname": "Beknazarov", "category": "IT"},
    "nilufar": {"password": "12345", "firstname": "Nilufar", "lastname": "Karimova", "category": "Finance"},
    "asadbek": {"password": "asdf", "firstname": "Asadbek", "lastname": "Rasulov", "category": "Manager"},
    "dilnoza": {"password": "xyz", "firstname": "Dilnoza", "lastname": "Islomova", "category": "HR"},
    "temurbek": {"password": "temur123", "firstname": "Temurbek", "lastname": "Xolmatov", "category": "Support"},
    "aziza": {"password": "aziza12", "firstname": "Aziza", "lastname": "G‘aniyeva", "category": "Developer"},
    "olim": {"password": "olim999", "firstname": "Olim", "lastname": "Murodov", "category": "Logistics"}
}

def check_user(username, password):
    user = users.get(username)
    if user and user["password"] == password:
        return user["firstname"], user["lastname"], user["category"]
    return None

# Streamlit login panel
st.title("Login")

login = st.text_input("Login")
password = st.text_input("Parol", type="password")

if st.button("Kirish"):
    result = check_user(login, password)
    if result:
        firstname, lastname, category = result
        st.success(f"Xush kelibsiz, {firstname} {lastname}!\nKategoriya: {category}")
    else:
        st.error("Login yoki parol noto‘g‘ri.")

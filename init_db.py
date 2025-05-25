import sqlite3
import os

# Fayl nomini aniqlaymiz
DB_PATH = "users.db"

def init_db():
    # Agar bazaviy fayl mavjud bo‘lsa, o‘chiramiz (yangi baza yaratish uchun)
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Jadval yaratish
    c.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        firstname TEXT,
        lastname TEXT,
        category TEXT
    )
    ''')

    # Foydalanuvchilar ro'yxati
    users = [
        ("testuser", "1234", "Ali", "Valiyev", "Admin"),
        ("johndoe", "abcd", "John", "Doe", "Staff"),
        ("janedoe", "pass", "Jane", "Doe", "HR"),
        ("anvarbek", "qwerty", "Anvar", "Beknazarov", "IT"),
        ("nilufar", "12345", "Nilufar", "Karimova", "Finance"),
        ("asadbek", "asdf", "Asadbek", "Rasulov", "Manager"),
        ("dilnoza", "xyz", "Dilnoza", "Islomova", "HR"),
        ("temurbek", "temur123", "Temurbek", "Xolmatov", "Support"),
        ("aziza", "aziza12", "Aziza", "G‘aniyeva", "Developer"),
        ("olim", "olim999", "Olim", "Murodov", "Logistics")
    ]

    # Ma'lumotlarni qo'shamiz
    for user in users:
        c.execute(
            "INSERT INTO users (username, password, firstname, lastname, category) VALUES (?, ?, ?, ?, ?)",
            user
        )

    conn.commit()
    conn.close()
    print("✅ Foydalanuvchilar bazasi muvaffaqiyatli yaratildi!")

# Fayl bevosita ishga tushirilsa
if __name__ == "__main__":
    init_db()

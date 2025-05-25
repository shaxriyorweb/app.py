import sqlite3
import os

DB_PATH = "users.db"

def init_db():
    # Fayl mavjud bo‘lsa, o‘chirib yangi baza yaratamiz
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Jadval yaratish (category ustuni bilan)
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

    # 10 ta xodim qo‘shish
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

    for user in users:
        c.execute(
            "INSERT INTO users (username, password, firstname, lastname, category) VALUES (?, ?, ?, ?, ?)",
            user
        )

    conn.commit()
    conn.close()
    print("✅ Foydalanuvchilar bazasi muvaffaqiyatli yaratildi!")

# To‘g‘ridan-to‘g‘ri ishga tushganda bajariladi
if __name__ == "__main__":
    init_db()

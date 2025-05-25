import sqlite3

# Bazani ulaymiz
conn = sqlite3.connect('users.db')
c = conn.cursor()

# Jadvalni yaratamiz (agar mavjud bo'lmasa)
c.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT,
    firstname TEXT,
    lastname TEXT
)
''')

# Foydalanuvchilar ro'yxati (10 ta xodim)
users = [
    ("testuser", "1234", "Ali", "Valiyev"),
    ("johndoe", "abcd", "John", "Doe"),
    ("janedoe", "pass", "Jane", "Doe"),
    ("anvarbek", "qwerty", "Anvar", "Beknazarov"),
    ("nilufar", "12345", "Nilufar", "Karimova"),
    ("asadbek", "asdf", "Asadbek", "Rasulov"),
    ("dilnoza", "xyz", "Dilnoza", "Islomova"),
    ("temurbek", "temur123", "Temurbek", "Xolmatov"),
    ("aziza", "aziza12", "Aziza", "G‘aniyeva"),
    ("olim", "olim999", "Olim", "Murodov")
]

# Har bir foydalanuvchini qo‘shamiz (agar mavjud bo‘lmasa)
for user in users:
    try:
        c.execute("INSERT INTO users (username, password, firstname, lastname) VALUES (?, ?, ?, ?)", user)
    except sqlite3.IntegrityError:
        pass  # allaqachon mavjud foydalanuvchi

# O‘zgarishlarni saqlaymiz
conn.commit()
conn.close()

print("✅ Baza yaratildi va 10 ta xodim qo‘shildi.")

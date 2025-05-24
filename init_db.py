import sqlite3

def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    # users jadvalini yaratamiz
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL
        )
    ''')
    # Test foydalanuvchi qo'shamiz (login=user1, parol=12345)
    c.execute('''
        INSERT OR IGNORE INTO users (username, password, first_name, last_name)
        VALUES (?, ?, ?, ?)
    ''', ('user1', '12345', 'Ali', 'Valiyev'))
    conn.commit()
    conn.close()
    print("Bazani yaratish va test foydalanuvchi qo'shish tugadi.")

if __name__ == "__main__":
    init_db()

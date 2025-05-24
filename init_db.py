import sqlite3

conn = sqlite3.connect('users.db')
c = conn.cursor()

# Foydalanuvchilar jadvali
c.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT,
    firstname TEXT,
    lastname TEXT
)
''')

# Misol foydalanuvchi
c.execute("INSERT INTO users (username, password, firstname, lastname) VALUES (?, ?, ?, ?)",
          ('testuser', '1234', 'Ali', 'Valiyev'))

conn.commit()
conn.close()

print("✅ Foydalanuvchilar bazasi yaratildi.")

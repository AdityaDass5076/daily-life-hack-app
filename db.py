import sqlite3

def init_db():
    conn = sqlite3.connect('lifehacks.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS hacks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT,
            tip TEXT,
            date TEXT,
            lang TEXT
        )
    ''')
    conn.commit()
    conn.close()

def insert_hack(user, tip, date, lang):
    conn = sqlite3.connect('lifehacks.db')
    c = conn.cursor()
    c.execute('INSERT INTO hacks (user, tip, date, lang) VALUES (?, ?, ?, ?)', 
              (user, tip, date, lang))
    conn.commit()
    conn.close()

def get_hacks():
    conn = sqlite3.connect('lifehacks.db')
    c = conn.cursor()
    c.execute('SELECT * FROM hacks ORDER BY id DESC')
    hacks = c.fetchall()
    conn.close()
    return hacks

def search_hacks(keyword):
    conn = sqlite3.connect('lifehacks.db')
    c = conn.cursor()
    c.execute('SELECT * FROM hacks WHERE tip LIKE ?', (f'%{keyword}%',))
    hacks = c.fetchall()
    conn.close()
    return hacks

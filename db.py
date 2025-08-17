import sqlite3

# Initialize DB and create tables if not exist
def init_db():
    conn = sqlite3.connect("life_hacks.db", check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS hacks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT,
            tip TEXT NOT NULL,
            date TEXT,
            language TEXT,
            category TEXT,
            image_url TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS translations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            hack_id INTEGER NOT NULL,
            target_lang TEXT NOT NULL,
            translated_text TEXT NOT NULL,
            UNIQUE(hack_id, target_lang),
            FOREIGN KEY (hack_id) REFERENCES hacks(id) ON DELETE CASCADE
        )
    """)
    conn.commit()
    return conn, cursor

conn, cursor = init_db()

# Insert a new hack
def insert_hack(user, tip, date, language, category, image_url):
    cursor.execute("""
        INSERT INTO hacks (user, tip, date, language, category, image_url)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (user, tip, date, language, category, image_url))
    conn.commit()

# Search hacks by keyword in tip (case insensitive)
def search_hacks(query):
    like_query = f"%{query.lower()}%"
    cursor.execute("""
        SELECT id, user, tip, date, language, category, NULL as upvotes, image_url 
        FROM hacks WHERE LOWER(tip) LIKE ?
        ORDER BY date DESC
    """, (like_query,))
    return cursor.fetchall()

# Get hacks by category (if 'All' then get all)
def get_hacks_by_category(category):
    if category == "All":
        cursor.execute("""
            SELECT id, user, tip, date, language, category, NULL as upvotes, image_url 
            FROM hacks
            ORDER BY date DESC
        """)
    else:
        cursor.execute("""
            SELECT id, user, tip, date, language, category, NULL as upvotes, image_url 
            FROM hacks WHERE category=?
            ORDER BY date DESC
        """, (category,))
    return cursor.fetchall()

# Insert or update a translation for a hack
def insert_translation(hack_id, target_lang, translated_text):
    cursor.execute("""
        INSERT OR REPLACE INTO translations (hack_id, target_lang, translated_text)
        VALUES (?, ?, ?)
    """, (hack_id, target_lang, translated_text))
    conn.commit()

# Get cached translation if exists
def get_translation(hack_id, target_lang):
    cursor.execute("""
        SELECT translated_text FROM translations WHERE hack_id=? AND target_lang=?
    """, (hack_id, target_lang))
    row = cursor.fetchone()
    if row:
        return row[0]
    return None

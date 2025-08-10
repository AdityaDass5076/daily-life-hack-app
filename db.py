import sqlite3
from datetime import datetime

DB_NAME = "lifehacks.db"

def init_db():
    """
    Create the hacks table if it does not exist.
    Added: upvotes (int), image_url (text).
    """
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS hacks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT NOT NULL,
            tip TEXT NOT NULL,
            date TEXT NOT NULL,
            language TEXT,
            category TEXT,
            upvotes INTEGER DEFAULT 0,
            image_url TEXT
        )
        """
    )
    conn.commit()
    cur.close()
    conn.close()

def add_missing_columns():
    """
    Add missing columns to hacks table without losing data.
    """
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("PRAGMA table_info(hacks)")
    columns = [col[1] for col in cur.fetchall()]

    alter_statements = []
    if "language" not in columns:
        alter_statements.append("ALTER TABLE hacks ADD COLUMN language TEXT")
    if "category" not in columns:
        alter_statements.append("ALTER TABLE hacks ADD COLUMN category TEXT")
    if "upvotes" not in columns:
        alter_statements.append("ALTER TABLE hacks ADD COLUMN upvotes INTEGER DEFAULT 0")
    if "image_url" not in columns:
        alter_statements.append("ALTER TABLE hacks ADD COLUMN image_url TEXT")

    for stmt in alter_statements:
        cur.execute(stmt)
        conn.commit()

    cur.close()
    conn.close()

# Init and ensure schema is updated
init_db()
add_missing_columns()

def insert_hack(user, tip, date=None, language=None, category=None, image_url=None):
    """
    Insert a new hack into the database.
    """
    if not date:
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO hacks (user, tip, date, language, category, upvotes, image_url)
        VALUES (?, ?, ?, ?, ?, 0, ?)
        """,
        (user, tip, date, language, category, image_url),
    )
    conn.commit()
    cur.close()
    conn.close()

def get_hacks():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute(
        "SELECT id, user, tip, date, language, category, upvotes, image_url FROM hacks ORDER BY date DESC"
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

def search_hacks(keyword):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    pattern = f"%{keyword}%"
    cur.execute(
        "SELECT id, user, tip, date, language, category, upvotes, image_url FROM hacks WHERE tip LIKE ? ORDER BY date DESC",
        (pattern,),
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

def get_hacks_by_category(category):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    if category.lower() == "all":
        cur.execute("SELECT id, user, tip, date, language, category, upvotes, image_url FROM hacks ORDER BY date DESC")
    else:
        cur.execute("SELECT id, user, tip, date, language, category, upvotes, image_url FROM hacks WHERE category=? ORDER BY date DESC", (category,))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

def get_hack_by_id(hack_id):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT id, user, tip, date, language, category, upvotes, image_url FROM hacks WHERE id=?", (hack_id,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    return row

def upvote_hack(hack_id):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("UPDATE hacks SET upvotes = upvotes + 1 WHERE id=?", (hack_id,))
    conn.commit()
    cur.close()
    conn.close()

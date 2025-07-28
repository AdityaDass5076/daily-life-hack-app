import sqlite3

DB_NAME = "lifehacks.db"

def init_db():
    """
    Create the hacks table if it does not exist.
    The table has these columns:
    - id (primary key)
    - user (text)
    - tip (text)
    - date (text)
    - language (text)
    - category (text)
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
            category TEXT
        )
        """
    )
    conn.commit()
    cur.close()
    conn.close()

def add_missing_columns():
    """
    Check existing columns in 'hacks' table and add missing ones.
    Specifically checks for 'language' and 'category'.
    Run this once at app start to keep schema up to date.
    """
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    try:
        cur.execute("PRAGMA table_info(hacks)")
        columns = [col_info[1] for col_info in cur.fetchall()]  # list of column names
        # Add missing 'language' column if necessary
        if "language" not in columns:
            cur.execute("ALTER TABLE hacks ADD COLUMN language TEXT")
            conn.commit()
        # Add missing 'category' column if necessary
        if "category" not in columns:
            cur.execute("ALTER TABLE hacks ADD COLUMN category TEXT")
            conn.commit()
    except sqlite3.OperationalError as e:
        print("Error updating schema:", e)
    finally:
        cur.close()
        conn.close()

# Call these two functions at the module load or app start
init_db()
add_missing_columns()

def insert_hack(user, tip, date, language, category):
    """
    Insert a new hack into the database.
    """
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO hacks (user, tip, date, language, category)
        VALUES (?, ?, ?, ?, ?)
        """,
        (user, tip, date, language, category),
    )
    conn.commit()
    cur.close()
    conn.close()

def get_hacks():
    """
    Retrieve all hacks ordered by date descending.
    """
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute(
        """
        SELECT id, user, tip, date, language, category
        FROM hacks
        ORDER BY date DESC
        """
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

def search_hacks(keyword):
    """
    Search hacks by keyword in tip (case-insensitive).
    """
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    search_pattern = f"%{keyword}%"
    cur.execute(
        """
        SELECT id, user, tip, date, language, category
        FROM hacks
        WHERE tip LIKE ?
        ORDER BY date DESC
        """,
        (search_pattern,),
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

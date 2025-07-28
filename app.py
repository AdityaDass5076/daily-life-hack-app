import streamlit as st
from datetime import datetime
from db import init_db, insert_hack

# Initialize the database (creates table on first run)
init_db()

st.title("🛠️ Daily Life Hack Exchange")

# Define your hack categories
CATEGORIES = ["Kitchen", "Study", "Productivity", "Health", "Money", "Travel", "Other"]

# Section to submit a new life hack
with st.expander("Share a Life Hack"):
    user = st.text_input("Your Name (optional)").strip() or "Anonymous"
    tip = st.text_area("Your life hack (max 240 chars)", max_chars=240)
    lang = st.text_input("Language (e.g., Hindi, Telugu, English)")
    category = st.selectbox("Choose a category for your hack:", CATEGORIES)

    if st.button("Submit"):
        if tip.strip() == "":
            st.error("Please enter a valid life hack.")
        else:
            insert_hack(user, tip, datetime.now().strftime("%Y-%m-%d"), lang, category)
            st.success(f"Thank you! Your life hack has been submitted under category '{category}'.")

# Section to search and browse hacks

# Input for keyword search
search = st.text_input("Search for hacks by keyword")

# Function to get distinct categories from DB dynamically
def get_categories():
    import sqlite3
    conn = sqlite3.connect("lifehacks.db")
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT category FROM hacks WHERE category IS NOT NULL AND category != ''")
    categories = [row[0] for row in cur.fetchall()]
    cur.close()
    conn.close()
    return categories

# Fetch categories for filter dropdown (including "All" option)
categories = get_categories()
selected_category = st.selectbox("Filter by category:", ["All"] + categories)

# Function to fetch hacks filtered by search text and category
def fetch_hacks_by_search_and_category(search_text, category_filter):
    import sqlite3
    conn = sqlite3.connect("lifehacks.db")
    cur = conn.cursor()

    query = "SELECT id, user, tip, date, language, category FROM hacks WHERE 1=1"
    params = []

    if search_text and search_text.strip():
        query += " AND tip LIKE ?"
        params.append(f"%{search_text}%")

    if category_filter and category_filter != "All":
        query += " AND category = ?"
        params.append(category_filter)

    query += " ORDER BY date DESC"
    cur.execute(query, params)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

# Get the hacks based on current filters
hacks = fetch_hacks_by_search_and_category(search, selected_category)

st.subheader("Life Hacks")

if hacks:
    for hack in hacks:
        # hack tuple indices:
        # 0=id, 1=user, 2=tip, 3=date, 4=language, 5=category
        st.write(f"- {hack[2]}  \n*Category: {hack[5]}, Language: {hack[4]}, By {hack[1]}, on {hack[3]}*")
else:
    st.write("No life hacks found.")

st.caption("Share your daily life wisdom. Supports all Indian languages. Works on slow internet!")

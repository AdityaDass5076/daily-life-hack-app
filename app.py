import streamlit as st
from datetime import datetime
import db  # Uses your improved db.py

st.set_page_config(page_title="Life Hacks Hub", page_icon="💡", layout="wide")

# === Custom CSS for Modern UI ===
st.markdown("""
<style>
body {background-color: #f0f4f8;}
header {background-color: #4a90e2; color: white; padding: 1rem; text-align: center; font-size: 2rem; font-weight: bold; border-radius: 0 0 15px 15px;}
.card {background: white; padding: 1.2rem; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.07); margin-bottom: 1.5rem;}
.card:hover {transform: translateY(-5px); box-shadow: 0 8px 20px rgba(0, 0, 0, 0.12);}
.category {background-color: #50e3c2; color: white; padding: 4px 10px; border-radius: 20px; font-size: 13px; display: inline-block; margin-right: 10px;}
.upvote-btn {background-color: #e94e77; color: white; padding: 6px 18px; border-radius: 30px; cursor: pointer; border: none; font-size: 1rem;}
.upvote-btn:hover {background-color: #c8365e;}
</style>
""", unsafe_allow_html=True)

# === App Header ===
st.markdown("<header>💡 Life Hacks Hub</header>", unsafe_allow_html=True)
st.markdown("Welcome! Discover and share creative life hacks every day.")

# ---- Search and Category Filter ----
categories = ["All", "Productivity", "Cooking", "Home", "Work", "Health", "Study", "Kitchen", "Money", "Travel", "Other"]
search_query = st.text_input("🔍 Search hacks by keyword...")
cat_col, search_col = st.columns([2, 3])
with cat_col:
    selected_category = st.selectbox("📂 Filter by Category", categories)

# ---- Fetch Hacks from DB ----
if search_query:
    hacks_data = db.search_hacks(search_query)
else:
    hacks_data = db.get_hacks_by_category(selected_category)

# ---- Show All Hacks ----
st.subheader("🛠️ Life Hacks")
if hacks_data:
    for hack in hacks_data:
        hack_id, user, tip, date, language, category, upvotes, image_url = hack
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown(f"**{tip}**")
        tag_str = f"<span class='category'>{category if category else 'Other'}</span>"
        st.markdown(tag_str, unsafe_allow_html=True)
        if image_url:
            st.image(image_url, use_column_width=True)
        st.write(f"👤 By {user} | 🕒 {date} | 🌐 {language if language else 'Any Language'}")
        col1, col2 = st.columns([10, 1])
        with col1:
            st.write("")
        with col2:
            if st.button(f"⬆️ {upvotes}", key=f"upvote_{hack_id}"):
                db.upvote_hack(hack_id)
                st.experimental_rerun()
        st.markdown("</div>", unsafe_allow_html=True)
else:
    st.info("No life hacks found for your selection.")

# ---- Submission Form ----
st.markdown("---")
with st.expander("➕ Share a New Life Hack"):
    st.markdown("Help others and get karma! Any tip or clever hack that improves everyday life.")
    with st.form("submit_form"):
        user = st.text_input("👤 Your Name (optional)").strip() or "Anonymous"
        tip = st.text_area("💡 Your Life Hack (max 240 chars)", max_chars=240)
        category = st.selectbox("📂 Category", categories[1:])
        language = st.text_input("🌐 Language (optional)")
        image_url = st.text_input("🖼️ Image URL (optional, direct link to image)")
        submitted = st.form_submit_button("Submit Hack")
        if submitted:
            if tip.strip():
                db.insert_hack(user, tip, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), language, category, image_url)
                st.success(f"🎉 Thank you! Your hack is up for everyone!")
                st.experimental_rerun()
            else:
                st.error("Please enter a valid life hack (description required).")

st.caption("Share your daily life wisdom. All Indian languages welcome. Works even on slow internet! 🚀")

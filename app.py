import streamlit as st
from datetime import datetime
import db  # Your improved db.py with required functions

# ================== APP CONFIG ================== #
st.set_page_config(
    page_title="Jugaadify - The Smart Way",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ================= THEME TOGGLE =================== #
if "theme" not in st.session_state:
    st.session_state.theme = "light"

def toggle_theme():
    st.session_state.theme = "dark" if st.session_state.theme == "light" else "light"

st.button(
    "🌙 Dark Mode" if st.session_state.theme == "light" else "☀️ Light Mode",
    on_click=toggle_theme,
)

# ================= LIGHT THEME ================== #
light_theme = """
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #fdfbfb, #ebedee, #dde7ff, #fef9d7);
    font-family: 'Trebuchet MS', sans-serif;
    font-size: 20px;
    color: #1a1a1a;
    font-weight: 700;
}
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #ececff, #f9f9ff);
    border-right: 2px solid black;
    color: black;
    font-weight: 700;
    font-size: 18px;
    padding-top: 0.5rem;
}
header {
    background: linear-gradient(90deg, #6a5acd, #7b68ee, #9370db);
    color: white;
    padding: 1.3rem;
    text-align: center;
    font-size: 3rem;
    font-weight: 900;
    border-radius: 15px;
    border: 3px solid black;
    margin-bottom: 1.5rem;
}
.card {
    background: rgba(255,255,255,0.9);
    padding: 1.5rem;
    border-radius: 18px;
    box-shadow: 0 6px 18px rgba(0,0,0,0.2);
    margin-bottom: 1.5rem;
    border: 2px solid black;
    font-size: 18px;
}
button[kind="primary"] {
    font-size: 20px !important;
    font-weight: 700 !important;
    padding: 12px 22px !important;
    border-radius: 12px !important;
    cursor: pointer;
}
.category {
    background: #6a5acd;
    color: white;
    font-weight: 800;
    padding: 6px 16px;
    border-radius: 30px;
    font-size: 17px;
    margin-right: 10px;
    text-transform: uppercase;
    user-select: none;
}
.stTextInput>div>div>input,
.stTextArea>div>textarea,
.stSelectbox>div>div>div {
    font-size: 18px !important;
    font-weight: 700 !important;
    padding: 6px;
}
h2, h3 {
    font-weight: 900;
}
</style>
"""

# ================= DARK THEME ==================== #
dark_theme = """
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(160deg, #000000, #0d0d0d, #1a1a1a);
    font-family: 'Trebuchet MS', sans-serif;
    font-size: 20px;
    color: #ffffff;
    font-weight: 700;
}
[data-testid="stSidebar"] {
    background: #000000;
    border-right: 2px solid #444;
    color: #ffffff;
    font-weight: 700;
    font-size: 18px;
    padding-top: 0.5rem;
}
header {
    background: linear-gradient(90deg, #ff385c, #ff007a, #ff4d4d);
    color: white;
    padding: 1.3rem;
    text-align: center;
    font-size: 3rem;
    font-weight: 900;
    border-radius: 15px;
    border: 3px solid white;
    margin-bottom: 1.5rem;
    text-shadow: 1px 1px 3px black;
}
.card {
    background: #121212;
    padding: 1.5rem;
    border-radius: 18px;
    box-shadow: 0 6px 20px rgba(255,255,255,0.1);
    margin-bottom: 1.5rem;
    border: 2px solid #fff;
    color: #ffffff;
    font-weight: 700;
    font-size: 18px;
}
button[kind="primary"] {
    font-size: 20px !important;
    font-weight: 700 !important;
    padding: 12px 22px !important;
    border-radius: 12px !important;
    cursor: pointer;
}
.category {
    background: #ffcc00;
    color: black;
    font-weight: 900;
    padding: 6px 16px;
    border-radius: 30px;
    font-size: 17px;
    margin-right: 10px;
    text-transform: uppercase;
    user-select: none;
}
.stTextInput>div>div>input,
.stTextArea>div>textarea,
.stSelectbox>div>div>div {
    background-color: #1e1e1e !important;
    color: #ffffff !important;
    border: 2px solid #555 !important;
    border-radius: 8px;
    font-size: 18px !important;
    font-weight: 700 !important;
    padding: 6px;
}
label, .st.markdown, .stRadio > label, .stSelectbox > label {
    color: #ffffff !important;
    font-weight: 700;
}
h2, h3 {
    font-weight: 900;
}
</style>
"""

# ================== APPLY THEME ================== #
st.markdown(light_theme if st.session_state.theme == "light" else dark_theme, unsafe_allow_html=True)

# ================= HEADER ================== #
st.markdown("<header>⚡ Jugaadify - The Smart Way</header>", unsafe_allow_html=True)
st.markdown("🚀 Explore, share, and upvote the smartest hacks for everyday life!")

# ====================== TABS ===================== #
tab_explore, tab_submit, tab_categories = st.tabs(
    ["🔍 Explore Hacks", "➕ Submit Hack", "📂 Categories"]
)

# ================= CATEGORIES INCLUDING SELCARE ================== #
categories = [
    "All", "Productivity", "Cooking", "Home", "Work",
    "Health", "Study", "Kitchen", "Money", "Travel",
    "Selfcare", "Other"
]

# ================= SIDEBAR CATEGORY FILTER ================= #
with st.sidebar:
    st.markdown("### 📂 Quick Category Filter")
    selected_category_sidebar = st.radio("Select category:", categories)

# ------------------- EXPLORE HACKS TAB ------------------- #
with tab_explore:
    search_query = st.text_input("🔍 Search hacks by keyword...", placeholder="Type keyword here...")

    if search_query:
        hacks = db.search_hacks(search_query)
    else:
        hacks = db.get_hacks_by_category(selected_category_sidebar)

    st.markdown("## 🛠️ Smart Life Hacks")
    if hacks:
        for hack in hacks:
            hack_id, user, tip, date, language, category, upvotes, image_url = hack

            # Card container
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown(f"✨ **{tip}**")
            st.markdown(f"<span class='category'>{category if category else 'Other'}</span>", unsafe_allow_html=True)

            if image_url:
                st.image(image_url, use_column_width=True)

            # View details button for user info
            if st.button(f"View Details", key=f"details_{hack_id}"):
                st.info(
                    f"👤 Submitted by: {user}\n\n🕒 Date: {date}\n\n🌐 Language: {language if language else 'Any Language'}"
                )

            st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.info("😕 No life hacks found for your selection.")

# ------------------- SUBMIT HACK TAB ------------------- #
with tab_submit:
    st.markdown("## 💡 Share your best life hack! (Supports Hindi, Telugu, English, and more)")
    with st.form("submit_form"):
        user = st.text_input("👤 Your Name (optional)").strip() or "Anonymous"
        tip = st.text_area(
            "💡 Your Life Hack (max 240 characters)",
            max_chars=240,
            placeholder="Type your smart hack here...",
        )
        category = st.selectbox("📂 Category", categories[1:])  # exclude "All"
        language = st.text_input("🌐 Language (optional)", placeholder="e.g. Hindi, English, Telugu...")
        image_url = st.text_input("🖼️ Image URL (optional, direct image link)")

        submitted = st.form_submit_button("🚀 Submit Hack")

        if submitted:
            if tip.strip():
                db.insert_hack(
                    user,
                    tip,
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    language,
                    category,
                    image_url,
                )
                st.success(f"🎉 Thanks {user}! Your hack is now live on Jugaadify ⚡")
            else:
                st.error("⚠️ Please enter a valid life hack description.")

# ------------------- CATEGORIES TAB ------------------- #
with tab_categories:
    st.markdown("## 📂 Categories Overview")
    for cat in categories:
        st.button(f"📌 {cat}", key=f"cat_{cat}")

# ================ Footer Caption ================ #
st.caption("⚡ Jugaadify - Smart hacks for a smart life | Made aesthetic for Gen-Z 💜")

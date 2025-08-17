import streamlit as st
from datetime import datetime
from translate import Translator
import db  # Your improved db.py with required functions

# == APP CONFIG == #
st.set_page_config(
    page_title="Jugaadify - The Smart Way",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# = THEME TOGGLE === #
if "theme" not in st.session_state:
    st.session_state.theme = "light"

# Track selected category in Categories tab
if "selected_category_in_cat_tab" not in st.session_state:
    st.session_state.selected_category_in_cat_tab = None

def toggle_theme():
    st.session_state.theme = "dark" if st.session_state.theme == "light" else "light"

def select_category(category):
    st.session_state.selected_category_in_cat_tab = category

st.button(
    "🌙 Dark Mode" if st.session_state.theme == "light" else "☀️ Light Mode",
    on_click=toggle_theme,
)

# == THEMES WITH BORDER STYLE ADDED ==
light_theme = """
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #fdfbfb, #ebedee, #dde7ff, #fef9d7);
    font-family: 'Trebuchet MS', sans-serif;
    font-size: 20px;
    color: #1a1a1a;
    font-weight: 700;
    border: 5px solid black;
    border-radius: 15px;
    margin: 10px;
    padding: 15px;
}
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #ececff, #f9f9ff);
    border: 5px solid black;
    border-radius: 15px;
    padding-top: 0.5rem;
    margin: 10px 10px 10px 10px;
}
/* Remove only the unwanted white box above theme toggle */
[data-testid="stSidebar"] > div > div > div > div:first-child > div:first-child {
    display: none;
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
    margin-bottom: 1rem;
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
    font-size: 20px;
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
    margin-bottom: 0.5rem;
}
/* Ensure button text visible in light theme */
.stButton>button, button[kind="primary"] {
    color: #1a1a1a !important;
    font-weight: 700 !important;
}
</style>
"""

dark_theme = """
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(160deg, #000000, #0d0d0d, #1a1a1a);
    font-family: 'Trebuchet MS', sans-serif;
    font-size: 20px;
    color: #ffffff;
    font-weight: 700;
    border: 5px solid white;
    border-radius: 15px;
    margin: 10px;
    padding: 15px;
}
[data-testid="stSidebar"] {
    background: #000000;
    border: 5px solid white;
    border-radius: 15px;
    padding-top: 0.5rem;
    margin: 10px 10px 10px 10px;
}
/* Remove only the unwanted white box above theme toggle */
[data-testid="stSidebar"] > div > div > div > div:first-child > div:first-child {
    display: none;
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
    margin-bottom: 1rem;
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
    margin-bottom: 0.5rem;
}
/* Make button text fully white by default */
.stButton>button, button[kind="primary"] {
    color: #fff !important;
    font-weight: 700 !important;
    transition: color 0.3s ease;
}
/* On hover, highlight with color */
.stButton>button:hover, button[kind="primary"]:hover {
    color: #ffcc00 !important;
}
/* Make pinned categories button text black and visible */
.stSidebar button[key^="cat_"] {
    color: black !important;
    font-weight: 900 !important;
    font-size: 17px;
    text-transform: uppercase;
    margin-bottom: 6px;
    background-color: transparent !important;
    border: none !important;
    cursor: pointer;
    transition: color 0.3s ease;
}
.stSidebar button[key^="cat_"]:hover {
    color: #ffcc00 !important;
}
/* Make category filter radio labels white */
.stRadio > label {
    color: white !important;
    font-weight: 700;
}
/* View Details button text white */
button[key^="details_"] {
    color: white !important;
    font-weight: 700 !important;
}
button[key^="details_"]:hover {
    color: #ffcc00 !important;
}
</style>
"""

# == APPLY THEME == #
st.markdown(light_theme if st.session_state.theme == "light" else dark_theme, unsafe_allow_html=True)

# = HEADER == #
st.markdown("<header>⚡ Jugaadify - The Smart Way</header>", unsafe_allow_html=True)
st.markdown("🚀 Explore and share the smartest hacks for everyday life!")

# == TABS === #
tab_explore, tab_submit, tab_categories = st.tabs(
    ["🔍 Explore Hacks", "➕ Submit Hack", "📂 Categories"]
)

# = CATEGORIES INCLUDING SELCARE == #
categories = [
    "All", "Productivity", "Cooking", "Home", "Work",
    "Health", "Study", "Kitchen", "Money", "Travel",
    "Selfcare", "Other"
]

# State variable for category selected in Categories tab
if "selected_category_in_cat_tab" not in st.session_state:
    st.session_state.selected_category_in_cat_tab = None

def select_category(category):
    st.session_state.selected_category_in_cat_tab = category

# = SIDEBAR CATEGORY FILTER = #
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
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown(f"✨ **{tip}**")
            st.markdown(f"<span class='category'>{category if category else 'Other'}</span>", unsafe_allow_html=True)
            if image_url:
                st.image(image_url, use_column_width=True)
            with st.expander("🌐 Translate this hack"):
                target_lang = st.selectbox(
                    "Translate To:",
                    options=["", "hi", "en", "te"],
                    format_func=lambda x: {"": "Select language", "hi":"Hindi", "en":"English", "te":"Telugu"}[x],
                    key=f"translate_select_{hack_id}"
                )
                if st.button("Translate", key=f"translate_btn_{hack_id}"):
                    if target_lang == "" or target_lang == language:
                        st.warning("Please select a different target language to translate to.")
                    else:
                        try:
                            translator = Translator(to_lang=target_lang)
                            translated_text = translator.translate(tip)
                            db.insert_translation(hack_id, target_lang, translated_text)
                            st.success(f"Translation ({target_lang}):")
                            st.write(translated_text)
                        except Exception as e:
                            st.error(f"Translation error: {e}")
            if st.button(f"View Details", key=f"details_{hack_id}"):
                st.info(
                    f"👤 Submitted by: {user}\n\n🕒 Date: {date}\n\n🌐 Language: {language if language else 'Any Language'}"
                )
            st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.info("😕 No life hacks found for your selection.")

# ------------------- SUBMIT HACK TAB ------------------- #
with tab_submit:
    st.markdown("## 💡 Share your best life hack! Your Desi Jugaad! ")
    with st.form("submit_form"):
        user = st.text_input("👤 Your Name (optional)").strip() or "Anonymous"
        tip = st.text_area(
            "💡 Your Life Hack (max 240 characters)",
            max_chars=240,
            placeholder="Type your smart hack here...",
        )
        category = st.selectbox("📂 Category", categories[1:])  # exclude "All"
        language = st.selectbox(
            "🌐 Language (optional)",
            options=["", "Hindi", "English", "Telugu", "Other"],
            help="Select language of your hack"
        )
        lang_map = {"Hindi": "hi", "English": "en", "Telugu": "te", "Other": ""}
        lang_code = lang_map.get(language, "")
        image_url = st.text_input("🖼️ Image URL (optional, direct image link)")
        submitted = st.form_submit_button("🚀 Submit Hack")
        if submitted:
            if tip.strip():
                db.insert_hack(
                    user,
                    tip,
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    lang_code,
                    category,
                    image_url,
                )
                st.success(f"🎉 Thanks {user}! Your hack is now live on Jugaadify ⚡")
            else:
                st.error("⚠️ Please enter a valid life hack description.")

# ------------------- CATEGORIES TAB ------------------- #
with tab_categories:
    st.markdown("## 📂 Categories Overview")
    cols = st.columns(4)
    for i, cat in enumerate(categories):
        if cols[i % 4].button(f"📌 {cat}", key=f"cat_{cat}"):
            select_category(cat)
    # Show hacks for selected category button
    if st.session_state.selected_category_in_cat_tab:
        sel_cat = st.session_state.selected_category_in_cat_tab
        st.markdown(f"### Hacks in category: **{sel_cat}**")
        if sel_cat == "All":
            hacks = db.get_hacks_by_category("All")
        else:
            hacks = db.get_hacks_by_category(sel_cat)
        if hacks:
            for hack in hacks:
                hack_id, user, tip, date, language, category, upvotes, image_url = hack
                st.markdown("<div class='card'>", unsafe_allow_html=True)
                st.markdown(f"✨ **{tip}**")
                st.markdown(f"<span class='category'>{category if category else 'Other'}</span>", unsafe_allow_html=True)
                if image_url:
                    st.image(image_url, use_column_width=True)
                with st.expander("🌐 Translate this hack"):
                    target_lang = st.selectbox(
                        "Translate To:",
                        options=["", "hi", "en", "te"],
                        format_func=lambda x: {"": "Select language", "hi":"Hindi", "en":"English", "te":"Telugu"}[x],
                        key=f"translate_select_cat_{hack_id}"
                    )
                    if st.button("Translate", key=f"translate_btn_cat_{hack_id}"):
                        if target_lang == "" or target_lang == language:
                            st.warning("Please select a different target language to translate to.")
                        else:
                            try:
                                translator = Translator(to_lang=target_lang)
                                translated_text = translator.translate(tip)
                                db.insert_translation(hack_id, target_lang, translated_text)
                                st.success(f"Translation ({target_lang}):")
                                st.write(translated_text)
                            except Exception as e:
                                st.error(f"Translation error: {e}")
                if st.button(f"View Details", key=f"details_cat_{hack_id}"):
                    st.info(
                        f"👤 Submitted by: {user}\n\n🕒 Date: {date}\n\n🌐 Language: {language if language else 'Any Language'}"
                    )
                st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.info("😕 No life hacks found for this category.")

# == Footer Caption == #
st.caption("⚡ Jugaadify - Smart hacks for a smart life | Find all your Jugaads in one place ")

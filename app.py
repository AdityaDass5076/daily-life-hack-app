import streamlit as st
from datetime import datetime
from db import init_db, insert_hack, get_hacks, search_hacks

# Initialize the database (creates table on first run)
init_db()

st.title("🛠️ Daily Life Hack Exchange")

# Section to submit a new life hack
with st.expander("Share a Life Hack"):
    user = st.text_input("Your Name (optional)").strip() or "Anonymous"
    tip = st.text_area("Your life hack (max 240 chars)", max_chars=240)
    lang = st.text_input("Language (e.g., Hindi, Telugu, English)")
    
    if st.button("Submit"):
        if tip.strip() == "":
            st.error("Please enter a valid life hack.")
        else:
            insert_hack(user, tip, datetime.now().strftime("%Y-%m-%d"), lang)
            st.success("Thank you! Your life hack has been submitted.")

# Section to search and browse hacks
search = st.text_input("Search for hacks by keyword")

if search:
    hacks = search_hacks(search)
else:
    hacks = get_hacks()

st.subheader("Life Hacks")
if hacks:
    for hack in hacks:
        # hack indices: 0=id,1=user,2=tip,3=date,4=lang
        st.write(f"- {hack[2]}  \n*Language: {hack[4]}, By {hack[1]}, on {hack[3]}*")
else:
    st.write("No life hacks found.")

st.caption("Share your daily life wisdom. Supports all Indian languages. Works on slow internet!")

import streamlit as st
import pandas as pd
from textblob import TextBlob
import os
import csv  # Moved here
# Create folders if not exist
os.makedirs("data", exist_ok=True)

st.set_page_config(page_title="Mood Predictor App", layout="centered")

# Initialize session state
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'User Info'

# Sidebar Navigation (locked step-by-step)
st.sidebar.title("🧭 Navigation")

pages = ["User Info", "Dashboard", "Suggestions", "Feedback"]
current_idx = pages.index(st.session_state.current_page)

for i, page in enumerate(pages):
    if i <= current_idx:
        if st.sidebar.button(f"{i+1}. {page}", key=page):
            st.session_state.current_page = page
    else:
        st.sidebar.markdown(f"{i+1}. {page} 🔒")

# Page Navigator
def go_next():
    next_idx = pages.index(st.session_state.current_page) + 1
    if next_idx < len(pages):
        st.session_state.current_page = pages[next_idx]

# ========== Page 1: User Info ==========
if st.session_state.current_page == 'User Info':
    st.title("🧑 User Information")
    st.markdown("Please fill in your details to get started 👇")
    name = st.text_input("Your Name")
    age = st.number_input("Your Age", min_value=10, max_value=100, step=1)
    gender = st.selectbox("Select your gender:", ["Male", "Female", "Other", "Prefer not to say"])
    st.write("You selected:", gender)

    if st.button("Continue to Dashboard"):
        if name:
            st.session_state.name = name
            st.session_state.age = age
            st.session_state.gender = gender

            # Save user info
            with open("data/user_info.csv", "a", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([name, age, gender])

            go_next()
        else:
            st.warning("Please enter your name to continue.")

# ========== Page 2: Dashboard ==========
elif st.session_state.current_page == 'Dashboard':
    st.title("📊 Mood Dashboard")

    journal_entry = st.text_area("✍️ Write your journal entry here:")

    if journal_entry:
        df = pd.DataFrame({'journal_entry': [journal_entry]})

        st.write("Your entry has been recorded:")
        st.dataframe(df)

        def analyze_mood(text):
            return TextBlob(str(text)).sentiment.polarity

        df['Mood Score'] = df['journal_entry'].apply(analyze_mood)
        avg_mood = df['Mood Score'].mean()

        if avg_mood > 0.3:
            risk = "Low"
        elif avg_mood > 0.0:
            risk = "Moderate"
        else:
            risk = "High"

        st.metric("Average Mood Score", f"{avg_mood:.2f}")
        st.metric("Burnout Risk", risk)

        st.session_state.avg_mood = avg_mood
        st.session_state.risk = risk

        # Save journal entry
        with open("data/journal_entries.csv", "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([st.session_state.name, journal_entry, avg_mood])

        if st.button("Continue to Suggestions"):
            go_next()

# ========== Page 3: Suggestions ==========
elif st.session_state.current_page == 'Suggestions':
    st.title("🧘 Wellness Suggestions")

    risk = st.session_state.get('risk', 'Moderate')

    if risk in ['Moderate', 'High']:
        st.subheader("You might be feeling overwhelmed.")
        st.video("https://www.youtube.com/watch?v=2OEL4P1Rz04")
        st.markdown("[Burnout Management Tips from CDC](https://www.cdc.gov/mentalhealth/stress-coping/cope-with-stress/index.html)")
    else:
        st.success("You're doing great! Keep it up 🥳")

    if st.button("Continue to Feedback"):
        go_next()

# ========== Page 4: Feedback ==========
elif st.session_state.current_page == 'Feedback':
    st.title("💬 Feedback")
    st.write("Thank you for using our Mood Prediction App!")

    feedback = st.text_area("How was your experience?")
    if st.button("Submit Feedback"):
        with open("data/feedback.csv", "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([st.session_state.get("name", "Anonymous"), feedback])
        st.success("Thanks for your feedback! 🌟")

















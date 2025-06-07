import streamlit as st
import pandas as pd
from textblob import TextBlob

# Step tracker
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'User Info'

# Function to go next
def go_next(page):
    st.session_state.current_page = page

# ========== Page 1: User Info ==========
if st.session_state.current_page == 'User Info':
    st.title("🧑 User Information")
    name = st.text_input("Your Name")
    age = st.number_input("Your Age", min_value=10, max_value=100, step=1)
    
    if st.button("Continue to Dashboard"):
        st.session_state.name = name
        st.session_state.age = age
        go_next('Dashboard')

# ========== Page 2: Dashboard ==========
elif st.session_state.current_page == 'Dashboard':
    st.title("📊 Mood Dashboard")
    uploaded_file = st.file_uploader("Upload journal CSV", type=["csv"])
    
    if uploaded_file:
        df = pd.read_csv(uploaded_file)

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
        
        st.metric("Mood Score", f"{avg_mood:.2f}")
        st.metric("Burnout Risk", risk)
        
        st.session_state.avg_mood = avg_mood
        st.session_state.risk = risk

        if st.button("Continue to Suggestions"):
            go_next('Suggestions')

# ========== Page 3: Wellness Suggestions ==========
elif st.session_state.current_page == 'Suggestions':
    st.title("🧘 Wellness Suggestions")

    risk = st.session_state.get('risk', 'Moderate')

    if risk in ['Moderate', 'High']:
        st.write("Here’s some calming music and tips:")
        st.video("https://www.youtube.com/watch?v=2OEL4P1Rz04")
        st.markdown("[Burnout Tips](https://www.cdc.gov/mentalhealth/stress-coping/cope-with-stress/index.html)")
    else:
        st.success("You're doing great! Keep it up.")

    if st.button("Continue to Feedback"):
        go_next('Feedback')

# ========== Page 4: Feedback ==========
elif st.session_state.current_page == 'Feedback':
    st.title("💬 Feedback")
    feedback = st.text_area("How was your experience?")
    if st.button("Submit"):
        st.success("Thank you for your feedback! 🌟")















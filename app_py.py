# 📁 File: student_wellness_app.py

import streamlit as st
from textblob import TextBlob

st.set_page_config(page_title="Student Wellness App", layout="centered")

# Initialize state
if "page" not in st.session_state:
    st.session_state.page = "User Info"
if "user_info" not in st.session_state:
    st.session_state.user_info = {}
if "burnout_risk" not in st.session_state:
    st.session_state.burnout_risk = None
if "mood_score" not in st.session_state:
    st.session_state.mood_score = None
if "quiz_answers" not in st.session_state:
    st.session_state.quiz_answers = {}

# Sidebar Navigation
pages = ["User Info", "Dashboard", "Quiz", "Personalized Plan", "Feedback"]
disabled_pages = [
    page for page in pages
    if page != "User Info" and (
        (page == "Dashboard" and not st.session_state.user_info) or
        (page == "Quiz" and st.session_state.burnout_risk not in ["Moderate", "High"]) or
        (page == "Personalized Plan" and not st.session_state.quiz_answers)
    )
]
selected = st.sidebar.radio("Navigate", pages, disabled=[p in disabled_pages for p in pages])
st.session_state.page = selected

# --- PAGE 1: User Info ---
if selected == "User Info":
    st.title("👤 User Information")
    with st.form("user_form"):
        name = st.text_input("Your Name")
        gender = st.selectbox("Gender", ["Prefer not to say", "Male", "Female", "Other"])
        submit = st.form_submit_button("Continue to Dashboard")
    if submit:
        st.session_state.user_info = {"name": name, "gender": gender}
        st.success("Information saved. Proceed to Dashboard from sidebar.")

# --- PAGE 2: Dashboard ---
elif selected == "Dashboard":
    st.title("🌿 Wellness Dashboard")
    st.markdown("Write your journal entry and wellness habits for today:")

    with st.form("journal_form"):
        journal = st.text_area("📝 Journal Entry", height=150)
        sleep_hours = st.number_input("🛌 Sleep Hours", 0.0, 24.0, step=0.5)
        screen_time = st.number_input("📱 Screen Time (hrs)", 0.0, 24.0, step=0.5)
        workout_done = st.selectbox("🏋️ Workout Today?", ["No", "Yes"])
        analyze = st.form_submit_button("Analyze Mood")

    if analyze:
        score = round(TextBlob(journal).sentiment.polarity, 2)
        st.session_state.mood_score = score
        if score > 0.3:
            risk = "Low"
        elif score > 0.0:
            risk = "Moderate"
        else:
            risk = "High"
        st.session_state.burnout_risk = risk

        st.markdown(f"### 🧠 Mood Score: `{score}`")
        st.metric("🧭 Burnout Risk", risk)

        if risk in ["Moderate", "High"]:
            if st.button("Continue to Quiz"):
                st.session_state.page = "Quiz"
                st.experimental_rerun()

# --- PAGE 3: Quiz ---
elif selected == "Quiz":
    st.title("🧪 Quick Check-In Quiz")
    with st.form("quiz_form"):
        q1 = st.radio("How often do you feel overwhelmed?", ["Rarely", "Sometimes", "Often"])
        q2 = st.radio("Do you feel supported by peers/family?", ["Yes", "Somewhat", "No"])
        q3 = st.radio("How would you rate your energy today?", ["High", "Medium", "Low"])
        submit_quiz = st.form_submit_button("Submit Quiz")

    if submit_quiz:
        st.session_state.quiz_answers = {"Q1": q1, "Q2": q2, "Q3": q3}
        st.success("Quiz submitted.")
        st.session_state.page = "Personalized Plan"
        st.experimental_rerun()

# --- PAGE 4: Personalized Plan ---
elif selected == "Personalized Plan":
    st.title("📝 Your Personalized Wellness Plan")
    risk = st.session_state.burnout_risk
    st.markdown(f"### Based on your burnout level: **{risk}**")

    if risk == "High":
        st.error("⚠️ High risk detected. Prioritize rest and support.")
        st.markdown("**Diet:** Rich in omega-3s, fruits, hydration.")
        st.markdown("**Workout:** Light walks, yoga, avoid overexertion.")
    elif risk == "Moderate":
        st.warning("🚧 Moderate risk. Balance needed.")
        st.markdown("**Diet:** Include whole grains, greens, nuts.")
        st.markdown("**Workout:** Brisk walking, short strength sessions.")
    else:
        st.success("✅ You're doing well!")
        st.markdown("**Diet:** Maintain variety, reduce sugar.")
        st.markdown("**Workout:** Keep up your regular routine.")

# --- PAGE 5: Feedback ---
elif selected == "Feedback":
    st.title("💬 We value your feedback")
    feedback = st.text_area("Let us know how we can improve:")
    if st.button("Submit Feedback"):
        st.success("Thanks for sharing your feedback!")











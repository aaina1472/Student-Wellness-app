import streamlit as st
from textblob import TextBlob

st.set_page_config(page_title="Student Wellness App", layout="centered")

# Initialize session state
if "page" not in st.session_state:
    st.session_state.page = "User Info"
    st.session_state.user_info = {}
    st.session_state.journal_input = ""
    st.session_state.sleep_hours = 0.0
    st.session_state.screen_time = 0.0
    st.session_state.workout_done = "No"
    st.session_state.mood_score = None
    st.session_state.burnout_risk = None
    st.session_state.quiz_answers = {}
    st.session_state.quiz_complete = False

# Sidebar navigation
pages = ["User Info", "Dashboard", "Quiz", "Personalized Plan", "Feedback"]
accessible_pages = pages[:1]
if st.session_state.user_info:
    accessible_pages.append("Dashboard")
if st.session_state.burnout_risk in ["Moderate", "High"]:
    accessible_pages.append("Quiz")
if st.session_state.quiz_complete:
    accessible_pages.append("Personalized Plan")
if st.session_state.page == "Personalized Plan":
    accessible_pages.append("Feedback")

st.sidebar.title("Navigation")
st.session_state.page = st.sidebar.radio("Go to", accessible_pages)

# User Info Page
if st.session_state.page == "User Info":
    st.title("👤 User Information")
    with st.form("user_info_form"):
        name = st.text_input("Name")
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        age = st.number_input("Age", min_value=10, max_value=100)
        submitted = st.form_submit_button("Continue")
        if submitted and name:
            st.session_state.user_info = {"name": name, "gender": gender, "age": age}
            st.success("Information saved. Proceed to Dashboard from sidebar.")

# Dashboard Page
elif st.session_state.page == "Dashboard":
    st.title("🌿 Student Wellness Dashboard")
    with st.form("wellness_form"):
        st.text_area("📝 Journal Entry", key="journal_input", height=150)
        st.number_input("🛌 Sleep hours", min_value=0.0, max_value=24.0, step=0.5, key="sleep_hours")
        st.number_input("📱 Screen time (hours)", min_value=0.0, max_value=24.0, step=0.5, key="screen_time")
        st.selectbox("🏋️ Workout today?", ["No", "Yes"], key="workout_done")
        analyze_button = st.form_submit_button("Analyze")

    if analyze_button:
        journal = st.session_state.journal_input.strip()
        if journal:
            blob = TextBlob(journal)
            score = round(blob.sentiment.polarity, 2)
            st.session_state.mood_score = score
            risk = "Low" if score > 0.3 else "Moderate" if score > 0.0 else "High"
            st.session_state.burnout_risk = risk
            st.markdown("---")
            st.subheader("📊 Mood & Burnout Report")
            emoji = "😄" if score > 0.3 else "😐" if score > 0.0 else "😞"
            st.write(f"🧠 **Mood Score:** `{score}` {emoji}")
            st.progress((score + 1) / 2)
            st.metric("🧭 Burnout Risk Level", risk)
            if risk in ["Moderate", "High"]:
                st.info("You can proceed to Quiz from the sidebar.")

# Quiz Page
elif st.session_state.page == "Quiz":
    st.title("📝 Burnout Risk Quiz")
    with st.form("quiz_form"):
        st.session_state.quiz_answers["q1"] = st.radio("How often do you feel tired?", ["Rarely", "Sometimes", "Often"])
        st.session_state.quiz_answers["q2"] = st.radio("Do you find it hard to concentrate?", ["No", "Sometimes", "Yes"])
        st.session_state.quiz_answers["q3"] = st.radio("How is your appetite lately?", ["Normal", "Less than usual", "More than usual"])
        st.session_state.quiz_answers["q4"] = st.radio("Are you feeling overwhelmed?", ["No", "Sometimes", "Yes"])
        st.session_state.quiz_answers["q5"] = st.radio("Are you socially withdrawing?", ["Not at all", "A bit", "Yes"])
        quiz_submit = st.form_submit_button("Submit Quiz")
        if quiz_submit:
            st.session_state.quiz_complete = True
            st.success("Quiz submitted. Proceed to Personalized Plan from sidebar.")

# Personalized Plan Page
elif st.session_state.page == "Personalized Plan":
    st.title("🍎 Personalized Diet & Workout Plan")
    risk = st.session_state.burnout_risk
    st.write(f"Burnout Risk: **{risk}**")
    st.markdown("---")
    if risk == "High":
        st.subheader("Diet Plan")
        st.markdown("- High-protein meals\n- Omega-3 rich food (salmon, flaxseeds)\n- Avoid caffeine/sugar overload")
        st.subheader("Workout Plan")
        st.markdown("- Light yoga\n- Breathing exercises\n- 15 mins walk daily")
    elif risk == "Moderate":
        st.subheader("Diet Plan")
        st.markdown("- Balanced carbs and protein\n- Hydration focus\n- Green leafy vegetables")
        st.subheader("Workout Plan")
        st.markdown("- 20–30 mins stretching\n- Brisk walking\n- Low intensity home workouts")
    else:
        st.success("You're in great shape! Maintain a balanced routine.")

# Feedback Page
elif st.session_state.page == "Feedback":
    st.title("🗣️ Feedback")
    feedback = st.text_area("Tell us about your experience")
    if st.button("Submit Feedback"):
        st.success("🙏 Thank you for your feedback!")











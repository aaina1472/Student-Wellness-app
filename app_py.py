import streamlit as st
from textblob import TextBlob

st.set_page_config(page_title="Student Wellness App", layout="centered")

# --- INITIALIZE SESSION STATE ---
if "page" not in st.session_state:
    st.session_state.page = "User Info"
    st.session_state.user_info = {}
    st.session_state.journal_input = ""
    st.session_state.sleep_hours = 8.0
    st.session_state.screen_time = 4.0
    st.session_state.workout_done = "No"
    st.session_state.mood_score = None
    st.session_state.burnout_risk = None
    st.session_state.quiz_complete = False

# --- SMART SIDEBAR NAVIGATION ---
sidebar_options = ["User Info"]

if st.session_state.user_info:
    sidebar_options.append("Dashboard")

if st.session_state.burnout_risk in ["Moderate", "High"]:
    sidebar_options.append("Quiz")

if st.session_state.quiz_complete:
    sidebar_options.append("Personalized Plan")
    sidebar_options.append("Feedback")

selected_page = st.sidebar.radio("Go to", sidebar_options, key="nav_radio_main")

# --- PAGE 1: USER INFO ---
if selected_page == "User Info":
    st.title("👤 User Information")
    st.write("Please enter your details to get started.")
    with st.form("user_info_form"):
        name = st.text_input("Name", value=st.session_state.user_info.get("name", ""))
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        age = st.number_input("Age", min_value=10, max_value=100, value=st.session_state.user_info.get("age", 18))
        submitted = st.form_submit_button("Save Information")

        if submitted and name:
            st.session_state.user_info = {"name": name, "gender": gender, "age": age}
            st.success("Information saved! Go to Dashboard from sidebar.")

# --- PAGE 2: DASHBOARD ---
elif selected_page == "Dashboard":
    st.title(f"🌿 Welcome, {st.session_state.user_info.get('name', 'User')}!")
    st.header("Student Wellness Dashboard")

    with st.form("wellness_form"):
        st.text_area("📝 Journal Entry: How are you feeling today?", key="journal_input", height=150)
        st.slider("🛌 Last night's sleep (hours)", min_value=0.0, max_value=24.0, step=0.5, key="sleep_hours")
        st.slider("📱 Today's screen time (hours)", min_value=0.0, max_value=24.0, step=0.5, key="screen_time")
        st.selectbox("🏋️ Did you workout today?", ["No", "Yes"], key="workout_done")
        analyze_button = st.form_submit_button("Analyze My Day")

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
                st.info("Your burnout risk is elevated. Please go to the Quiz section.")
        else:
            st.warning("Please write a journal entry to analyze your mood.")

# --- PAGE 3: QUIZ ---
elif selected_page == "Quiz":
    if st.session_state.burnout_risk not in ["Moderate", "High"]:
        st.warning("Quiz is only for Moderate or High burnout risk.")
        st.stop()

    st.title("📝 Burnout Risk Quiz")
    with st.form("quiz_form"):
        q1 = st.selectbox("Do you feel emotionally drained?", ["Never", "Sometimes", "Often", "Always"])
        q2 = st.selectbox("Do you find it hard to concentrate?", ["Never", "Sometimes", "Often", "Always"])
        q3 = st.selectbox("Do you enjoy your daily routine?", ["Yes", "Somewhat", "No"])
        q4 = st.selectbox("How is your appetite recently?", ["Normal", "Less", "More than usual"])
        q5 = st.selectbox("Do you feel isolated or lonely?", ["No", "Sometimes", "Frequently"])

        quiz_submit = st.form_submit_button("Submit Quiz")

    if quiz_submit:
        st.session_state.quiz_complete = True
        st.success("Quiz submitted! Go to 'Personalized Plan' from sidebar.")

# --- PAGE 4: PERSONALIZED PLAN ---
elif selected_page == "Personalized Plan":
    if not st.session_state.quiz_complete:
        st.warning("Please complete the quiz first.")
        st.stop()

    st.title("🍎 Personalized Diet & Workout Plan")
    st.markdown("Based on your quiz responses and burnout level:")

    st.subheader("🥗 Diet Suggestions")
    st.markdown("- Eat more fruits, vegetables, and whole grains.")
    st.markdown("- Reduce sugar and caffeine if feeling anxious.")
    st.markdown("- Drink at least 2-3 liters of water per day.")

    st.subheader("🏃 Workout Plan")
    st.markdown("- Try light exercises like yoga or walking.")
    st.markdown("- 20–30 minutes of physical activity daily.")
    st.markdown("- Avoid intense workouts if you're feeling drained.")

    st.subheader("🎧 Mental Wellness Resources")
    st.markdown("**Guided Meditation:**")
    st.video("https://www.youtube.com/watch?v=inpok4MKVLM")
    st.markdown("**Podcast:** [The Happiness Lab](https://www.happinesslab.fm/)")

# --- PAGE 5: FEEDBACK ---
elif selected_page == "Feedback":
    st.title("🗣️ Your Feedback")
    feedback = st.text_area("How was your experience using this app?")
    if st.button("Submit Feedback"):
        st.success("Thank you for your feedback!")











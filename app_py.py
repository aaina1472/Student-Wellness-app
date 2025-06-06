import streamlit as st
from textblob import TextBlob

st.set_page_config(page_title="Student Wellness App", layout="centered")

# --- SESSION STATE INITIALIZATION ---
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

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("Navigation")
pages = ["User Info", "Dashboard", "Quiz", "Personalized Plan", "Feedback"]
st.session_state.page = st.sidebar.radio("Go to", pages)

# --- PAGE: USER INFO ---
if st.session_state.page == "User Info":
    st.title("👤 User Information")
    with st.form("user_info_form"):
        name = st.text_input("Name", value=st.session_state.user_info.get("name", ""))
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        age = st.number_input("Age", min_value=10, max_value=100, value=18)
        submitted = st.form_submit_button("Save Information")
        if submitted and name:
            st.session_state.user_info = {"name": name, "gender": gender, "age": age}
            st.success("✅ Information saved!")

# --- PAGE: DASHBOARD ---
elif st.session_state.page == "Dashboard":
    st.title("🌿 Wellness Dashboard")
    with st.form("wellness_form"):
        journal = st.text_area("📝 How are you feeling today?", key="journal_input")
        st.slider("😴 Sleep (hours)", 0.0, 24.0, key="sleep_hours")
        st.slider("📱 Screen Time (hours)", 0.0, 24.0, key="screen_time")
        st.selectbox("🏋️‍♂️ Workout Today?", ["No", "Yes"], key="workout_done")
        analyze = st.form_submit_button("Analyze My Day")
    
    if analyze and journal.strip():
        score = round(TextBlob(journal).sentiment.polarity, 2)
        st.session_state.mood_score = score
        risk = "Low" if score > 0.3 else "Moderate" if score > 0.0 else "High"
        st.session_state.burnout_risk = risk

        st.subheader("📊 Mood Analysis")
        st.write(f"🧠 Mood Score: `{score}`")
        st.metric("🔥 Burnout Risk", risk)

        if risk in ["Moderate", "High"]:
            st.info("Your burnout risk is elevated. Please take the quiz for deeper analysis.")
    elif analyze:
        st.warning("Please write something to analyze.")

# --- PAGE: QUIZ ---
elif st.session_state.page == "Quiz":
    st.title("📝 Burnout Assessment Quiz")
    if st.session_state.burnout_risk not in ["Moderate", "High"]:
        st.info("This quiz is most useful when your burnout risk is Moderate or High.")

    with st.form("quiz_form"):
        q1 = st.slider("How often do you feel tired?", 1, 5, 3)
        q2 = st.slider("How often do you feel unmotivated?", 1, 5, 3)
        q3 = st.slider("How often do you feel overwhelmed?", 1, 5, 3)
        quiz_submit = st.form_submit_button("Submit Quiz")
        if quiz_submit:
            st.session_state.quiz_complete = True
            st.success("✅ Quiz complete! Visit the Personalized Plan tab.")

# --- PAGE: PLAN ---
elif st.session_state.page == "Personalized Plan":
    st.title("🍏 Personalized Diet & Workout Plan")
    if not st.session_state.quiz_complete:
        st.info("Fill the Quiz tab first for more accurate plans.")

    st.markdown("""
    ### 🥗 Diet Recommendations
    - Include fresh fruits and veggies daily
    - Drink 8+ glasses of water
    - Avoid processed and fried food

    ### 🏃 Workout Suggestions
    - 15-20 min of yoga or walking
    - Try deep breathing/stretching exercises

    ### 🧠 Mental Wellness
    - Practice mindfulness or journaling
    - Try these:
        - [Relaxing Music 🎵](https://www.youtube.com/watch?v=2OEL4P1Rz04)
        - [Meditation Video 🧘](https://www.youtube.com/watch?v=inpok4MKVLM)
        - [The Happiness Lab Podcast](https://www.happinesslab.fm/)
    """)

# --- PAGE: FEEDBACK ---
elif st.session_state.page == "Feedback":
    st.title("🗣️ Feedback")
    st.write("We'd love to hear from you!")
    feedback = st.text_area("💬 Share your thoughts or suggestions:")
    if st.button("Submit Feedback"):
        st.success("✅ Thank you for your feedback!")












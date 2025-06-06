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
    st.session_state.quiz_answers = {}
    st.session_state.quiz_complete = False

# --- SIDEBAR NAVIGATION (ALL PAGES VISIBLE) ---
pages = ["User Info", "Dashboard", "Quiz", "Personalized Plan", "Feedback"]
st.sidebar.title("Navigation")
st.session_state.page = st.sidebar.radio("Go to", pages)

# --- PAGE: USER INFO ---
if st.session_state.page == "User Info":
    st.title("👤 User Information")
    with st.form("user_info_form"):
        name = st.text_input("Name", value=st.session_state.user_info.get("name", ""))
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        age = st.number_input("Age", min_value=10, max_value=100, value=st.session_state.user_info.get("age", 18))
        submitted = st.form_submit_button("Save Information")
        if submitted and name:
            st.session_state.user_info = {"name": name, "gender": gender, "age": age}
            st.success("Information saved! You can now visit other pages.")

# --- PAGE: DASHBOARD ---
elif st.session_state.page == "Dashboard":
    if not st.session_state.user_info:
        st.warning("Please fill in your User Information first.")
        st.stop()

    st.title(f"🌿 Welcome, {st.session_state.user_info.get('name', 'User')}!")
    st.header("Student Wellness Dashboard")

    with st.form("wellness_form"):
        journal = st.text_area("📝 Journal Entry: How are you feeling today?", key="journal_input", value=st.session_state.journal_input)
        sleep_hours = st.slider("🛌 Last night's sleep (hours)", min_value=0.0, max_value=24.0, step=0.5, value=st.session_state.sleep_hours)
        screen_time = st.slider("📱 Today's screen time (hours)", min_value=0.0, max_value=24.0, step=0.5, value=st.session_state.screen_time)
        workout_done = st.selectbox("🏋️ Did you workout today?", ["No", "Yes"], index=0 if st.session_state.workout_done=="No" else 1)
        analyze_button = st.form_submit_button("Analyze My Day")

    if analyze_button:
        if journal.strip():
            score = round(TextBlob(journal).sentiment.polarity, 2)
            st.session_state.mood_score = score
            st.session_state.journal_input = journal
            st.session_state.sleep_hours = sleep_hours
            st.session_state.screen_time = screen_time
            st.session_state.workout_done = workout_done

            if score > 0.3:
                burnout_risk = "Low"
            elif score > 0.0:
                burnout_risk = "Moderate"
            else:
                burnout_risk = "High"
            st.session_state.burnout_risk = burnout_risk

            st.markdown("---")
            st.subheader("📊 Mood & Burnout Report")
            emoji = "😄" if score > 0.3 else "😐" if score > 0.0 else "😞"
            st.write(f"🧠 **Mood Score:** `{score}` {emoji}")
            st.metric("🧭 Burnout Risk Level", burnout_risk)

            if burnout_risk in ["Moderate", "High"]:
                st.info("Your burnout risk is elevated. Please check the 'Quiz' page for a deeper analysis.")
        else:
            st.warning("Please write a journal entry to analyze your mood.")

# --- PAGE: QUIZ ---
elif st.session_state.page == "Quiz":
    if st.session_state.burnout_risk not in ["Moderate", "High"]:
        st.warning("The quiz is available only if your burnout risk is Moderate or High. Please complete the Dashboard analysis first.")
        st.stop()

    st.title("📝 Burnout Risk Quiz")
    with st.form("quiz_form"):
        st.write("Answer these questions based on how you've felt over the last two weeks.")
        q1 = st.slider("How often do you feel tired?", 1, 5, 3)
        q2 = st.slider("How often do you feel unmotivated?", 1, 5, 3)
        q3 = st.slider("How often do you feel overwhelmed?", 1, 5, 3)
        quiz_submit = st.form_submit_button("Submit Quiz")

        if quiz_submit:
            # Save answers (just example)
            st.session_state.quiz_answers = {"q1": q1, "q2": q2, "q3": q3}
            st.session_state.quiz_complete = True
            st.success("Quiz submitted! Please visit 'Personalized Plan' for your tailored suggestions.")

# --- PAGE: PERSONALIZED PLAN ---
elif st.session_state.page == "Personalized Plan":
    if not st.session_state.quiz_complete:
        st.warning("Please complete the Quiz before viewing your Personalized Plan.")
        st.stop()

    st.title("🍎 Personalized Diet & Workout Plan")
    st.write("Based on your mood, sleep, screen time, and quiz answers, here are some personalized recommendations:")

    # Simple example logic
    st.markdown(f"""
    - **Sleep Hours:** {st.session_state.sleep_hours}  
    - **Screen Time:** {st.session_state.screen_time}  
    - **Workout Done Today:** {st.session_state.workout_done}  

    ### Diet Suggestions
    - Eat more fresh fruits and vegetables.
    - Avoid caffeine in the evening.
    - Stay hydrated.

    ### Workout Suggestions
    - Try gentle stretching or yoga.
    - Aim for at least 30 minutes of light exercise daily.

    ### Support
    - Consider talking to a mentor or counselor if feelings persist.
    """)

# --- PAGE: FEEDBACK ---
elif st.session_state.page == "Feedback":
    if not st.session_state.quiz_complete:
        st.warning("Please complete the Quiz and Personalized Plan before giving feedback.")
        st.stop()

    st.title("🗣️ Feedback")
    feedback = st.text_area("Please share your feedback or suggestions:")
    if st.button("Submit Feedback"):
        st.success("Thank you for your feedback!")














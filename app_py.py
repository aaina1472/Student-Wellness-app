import streamlit as st
from textblob import TextBlob
from datetime import datetime

st.set_page_config(page_title="Student Wellness App", layout="centered")

# Initialize session state defaults
for key, default in {
    "page": "user_info",
    "name": "",
    "gender": "",
    "journal_input": "",
    "sleep_hours": 0.0,
    "screen_time": 0.0,
    "workout_done": "No",
    "mood_score": None,
    "burnout_risk": None,
    "quiz_submitted": False,
    "quiz_answers": {},
    "feedback_text": "",
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

def analyze_mood(text):
    blob = TextBlob(text)
    return round(blob.sentiment.polarity, 2)

def get_personalized_plan(risk_level, quiz_answers):
    diet = ""
    workout = ""

    poor_sleep = quiz_answers.get("sleep_quality", "") == "Poor"
    no_exercise = quiz_answers.get("exercise_freq", "") == "No"

    if risk_level == "High":
        diet = (
            "Focus on nutrient-rich foods like fruits, vegetables, and whole grains. "
            "Avoid caffeine and heavy meals before bedtime."
        )
        workout = (
            "Gentle activities like yoga, stretching, and breathing exercises are recommended. "
            "Avoid strenuous workouts until you feel better."
        )
        if poor_sleep:
            diet += " Consider herbal teas like chamomile to improve sleep."
        if no_exercise:
            workout += " Start with 5-10 minutes of light walking daily."

    elif risk_level == "Moderate":
        diet = (
            "Maintain a balanced diet including lean proteins, healthy fats, and complex carbs."
        )
        workout = (
            "Aim for moderate cardio (like brisk walking or cycling) 3-4 times a week."
        )
        if poor_sleep:
            diet += " Limit screen time before bed to improve sleep quality."
        if no_exercise:
            workout += " Gradually increase activity; even short workouts help."

    else:
        diet = "Keep up your healthy eating habits!"
        workout = "Continue your regular workout routine."

    return {"diet": diet, "workout": workout}

# === PAGE: User Info ===
if st.session_state.page == "user_info":
    st.title("👤 User Information")
    st.text_input("Enter your name:", key="name")
    st.selectbox("Select your gender:", ["Prefer not to say", "Male", "Female", "Other"], key="gender")

    if st.button("Next"):
        if st.session_state.name.strip() == "":
            st.warning("Please enter your name to proceed.")
        else:
            st.session_state.page = "journal"

# === PAGE: Journal + Inputs + Mood Analysis ===
elif st.session_state.page == "journal":
    st.title("🌿 Student Wellness Dashboard")
    st.markdown("Write about your day or feelings, and get personalized mood analysis and wellness support.")

    with st.form("wellness_form"):
        st.text_area(
            "📝 Write your journal entry here:",
            key="journal_input",
            placeholder="Start writing...",
            height=150,
            value=st.session_state.journal_input,
        )
        st.number_input(
            "🛌 Sleep hours",
            min_value=0.0,
            max_value=24.0,
            step=0.5,
            key="sleep_hours",
            value=st.session_state.sleep_hours,
        )
        st.number_input(
            "📱 Screen time (hours)",
            min_value=0.0,
            max_value=24.0,
            step=0.5,
            key="screen_time",
            value=st.session_state.screen_time,
        )
        st.selectbox(
            "🏋️ Workout today?",
            ["No", "Yes"],
            key="workout_done",
            index=0 if st.session_state.workout_done == "No" else 1,
        )
        analyze_button = st.form_submit_button("Analyze Mood")

    if analyze_button:
        journal = st.session_state.journal_input.strip()
        if journal == "":
            st.warning("⚠️ Please write something in your journal before analyzing.")
        else:
            score = analyze_mood(journal)
            st.session_state.mood_score = score
            burnout_risk = (
                "Low" if score > 0.3 else
                "Moderate" if score > 0.0 else
                "High"
            )
            st.session_state.burnout_risk = burnout_risk
            st.session_state.page = "results"

# === PAGE: Results & Quiz for Moderate/High Burnout Risk ===
elif st.session_state.page == "results":
    st.title(f"Hello, {st.session_state.name}!")
    score = st.session_state.mood_score
    risk = st.session_state.burnout_risk

    st.subheader("📊 Mood & Burnout Report")

    emoji = "😄" if score > 0.3 else "😐" if score > 0.0 else "😞"
    st.write(f"🧠 **Mood Score:** `{score}` {emoji}")
    st.progress((score + 1) / 2)  # Normalize polarity for progress bar

    st.metric("🧭 Burnout Risk Level", risk)

    if risk in ["Moderate", "High"]:
        st.subheader("🧘 Wellness Recommendations")
        if risk == "High":
            st.error("⚠️ High Burnout Risk Detected. Please take care of your mental health.")
        st.markdown("### 🎵 Relaxing Music")
        st.markdown(
            """<iframe width="100%" height="80" src="https://www.youtube.com/embed/2OEL4P1Rz04?autoplay=1&loop=1&playlist=2OEL4P1Rz04"
            frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>""",
            unsafe_allow_html=True)

        st.markdown("### 🧘 Guided Meditation")
        st.video("https://www.youtube.com/watch?v=inpok4MKVLM")

        st.markdown("### 🎧 Uplifting Podcasts")
        st.markdown(
            """
            - [🧠 The Daily Shine](https://www.theshineapp.com/)
            - [😄 The Happiness Lab](https://www.happinesslab.fm/)
            - [🕌 Mindful Muslim Podcast](https://mindful-muslimah.com/podcast/)
            """)

        # Quiz Section
        st.subheader("📋 Quick Wellness Quiz")
        with st.form("quiz_form"):
            sleep_quality = st.selectbox(
                "How would you rate your sleep quality?",
                ["Good", "Average", "Poor"],
                key="sleep_quality"
            )
            exercise_freq = st.selectbox(
                "Do you exercise regularly?",
                ["Yes", "No"],
                key="exercise_freq"
            )
            quiz_submit = st.form_submit_button("Submit Quiz")

        if quiz_submit:
            st.session_state.quiz_answers = {
                "sleep_quality": sleep_quality,
                "exercise_freq": exercise_freq,
            }
            st.session_state.quiz_submitted = True

    else:
        st.success("✅ You're doing great! Keep journaling to maintain emotional well-being.")
        st.session_state.quiz_submitted = False

    # Show personalized plan after quiz submission
    if st.session_state.quiz_submitted:
        plan = get_personalized_plan(risk, st.session_state.quiz_answers)
        st.subheader("🍏 Personalized Diet Plan")
        st.write(plan["diet"])
        st.subheader("🏋️ Personalized Workout Plan")
        st.write(plan["workout"])

    # Button to restart flow
    if st.button("Start Over"):
        for key in st.session_state.keys():
            del st.session_state[key]
        st.session_state.page = "user_info"

# === PAGE: Feedback ===
elif st.session_state.page == "feedback":
    st.title("💬 Feedback")

    st.text_area("Share your feedback:", key="feedback_text", height=100)
    if st.button("Submit Feedback"):
        feedback = st.session_state.feedback_text.strip()
        if feedback:
            with open("feedback.txt", "a", encoding="utf-8") as f:
                f.write(f"{datetime.now()} - {st.session_state.name}: {feedback}\n")
            st.success("Thanks for your feedback!")
            st.session_state.feedback_text = ""
        else:
            st.warning("Please enter feedback before submitting.")

    if st.button("Back to Start"):
        for key in st.session_state.keys():
            del st.session_state[key]
        st.session_state.page = "user_info"




import streamlit as st
from textblob import TextBlob
from datetime import datetime

st.set_page_config(page_title="Student Wellness App", layout="wide")

# Initialize session state defaults
defaults = {
    "name": "",
    "gender": "Prefer not to say",
    "journal_input": "",
    "sleep_hours": 0.0,
    "screen_time": 0.0,
    "workout_done": "No",
    "mood_score": None,
    "burnout_risk": None,
    "quiz_answers": {},
    "quiz_submitted": False,
    "feedback_text": "",
    "current_page": "User Info",  # to programmatically switch pages
}

for key, val in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = val

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

# --- Sidebar navigation ---
st.sidebar.title("Navigation")

def get_menu_options():
    base = ["User Info", "Dashboard"]
    # Show quiz and plan only if burnout risk moderate/high and journal analyzed
    if st.session_state.burnout_risk in ["Moderate", "High"]:
        base += ["Quiz"]
        if st.session_state.quiz_submitted:
            base += ["Personalized Plan"]
    base += ["Feedback"]
    return base

menu_options = get_menu_options()

# Set default page to session state current_page if valid, else first in menu_options
if st.session_state.current_page not in menu_options:
    st.session_state.current_page = menu_options[0]

page = st.sidebar.radio("Go to", menu_options, index=menu_options.index(st.session_state.current_page))
st.session_state.current_page = page  # sync page state

# --- User Info Page ---
if page == "User Info":
    st.title("👤 User Information")
    st.text_input("Enter your name:", key="name")
    st.selectbox("Select your gender:", ["Prefer not to say", "Male", "Female", "Other"], key="gender")

    if st.button("Save and Continue"):
        if st.session_state.name.strip() == "":
            st.warning("Please enter your name to proceed.")
        else:
            st.success("User information saved. You can navigate to the Dashboard now.")
            st.session_state.current_page = "Dashboard"
            st.experimental_rerun()

# --- Dashboard Page ---
elif page == "Dashboard":
    st.title("🌿 Student Wellness Dashboard")
    st.markdown("Write about your day or feelings, and get personalized mood analysis and wellness support.")

    with st.form("wellness_form"):
        st.text_area(
            "📝 Write your journal entry here:",
            key="journal_input",
            placeholder="Start writing...",
            height=150,
        )
        st.number_input(
            "🛌 Sleep hours",
            min_value=0.0,
            max_value=24.0,
            step=0.5,
            key="sleep_hours",
        )
        st.number_input(
            "📱 Screen time (hours)",
            min_value=0.0,
            max_value=24.0,
            step=0.5,
            key="screen_time",
        )
        st.selectbox(
            "🏋️ Workout today?",
            ["No", "Yes"],
            key="workout_done",
        )
        submitted = st.form_submit_button("Analyze Mood")

    if submitted:
        journal = st.session_state.journal_input.strip()
        if journal == "":
            st.warning("⚠️ Please write something in your journal before analyzing.")
        else:
            score = analyze_mood(journal)
            st.session_state.mood_score = score
            risk = (
                "Low" if score > 0.3 else
                "Moderate" if score > 0.0 else
                "High"
            )
            st.session_state.burnout_risk = risk

            st.success(f"Analysis done! Mood Score: {score} | Burnout Risk: {risk}")

    if st.session_state.burnout_risk in ["Moderate", "High"]:
        st.info("Based on your burnout risk, you can continue to the Quiz for a personalized plan.")
        if st.button("Continue to Quiz"):
            st.session_state.current_page = "Quiz"
            st.experimental_rerun()

# --- Quiz Page ---
elif page == "Quiz":
    if st.session_state.burnout_risk not in ["Moderate", "High"]:
        st.warning("Quiz is available only if your burnout risk is Moderate or High. Please complete the Dashboard analysis first.")
    else:
        st.title("📋 Quick Wellness Quiz")
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
            submitted = st.form_submit_button("Submit Quiz")

        if submitted:
            st.session_state.quiz_answers = {
                "sleep_quality": sleep_quality,
                "exercise_freq": exercise_freq,
            }
            st.session_state.quiz_submitted = True
            st.success("Quiz answers saved! Now check your Personalized Plan page.")
            # Move user to Personalized Plan page automatically
            st.session_state.current_page = "Personalized Plan"
            st.experimental_rerun()

# --- Personalized Plan Page ---
elif page == "Personalized Plan":
    if st.session_state.burnout_risk not in ["Moderate", "High"]:
        st.warning("Personalized Plan is available only if your burnout risk is Moderate or High. Please complete the Dashboard analysis first.")
    elif not st.session_state.quiz_submitted:
        st.warning("Please complete the Quiz before viewing the Personalized Plan.")
    else:
        st.title("🍏 Personalized Diet & Workout Plan")
        plan = get_personalized_plan(st.session_state.burnout_risk, st.session_state.quiz_answers)
        st.subheader("Diet Plan")
        st.write(plan["diet"])
        st.subheader("Workout Plan")
        st.write(plan["workout"])

# --- Feedback Page ---
elif page == "Feedback":
    st.title("💬 Feedback")
    st.text_area("Share your feedback:", key="feedback_text", height=150)

    if st.button("Submit Feedback"):
        feedback = st.session_state.feedback_text.strip()
        if feedback:
            # Save feedback to a local file - in production, replace with DB or other storage
            with open("feedback.txt", "a", encoding="utf-8") as f:
                f.write(f"{datetime.now()} - {st.session_state.name}: {feedback}\n")
            st.success("Thanks for your feedback!")
            st.session_state.feedback_text = ""
        else:
            st.warning("Please enter feedback before submitting.")





import streamlit as st
from textblob import TextBlob

st.set_page_config(page_title="Student Wellness App", layout="wide")

# Initialize session state defaults
def init_state():
    defaults = {
        "name": "",
        "gender": "Prefer not to say",
        "journal_input": "",
        "sleep_hours": 0.0,
        "screen_time": 0.0,
        "workout_done": "No",
        "mood_score": None,
        "burnout_risk": None,
        "quiz_submitted": False,
        "quiz_answers": {},
        "personalized_plan_generated": False,
        "current_page": "User Info",
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val

init_state()

def analyze_mood(text):
    blob = TextBlob(text)
    return round(blob.sentiment.polarity, 2)

# Sidebar menu logic based on session state
def get_menu_options():
    base = ["User Info", "Dashboard"]
    if st.session_state.burnout_risk in ["Moderate", "High"]:
        base.append("Quiz")
        if st.session_state.quiz_submitted:
            base.append("Personalized Plan")
    base.append("Feedback")
    return base

# Sidebar
with st.sidebar:
    st.title("Menu")
    options = get_menu_options()
    page = st.radio("Go to", options, index=options.index(st.session_state.current_page) if st.session_state.current_page in options else 0)
    st.session_state.current_page = page

# --- Pages --- #

# User Info Page
if page == "User Info":
    st.header("👤 User Information")
    st.session_state.name = st.text_input("Name", st.session_state.name)
    st.session_state.gender = st.selectbox("Gender", ["Male", "Female", "Other", "Prefer not to say"], index=["Male", "Female", "Other", "Prefer not to say"].index(st.session_state.gender))

    if st.button("Continue to Dashboard"):
        if not st.session_state.name.strip():
            st.warning("Please enter your name to continue.")
        else:
            st.session_state.current_page = "Dashboard"
            st.experimental_rerun()

# Dashboard Page
elif page == "Dashboard":
    st.header("🌿 Student Wellness Dashboard")
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

            # Rerun to update sidebar options
            st.experimental_rerun()

    # If burnout risk is Moderate/High, show continue button to quiz
    if st.session_state.burnout_risk in ["Moderate", "High"]:
        st.info("Based on your burnout risk, you can continue to the Quiz for a personalized plan.")
        if st.button("Continue to Quiz"):
            st.session_state.current_page = "Quiz"
            st.experimental_rerun()

    # Show last analysis if exists
    if st.session_state.mood_score is not None:
        st.markdown("---")
        st.subheader("📊 Last Mood & Burnout Report")
        emoji = "😄" if st.session_state.mood_score > 0.3 else "😐" if st.session_state.mood_score > 0.0 else "😞"
        st.write(f"🧠 **Mood Score:** `{st.session_state.mood_score}` {emoji}")
        st.metric("🧭 Burnout Risk Level", st.session_state.burnout_risk)

# Quiz Page
elif page == "Quiz":
    st.header("📝 Burnout Quiz")

    if st.session_state.burnout_risk not in ["Moderate", "High"]:
        st.warning("You need moderate or high burnout risk to take the quiz. Please complete the journal entry first.")
        if st.button("Go to Dashboard"):
            st.session_state.current_page = "Dashboard"
            st.experimental_rerun()
    else:
        # Simple quiz questions example
        with st.form("quiz_form"):
            q1 = st.radio("How often do you feel tired during the day?", ["Rarely", "Sometimes", "Often"], index=st.session_state.quiz_answers.get("q1", 0))
            q2 = st.radio("How is your appetite lately?", ["Normal", "Reduced", "Increased"], index=st.session_state.quiz_answers.get("q2", 0))
            q3 = st.radio("Do you find it hard to focus on tasks?", ["No", "Sometimes", "Yes"], index=st.session_state.quiz_answers.get("q3", 0))

            submitted = st.form_submit_button("Submit Quiz")

        if submitted:
            st.session_state.quiz_answers = {"q1": q1, "q2": q2, "q3": q3}
            st.session_state.quiz_submitted = True
            st.success("Quiz submitted! You can now view your personalized plan.")
            st.session_state.current_page = "Personalized Plan"
            st.experimental_rerun()

# Personalized Plan Page
elif page == "Personalized Plan":
    st.header("🥗 Personalized Diet & Workout Plan")

    if not st.session_state.quiz_submitted:
        st.warning("Please complete the quiz first.")
        if st.button("Go to Quiz"):
            st.session_state.current_page = "Quiz"
            st.experimental_rerun()
    else:
        # Example simple plan based on burnout risk and quiz answers
        risk = st.session_state.burnout_risk
        answers = st.session_state.quiz_answers

        st.write(f"**User:** {st.session_state.name} | **Burnout Risk:** {risk}")
        st.write("Based on your mood and quiz answers, here is your personalized plan:")

        if risk == "High":
            st.subheader("Diet Plan for High Burnout Risk")
            st.markdown("""
            - Increase intake of antioxidants (fruits, vegetables).
            - Stay hydrated.
            - Avoid caffeine and sugar late in the day.
            """)

            st.subheader("Workout Plan for High Burnout Risk")
            st.markdown("""
            - Gentle yoga or stretching 20 min daily.
            - Light walks.
            - Avoid intense workouts until feeling better.
            """)

        elif risk == "Moderate":
            st.subheader("Diet Plan for Moderate Burnout Risk")
            st.markdown("""
            - Balanced meals with protein and fiber.
            - Include nuts and seeds.
            - Moderate caffeine intake.
            """)

            st.subheader("Workout Plan for Moderate Burnout Risk")
            st.markdown("""
            - Moderate cardio (e.g., brisk walking 30 min).
            - Strength training 2-3 times a week.
            """)

        else:
            st.info("Your burnout risk is low. Keep up the good work!")

        # Show quiz answers summary
        st.markdown("---")
        st.subheader("Your Quiz Answers")
        for k, v in answers.items():
            st.write(f"{k}: {v}")

# Feedback Page
elif page == "Feedback":
    st.header("🗣️ Feedback")

    feedback = st.text_area("Please leave your feedback or suggestions here:", height=150)
    if st.button("Submit Feedback"):
        if feedback.strip():
            st.success("Thank you for your feedback!")
            # Here you could add logic to save feedback to a file/db
            # For demo, just clear text area
            st.experimental_rerun()
        else:
            st.warning("Please write something before submitting feedback.")







import streamlit as st
from textblob import TextBlob

st.set_page_config(page_title="Student Wellness App", layout="wide")

# Initialize session state defaults
def init_state():
    defaults = {
        "name": "",
        "gender": "",
        "journal_input": "",
        "sleep_hours": 0.0,
        "screen_time": 0.0,
        "workout_done": "No",
        "mood_score": None,
        "burnout_risk": None,
        "quiz_answers": {},
        "personalized_plan": None,
        "current_page": "User Info",
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val

init_state()

# Mood analyzer
def analyze_mood(text):
    blob = TextBlob(text)
    return round(blob.sentiment.polarity, 2)

# Sidebar navigation (disable invalid options by warning if user jumps ahead)
allowed_pages = ["User Info", "Dashboard", "Quiz", "Personalized Plan", "Feedback"]

# Limit accessible pages based on progress
def get_allowed_pages():
    pages = ["User Info"]
    if st.session_state.name and st.session_state.gender:
        pages.append("Dashboard")
    if st.session_state.mood_score is not None:
        pages.append("Quiz")
    if st.session_state.personalized_plan is not None:
        pages.append("Personalized Plan")
    pages.append("Feedback")
    return pages

allowed_pages = get_allowed_pages()

page = st.sidebar.radio("Navigation", allowed_pages, index=allowed_pages.index(st.session_state.current_page) if st.session_state.current_page in allowed_pages else 0)
st.session_state.current_page = page

if page == "User Info":
    st.title("👤 Enter Your Information")
    st.session_state.name = st.text_input("Name", value=st.session_state.name)
    st.session_state.gender = st.selectbox("Gender", ["", "Male", "Female", "Other"], index=["", "Male", "Female", "Other"].index(st.session_state.gender) if st.session_state.gender in ["", "Male", "Female", "Other"] else 0)

    if st.button("Continue to Dashboard"):
        if not st.session_state.name.strip():
            st.warning("Please enter your name to continue.")
        elif not st.session_state.gender:
            st.warning("Please select your gender to continue.")
        else:
            st.session_state.current_page = "Dashboard"

elif page == "Dashboard":
    if not st.session_state.name or not st.session_state.gender:
        st.warning("Please complete your user info first.")
    else:
        st.title(f"🌿 Welcome {st.session_state.name} to Your Wellness Dashboard")
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
            analyze_button = st.form_submit_button("Analyze Mood")

        if analyze_button:
            journal = st.session_state.journal_input.strip()
            if not journal:
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

                st.markdown("---")
                st.subheader("📊 Mood & Burnout Report")

                emoji = "😄" if score > 0.3 else "😐" if score > 0.0 else "😞"
                st.write(f"🧠 **Mood Score:** `{score}` {emoji}")
                st.progress((score + 1) / 2)  # Normalize from -1 to 1 into 0-1 range

                st.metric("🧭 Burnout Risk Level", burnout_risk)

                if burnout_risk in ["Moderate", "High"]:
                    st.subheader("🧘 Wellness Recommendations")

                    if burnout_risk == "High":
                        st.error("⚠️ High Burnout Risk Detected. Please take care of your mental health.")

                    st.markdown("### 🎵 Relaxing Music")
                    st.markdown("""
                    <iframe width="100%" height="80" src="https://www.youtube.com/embed/2OEL4P1Rz04?autoplay=1&loop=1&playlist=2OEL4P1Rz04" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>
                    """, unsafe_allow_html=True)

                    st.markdown("### 🧘 Guided Meditation")
                    st.video("https://www.youtube.com/watch?v=inpok4MKVLM")

                    st.markdown("### 🎧 Uplifting Podcasts")
                    st.markdown("""
                    - [🧠 The Daily Shine](https://www.theshineapp.com/)
                    - [😄 The Happiness Lab](https://www.happinesslab.fm/)
                    - [🕌 Mindful Muslim Podcast](https://mindful-muslimah.com/podcast/)
                    """)

                else:
                    st.success("✅ You're doing great! Keep journaling to maintain emotional well-being.")

elif page == "Quiz":
    if st.session_state.mood_score is None:
        st.warning("Please complete your journal entry and mood analysis on the Dashboard first.")
    else:
        st.title("📝 Burnout Risk Quiz")

        def quiz_questions():
            q1 = st.radio("1. How often do you feel physically exhausted?", ["Never", "Sometimes", "Often", "Always"], key="q1")
            q2 = st.radio("2. Do you find it hard to concentrate?", ["Never", "Sometimes", "Often", "Always"], key="q2")
            q3 = st.radio("3. How is your appetite recently?", ["Good", "Average", "Poor"], key="q3")
            q4 = st.radio("4. How many hours of sleep do you get on average?", ["Less than 5", "5-7", "7-9", "More than 9"], key="q4")
            q5 = st.radio("5. How often do you exercise?", ["Never", "Sometimes", "Regularly"], key="q5")

        with st.form("quiz_form"):
            quiz_questions()
            submit_quiz = st.form_submit_button("Submit Quiz")

        if submit_quiz:
            answers = {
                "exhausted": st.session_state.q1,
                "concentration": st.session_state.q2,
                "appetite": st.session_state.q3,
                "sleep": st.session_state.q4,
                "exercise": st.session_state.q5,
            }
            st.session_state.quiz_answers = answers

            risk = st.session_state.burnout_risk
            plan = ""
            if risk == "High":
                plan = """
                ### 🥗 Personalized Diet Plan for High Burnout Risk
                - Increase intake of omega-3 fatty acids (fish, flaxseed)
                - Eat antioxidant-rich fruits and veggies
                - Stay hydrated
                
                ### 🏋️‍♂️ Workout Routine
                - Light yoga/stretching daily
                - Short walks to reduce stress
                - Avoid high-intensity workouts until recovery
                """
            elif risk == "Moderate":
                plan = """
                ### 🥗 Personalized Diet Plan for Moderate Burnout Risk
                - Balanced meals with proteins, carbs, and fats
                - Include nuts and seeds for energy
                - Moderate caffeine intake
                
                ### 🏋️‍♂️ Workout Routine
                - Moderate cardio 3-4 times a week
                - Strength training twice a week
                - Include rest days
                """
            else:
                plan = "You have low burnout risk; maintain your healthy lifestyle!"

            st.session_state.personalized_plan = plan
            st.success("✅ Quiz submitted! Your personalized plan is ready.")

elif page == "Personalized Plan":
    if not st.session_state.personalized_plan:
        st.warning("Please complete the quiz first to get your personalized plan.")
    else:
        st.title("📋 Your Personalized Wellness Plan")
        st.markdown(st.session_state.personalized_plan)

elif page == "Feedback":
    st.title("📝 Your Feedback")
    feedback = st.text_area("Please share your feedback about the app:")

    if st.button("Submit Feedback"):
        if feedback.strip():
            st.success("Thank you for your feedback!")
            # Save feedback externally if you want
        else:
            st.warning("Please enter some feedback before submitting.")










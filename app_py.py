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

# --- CORRECTED SIDEBAR NAVIGATION ---
st.sidebar.title("Navigation")

# Define all possible pages
all_pages = ["User Info", "Dashboard", "Quiz", "Personalized Plan", "Feedback"]

# Logic to determine which pages are accessible
accessible_pages = []
if 'user_info' in st.session_state and st.session_state.user_info:
    accessible_pages.append("User Info")
    accessible_pages.append("Dashboard")
else:
    accessible_pages.append("User Info")

if 'burnout_risk' in st.session_state and st.session_state.burnout_risk in ["Moderate", "High"]:
    if "Quiz" not in accessible_pages:
        accessible_pages.append("Quiz")

if 'quiz_complete' in st.session_state and st.session_state.quiz_complete:
    if "Quiz" not in accessible_pages:
         accessible_pages.append("Quiz")
    if "Personalized Plan" not in accessible_pages:
        accessible_pages.append("Personalized Plan")
    if "Feedback" not in accessible_pages:
        accessible_pages.append("Feedback")


st.session_state.page = st.sidebar.radio("Go to", accessible_pages, index=accessible_pages.index(st.session_state.page) if st.session_state.page in accessible_pages else 0)


# User Info Page
if st.session_state.page == "User Info":
    st.title("👤 User Information")
    with st.form("user_info_form"):
        name = st.text_input("Name", value=st.session_state.user_info.get("name", ""))
        gender = st.selectbox("Gender", ["Male", "Female", "Other"], index=["Male", "Female", "Other"].index(st.session_state.user_info.get("gender", "Male")))
        age = st.number_input("Age", min_value=10, max_value=100, value=st.session_state.user_info.get("age", 18))
        submitted = st.form_submit_button("Continue")
        if submitted and name:
            st.session_state.user_info = {"name": name, "gender": gender, "age": age}
            st.success("Information saved! You can now access the Dashboard from the sidebar.")
            # Automatically switch to the dashboard page after submitting user info
            st.session_state.page = "Dashboard"
            st.experimental_rerun()

# Dashboard Page
elif st.session_state.page == "Dashboard":
    st.title(f"🌿 Welcome, {st.session_state.user_info.get('name', 'User')}!")
    st.header("Student Wellness Dashboard")
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
                st.info("Your burnout risk is moderate to high. You can now access the Quiz from the sidebar to get a more detailed analysis.")
        else:
            st.warning("Please enter a journal entry to analyze your mood.")


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
            st.success("Quiz submitted! You can now access your Personalized Plan from the sidebar.")
            # Automatically switch to the Personalized Plan page
            st.session_state.page = "Personalized Plan"
            st.experimental_rerun()


# Personalized Plan Page
elif st.session_state.page == "Personalized Plan":
    st.title("🍎 Personalized Diet & Workout Plan")
    risk = st.session_state.burnout_risk
    st.write(f"This plan is based on your burnout risk level of: **{risk}**")
    st.markdown("---")
    if risk == "High":
        st.subheader("Diet Plan")
        st.markdown("- **Focus on Nutrient-Dense Foods**: Incorporate foods rich in Omega-3s (like salmon and flaxseeds), magnesium (leafy greens, nuts), and B vitamins (eggs, legumes).\n- **Stay Hydrated**: Drink plenty of water throughout the day.\n- **Avoid Stimulants and Sugar**: Minimize caffeine and sugary foods that can lead to energy crashes.")
        st.subheader("Workout Plan")
        st.markdown("- **Gentle Movement**: Focus on restorative activities like light yoga or tai chi.\n- **Mindful Breathing**: Practice deep breathing exercises to calm your nervous system.\n- **Short Walks**: A 15-minute walk in nature can significantly boost your mood.")
    elif risk == "Moderate":
        st.subheader("Diet Plan")
        st.markdown("- **Balanced Macronutrients**: Ensure a good mix of complex carbohydrates, lean protein, and healthy fats in every meal.\n- **Eat Regularly**: Avoid skipping meals to maintain stable blood sugar and energy levels.\n- **Incorporate Greens**: Add a serving of green leafy vegetables to your daily diet.")
        st.subheader("Workout Plan")
        st.markdown("- **Consistent Cardio**: Aim for 20-30 minutes of brisk walking, jogging, or cycling most days of the week.\n- **Stretching**: Incorporate regular stretching or a short yoga routine to release muscle tension.\n- **Low-Intensity Workouts**: Try bodyweight exercises or light resistance training at home.")
    else: # Low risk
        st.balloons()
        st.success("You're in great shape! Your current routines are effective. Keep up the balanced diet and regular exercise.")


# Feedback Page
elif st.session_state.page == "Feedback":
    st.title("🗣️ Feedback")
    feedback = st.text_area("Please tell us about your experience with the app.")
    if st.button("Submit Feedback"):
        if feedback:
            st.success("🙏 Thank you for your valuable feedback!")
            # You can add code here to save the feedback to a file or database
        else:
            st.warning("Please enter your feedback before submitting.")











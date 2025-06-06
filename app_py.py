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

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("Navigation")

# This list will hold the pages the user can currently access.
accessible_pages = ["User Info"]

# Once user info is filled, Dashboard becomes (and stays) accessible.
if st.session_state.user_info:
    accessible_pages.append("Dashboard")

# If burnout risk is moderate/high, Quiz becomes (and stays) accessible.
if st.session_state.burnout_risk in ["Moderate", "High"]:
    accessible_pages.append("Quiz")

# Once the quiz is done, Personalized Plan and Feedback become (and stay) accessible.
if st.session_state.quiz_complete:
    # Ensure Quiz is still accessible if the user navigates away
    if "Quiz" not in accessible_pages:
        accessible_pages.append("Quiz")
    accessible_pages.append("Personalized Plan")
    accessible_pages.append("Feedback")

# Determine the default selected page in the radio button
# This prevents errors if the state changes and the current page is no longer in the accessible list
try:
    current_page_index = accessible_pages.index(st.session_state.page)
except ValueError:
    current_page_index = 0

st.session_state.page = st.sidebar.radio("Go to", accessible_pages, index=current_page_index)


# --- PAGE CONTENT ---

# User Info Page
if st.session_state.page == "User Info":
    st.title("👤 User Information")
    with st.form("user_info_form"):
        name = st.text_input("Name", value=st.session_state.user_info.get("name", ""))
        gender = st.selectbox("Gender", ["Male", "Female", "Other"], index=["Male", "Female", "Other"].index(st.session_state.user_info.get("gender", "Male")))
        age = st.number_input("Age", min_value=10, max_value=100, value=st.session_state.user_info.get("age", 18))
        submitted = st.form_submit_button("Save and Continue")
        if submitted and name:
            st.session_state.user_info = {"name": name, "gender": gender, "age": age}
            st.success("Information saved! Please select 'Dashboard' from the sidebar to proceed.")
            # NOTE: No automatic rerun. The user will click on the sidebar.

# Dashboard Page
elif st.session_state.page == "Dashboard":
    st.title(f"🌿 Welcome, {st.session_state.user_info.get('name', 'User')}!")
    st.header("Student Wellness Dashboard")
    with st.form("wellness_form"):
        st.text_area("📝 Journal Entry: How are you feeling today?", key="journal_input", height=150)
        st.number_input("🛌 Last night's sleep (hours)", min_value=0.0, max_value=24.0, step=0.5, key="sleep_hours")
        st.number_input("📱 Today's screen time (hours)", min_value=0.0, max_value=24.0, step=0.5, key="screen_time")
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
            st.progress((score + 1) / 2) # Normalizes score from [-1, 1] to [0, 1]
            st.metric("🧭 Burnout Risk Level", risk)

            if risk in ["Moderate", "High"]:
                st.info("Your burnout risk is elevated. Please navigate to the 'Quiz' in the sidebar for a deeper analysis.")
        else:
            st.warning("Please write a journal entry to analyze your mood.")

# Quiz Page
elif st.session_state.page == "Quiz":
    st.title("📝 Burnout Risk Quiz")
    with st.form("quiz_form"):
        st.write("Answer these questions based on how you've felt over the last two weeks.")
        st.session_state.quiz_answers["q1"] = st.radio("How often do you feel emotionally drained from your studies?", ["Never", "Sometimes", "Often"])
        st.session_state.quiz_answers["q2"] = st.radio("Do you find it hard to concentrate on your academic work?", ["Never", "Sometimes", "Often"])
        st.session_state.quiz_answers["q3"] = st.radio("Have you become more cynical or detached from your studies?", ["No", "A little", "Yes, very much"])
        st.session_state.quiz_answers["q4"] = st.radio("Do you feel overwhelmed by your workload?", ["Rarely", "Sometimes", "Frequently"])
        st.session_state.quiz_answers["q5"] = st.radio("Are you finding less satisfaction in your achievements?", ["No, I feel satisfied", "Sometimes", "Yes, I feel less satisfied"])
        quiz_submit = st.form_submit_button("Submit Quiz")
        
        if quiz_submit:
            st.session_state.quiz_complete = True
            st.success("Quiz submitted! Please select 'Personalized Plan' from the sidebar to see your recommendations.")
            # NOTE: No automatic rerun. User clicks on the sidebar.

# Personalized Plan Page
elif st.session_state.page == "Personalized Plan":
    st.title("🍎 Personalized Diet & Workout Plan")
    risk = st.session_state.burnout_risk
    st.write(f"This plan is based on your burnout risk level of: **{risk}**")
    st.markdown("---")
    if risk == "High":
        st.subheader("Diet Plan (Focus: Recovery & Support)")
        st.markdown("- **Focus on Nutrient-Dense Foods**: Incorporate foods rich in Omega-3s (like salmon and flaxseeds), magnesium (leafy greens, nuts), and B vitamins (eggs, legumes).\n- **Stay Hydrated**: Drink plenty of water throughout the day.\n- **Avoid Stimulants and Sugar**: Minimize caffeine and sugary foods that can lead to energy crashes and anxiety.")
        st.subheader("Workout Plan (Focus: Restoration)")
        st.markdown("- **Gentle Movement**: Focus on restorative activities like light yoga or tai chi.\n- **Mindful Breathing**: Practice 5 minutes of deep belly breathing daily to calm your nervous system.\n- **Short Walks**: A 15-minute walk in nature can significantly boost your mood without causing exhaustion.")
    elif risk == "Moderate":
        st.subheader("Diet Plan (Focus: Balance & Energy)")
        st.markdown("- **Balanced Macronutrients**: Ensure a good mix of complex carbohydrates (oats, brown rice), lean protein, and healthy fats in every meal.\n- **Eat Regularly**: Avoid skipping meals to maintain stable blood sugar and energy levels.\n- **Incorporate Greens**: Add a serving of green leafy vegetables to your daily diet for essential vitamins.")
        st.subheader("Workout Plan (Focus: Consistency)")
        st.markdown("- **Consistent Cardio**: Aim for 20-30 minutes of brisk walking, jogging, or cycling most days of the week.\n- **Stretching**: Incorporate regular stretching or a short yoga routine to release muscle tension from studying.\n- **Low-Intensity Workouts**: Try bodyweight exercises or light resistance training at home to build resilience.")
    else: # Low risk
        st.balloons()
        st.success("You're in great shape! Your current routines are effective. Keep up the balanced diet and regular exercise to maintain this state.")

# Feedback Page
elif st.session_state.page == "Feedback":
    st.title("🗣️ Feedback")
    feedback = st.text_area("Please tell us about your experience with the app or any suggestions you have.", height=150)
    if st.button("Submit Feedback"):
        if feedback:
            st.success("🙏 Thank you for your valuable feedback!")
            # You can add code here to save the feedback to a file or database
        else:
            st.warning("Please enter your feedback before submitting.")











import streamlit as st
from textblob import TextBlob

st.set_page_config(page_title="Student Wellness App", layout="centered")

# --- SESSION STATE INITIALIZATION ---
# Initialize session state only if it's the first run
if "page" not in st.session_state:
    st.session_state.page = "User Info"
    st.session_state.user_info = {}
    st.session_state.journal_input = ""
    st.session_state.sleep_hours = 8.0  # Set a reasonable default
    st.session_state.screen_time = 4.0 # Set a reasonable default
    st.session_state.workout_done = "No"
    st.session_state.mood_score = None
    st.session_state.burnout_risk = None
    st.session_state.quiz_answers = {}
    st.session_state.quiz_complete = False

# --- SIDEBAR NAVIGATION ---
# Display all pages in the sidebar from the start.
st.sidebar.title("Navigation")
pages = ["User Info", "Dashboard", "Quiz", "Personalized Plan", "Feedback"]
st.session_state.page = st.sidebar.radio("Go to", pages, key="navigation_radio")


# --- PAGE CONTENT ---

# Page 1: User Info
if st.session_state.page == "User Info":
    st.title("👤 User Information")
    st.write("Please enter your details to get started.")
    with st.form("user_info_form"):
        name = st.text_input("Name", value=st.session_state.user_info.get("name", ""))
        gender = st.selectbox("Gender", ["Male", "Female", "Other"], index=["Male", "Female", "Other"].index(st.session_state.user_info.get("gender", "Male")))
        age = st.number_input("Age", min_value=10, max_value=100, value=st.session_state.user_info.get("age", 18))
        submitted = st.form_submit_button("Save Information")

        if submitted and name:
            st.session_state.user_info = {"name": name, "gender": gender, "age": age}
            st.success("Information saved! You can now proceed to the 'Dashboard'.")
            
# Page 2: Dashboard
elif st.session_state.page == "Dashboard":
    # This is a "page guard". It checks if the prerequisite is met.
    if not st.session_state.user_info:
        st.warning("Please complete the User Information on the 'User Info' page before accessing the dashboard.")
        st.stop() # Stop rendering the rest of the page

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
            st.progress((score + 1) / 2) # Normalizes score from [-1, 1] to [0, 1]
            st.metric("🧭 Burnout Risk Level", risk)

            if risk in ["Moderate", "High"]:
                st.info("Your burnout risk is elevated. Please navigate to the 'Quiz' for a deeper analysis.")
        else:
            st.warning("Please write a journal entry to analyze your mood.")

# Page 3: Quiz
elif st.session_state.page == "Quiz":
    # Page guard
    if st.session_state.burnout_risk not in ["Moderate", "High"]:
        st.warning("The quiz is available only if your burnout risk is 'Moderate' or 'High'.")
        st.info("Please complete the analysis on the 'Dashboard' page first to determine your risk level.")
        st.stop()

    st.title("📝 Burnout Risk Quiz")
    with st.form("quiz_form"):
        st.write("Answer these questions based on how you've felt over the last two weeks.")
        st.session_state.quiz_answers["q1"] = st.radio("How often do you feel emotionally drained from your studies?", ["Never", "Sometimes", "Often"])
        st.session_state.quiz_answers["q2"] = st.radio("Do you find it hard to concentrate on your academic work?", ["Never", "Sometimes", "Often"])
        st.session_state.quiz_answers["q3"] = st.radio("Have you become more cynical or detached from your studies?", ["No", "A little", "Yes, very much"])
        quiz_submit = st.form_submit_button("Submit Quiz")
        
        if quiz_submit:
            st.session_state.quiz_complete = True
            st.success("Quiz submitted! Please select 'Personalized Plan' from the sidebar.")

# Page 4: Personalized Plan
elif st.session_state.page == "Personalized Plan":
    # Page guard
    if not st.session_state.quiz_complete:
        st.warning("Please complete the 'Quiz' to generate your personalized plan.")
        st.stop()

    st.title("🍎 Personalized Diet & Workout Plan")
    risk = st.session_state.burnout_risk
    st.write(f"This plan is based on your burnout risk level of: **{risk}**")
    st.markdown("---")
    # Content remains the same...

# Page 5: Feedback
elif st.session_state.page == "Feedback":
    # Page guard
    if not st.session_state.quiz_complete:
        st.warning("We'd love your feedback after you have gone through the full process.")
        st.info("Please complete the 'Quiz' and view your 'Personalized Plan' first.")
        st.stop()

    st.title("🗣️ Feedback")
    feedback = st.text_area("Please tell us about your experience or any suggestions you have.", height=150)
    if st.button("Submit Feedback"):
        if feedback:
            st.success("🙏 Thank you for your valuable feedback!")
        else:
            st.warning("Please enter feedback before submitting.")











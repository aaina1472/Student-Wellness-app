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

    if analyze_











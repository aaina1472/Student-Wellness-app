import streamlit as st
from textblob import TextBlob

st.set_page_config(page_title="Student Wellness App", layout="centered")

# --- Sidebar Navigation ---
page = st.sidebar.radio("Navigation", ["User Info", "Mood Analyzer", "Quiz", "Personalized Plan", "Feedback"])

# --- Page: User Info ---
if page == "User Info":
    st.title("👤 User Information")
    with st.form("user_info_form"):
        name = st.text_input("Name")
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        age = st.number_input("Age", min_value=10, max_value=100, value=18)
        submitted = st.form_submit_button("Save Information")

    if submitted:
        if name.strip() == "":
            st.warning("Please enter your name.")
        else:
            st.success(f"Information saved! Welcome, {name}.")

            # Save info to session state for later use if needed
            st.session_state.user_info = {"name": name, "gender": gender, "age": age}

# --- Page: Mood Analyzer ---
elif page == "Mood Analyzer":
    st.title("🌿 Student Wellness Dashboard")
    if "user_info" in st.session_state:
        st.write(f"Welcome back, **{st.session_state.user_info['name']}!**")
    else:
        st.info("Please enter your information in the User Info tab for a personalized experience.")

    st.markdown("Write about your day or feelings, and get personalized mood analysis and wellness support.")

    def analyze_mood(text):
        blob = TextBlob(str(text))
        return round(blob.sentiment.polarity, 2)

    journal_input = st.text_area("📝 Write your journal entry here:")

    if st.button("Analyze My Mood"):
        if journal_input.strip():
            score = analyze_mood(journal_input)
            st.write(f"🧠 **Mood Score:** `{score}`")

            if score > 0.3:
                burnout_risk = "Low"
            elif score > 0.0:
                burnout_risk = "Moderate"
            else:
                burnout_risk = "High"

            st.metric("🧭 Burnout Risk Level", burnout_risk)

            if burnout_risk in ["Moderate", "High"]:
                st.markdown("---")
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
                - [The Daily Shine – Mental Health & Mindfulness](https://www.theshineapp.com/)
                - [The Happiness Lab with Dr. Laurie Santos](https://www.happinesslab.fm/)
                - [Mindful Muslim Podcast](https://mindful-muslimah.com/podcast/)
                """)

            else:
                st.success("✅ You're doing great! Keep journaling to maintain emotional well-being.")
        else:
            st.warning("Please enter some text to analyze.")

# --- Page: Quiz ---
elif page == "Quiz":
    st.title("📝 Burnout Risk Quiz")
    st.write("Here you can add your quiz questions and logic...")

# --- Page: Personalized Plan ---
elif page == "Personalized Plan":
    st.title("🍎 Personalized Diet & Workout Plan")
    st.write("Here you can show personalized plans based on quiz or mood score...")

# --- Page: Feedback ---
elif page == "Feedback":
    st.title("🗣️ Feedback")
    st.write("Let users send feedback here...")













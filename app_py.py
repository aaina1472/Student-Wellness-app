import streamlit as st
from textblob import TextBlob

st.set_page_config(page_title="Student Wellness App", layout="centered")

st.title("🌿 Student Wellness Dashboard")
st.markdown("Write about your day or feelings, and get personalized mood analysis and wellness support.")

# Initialize session state only if keys are missing
if "journal_input" not in st.session_state:
    st.session_state.journal_input = ""
if "sleep_hours" not in st.session_state:
    st.session_state.sleep_hours = 0.0
if "screen_time" not in st.session_state:
    st.session_state.screen_time = 0.0
if "workout_done" not in st.session_state:
    st.session_state.workout_done = "No"
if "mood_score" not in st.session_state:
    st.session_state.mood_score = None
if "burnout_risk" not in st.session_state:
    st.session_state.burnout_risk = None

# Define mood analyzer
def analyze_mood(text):
    blob = TextBlob(str(text))
    return round(blob.sentiment.polarity, 2)

# User Inputs
st.session_state.journal_input = st.text_area("📝 Write your journal entry here:", value=st.session_state.journal_input)
st.session_state.sleep_hours = st.number_input("🛌 Sleep hours", min_value=0.0, max_value=24.0, step=0.5, value=st.session_state.sleep_hours)
st.session_state.screen_time = st.number_input("📱 Screen time (in hours)", min_value=0.0, max_value=24.0, step=0.5, value=st.session_state.screen_time)
st.session_state.workout_done = st.selectbox("🏋️‍♂️ Workout done today?", options=["No", "Yes"], index=0 if st.session_state.workout_done == "No" else 1)

# Buttons
col1, col2 = st.columns(2)
with col1:
    analyze_clicked = st.button("Analyze My Mood")
with col2:
    refresh_clicked = st.button("🔄 Refresh")

# Refresh button action
if refresh_clicked:
    for key in ["journal_input", "sleep_hours", "screen_time", "workout_done", "mood_score", "burnout_risk"]:
        del st.session_state[key]
    st.experimental_rerun()

# Analyze action
if analyze_clicked:
    journal = st.session_state.journal_input.strip()
    if journal:
        score = analyze_mood(journal)
        st.session_state.mood_score = score

        if score > 0.3:
            burnout_risk = "Low"
        elif score > 0.0:
            burnout_risk = "Moderate"
        else:
            burnout_risk = "High"
        st.session_state.burnout_risk = burnout_risk

        st.markdown("---")
        st.subheader("📊 Mood & Burnout Report")
        st.write(f"🧠 **Mood Score:** `{score}`")
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
            - [The Daily Shine – Mental Health & Mindfulness](https://www.theshineapp.com/)
            - [The Happiness Lab with Dr. Laurie Santos](https://www.happinesslab.fm/)
            - [Mindful Muslim Podcast](https://mindful-muslimah.com/podcast/)
            """)
        else:
            st.success("✅ You're doing great! Keep journaling to maintain emotional well-being.")
    else:
        st.warning("Please write something in your journal before analyzing.")

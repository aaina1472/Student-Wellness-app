import streamlit as st
from textblob import TextBlob

st.set_page_config(page_title="Student Wellness App", layout="centered")

st.title("🌿 Student Wellness Dashboard")
st.markdown("Write about your day or feelings, and get personalized mood analysis and wellness support.")

# Initialize session state defaults
st.session_state.setdefault("journal_input", "")
st.session_state.setdefault("sleep_hours", 0.0)
st.session_state.setdefault("screen_time", 0.0)
st.session_state.setdefault("workout_done", "No")
st.session_state.setdefault("mood_score", None)
st.session_state.setdefault("burnout_risk", None)

# Mood analyzer function
def analyze_mood(text):
    blob = TextBlob(text)
    return round(blob.sentiment.polarity, 2)

# Main input form
with st.form("wellness_form"):
    journal_input = st.text_area("📝 Write your journal entry here:", value=st.session_state.journal_input)
    sleep_hours = st.number_input("🛌 Sleep hours", min_value=0.0, max_value=24.0, step=0.5, value=st.session_state.sleep_hours)
    screen_time = st.number_input("📱 Screen time (hours)", min_value=0.0, max_value=24.0, step=0.5, value=st.session_state.screen_time)
    workout_done = st.selectbox("🏋️ Workout today?", ["No", "Yes"], index=0 if st.session_state.workout_done == "No" else 1)

    col1, col2 = st.columns(2)
    with col1:
        analyze_button = st.form_submit_button("Analyze")
    with col2:
        reset_button = st.form_submit_button("🔄 Reset")

# Handle reset
if reset_button:
    st.session_state.journal_input = ""
    st.session_state.sleep_hours = 0.0
    st.session_state.screen_time = 0.0
    st.session_state.workout_done = "No"
    st.session_state.mood_score = None
    st.session_state.burnout_risk = None
    st.success("✅ Form has been reset. You can enter new info.")

# Handle analysis
if analyze_button:
    journal = journal_input.strip()
    if journal:
        score = analyze_mood(journal)
        st.session_state.mood_score = score
        st.session_state.burnout_risk = (
            "Low" if score > 0.3 else
            "Moderate" if score > 0.0 else
            "High"
        )

        # Save back values
        st.session_state.journal_input = journal
        st.session_state.sleep_hours = sleep_hours
        st.session_state.screen_time = screen_time
        st.session_state.workout_done = workout_done

        # Output section
        st.markdown("---")
        st.subheader("📊 Mood & Burnout Report")
        st.write(f"🧠 **Mood Score:** `{score}`")
        st.metric("🧭 Burnout Risk Level", st.session_state.burnout_risk)

        # Recommendations
        if st.session_state.burnout_risk in ["Moderate", "High"]:
            st.subheader("🧘 Wellness Recommendations")

            if st.session_state.burnout_risk == "High":
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


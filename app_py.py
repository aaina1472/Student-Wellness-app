import streamlit as st
from textblob import TextBlob

st.set_page_config(page_title="Student Wellness App", layout="centered")

st.title("🌿 Student Wellness Dashboard")
st.markdown("Write about your day or feelings, and get personalized mood analysis and wellness support.")

# Initialize default session state values
for key, default in {
    "journal_input": "",
    "sleep_hours": 0.0,
    "screen_time": 0.0,
    "workout_done": "No",
    "mood_score": None,
    "burnout_risk": None
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# Mood analyzer function
def analyze_mood(text):
    blob = TextBlob(text)
    return round(blob.sentiment.polarity, 2)

# UI form for input
with st.form("wellness_form"):
    st.text_area(
        "📝 Write your journal entry here:",
        key="journal_input",
        placeholder="Start writing...",
        height=150
    )
    st.number_input(
        "🛌 How many hours did you sleep last night?",
        min_value=0.0,
        max_value=24.0,
        step=0.5,
        key="sleep_hours"
    )
    st.number_input(
        "📱 How many hours did you spend on screen today?",
        min_value=0.0,
        max_value=24.0,
        step=0.5,
        key="screen_time"
    )
    st.selectbox(
        "🏋️ Workout today?",
        ["No", "Yes"],
        key="workout_done"
    )

    col1, col2 = st.columns(2)
    with col1:
        analyze_button = st.form_submit_button("Analyze")
    with col2:
        reset_button = st.form_submit_button("🔄 Reset")

# Reset action
if reset_button:
    st.session_state.journal_input = ""
    st.session_state.sleep_hours = 0.0
    st.session_state.screen_time = 0.0
    st.session_state.workout_done = "No"
    st.session_state.mood_score = None
    st.session_state.burnout_risk = None
    st.success("✅ Form has been reset.")

# Analyze action
if analyze_button:
    journal = st.session_state.journal_input.strip()
    if journal:
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

        # Emoji based on mood
        emoji = "😄" if score > 0.3 else "😐" if score > 0.0 else "😞"
        st.write(f"🧠 **Mood Score:** `{score}` {emoji}")
        st.progress((score + 1) / 2)  # Convert polarity (-1 to 1) into 0 to 1

        st.metric("🧭 Burnout Risk Level", burnout_risk)

        # Recommendations
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
    else:
        st.warning("⚠️ Please write something in your journal before analyzing.")


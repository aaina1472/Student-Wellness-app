import streamlit as st
from textblob import TextBlob

st.set_page_config(page_title="Student Wellness App", layout="centered")

st.title("🌿 Student Wellness Dashboard")
st.markdown("Write about your day or feelings, and get personalized mood analysis and wellness support.")

# Mood analyzer using TextBlob
def analyze_mood(text):
    blob = TextBlob(str(text))
    return round(blob.sentiment.polarity, 2)

# Function to reset session state variables
def reset_inputs():
    st.session_state.journal_input = ""
    st.session_state.sleep_hours = 0.0
    st.session_state.screen_time = 0.0
    st.session_state.workout_done = "No"
    st.session_state.mood_score = None
    st.session_state.burnout_risk = None

# Initialize session state variables if they don't exist
if "journal_input" not in st.session_state:
    reset_inputs()

# Input widgets with session state for persistence and refresh functionality
journal_input = st.text_area("📝 Write your journal entry here:", value=st.session_state.journal_input, key="journal_input")
sleep_hours = st.number_input("🛌 How many hours did you sleep last night?", min_value=0.0, max_value=24.0, value=st.session_state.sleep_hours, step=0.5, key="sleep_hours")
screen_time = st.number_input("📱 How many hours did you spend on screen today?", min_value=0.0, max_value=24.0, value=st.session_state.screen_time, step=0.5, key="screen_time")
workout_done = st.selectbox("🏋️‍♂️ Did you workout today?", options=["No", "Yes"], index=0 if st.session_state.workout_done == "No" else 1, key="workout_done")

col1, col2 = st.columns(2)
with col1:
    analyze_clicked = st.button("Analyze My Mood")
with col2:
    refresh_clicked = st.button("Refresh")

# Refresh button logic: reset inputs and clear outputs
if refresh_clicked:
    reset_inputs()
    st.experimental_rerun()

if analyze_clicked:
    if journal_input.strip():
        score = analyze_mood(journal_input)
        st.session_state.mood_score = score

        # Display inputs summary
        st.markdown("---")
        st.subheader("📝 Your Input Summary")
        st.write(f"**Journal Entry:** {journal_input}")
        st.write(f"**Sleep Hours:** {sleep_hours}")
        st.write(f"**Screen Time (hours):** {screen_time}")
        st.write(f"**Workout Done:** {workout_done}")

        st.markdown("---")
        st.write(f"🧠 **Mood Score:** `{score}`")

        # Determine burnout risk level (can also factor inputs here if desired)
        if score > 0.3:
            burnout_risk = "Low"
        elif score > 0.0:
            burnout_risk = "Moderate"
        else:
            burnout_risk = "High"

        st.session_state.burnout_risk = burnout_risk
        st.metric("🧭 Burnout Risk Level", burnout_risk)

        # Recommend wellness content for Moderate or High risk
        if burnout_risk in ["Moderate", "High"]:
            st.markdown("---")
            st.subheader("🧘 Wellness Recommendations")

            if burnout_risk == "High":
                st.error("⚠️ High Burnout Risk Detected. Please take care of your mental health.")

            # Music
            st.markdown("### 🎵 Relaxing Music")
            st.markdown("""
            <iframe width="100%" height="80" src="https://www.youtube.com/embed/2OEL4P1Rz04?autoplay=1&loop=1&playlist=2OEL4P1Rz04" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>
            """, unsafe_allow_html=True)

            # Meditation
            st.markdown("### 🧘 Guided Meditation")
            st.video("https://www.youtube.com/watch?v=inpok4MKVLM")

            # Podcast
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






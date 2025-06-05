import streamlit as st
from textblob import TextBlob

st.set_page_config(page_title="Student Wellness App", layout="centered")

st.title("🌿 Student Wellness Dashboard")
st.markdown("Write about your day or feelings, and get personalized mood analysis and wellness support.")

# Mood analyzer using TextBlob
def analyze_mood(text):
    blob = TextBlob(str(text))
    return round(blob.sentiment.polarity, 2)

# Journal input from user
journal_input = st.text_area("📝 Write your journal entry here:")
if st.button("Analyze My Mood"):
    if journal_input.strip():
        score = analyze_mood(journal_input)
        st.write(f"🧠 **Mood Score:** `{score}`")

        # Determine burnout risk level
        if score > 0.3:
            burnout_risk = "Low"
        elif score > 0.0:
            burnout_risk = "Moderate"
        else:
            burnout_risk = "High"

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





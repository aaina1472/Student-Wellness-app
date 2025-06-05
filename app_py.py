import streamlit as st
import pandas as pd
from textblob import TextBlob
import matplotlib.pyplot as plt

st.set_page_config(page_title="Student Wellness App", layout="centered")

st.title("🌿 Student Wellness Dashboard")
st.markdown("Analyze your journal entries to track mood and burnout risk.")

uploaded_file = st.file_uploader("Upload your journal entries CSV file", type=["csv"])
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    
    # Check required columns
    if 'journal_text' not in df.columns or 'date' not in df.columns:
        st.error("CSV must contain 'journal_text' and 'date' columns.")
        st.stop()

    # Convert date to datetime
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    if df['date'].isnull().all():
        st.error("Date column cannot be parsed as dates.")
        st.stop()

else:
    st.warning("Please upload a CSV file to continue.")
    st.stop()


def analyze_mood(text):
    blob = TextBlob(str(text))
    return round(blob.sentiment.polarity, 2)


journal_input = st.text_area("Write your journal entry here:")
if st.button("Analyze"):
    if journal_input.strip() == "":
        st.warning("Please enter some text to analyze.")
    else:
        score = analyze_mood(journal_input)
        st.write(f"🧠 Mood Score: {score}")

df['Mood Score'] = df['journal_text'].apply(analyze_mood)

avg_mood = df['Mood Score'].mean()

if avg_mood > 0.3:
    burnout_risk = "Low"
elif avg_mood > 0.0:
    burnout_risk = "Moderate"
else:
    burnout_risk = "High"

st.subheader("Summary")
st.metric(label="Average Mood Score", value=f"{avg_mood:.2f}")
st.metric(label="Burnout Risk Level", value=burnout_risk)

st.subheader("Mood Trend Over Time")
fig, ax = plt.subplots(figsize=(8,4))
ax.plot(df['date'], df['Mood Score'], marker='o', linestyle='-', color='teal')
ax.set_xlabel("Date")
ax.set_ylabel("Mood Score")
plt.xticks(rotation=45)
ax.grid(True)
st.pyplot(fig)

if burnout_risk in ["Moderate", "High"]:
    st.markdown("---")
    st.subheader("🧘‍♀️ Take a Break — Resources for You")

    if burnout_risk == "High":
        st.error("⚠️ High Burnout Risk Detected! Please take care of yourself.")

    st.markdown("### 🎵 Calming Music to Relax")
    st.markdown("""
    <iframe width="100%" height="80" src="https://www.youtube.com/embed/2OEL4P1Rz04?autoplay=1&loop=1&playlist=2OEL4P1Rz04" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>
    """, unsafe_allow_html=True)

    st.markdown("### Helpful Articles")
    st.markdown("""
    - [Managing Burnout - Mayo Clinic](https://www.mayoclinic.org/healthy-lifestyle/adult-health/in-depth/burnout/art-20488374)
    - [Stress Management Tips - CDC](https://www.cdc.gov/mentalhealth/stress-coping/cope-with-stress/index.html)
    - [Meditation Techniques - Headspace](https://www.headspace.com/meditation/techniques)
    """)

else:
    st.success("😊 Your burnout risk level is low. Keep up the good work!")




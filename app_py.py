import streamlit as st
import pandas as pd
from textblob import TextBlob
import matplotlib.pyplot as plt

st.set_page_config(page_title="Student Wellness App", layout="centered")

st.title("🌿 Student Wellness Dashboard")
st.markdown("Analyze your journal entries to track mood and burnout risk.")

# Upload CSV or load static
uploaded_file = st.file_uploader("Upload your journal entries CSV file", type=["csv"])
if uploaded_file:
    df = pd.read_csv(uploaded_file)
else:
    st.warning("Please upload a CSV file to continue.")
    st.stop()

# Basic sentiment and mood scoring
def analyze_mood(text):
    blob = TextBlob(str(text))
    return blob.sentiment.polarity

df['Mood Score'] = df['journal_text'].apply(analyze_mood)

# Classify burnout risk based on average mood score
avg_mood = df['Mood Score'].mean()

if avg_mood > 0.3:
    burnout_risk = "Low"
elif avg_mood > 0.0:
    burnout_risk = "Moderate"
else:
    burnout_risk = "High"

# Show summary metrics
st.subheader("Summary")
st.metric(label="Average Mood Score", value=f"{avg_mood:.2f}")
st.metric(label="Burnout Risk Level", value=burnout_risk)

# Mood trend plot
st.subheader("Mood Trend Over Time")
plt.figure(figsize=(8,4))
plt.plot(df['date'], df['Mood Score'], marker='o', linestyle='-', color='teal')
plt.xlabel("Date")
plt.ylabel("Mood Score")
plt.xticks(rotation=45)
plt.grid(True)
st.pyplot(plt)

# Helpful resources & music for moderate or high burnout risk
if burnout_risk in ["Moderate", "High"]:
    st.markdown("---")
    st.subheader("🧘‍♀️ Take a Break — Resources for You")

    if burnout_risk == "High":
        st.error("⚠️ High Burnout Risk Detected! Please take care of yourself.")

    # Calming music embedded using an iframe or external link
    st.markdown("### 🎵 Calming Music to Relax")
    st.markdown("""
    <iframe width="100%" height="80" src="https://www.youtube.com/embed/2OEL4P1Rz04?autoplay=1&loop=1&playlist=2OEL4P1Rz04" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>
    """, unsafe_allow_html=True)

    # Useful links
    st.markdown("### Helpful Articles")
    st.markdown("""
    - [Managing Burnout - Mayo Clinic](https://www.mayoclinic.org/healthy-lifestyle/adult-health/in-depth/burnout/art-20488374)
    - [Stress Management Tips - CDC](https://www.cdc.gov/mentalhealth/stress-coping/cope-with-stress/index.html)
    - [Meditation Techniques - Headspace](https://www.headspace.com/meditation/techniques)
    """)

else:
    st.success("😊 Your burnout risk level is low. Keep up the good work!")



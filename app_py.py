import streamlit as st
import pandas as pd
from textblob import TextBlob

st.set_page_config(page_title="Student Wellness App", layout="centered")

st.title("🌿 Student Wellness Dashboard")
st.markdown("Analyze your journal entries to track mood and get wellness support.")

# Upload CSV with journal_text column
uploaded_file = st.file_uploader("Upload your journal entries CSV file", type=["csv"])
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    
    # Validate expected column
    if 'journal_text' not in df.columns:
        st.error("CSV must contain a 'journal_text' column.")
        st.stop()
else:
    st.warning("Please upload a CSV file to continue.")
    st.stop()

# Mood analyzer using TextBlob
def analyze_mood(text):
    blob = TextBlob(str(text))
    return round(blob.sentiment.polarity, 2)

# Analyze all entries in uploaded file
df['Mood Score'] = df['journal_text'].apply(analyze_mood)

# Journal input from user (optional)
st.subheader("Try it Yourself:")
journal_input = st.text_area("Write your own journal entry:")
if st.button("Analyze My Entry"):
    if journal_input.strip():
        score = analyze_mood(journal_input)
        st.write(f"🧠 Your Mood Score: `{score}`")
    else:
        st.warning("Please enter some text to analyze.")

# Calculate burnout risk based on overall mood
avg_mood = df['Mood Score'].mean()

if avg_mood > 0.3:
    burnout_risk = "Low"
elif avg_mood > 0.0:
    burnout_risk = "Moderate"
else:
    burnout_risk = "High"

# Summary section
st.subheader("📊 Summary from Uploaded Journal Entries")
st.metric("Average Mood Score", f"{avg_mood:.2f}")
st.metric("Estimated Burnout Risk", burnout_risk)

# Suggest wellness content
if burnout_risk in ["Moderate", "High"]:
    st.markdown("---")
    st.subheader("🧘 Wellness Recommendations")

    if burnout_risk == "High":
        st.error("⚠️ High Burnout Risk Detected. Please prioritize self-care.")

    st.markdown("### 🎵 Relaxing Music")
    st.markdown("""
    <iframe width="100%" height="80" src="https://www.youtube.com/embed/2OEL4P1Rz04?autoplay=1&loop=1&playlist=2OEL4P1Rz04" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>
    """, unsafe_allow_html=True)

    st.markdown("### 🧘 Guided Meditation")
    st.video("https://www.youtube.com/watch?v=inpok4MKVLM")

    st.markdown("### Helpful Reads")
    st.markdown("""
    - [Manage Burnout - Mayo Clinic](https://www.mayoclinic.org/healthy-lifestyle/adult-health/in-depth/burnout/art-20488374)  
    - [Coping with Stress - CDC](https://www.cdc.gov/mentalhealth/stress-coping/cope-with-stress/index.html)  
    - [Mindfulness for Beginners](https://www.headspace.com/mindfulness)  
    """)

else:
    st.success("✅ Burnout risk is low. You're doing well — keep journaling!")




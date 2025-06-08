import streamlit as st
import pandas as pd
from textblob import TextBlob
import os
import csv
from streamlit_lottie import st_lottie
import requests
import altair as alt
from datetime import datetime

# ========== Utility Functions ==========
@st.cache_data(ttl=3600)
def load_lottie_url(url):
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except Exception:
        return None

def parse_time(t):
    return datetime.strptime(t.split(" - ")[0], "%I:%M %p")

def get_routine_df():
    routine = [
        {"Time": "6:00 AM - 7:00 AM", "Activity": "Wake up & Morning exercise (stretch, yoga)"},
        {"Time": "7:00 AM - 7:30 AM", "Activity": "Healthy breakfast (include green veggies, fruits)"},
        {"Time": "7:30 AM - 9:00 AM", "Activity": "Focused study session"},
        {"Time": "9:00 AM - 9:15 AM", "Activity": "Short break (walk/stretch)"},
        {"Time": "9:15 AM - 11:00 AM", "Activity": "Study / Assignments"},
        {"Time": "11:00 AM - 12:00 PM", "Activity": "Light snack & rest"},
        {"Time": "12:00 PM - 1:00 PM", "Activity": "Lunch (balanced with veggies and protein)"},
        {"Time": "1:00 PM - 2:00 PM", "Activity": "Power nap or relaxation"},
        {"Time": "2:00 PM - 4:00 PM", "Activity": "Study or project work"},
        {"Time": "4:00 PM - 4:30 PM", "Activity": "Physical activity (walk, cycling, sport)"},
        {"Time": "4:30 PM - 5:00 PM", "Activity": "Healthy snack"},
        {"Time": "5:00 PM - 7:00 PM", "Activity": "Study / Revision"},
        {"Time": "7:00 PM - 8:00 PM", "Activity": "Dinner (include green vegetables)"},
        {"Time": "8:00 PM - 9:00 PM", "Activity": "Leisure time (reading, hobbies)"},
        {"Time": "9:00 PM - 10:00 PM", "Activity": "Prepare for next day & relax"},
        {"Time": "10:00 PM", "Activity": "Sleep early for recovery"},
    ]
    df = pd.DataFrame(routine)
    df['Start Time'] = df['Time'].apply(lambda x: parse_time(x))
    df['End Time'] = df['Time'].apply(lambda x: datetime.strptime(x.split(" - ")[1], "%I:%M %p") if " - " in x else parse_time(x))
    return df

def display_routine_chart(df):
    chart = alt.Chart(df).mark_bar().encode(
        x=alt.X('Start Time:T', axis=alt.Axis(title='Time of Day', format='%I:%M %p')),
        x2='End Time:T',
        y=alt.Y('Activity:N', sort=None),
        color=alt.Color('Activity:N', legend=None)
    ).properties(
        height=400,
        width=700,
        title='Daily Routine Timeline'
    )
    st.altair_chart(chart, use_container_width=True)

def motivational_quote():
    quotes = [
        "🌟 *Believe you can and you're halfway there.*",
        "🌱 *Small steps every day lead to big change.*",
        "💪 *Your only limit is your mind.*",
        "🌞 *A fresh mind is a focused mind.*"
    ]
    st.markdown(f"**Motivational Quote of the Day:** {quotes[hash(st.session_state.get('name', '')) % len(quotes)]}")

# ========== App Initialization ==========
st.set_page_config(page_title="Mood Predictor App", layout="centered")
os.makedirs("data", exist_ok=True)

# Session State
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'User Info'

# ========== Navigation ==========
st.sidebar.title("Navigation")
pages = ["User Info", "Dashboard", "Suggestions", "Feedback"]
current_idx = pages.index(st.session_state.current_page)

for i, page in enumerate(pages):
    if i <= current_idx:
        if st.sidebar.button(f"{i+1}. {page}", key=page):
            st.session_state.current_page = page
    else:
        st.sidebar.markdown(f"{i+1}. {page} 🔒")

def go_next():
    next_idx = pages.index(st.session_state.current_page) + 1
    if next_idx < len(pages):
        st.session_state.current_page = pages[next_idx]

# ========== Page 1: User Info ==========
if st.session_state.current_page == 'User Info':
    st.title("User Information")
    st.markdown("Please fill in your details to get started")

    animation = load_lottie_url("https://assets2.lottiefiles.com/packages/lf20_1pxqjqps.json")
    if animation:
        st_lottie(animation, height=220, key="character_animation")

    name = st.text_input("Your Name")
    age = st.number_input("Your Age", min_value=10, max_value=100, step=1)
    gender = st.selectbox("Select your gender:", ["Male", "Female", "Other", "Prefer not to say"])

    if st.button("Continue to Dashboard"):
        if name:
            st.session_state.name = name
            st.session_state.age = age
            st.session_state.gender = gender
            with open("data/user_info.csv", "a", newline="") as f:
                csv.writer(f).writerow([name, age, gender])
            go_next()
        else:
            st.warning("Please enter your name to continue.")

# ========== Page 2: Dashboard ==========
elif st.session_state.current_page == 'Dashboard':
    st.title("Mood Dashboard")
    journal_entry = st.text_area("Write your journal entry here:")

    if 'mood_analyzed' not in st.session_state:
        st.session_state.mood_analyzed = False

    if st.button("Analyze My Mood"):
        if journal_entry.strip():
            score = TextBlob(journal_entry).sentiment.polarity
            risk = "Low" if score > 0.3 else "Moderate" if score > 0.0 else "High"
            st.metric("Mood Score", f"{score:.2f}")
            st.metric("Burnout Risk", risk)

            st.session_state.avg_mood = score
            st.session_state.risk = risk
            st.session_state.mood_analyzed = True

            if risk == "Low":
                flower = load_lottie_url("https://assets4.lottiefiles.com/packages/lf20_touohxv0.json")
                if flower: st_lottie(flower, height=150)

            with open("data/journal_entries.csv", "a", newline="") as f:
                csv.writer(f).writerow([st.session_state.name, journal_entry, score])
        else:
            st.warning("Please write something first!")

    if st.session_state.mood_analyzed:
        if st.button("Continue to Suggestions"):
            go_next()

        # Download Option
        st.download_button("📥 Download My Journal Data",
                           data=open("data/journal_entries.csv", "rb"),
                           file_name="journal_entries.csv")

# ========== Page 3: Suggestions ==========
elif st.session_state.current_page == 'Suggestions':
    st.title("🧘 Wellness Suggestions")

    risk = st.session_state.get('risk', 'Moderate')
    st.subheader("You might be feeling overwhelmed." if risk in ["High", "Moderate"] else "You're doing great! Keep it up 🥳")

    st.video("https://www.youtube.com/watch?v=2OEL4P1Rz04")
    st.markdown("[🩺 Burnout Tips from CDC](https://www.cdc.gov/mentalhealth/stress-coping/cope-with-stress/index.html)")

    if risk in ["High", "Moderate"]:
        st.markdown("### 🗓️ Recommended Daily Routine:")
        routine_df = get_routine_df()
        st.table(routine_df)
        display_routine_chart(routine_df)

        # Add motivational content
        motivational_quote()
        st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3", format="audio/mp3")

    if st.button("Continue to Feedback"):
        go_next()

# ========== Page 4: Feedback ==========
elif st.session_state.current_page == 'Feedback':
    st.title("💬 Feedback")
    st.write("Thank you for using our Mood Prediction App!")

    feedback = st.text_area("How was your experience?")
    if st.button("Submit Feedback"):
        with open("data/feedback.csv", "a", newline="") as f:
            csv.writer(f).writerow([st.session_state.get("name", "Anonymous"), feedback])
        st.success("Thanks for your feedback! 🌟")

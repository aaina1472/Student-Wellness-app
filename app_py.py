import streamlit as st
import pandas as pd
from textblob import TextBlob
from streamlit_lottie import st_lottie
import requests
import csv

st.set_page_config(page_title="Student Wellness App", layout="centered")

# Initialize session state
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'User Info'
if 'name' not in st.session_state:
    st.session_state.name = ""
if 'avg_mood' not in st.session_state:
    st.session_state.avg_mood = 0
if 'risk' not in st.session_state:
    st.session_state.risk = "Unknown"
if 'mood_analyzed' not in st.session_state:
    st.session_state.mood_analyzed = False

# Navigation
st.sidebar.title("🧭 Navigation")
pages = ["User Info", "Dashboard", "Quiz", "Wellness Plan", "Feedback"]
for i, page in enumerate(pages):
    if i == 0 or all(st.session_state.get(pages[j].lower().replace(" ", "_") + "_done", False) for j in range(i)):
        if st.sidebar.button(page):
            st.session_state.current_page = page

# Navigation Helper
def complete_page():
    current = st.session_state.current_page.lower().replace(" ", "_")
    st.session_state[current + "_done"] = True
    current_idx = pages.index(st.session_state.current_page)
    if current_idx < len(pages) - 1:
        st.session_state.current_page = pages[current_idx + 1]

# Load Lottie animation
def load_lottie_url(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# ========== Page 1: User Info ==========
if st.session_state.current_page == "User Info":
    st.title("🧍‍♂️ User Info")
    st.session_state.name = st.text_input("What's your name?")
    age = st.number_input("Age", min_value=10, max_value=100, step=1)

    if st.button("Continue"):
        if st.session_state.name.strip() != "":
            complete_page()
        else:
            st.warning("Please enter your name.")

# ========== Page 2: Dashboard ==========
elif st.session_state.current_page == "Dashboard":
    st.title("📊 Wellness Dashboard")
    st.write("Welcome,", st.session_state.name)

    journal_entry = st.text_area("How was your day? Write your thoughts here.")
    sleep_hours = st.slider("Hours of Sleep", 0, 12, 6)
    screen_time = st.slider("Screen Time (in hours)", 0, 12, 4)
    workout_done = st.radio("Did you workout today?", ["Yes", "No"])

    if st.button("Analyze My Mood"):
        if journal_entry.strip():
            # 1. NLP Sentiment Analysis
            polarity = TextBlob(journal_entry).sentiment.polarity

            # 2. Encode structured inputs
            sleep_score = sleep_hours
            workout_score = 1 if workout_done == "Yes" else 0
            screen_score = screen_time

            # 3. Combine all into a "Mood Score"
            mood_score = (
                (0.4 * polarity) + 
                (0.3 * (sleep_score / 10)) + 
                (0.2 * workout_score) - 
                (0.2 * (screen_score / 10))
            )

            # 4. Classify Mood
            if mood_score > 0.4:
                mood = "Happy 😊"
                risk = "Low"
            elif mood_score > 0.1:
                mood = "Okay 🙂"
                risk = "Moderate"
            else:
                mood = "Stressed 😟"
                risk = "High"

            # 5. Display the result
            st.metric("Mood", mood)
            st.metric("Mood Score", f"{mood_score:.2f}")
            st.metric("Burnout Risk", risk)

            st.session_state.avg_mood = mood_score
            st.session_state.risk = risk
            st.session_state.mood_analyzed = True

            if risk == "Low":
                flower_animation = load_lottie_url("https://assets4.lottiefiles.com/packages/lf20_touohxv0.json")
                if flower_animation:
                    st_lottie(flower_animation, height=150, key="flower_animation")
                else:
                    st.warning("⚠️ Flower animation failed to load.")

            # Save data
            with open("data/journal_entries.csv", "a", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([st.session_state.name, journal_entry, mood_score])

            complete_page()
        else:
            st.warning("Please enter something in your journal to analyze.")

# ========== Page 3: Quiz ==========
elif st.session_state.current_page == "Quiz":
    st.title("📝 Self-Check Quiz")

    st.write("Answer these questions honestly:")
    q1 = st.radio("Do you feel energetic most of the day?", ["Yes", "No"])
    q2 = st.radio("Are you able to focus well on tasks?", ["Yes", "No"])
    q3 = st.radio("Do you feel anxious frequently?", ["Yes", "No"])
    q4 = st.radio("Are you satisfied with your current routine?", ["Yes", "No"])
    q5 = st.radio("Do you get enough breaks during your day?", ["Yes", "No"])

    if st.button("Submit Quiz"):
        st.session_state.quiz_score = sum([
            1 if q1 == "Yes" else 0,
            1 if q2 == "Yes" else 0,
            0 if q3 == "Yes" else 1,
            1 if q4 == "Yes" else 0,
            1 if q5 == "Yes" else 0,
        ])
        complete_page()

# ========== Page 4: Personalized Plan ==========
elif st.session_state.current_page == "Wellness Plan":
    st.title("🌱 Personalized Wellness Plan")

    mood_score = st.session_state.avg_mood
    quiz_score = st.session_state.get("quiz_score", 2)

    if mood_score > 0.4 and quiz_score >= 4:
        st.success("You're doing well! Here's how to stay consistent:")
        st.markdown("""
        - Maintain 7–9 hours of sleep  
        - Keep exercising regularly  
        - Limit screen time before bed  
        - Practice gratitude journaling  
        """)
    elif mood_score > 0.1 or quiz_score >= 3:
        st.info("You're on track but need some adjustments:")
        st.markdown("""
        - Add 10 mins daily meditation  
        - Fix your sleep schedule  
        - Add a quick 20-min walk  
        - Digital detox twice a week  
        """)
    else:
        st.error("Looks like you need to focus more on wellness:")
        st.markdown("""
        - Talk to a friend or counselor  
        - Daily 30-min outdoor activity  
        - Avoid screen 1 hour before bed  
        - Journal every night  
        """)
    complete_page()

# ========== Page 5: Feedback ==========
elif st.session_state.current_page == "Feedback":
    st.title("💬 Feedback")
    feedback = st.text_area("Let us know what you think of this app!")
    if st.button("Submit Feedback"):
        st.success("Thanks for your feedback!")

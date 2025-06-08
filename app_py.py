import streamlit as st
import pandas as pd
from textblob import TextBlob
import os
import csv
from streamlit_lottie import st_lottie
import requests
from datetime import datetime
import altair as alt

# Cache animation loading
@st.cache_data(ttl=3600)
def load_lottie_url(url):
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except Exception:
        return None

# Create folders if not exist
os.makedirs("data", exist_ok=True)

st.set_page_config(page_title="🌙 Mood Predictor Pro", layout="centered", page_icon="🌈")

# ========== Stylish Dark Theme with Gradient ==========
bg_color = "#121212"
card_bg = "#1e1e2f"
button_gradient = "linear-gradient(90deg, #BB86FC 0%, #3700B3 100%)"
text_color = "#E0E0FF"
shadow = "0 8px 24px rgba(187, 134, 252, 0.6)"

st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;600&display=swap');

    body, .stApp {{
        background: {bg_color};
        color: {text_color};
        font-family: 'Poppins', sans-serif;
        transition: background 0.3s ease;
    }}

    .stButton>button {{
        background: {button_gradient} !important;
        color: white !important;
        border-radius: 12px !important;
        padding: 0.6rem 1.5rem !important;
        font-weight: 600 !important;
        box-shadow: {shadow} !important;
        border: none !important;
        transition: all 0.3s ease !important;
    }}
    .stButton>button:hover {{
        filter: brightness(1.2);
        cursor: pointer;
    }}

    div[data-testid="stMetric"] {{
        background-color: {card_bg};
        border-radius: 20px;
        padding: 18px 25px;
        box-shadow: {shadow};
        margin-bottom: 25px;
        font-weight: 700;
        font-size: 22px;
        color: #BB86FC;
    }}

    .stTextInput>div>div>input,
    .stTextArea>div>div>textarea {{
        background-color: #2a2a40;
        color: {text_color};
        border-radius: 15px;
        border: none;
        padding: 12px;
        font-size: 18px;
        font-weight: 400;
        transition: box-shadow 0.3s ease;
    }}
    .stTextInput>div>div>input:focus,
    .stTextArea>div>div>textarea:focus {{
        box-shadow: 0 0 8px 2px #BB86FC;
        outline: none;
    }}

    table {{
        background-color: {card_bg};
        border-radius: 15px;
        box-shadow: {shadow};
        color: {text_color};
        font-weight: 500;
    }}

    /* Tooltip style */
    [data-tooltip] {{
        position: relative;
        cursor: help;
    }}
    [data-tooltip]:hover::after {{
        content: attr(data-tooltip);
        position: absolute;
        bottom: 125%;
        left: 50%;
        transform: translateX(-50%);
        background-color: #3700B3;
        color: white;
        padding: 6px 10px;
        border-radius: 6px;
        white-space: nowrap;
        font-size: 14px;
        opacity: 0.95;
        pointer-events: none;
        z-index: 10;
    }}

    </style>
    """,
    unsafe_allow_html=True,
)

# === Functions ===

def analyze_mood(text):
    return TextBlob(text).sentiment.polarity

def parse_time(t):
    return datetime.strptime(t.split(" - ")[0], "%I:%M %p")

# === Main App ===

if 'page' not in st.session_state:
    st.session_state.page = 'User Info'

# Sidebar navigation with emojis and clear lock indication
pages = ["👤 User Info", "📊 Dashboard", "✨ Suggestions", "📝 Feedback"]
current_idx = pages.index(st.session_state.page)

st.sidebar.title("🚀 Navigate")
for i, page in enumerate(pages):
    if i <= current_idx:
        if st.sidebar.button(page, key=page):
            st.session_state.page = page
    else:
        st.sidebar.markdown(f"{page} 🔒")

def go_next():
    idx = pages.index(st.session_state.page)
    if idx + 1 < len(pages):
        st.session_state.page = pages[idx+1]

# --- User Info Page ---
if st.session_state.page == "👤 User Info":
    st.title("Welcome! Let's get to know you 😊")
    animation = load_lottie_url("https://assets2.lottiefiles.com/packages/lf20_1pxqjqps.json")
    if animation:
        st_lottie(animation, height=220)

    name = st.text_input("Enter your name", max_chars=30)
    age = st.number_input("Age", 10, 100)
    gender = st.selectbox("Gender", ["Male", "Female", "Other", "Prefer not to say"])

    if st.button("👉 Continue"):
        if name.strip():
            st.session_state.name = name
            st.session_state.age = age
            st.session_state.gender = gender
            go_next()
        else:
            st.warning("Please enter your name to continue!")

# --- Dashboard Page ---
elif st.session_state.page == "📊 Dashboard":
    st.title(f"Hello, {st.session_state.get('name','User')}! 🌈 How are you feeling today?")
    journal_entry = st.text_area("Write your thoughts or journal entry below:")

    if st.button("🔍 Analyze Mood"):
        if journal_entry.strip():
            mood_score = analyze_mood(journal_entry)
            st.session_state.mood_score = mood_score

            risk_level = "Low" if mood_score > 0.3 else "Moderate" if mood_score > 0 else "High"
            st.session_state.risk = risk_level

            # Display results with cool emojis & colors
            emoji_map = {"Low": "😄", "Moderate": "😐", "High": "😟"}
            color_map = {"Low": "#4caf50", "Moderate": "#ff9800", "High": "#f44336"}

            st.markdown(
                f"<div style='font-size:28px; font-weight:bold; color:{color_map[risk_level]};'>"
                f"Your Mood Score: {mood_score:.2f} {emoji_map[risk_level]}"
                "</div>",
                unsafe_allow_html=True,
            )

            st.markdown(
                f"<div style='font-size:22px; color:{color_map[risk_level]}; margin-bottom:20px;'>"
                f"Burnout Risk Level: {risk_level}"
                "</div>",
                unsafe_allow_html=True,
            )

            # Save journal data
            with open("data/journal_entries.csv", "a", newline="") as f:
                csv.writer(f).writerow([st.session_state.name, journal_entry, mood_score])

            # Animate flower if low risk
            if risk_level == "Low":
                flower_anim = load_lottie_url("https://assets4.lottiefiles.com/packages/lf20_touohxv0.json")
                if flower_anim:
                    st_lottie(flower_anim, height=150)

        else:
            st.warning("Please write something before analyzing.")

    if "mood_score" in st.session_state:
        if st.button("✨ Go to Suggestions"):
            go_next()

# --- Suggestions Page ---
elif st.session_state.page == "✨ Suggestions":
    st.title("Your Personalized Wellness Tips 🌟")

    risk = st.session_state.get("risk", "Moderate")

    if risk == "Low":
        st.success("You're doing great! Keep shining! ✨")
        st.balloons()
    else:
        # Suggestion cards with emoji headers and gradient backgrounds
        st.markdown(f"""
            <div style='background: {button_gradient}; padding: 20px; border-radius: 25px; margin-bottom: 20px; color: white; font-weight: 600; font-size: 20px;'>
            {("🔥" if risk=="High" else "⚠️")} Your risk level is <b>{risk}</b>. Here's what you can do:
            </div>
        """, unsafe_allow_html=True)

        st.video("https://www.youtube.com/watch?v=2OEL4P1Rz04")

        # Routine suggestions with shadow cards
        routine = [
            {"Time": "6:00 AM - 7:00 AM", "Activity": "Wake up & Morning exercise (stretch, yoga)"},
            {"Time": "7:00 AM - 7:30 AM", "Activity": "Healthy breakfast with fruits & veggies"},
            {"Time": "7:30 AM - 9:00 AM", "Activity": "Focused study/work session"},
            {"Time": "9:00 AM - 9:15 AM", "Activity": "Short break - walk/stretch"},
            {"Time": "9:15 AM - 11:00 AM", "Activity": "Study / Assignments"},
            {"Time": "11:00 AM - 12:00 PM", "Activity": "Light snack & rest"},
            {"Time": "12:00 PM - 1:00 PM", "Activity": "Lunch with protein and greens"},
            {"Time": "1:00 PM - 2:00 PM", "Activity": "Power nap or relaxation"},
            {"Time": "2:00 PM - 4:00 PM", "Activity": "Project work or study"},
            {"Time": "4:00 PM - 4:30 PM", "Activity": "Physical activity (walk/cycling)"},
            {"Time": "4:30 PM - 5:00 PM", "Activity": "Healthy snack"},
            {"Time": "5:00 PM - 7:00 PM", "Activity": "Light study/revision"},
            {"Time": "7:00 PM - 8:00 PM", "Activity": "Dinner with greens"},
            {"Time": "8:00 PM - 9:00 PM", "Activity": "Relax and hobbies"},
            {"Time": "9:00 PM - 10:00 PM", "Activity": "Prepare for next day & sleep early"},
        ]
        df = pd.DataFrame(routine)

        st.table(df)

        # Altair timeline chart
        df['Start Time'] = df['Time'].apply(parse_time)
        df['End Time'] = df['Time'].apply(lambda x: datetime.strptime(x.split(" - ")[1], "%I:%M %p"))
        chart = alt.Chart(df).mark_bar(cornerRadiusTopLeft=6, cornerRadiusTopRight=6).encode(
            x=alt.X('Start Time:T', axis=alt.Axis(title='Time')),
            x2='End Time:T',
            y=alt.Y('Activity:N', sort=None),
            color=alt.Color('Activity:N', legend=None)
        ).properties(
            height=400,
            width=700,
            title='Your Daily Routine Timeline'
        )
        st.altair_chart(chart, use_container_width=True)

    st.markdown("---")
    st.markdown("### 🎙️ Inspirational Talk")
    st.video("https://www.youtube.com/watch?v=iCvmsMzlF7o")
    st.caption("“Vulnerability is the birthplace of innovation, creativity and change.” – Brené Brown")

    if st.button("📝 Go to Feedback"):
        go_next()

# --- Feedback Page ---
elif st.session_state.page == "📝 Feedback":
    st.title("We value your feedback! 💬")
    feedback = st.text_area("Tell us about your experience:")

    if st.button("Submit Feedback"):
        with open("data/feedback.csv", "a", newline="") as f:
            csv.writer(f).writerow([st.session_state.get("name", "Anonymous"), feedback])
        st.success("Thank you for your feedback! 🎉")

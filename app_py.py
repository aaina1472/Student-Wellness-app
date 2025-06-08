import streamlit as st
import pandas as pd
from textblob import TextBlob
import os
import csv
from streamlit_lottie import st_lottie
import requests

def load_lottie_url(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Create folders if not exist
os.makedirs("data", exist_ok=True)

st.set_page_config(page_title="Mood Predictor App", layout="centered")

# Initialize session state
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'User Info'

# Sidebar Navigation (locked step-by-step)
st.sidebar.title("Navigation")

pages = ["User Info", "Dashboard", "Suggestions", "Feedback"]
current_idx = pages.index(st.session_state.current_page)

for i, page in enumerate(pages):
    if i <= current_idx:
        if st.sidebar.button(f"{i+1}. {page}", key=page):
            st.session_state.current_page = page
    else:
        st.sidebar.markdown(f"{i+1}. {page} 🔒")

# Page Navigator
def go_next():
    next_idx = pages.index(st.session_state.current_page) + 1
    if next_idx < len(pages):
        st.session_state.current_page = pages[next_idx]

# ========== Page 1: User Info ==========
if st.session_state.current_page == 'User Info':
    st.title("User Information")
    st.markdown("Please fill in your details to get started")

    # Load meditation and study animations
    meditation_animation = load_lottie_url("https://assets10.lottiefiles.com/packages/lf20_w51pcehl.json")
    study_animation = load_lottie_url("https://assets10.lottiefiles.com/packages/lf20_jcikwtux.json")

    # Show animations side by side using columns
    col1, col2 = st.columns(2)
    with col1:
        if meditation_animation:
            st_lottie(meditation_animation, height=180, key="meditation")
    with col2:
        if study_animation:
            st_lottie(study_animation, height=180, key="study")

    # Form Inputs
    name = st.text_input("Your Name")
    age = st.number_input("Your Age", min_value=10, max_value=100, step=1)
    gender = st.selectbox("Select your gender:", ["Male", "Female", "Other", "Prefer not to say"])

    if st.button("Continue to Dashboard"):
        if name:
            st.session_state.name = name
            st.session_state.age = age
            st.session_state.gender = gender

            # Save user info
            with open("data/user_info.csv", "a", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([name, age, gender])

            go_next()
        else:
            st.warning("Please enter your name to continue.")

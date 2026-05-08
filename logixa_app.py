import streamlit as st
import pandas as pd
import numpy as np
import requests
from fpdf import FPDF
import base64
import json
import os
from datetime import datetime

# 1. PEHLI LINE: Page Config
st.set_page_config(
    page_title="LOGIXA — Command Center",
    layout="wide",
    page_icon="⚡",
    initial_sidebar_state="expanded"
)

# --- Session Initialization ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_email' not in st.session_state:
    st.session_state.user_email = None

# --- Feedback Storage Logic ---
def save_feedback(email, rating, message):
    feedback_data = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "email": email,
        "rating": rating,
        "message": message
    }

    # Replit par ek local JSON file mein feedback save hoga
    file_path = "user_feedback.json"

    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            data = json.load(f)
    else:
        data = []

    data.append(feedback_data)

    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)

# ─── MAIN APP LOGIC ───────────────────────────────────────────
if not st.session_state.logged_in:

    # Login Page
    st.title("🛡️ LOGIXA SECURE LOGIN")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if email == "admin@logixa.io" and password == "logixa123":
            st.session_state.logged_in = True
            st.session_state.user_email = email
            st.rerun()
        else:
            st.error("Invalid email or password.")

else:

    # SIDEBAR
    with st.sidebar:
        st.title("🛡️ LOGIXA MENU")

        menu_choice = st.radio(
            "SELECT VIEW",
            ["📊 Command Center", "👤 Profile & Settings"]
        )

    # --- TAB 1: COMMAND CENTER ---
    if menu_choice == "📊 Command Center":

        st.header("📈 Financial Intelligence Dashboard")
        st.write("Welcome back! Your tools are ready.")

    # --- TAB 2: PROFILE & SETTINGS ---
    elif menu_choice == "👤 Profile & Settings":

        st.header("👤 User Account & Settings")

        # Profile Info
        col1, col2 = st.columns([1, 2])

        with col1:
            st.image(
                f"https://ui-avatars.com/api/?name={st.session_state.user_email}&size=128",
                width=120
            )

        with col2:
            st.subheader("Account Details")
            st.write(f"📧 **Email:** {st.session_state.user_email}")
            st.write("🌟 **Plan:** Global Beta (Free)")

        st.divider()

        # --- FEEDBACK SECTION ---
        st.subheader("📩 Send us your Feedback")

        st.info("Aapka feedback Logixa ko behtar banane mein madad karega.")

        with st.form("feedback_form", clear_on_submit=True):

            rating = st.select_slider(
                "Rate your experience:",
                options=["😞", "😐", "🙂", "😃", "🤩"]
            )

            feedback_msg = st.text_area(
                "Aapko tool kaisa laga? Koi naya feature chahiye?",
                placeholder="Write your message here..."
            )

            submit_feedback = st.form_submit_button("Submit Feedback")

            if submit_feedback:
                if feedback_msg:
                    save_feedback(
                        st.session_state.user_email,
                        rating,
                        feedback_msg
                    )

                    st.success(
                        "Shukriya! Aapka feedback record kar liya gaya hai. ✅"
                    )

                else:
                    st.warning(
                        "Please enter a message before submitting."
                    )

        st.divider()

        # Logout Button
        if st.button("🔴 Sign Out", use_container_width=True):
            st.session_state.logged_in = False
            st.rerun()

st.divider()

st.caption("© 2026 LOGIXA Systems • Feedback is stored securely.")

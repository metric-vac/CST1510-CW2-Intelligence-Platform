"""
CST1510 - Intelligence Platform
Week 7-10 Integration: Authentication, Database, and Dashboards
CW2 Tier 2: Cybersecurity + IT Operations Domains
Student: Nebil Abuabker Nasser (M01064011)
"""
import streamlit as st
import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent))

from app.data.db import create_tables
from app.services.db_auth import login_user_db, register_user_db, migrate_users_from_file

st.set_page_config(page_title="Intelligence Platform", page_icon="🔐", layout="wide")

# Initialize database and migrate users
try:
    create_tables()
    migrate_users_from_file()
except:
    pass

# Session state initialization
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "page" not in st.session_state:
    st.session_state.page = "home"

# Check which page to show
if st.session_state.logged_in and st.session_state.page == "cyber_dashboard":
    exec(open("pages/1_Cybersecurity_Dashboard.py").read())
    st.stop()
elif st.session_state.logged_in and st.session_state.page == "it_dashboard":
    exec(open("pages/2_IT_Operations_Dashboard.py").read())
    st.stop()

# If logged in, show dashboard options
if st.session_state.logged_in:
    st.success(f"✓ Logged in as **{st.session_state.username}**")
    
    st.markdown("### 📊 Select Dashboard")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🛡️ Cybersecurity Dashboard", use_container_width=True):
            st.session_state.page = "cyber_dashboard"
            st.rerun()
        st.caption("Incident analysis & phishing trends")
    
    with col2:
        if st.button("💻 IT Operations Dashboard", use_container_width=True):
            st.session_state.page = "it_dashboard"
            st.rerun()
        st.caption("Service desk & staff performance")
    
    st.divider()
    
    if st.button("Logout", type="secondary"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.page = "home"
        st.rerun()
    
    st.stop()

# Login/Register tabs
st.title("Intelligence Platform")
st.markdown("### Multi-Domain Intelligence & AI Assistant")
st.markdown("**CW2 Tier 2 Implementation** - Cybersecurity + IT Operations")

tab_login, tab_register = st.tabs(["Login", "Register"])

# LOGIN TAB
with tab_login:
    st.subheader("Login")
    
    login_username = st.text_input("Username", key="login_username")
    login_password = st.text_input("Password", type="password", key="login_password")
    
    if st.button("Log in", type="primary"):
        if login_user_db(login_username, login_password):
            st.session_state.logged_in = True
            st.session_state.username = login_username
            st.success(f"Welcome back, {login_username}!")
            st.rerun()
        else:
            st.error("Invalid username or password.")
    
    st.info("💡 **Demo accounts:** johnDoe, NebilAbubaker, or metricvac")

# REGISTER TAB
with tab_register:
    st.subheader("Register")
    
    new_username = st.text_input("Choose a username", key="register_username")
    new_password = st.text_input("Choose a password", type="password", key="register_password")
    confirm_password = st.text_input("Confirm password", type="password", key="register_confirm")
    
    if st.button("Create account"):
        if not new_username or not new_password:
            st.warning("Please fill in all fields.")
        elif new_password != confirm_password:
            st.error("Passwords do not match.")
        elif len(new_password) < 6:
            st.error("Password must be at least 6 characters.")
        elif register_user_db(new_username, new_password):
            st.success("✓ Account created! You can now log in.")
        else:
            st.error("Username already exists.")
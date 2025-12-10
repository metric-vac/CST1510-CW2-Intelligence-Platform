"""
Home Dashboard - Overview of Both Domains
Student: Nebil Abuabker Nasser (M01064011)
"""
import streamlit as st
import pandas as pd
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from app.data.db import get_all_incidents, get_all_tickets

# Check authentication
if "logged_in" not in st.session_state or not st.session_state.get("logged_in", False):
    st.warning("Please login first")
    st.stop()

# Header
st.title("Intelligence Platform - Home Dashboard")
st.markdown(f"**Welcome, {st.session_state.username}**")

st.divider()

# Get data
incidents = get_all_incidents()
tickets = get_all_tickets()

incidents_df = pd.DataFrame([dict(row) for row in incidents])
tickets_df = pd.DataFrame([dict(row) for row in tickets])

# Summary Cards
st.markdown("### Platform Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Incidents", len(incidents_df))
    
with col2:
    phishing = len(incidents_df[incidents_df['category'] == 'Phishing'])
    st.metric("Phishing Incidents", phishing, f"{phishing/len(incidents_df)*100:.1f}%")

with col3:
    st.metric("Total Tickets", len(tickets_df))

with col4:
    resolved = len(tickets_df[tickets_df['status'] == 'Resolved'])
    st.metric("Resolved Tickets", resolved, f"{resolved/len(tickets_df)*100:.1f}%")

st.divider()

# Two domain summaries
col1, col2 = st.columns(2)

with col1:
    st.markdown("### Cybersecurity Domain")
    st.info("""
    **Key Finding:** Phishing surge detected
    
    - 62 phishing incidents (53.9% of total)
    - Growing backlog of unresolved cases
    - Requires immediate resource allocation
    """)
    
    if st.button("View Cybersecurity Dashboard", use_container_width=True):
        st.session_state.page = "cyber_dashboard"
        st.rerun()

with col2:
    st.markdown("### IT Operations Domain")
    
    # Calculate staff performance
    resolved_tickets = tickets_df[tickets_df['resolution_time_hours'].notna()]
    if len(resolved_tickets) > 0:
        staff_perf = resolved_tickets.groupby('assigned_to')['resolution_time_hours'].mean()
        worst = staff_perf.max()
        best = staff_perf.min()
        
        st.warning(f"""
        Key Finding:
        - Performance gap: {worst/best:.1f}x difference
        - Slowest: {worst:.1f} hours average
        - Fastest: {best:.1f} hours average
        """)
    
    if st.button(" View IT Operations Dashboard", use_container_width=True):
        st.session_state.page = "it_dashboard"
        st.rerun()

st.divider()

# Logout button
if st.button("Logout", type="secondary"):
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.page = "login"
    st.rerun()
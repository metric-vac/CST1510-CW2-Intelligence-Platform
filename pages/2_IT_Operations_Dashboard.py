"""
Week 10: IT Operations Dashboard  
Student: Nebil Abuabker Nasser (M01064011)
CW2 Tier 2: IT Operations Domain Analysis
"""
import streamlit as st
import pandas as pd
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from app.data.db import get_all_tickets

# Check authentication
if "logged_in" not in st.session_state:
    st.set_page_config(page_title="IT Operations Dashboard", layout="wide")
    st.warning("Please login first")
    st.stop()

if not st.session_state.get("logged_in", False):
    st.warning("Please login first")
    st.stop()

# Header
st.title(" IT Operations Dashboard")
st.markdown(f"**Administrator:** {st.session_state.username}")

# Navigation
col1, col2, col3 = st.columns([1, 1, 4])
with col1:
    if st.button("Home"):
        st.session_state.page = "home" 
        st.rerun()
with col2:
    if st.button(" Cybersecurity"):
        st.session_state.page = "cyber_dashboard"
        st.rerun()

st.divider()

# Get tickets data
tickets = get_all_tickets()

if not tickets:
    st.warning("No ticket data available")
    st.stop()

# Convert to DataFrame
df = pd.DataFrame([dict(row) for row in tickets])

# Convert created_at to datetime
df['created_at'] = pd.to_datetime(df['created_at'])

# Key Metrics
st.markdown("### Key Metrics")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Tickets", len(df))

with col2:
    resolved_count = len(df[df['status'] == 'Resolved'])
    resolution_rate = (resolved_count / len(df) * 100) if len(df) > 0 else 0
    st.metric("Resolved", resolved_count, f"{resolution_rate:.1f}%")

with col3:
    high_count = len(df[df['priority'].isin(['High', 'Critical'])])
    st.metric("High/Critical Priority", high_count)

with col4:
    open_count = len(df[df['status'] == 'Open'])
    st.metric("Open Tickets", open_count)

st.divider()

# PROBLEM ANALYSIS: Staff Performance
st.markdown("### Problem Analysis: Service Desk Performance")

st.info("""
**Problem Statement:** The IT support team is struggling with slow resolution times. 
Management suspects a staff performance anomaly and process inefficiencies.
""")

# Staff performance analysis
resolved_df = df[df['resolution_time_hours'].notna()]

if len(resolved_df) > 0:
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("#### Staff Performance Analysis")
        
        # Calculate average resolution time per staff member
        staff_performance = resolved_df.groupby('assigned_to')['resolution_time_hours'].agg([
            ('avg_hours', 'mean'),
            ('tickets_handled', 'count')
        ]).reset_index()
        
        staff_performance = staff_performance.sort_values('avg_hours', ascending=False)
        staff_performance['avg_hours'] = staff_performance['avg_hours'].round(1)
        
        # Create bar chart
        st.bar_chart(staff_performance.set_index('assigned_to')['avg_hours'])
        
        # Identify performance anomaly
        worst_performer = staff_performance.iloc[0]
        best_performer = staff_performance.iloc[-1]
        
    
    with col2:
        st.markdown("#### Staff Performance Table")
        st.dataframe(staff_performance, use_container_width=True, hide_index=True)

st.divider()

# Priority and Status Analysis
st.markdown("### Priority & Status Breakdown")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### By Priority")
    priority_counts = df['priority'].value_counts()
    st.bar_chart(priority_counts)

with col2:
    st.markdown("#### By Status")
    status_counts = df['status'].value_counts()
    st.bar_chart(status_counts)

st.divider()

# Detailed Staff Analysis
if len(resolved_df) > 0:
    st.markdown("### Detailed Staff Performance Metrics")
    
    staff_detailed = resolved_df.groupby('assigned_to')['resolution_time_hours'].agg([
        ('Total Tickets', 'count'),
        ('Avg Hours', 'mean'),
        ('Min Hours', 'min'),
        ('Max Hours', 'max')
    ]).round(1).reset_index()
    
    staff_detailed.columns = ['Staff Member', 'Total Tickets', 'Avg Hours', 'Min Hours', 'Max Hours']
    staff_detailed = staff_detailed.sort_values('Avg Hours', ascending=False)
    
    st.dataframe(staff_detailed, use_container_width=True, hide_index=True)

st.divider()


st.divider()

# Recent Tickets Table
st.markdown("### Recent Tickets")

# Show most recent tickets
recent_df = df.sort_values('created_at', ascending=False).head(20)
display_cols = ['ticket_id', 'priority', 'status', 'assigned_to', 'created_at', 'resolution_time_hours', 'description']
st.dataframe(recent_df[display_cols], use_container_width=True, hide_index=True)

st.caption(f"Showing {len(recent_df)} most recent tickets out of {len(df)} total")
"""
Week 9-10: Cybersecurity Dashboard
Student: Nebil Abuabker Nasser (M01064011)
CW2 Tier 2: Cybersecurity Domain Analysis
"""
import streamlit as st
import pandas as pd
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from app.data.db import get_all_incidents

# Check authentication
if "logged_in" not in st.session_state:
    st.set_page_config(page_title="Cybersecurity Dashboard", page_icon="🛡️", layout="wide")
    st.warning("Please login first")
    st.stop()

if not st.session_state.get("logged_in", False):
    st.warning("Please login first")
    st.stop()

# Header
st.title("🛡️ Cybersecurity Dashboard")
st.markdown(f"**Analyst:** {st.session_state.username}")

# Navigation
col1, col2, col3 = st.columns([1, 1, 4])
with col1:
    if st.button("🏠 Home"):
        st.session_state.page = "home"
        st.rerun()
with col2:
    if st.button("💻 IT Operations"):
        st.session_state.page = "it_dashboard"
        st.rerun()

st.divider()

# Get incidents data
incidents = get_all_incidents()

if not incidents:
    st.warning("No incident data available")
    st.stop()

# Convert to DataFrame
df = pd.DataFrame([dict(row) for row in incidents])

# Convert timestamp to datetime
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Key Metrics
st.markdown("### 📊 Key Metrics")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Incidents", len(df))

with col2:
    phishing_count = len(df[df['category'] == 'Phishing'])
    phishing_pct = (phishing_count / len(df) * 100) if len(df) > 0 else 0
    st.metric("Phishing Incidents", phishing_count, f"{phishing_pct:.1f}%")

with col3:
    critical_count = len(df[df['severity'] == 'Critical'])
    st.metric("Critical Severity", critical_count)

with col4:
    open_count = len(df[df['status'].isin(['Open', 'In Progress'])])
    st.metric("Open/In Progress", open_count)

st.divider()

# PROBLEM ANALYSIS: Phishing Trend
st.markdown("### 🎯 Problem Analysis: Incident Response Bottleneck")

st.info("""
**Problem Statement:** The security team is facing a surge in Phishing incidents, 
leading to a growing backlog of high-severity, unresolved cases.
""")

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("#### Incident Trend Over Time")
    
    # Group by date and category
    df['date'] = df['timestamp'].dt.date
    daily_incidents = df.groupby(['date', 'category']).size().reset_index(name='count')
    
    # Pivot for chart
    pivot_data = daily_incidents.pivot(index='date', columns='category', values='count').fillna(0)
    
    st.line_chart(pivot_data)
    
    st.success(f"""
    **Key Finding:** Phishing accounts for **{phishing_pct:.1f}%** of all incidents, 
    significantly higher than other threat categories.
    """)

with col2:
    st.markdown("#### Incident Distribution")
    
    category_counts = df['category'].value_counts()
    st.bar_chart(category_counts)

st.divider()

# Severity and Status Analysis
st.markdown("### 📈 Severity & Status Analysis")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### By Severity")
    severity_counts = df['severity'].value_counts()
    st.bar_chart(severity_counts)

with col2:
    st.markdown("#### By Status")
    status_counts = df['status'].value_counts()
    st.bar_chart(status_counts)

st.divider()

# Detailed Analysis
st.markdown("### 🔍 Detailed Incident Analysis")

# Category breakdown
st.markdown("#### Incidents by Category and Status")
category_status = pd.crosstab(df['category'], df['status'])
st.dataframe(category_status, use_container_width=True)

st.divider()

# Recommendations
st.markdown("### 💡 Recommended Actions")
st.markdown("""
Based on the analysis, the security team should:
- Increase staffing for phishing incident response
- Implement better email filtering to reduce incoming phishing attempts  
- Set clear response time targets (SLAs) for different severity levels
- Provide regular security awareness training to reduce user susceptibility
- Consider automated tools to help analyze and categorize incidents faster
""")

st.divider()

# Recent Incidents Table
st.markdown("### 📋 Recent Incidents")

# Show most recent incidents
recent_df = df.sort_values('timestamp', ascending=False).head(20)
display_cols = ['incident_id', 'timestamp', 'category', 'severity', 'status', 'description']
st.dataframe(recent_df[display_cols], use_container_width=True, hide_index=True)

st.caption(f"Showing {len(recent_df)} most recent incidents out of {len(df)} total")
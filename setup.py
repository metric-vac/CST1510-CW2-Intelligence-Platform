#!/usr/bin/env python3
"""
Setup script to initialize database with all data
Run this once before starting the Streamlit app
"""

from app.data.db import create_tables, connect_database
from app.services.db_auth import migrate_users_from_file
import pandas as pd

print("Initializing CST1510 Week 7-10 Project...")
print()

# Create tables
create_tables()
print("Database tables created")

# Migrate users from Week 7 users.txt
migrate_users_from_file()
print("Users migrated from users.txt")

# Load CSV data
conn = connect_database()

# Cyber incidents
df = pd.read_csv('DATA/cyber_incidents.csv')
df.to_sql('cyber_incidents', conn, if_exists='replace', index=False)
print(f"✓ {len(df)} cyber incidents loaded")

# IT tickets
df = pd.read_csv('DATA/it_tickets.csv')
df.to_sql('it_tickets', conn, if_exists='replace', index=False)
print(f"✓ {len(df)} IT tickets loaded")

conn.close()

# Verify
conn = connect_database()
cursor = conn.cursor()
cursor.execute('SELECT COUNT(*) FROM users')
user_count = cursor.fetchone()[0]
cursor.execute('SELECT COUNT(*) FROM cyber_incidents')
incident_count = cursor.fetchone()[0]
cursor.execute('SELECT COUNT(*) FROM it_tickets')
ticket_count = cursor.fetchone()[0]
conn.close()

print()
print("Database Summary:")
print(f"   Users: {user_count}")
print(f"   Cyber Incidents: {incident_count}")
print(f"   IT Tickets: {ticket_count}")
print()
print("Setup complete. Run: streamlit run Home.py")
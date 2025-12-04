"""
Week 8: Database Module
Student: Nebil Abuabker Nasser (M01064011)
"""
import sqlite3

DB_FILE = "DATA/intelligence_platform.db"

def connect_database():
    """Connect to SQLite database."""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def create_tables():
    """Create all database tables."""
    conn = connect_database()
    cursor = conn.cursor()
    
    # Users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL
        )
    """)
    
    # Cyber incidents table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cyber_incidents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            incident_id INTEGER,
            timestamp TEXT,
            severity TEXT,
            category TEXT,
            status TEXT,
            description TEXT
        )
    """)
    
    # Datasets metadata table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS datasets_metadata (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            rows INTEGER,
            columns INTEGER,
            file_size_mb REAL,
            created_date TEXT
        )
    """)
    
    # IT tickets table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS it_tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticket_id INTEGER,
            priority TEXT,
            description TEXT,
            status TEXT,
            assigned_to TEXT,
            created_at TEXT,
            resolution_time_hours INTEGER
        )
    """)
    
    conn.commit()
    conn.close()

def get_all_incidents():
    """Get all cyber incidents."""
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cyber_incidents")
    results = cursor.fetchall()
    conn.close()
    return results

def get_all_datasets():
    """Get all datasets metadata."""
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM datasets_metadata")
    results = cursor.fetchall()
    conn.close()
    return results

def get_all_tickets():
    """Get all IT tickets."""
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM it_tickets")
    results = cursor.fetchall()
    conn.close()
    return results

"""
Week 8: Database Authentication
Integrates Week 7 authentication with Week 8 database
"""
import bcrypt
from app.data.db import connect_database

def hash_password(plain_text_password):
    """Hash a password using bcrypt."""
    password_bytes = plain_text_password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')

def verify_password(plain_text_password, hashed_password):
    """Verify a plaintext password against a stored bcrypt hash."""
    password_bytes = plain_text_password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_bytes)

def migrate_users_from_file():
    """Migrate users from users.txt to database."""
    conn = connect_database()
    cursor = conn.cursor()
    
    with open("DATA/users.txt", 'r') as f:
        for line in f:
            if line.strip():
                username, password_hash = line.strip().split(',')
                try:
                    cursor.execute("""
                        INSERT INTO users (username, password_hash, role)
                        VALUES (?, ?, 'user')
                    """, (username, password_hash))
                except:
                    pass  # Skip if user already exists
    
    conn.commit()
    conn.close()

def login_user_db(username, password):
    """Authenticate user from database."""
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute("SELECT password_hash FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    conn.close()
    
    if result:
        return verify_password(password, result['password_hash'])
    return False

def register_user_db(username, password):
    """Register a new user in database."""
    conn = connect_database()
    cursor = conn.cursor()
    
    try:
        hashed = hash_password(password)
        cursor.execute("""
            INSERT INTO users (username, password_hash, role)
            VALUES (?, ?, 'user')
        """, (username, hashed))
        conn.commit()
        conn.close()
        return True
    except:
        conn.close()
        return False

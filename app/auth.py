"""
Week 7: Authentication System
"""
import bcrypt
import os

USER_DATA_FILE = "DATA/users.txt"

def hash_password(plain_text_password):
    """Hash a password using bcrypt with automatic salt generation."""
    password_bytes = plain_text_password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')

def verify_password(plain_text_password, hashed_password):
    """Verify a plaintext password against a stored bcrypt hash."""
    password_bytes = plain_text_password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_bytes)

def user_exists(username):
    """Check if a username already exists in the user database."""
    if not os.path.exists(USER_DATA_FILE):
        return False
    
    with open(USER_DATA_FILE, 'r') as f:
        for line in f:
            if line.strip():
                stored_username = line.split(',')[0]
                if stored_username == username:
                    return True
    return False

def register_user(username, password):
    """Register a new user by hashing their password and storing credentials."""
    if user_exists(username):
        return False
    
    hashed = hash_password(password)
    
    with open(USER_DATA_FILE, 'a') as f:
        f.write(f"{username},{hashed}\n")
    
    return True

def login_user(username, password):
    """Authenticate a user by verifying their username and password."""
    if not os.path.exists(USER_DATA_FILE):
        return False
    
    with open(USER_DATA_FILE, 'r') as f:
        for line in f:
            if line.strip():
                parts = line.strip().split(',')
                if len(parts) == 2:
                    stored_username, stored_hash = parts
                    if stored_username == username:
                        return verify_password(password, stored_hash)
    
    return False

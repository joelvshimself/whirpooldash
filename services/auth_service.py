"""
Authentication service for user login
"""
import hashlib
from typing import Optional
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.models import SessionLocal, User


class AuthService:
    """Service for handling user authentication"""
    
    def __init__(self):
        self.session = SessionLocal()
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash password using SHA256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def authenticate(self, username: str, password: str) -> Optional[User]:
        """
        Authenticate user with username and password
        
        Args:
            username: Username
            password: Plain text password
            
        Returns:
            User object if authentication successful, None otherwise
        """
        password_hash = self.hash_password(password)
        
        user = self.session.query(User).filter(
            User.username == username,
            User.password_hash == password_hash
        ).first()
        
        return user
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        """Get user by username"""
        return self.session.query(User).filter(User.username == username).first()
    
    def __del__(self):
        """Close database session on cleanup"""
        if hasattr(self, 'session'):
            self.session.close()


"""
Initialize database tables and create admin user
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.models import create_tables, SessionLocal, User
from services.auth_service import AuthService


def init_database():
    """Initialize database: create tables and admin user"""
    print("Creating database tables...")
    create_tables()
    print("Tables created successfully!")
    
    print("\nCreating admin user...")
    session = SessionLocal()
    
    # Check if admin user already exists
    existing_user = session.query(User).filter(User.username == "admin").first()
    
    if existing_user:
        print("Admin user already exists. Skipping...")
    else:
        # Create admin user with password "admin"
        admin_user = User(
            username="admin",
            password_hash=AuthService.hash_password("admin")
        )
        session.add(admin_user)
        session.commit()
        print("Admin user created successfully! (username: admin, password: admin)")
    
    session.close()
    print("\nDatabase initialization complete!")


if __name__ == "__main__":
    init_database()


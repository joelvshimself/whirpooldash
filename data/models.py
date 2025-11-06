"""
SQLAlchemy models for Whirlpool Dashboard
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, Date, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import config

Base = declarative_base()


class User(Base):
    """User model for authentication"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<User(username='{self.username}')>"


class PriceHistory(Base):
    """Price prediction history model"""
    __tablename__ = "price_history"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    sku = Column(String(50), nullable=False)
    region = Column(String(100), nullable=False)
    partner = Column(String(100), nullable=False)
    release_date = Column(DateTime, nullable=False)
    price = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<PriceHistory(sku='{self.sku}', region='{self.region}', price={self.price})>"


class KPI(Base):
    """KPI metrics model"""
    __tablename__ = "kpis"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date, nullable=False, unique=True)
    todays_money = Column(Float, nullable=False)
    todays_users = Column(Integer, nullable=False)
    money_change = Column(Float, nullable=False)
    users_change = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<KPI(date='{self.date}', money={self.todays_money}, users={self.todays_users})>"


class SKU(Base):
    """SKU information model"""
    __tablename__ = "skus"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    company = Column(String(255), nullable=False)
    icon = Column(String(10), nullable=False)
    members = Column(Integer, nullable=False)
    budget = Column(Float, nullable=True)
    completion = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<SKU(company='{self.company}', completion={self.completion}%)>"


# Database engine and session factory
engine = create_engine(config.DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Test database connection
try:
    with engine.connect() as conn:
        print(f"✅ Successfully connected to database: {config.DB_NAME}")
        print(f"   Host: {config.DB_HOST}:{config.DB_PORT}")
except Exception as e:
    print(f"❌ Failed to connect to database: {e}")


def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    """Create all tables in the database"""
    Base.metadata.create_all(bind=engine)


def drop_tables():
    """Drop all tables in the database"""
    Base.metadata.drop_all(bind=engine)


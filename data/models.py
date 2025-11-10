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


# Database engine and session factory (lazy initialization)
_engine = None
_session_factory = None


def _get_engine():
    """Lazy initialization of database engine"""
    global _engine
    if _engine is None:
        try:
            # Try to import psycopg2, fallback to psycopg2cffi for PyPy compatibility
            try:
                import psycopg2
            except ImportError:
                try:
                    import psycopg2cffi
                    # Register psycopg2cffi as psycopg2 for compatibility
                    import psycopg2cffi.compat
                    psycopg2cffi.compat.register()
                except ImportError:
                    raise ImportError(
                        "psycopg2-binary or psycopg2cffi is required for database operations. "
                        "For CPython: pip install psycopg2-binary\n"
                        "For PyPy: pip install psycopg2cffi"
                    )
            
            _engine = create_engine(config.DATABASE_URL, echo=False)
            # Test database connection
            with _engine.connect() as conn:
                print(f"✅ Successfully connected to database: {config.DB_NAME}")
                print(f"   Host: {config.DB_HOST}:{config.DB_PORT}")
        except ImportError as e:
            if "psycopg2" in str(e).lower() or "psycopg2cffi" in str(e).lower():
                raise ImportError(
                    "psycopg2-binary or psycopg2cffi is required for database operations. "
                    "For CPython: pip install psycopg2-binary\n"
                    "For PyPy: pip install psycopg2cffi"
                ) from e
            raise
        except Exception as e:
            print(f"❌ Failed to connect to database: {e}")
            raise
    return _engine


def _get_session_factory():
    """Lazy initialization of session factory"""
    global _session_factory
    if _session_factory is None:
        engine = _get_engine()
        _session_factory = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return _session_factory


class LazySessionLocal:
    """Lazy sessionmaker that only initializes when first used"""
    def __call__(self, *args, **kwargs):
        return _get_session_factory()(*args, **kwargs)
    
    def __getattr__(self, name):
        return getattr(_get_session_factory(), name)


# SessionLocal is now a lazy callable that behaves like sessionmaker
SessionLocal = LazySessionLocal()


def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    """Create all tables in the database"""
    engine = _get_engine()
    Base.metadata.create_all(bind=engine)


def drop_tables():
    """Drop all tables in the database"""
    engine = _get_engine()
    Base.metadata.drop_all(bind=engine)


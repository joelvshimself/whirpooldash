"""
Seed database with dummy data
"""
import sys
import os
import random
from datetime import datetime, timedelta, date

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.models import SessionLocal, PriceHistory, KPI, SKU
import config


def seed_price_history(session):
    """Seed price history data"""
    print("Seeding price history...")
    
    partners = config.DEFAULT_PARTNERS
    regions = config.DEFAULT_REGIONS
    skus = config.DEFAULT_SKUS
    
    # Generate historical data for the past year
    for _ in range(200):
        days_ago = random.randint(1, 365)
        record = PriceHistory(
            sku=random.choice(skus),
            region=random.choice(regions),
            partner=random.choice(partners),
            release_date=datetime.now() - timedelta(days=days_ago),
            price=round(random.uniform(100, 2000), 2),
            created_at=datetime.now() - timedelta(days=days_ago)
        )
        session.add(record)
    
    session.commit()
    print(f"Seeded {200} price history records")


def seed_kpis(session):
    """Seed KPI data"""
    print("Seeding KPIs...")
    
    # Generate KPIs for the past 30 days
    for i in range(30):
        days_ago = 30 - i
        kpi_date = date.today() - timedelta(days=days_ago)
        
        # Check if KPI already exists for this date
        existing_kpi = session.query(KPI).filter(KPI.date == kpi_date).first()
        if not existing_kpi:
            kpi = KPI(
                date=kpi_date,
                todays_money=round(random.uniform(40000, 60000), 2),
                todays_users=random.randint(2000, 3000),
                money_change=round(random.uniform(-10, 100), 2),
                users_change=round(random.uniform(-5, 15), 2)
            )
            session.add(kpi)
    
    session.commit()
    print("Seeded 30 days of KPI data")


def seed_skus(session):
    """Seed SKU data"""
    print("Seeding SKUs...")
    
    companies = [
        {"name": "Xd Chakra Soft UI Version", "icon": "🎨"},
        {"name": "Add Progress Track", "icon": "📊"},
        {"name": "Fix Platform Errors", "icon": "🔧"},
        {"name": "Launch our Mobile App", "icon": "📱"},
        {"name": "Add the New Pricing Page", "icon": "💎"},
        {"name": "Redesign New Online Shop", "icon": "🛒"},
        {"name": "Optimize Dashboard", "icon": "📈"},
        {"name": "Update API Endpoints", "icon": "🔌"},
        {"name": "Enhance Security", "icon": "🔒"},
        {"name": "Improve Performance", "icon": "⚡"}
    ]
    
    budgets = [14000, 3000, None, 32000, 400, 7600, 12000, 5000, 8500, 9000]
    completions = [60, 10, 100, 100, 25, 40, 75, 50, 30, 90]
    
    for i, company in enumerate(companies):
        # Check if SKU already exists
        existing_sku = session.query(SKU).filter(SKU.company == company["name"]).first()
        if not existing_sku:
            sku = SKU(
                company=company["name"],
                icon=company["icon"],
                members=random.randint(1, 4),
                budget=budgets[i],
                completion=completions[i]
            )
            session.add(sku)
    
    session.commit()
    print(f"Seeded {len(companies)} SKU records")


def seed_database():
    """Seed all tables with dummy data"""
    print("Starting database seeding...\n")
    
    session = SessionLocal()
    
    try:
        seed_price_history(session)
        print()
        seed_kpis(session)
        print()
        seed_skus(session)
        print()
        print("Database seeding complete!")
    except Exception as e:
        print(f"Error seeding database: {e}")
        session.rollback()
    finally:
        session.close()


if __name__ == "__main__":
    seed_database()


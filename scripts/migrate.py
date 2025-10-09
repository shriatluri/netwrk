#!/usr/bin/env python3
"""
Database migration script for LinkedIn Networking Application
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

load_dotenv()

# Import after path is set
from src.backend.shared.database import engine, Base
from src.backend.shared.models import User, UserProfile, Resume, Company, CompanyEmployee, ConnectionRecommendation

def run_migrations():
    """Run database migrations"""
    try:
        print("Starting database migration...")
        print(f"Database URL: {os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@localhost:5432/linkedin_networking')}")

        # Create all tables
        print("Creating database tables...")
        Base.metadata.create_all(bind=engine)

        print("✓ Migration completed successfully!")
        print("\nCreated tables:")
        print("  - users")
        print("  - user_profiles")
        print("  - resumes")
        print("  - companies")
        print("  - company_employees")
        print("  - connection_recommendations")

    except Exception as e:
        print(f"✗ Migration failed: {e}")
        sys.exit(1)

def main():
    """Main migration function"""
    run_migrations()

if __name__ == "__main__":
    main()

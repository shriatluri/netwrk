#!/usr/bin/env python3
"""
Database migration script for LinkedIn Networking Application
"""

import os
import sys
import asyncio
import asyncpg
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.backend.core.config import settings

async def run_migrations():
    """Run database migrations"""
    try:
        # Connect to the database
        conn = await asyncpg.connect(settings.DATABASE_URL)
        
        print("Connected to database successfully")
        
        # Read and execute the init.sql file
        init_sql_path = Path(__file__).parent / "init.sql"
        
        if init_sql_path.exists():
            with open(init_sql_path, 'r') as f:
                init_sql = f.read()
            
            # Execute the SQL
            await conn.execute(init_sql)
            print("Database schema initialized successfully")
        else:
            print("Warning: init.sql file not found")
        
        # Close the connection
        await conn.close()
        print("Migration completed successfully")
        
    except Exception as e:
        print(f"Migration failed: {e}")
        sys.exit(1)

async def check_database_connection():
    """Check if database connection is available"""
    try:
        conn = await asyncpg.connect(settings.DATABASE_URL)
        await conn.close()
        print("Database connection successful")
        return True
    except Exception as e:
        print(f"Database connection failed: {e}")
        return False

async def create_database_if_not_exists():
    """Create database if it doesn't exist"""
    try:
        # Connect to postgres database to create the application database
        postgres_url = settings.DATABASE_URL.replace('/linkedin_networking', '/postgres')
        conn = await asyncpg.connect(postgres_url)
        
        # Check if database exists
        result = await conn.fetchval(
            "SELECT 1 FROM pg_database WHERE datname = 'linkedin_networking'"
        )
        
        if not result:
            await conn.execute("CREATE DATABASE linkedin_networking")
            print("Database 'linkedin_networking' created successfully")
        else:
            print("Database 'linkedin_networking' already exists")
        
        await conn.close()
        
    except Exception as e:
        print(f"Failed to create database: {e}")
        sys.exit(1)

async def main():
    """Main migration function"""
    print("Starting database migration...")
    
    # Check if we need to create the database
    if not await check_database_connection():
        print("Creating database...")
        await create_database_if_not_exists()
    
    # Run migrations
    await run_migrations()

if __name__ == "__main__":
    asyncio.run(main())

#!/usr/bin/env python3
"""
Database seeding script for LinkedIn Networking Application
"""

import os
import sys
import asyncio
import asyncpg
import json
from pathlib import Path
from datetime import datetime, timedelta
import uuid

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.backend.core.config import settings

async def seed_database():
    """Seed the database with sample data"""
    try:
        # Connect to the database
        conn = await asyncpg.connect(settings.DATABASE_URL)
        
        print("Connected to database successfully")
        
        # Seed companies
        await seed_companies(conn)
        
        # Seed users
        await seed_users(conn)
        
        # Seed company employees
        await seed_company_employees(conn)
        
        # Seed recommendations
        await seed_recommendations(conn)
        
        # Seed connections
        await seed_connections(conn)
        
        # Close the connection
        await conn.close()
        print("Database seeding completed successfully")
        
    except Exception as e:
        print(f"Seeding failed: {e}")
        sys.exit(1)

async def seed_companies(conn):
    """Seed companies table"""
    companies_data = [
        {
            'name': 'Google',
            'industry': 'Technology',
            'size': 'Large',
            'location': 'Mountain View, CA',
            'linkedin_company_id': '1441',
            'description': 'Google is a multinational technology company specializing in Internet-related services and products.',
            'website': 'https://google.com',
            'employee_count': 150000
        },
        {
            'name': 'Microsoft',
            'industry': 'Technology',
            'size': 'Large',
            'location': 'Redmond, WA',
            'linkedin_company_id': '1035',
            'description': 'Microsoft is a multinational technology company that develops, manufactures, licenses, supports and sells computer software.',
            'website': 'https://microsoft.com',
            'employee_count': 180000
        },
        {
            'name': 'Apple',
            'industry': 'Technology',
            'size': 'Large',
            'location': 'Cupertino, CA',
            'linkedin_company_id': '162479',
            'description': 'Apple Inc. is an American multinational technology company that specializes in consumer electronics.',
            'website': 'https://apple.com',
            'employee_count': 160000
        },
        {
            'name': 'Amazon',
            'industry': 'E-commerce',
            'size': 'Large',
            'location': 'Seattle, WA',
            'linkedin_company_id': '104409',
            'description': 'Amazon.com, Inc. is an American multinational technology company which focuses on e-commerce.',
            'website': 'https://amazon.com',
            'employee_count': 1500000
        },
        {
            'name': 'Meta',
            'industry': 'Technology',
            'size': 'Large',
            'location': 'Menlo Park, CA',
            'linkedin_company_id': '104409',
            'description': 'Meta Platforms, Inc., doing business as Meta, is an American multinational technology conglomerate.',
            'website': 'https://meta.com',
            'employee_count': 87000
        }
    ]
    
    for company in companies_data:
        await conn.execute("""
            INSERT INTO companies (name, industry, size, location, linkedin_company_id, description, website, employee_count)
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
            ON CONFLICT (linkedin_company_id) DO NOTHING
        """, company['name'], company['industry'], company['size'], company['location'],
        company['linkedin_company_id'], company['description'], company['website'], company['employee_count'])
    
    print("Companies seeded successfully")

async def seed_users(conn):
    """Seed users table"""
    users_data = [
        {
            'email': 'john.doe@example.com',
            'linkedin_id': 'john-doe-123',
            'profile_data': {
                'name': 'John Doe',
                'headline': 'Software Engineer at Tech Corp',
                'industry': 'Technology',
                'location': 'San Francisco, CA',
                'summary': 'Passionate software engineer with 5 years of experience in full-stack development.',
                'experience': [
                    {
                        'title': 'Senior Software Engineer',
                        'company': 'Tech Corp',
                        'duration': '2 years',
                        'description': 'Led development of microservices architecture'
                    }
                ],
                'education': [
                    {
                        'school': 'Stanford University',
                        'degree': 'Bachelor of Science',
                        'field': 'Computer Science',
                        'year': 2018
                    }
                ],
                'skills': ['Python', 'JavaScript', 'React', 'Node.js', 'AWS', 'Docker']
            },
            'preferences': {
                'target_companies': ['Google', 'Microsoft', 'Apple'],
                'connection_goals': 'Find senior engineering roles',
                'industry_focus': ['Technology', 'Software Development']
            }
        },
        {
            'email': 'jane.smith@example.com',
            'linkedin_id': 'jane-smith-456',
            'profile_data': {
                'name': 'Jane Smith',
                'headline': 'Product Manager at StartupCo',
                'industry': 'Technology',
                'location': 'New York, NY',
                'summary': 'Product manager with expertise in user experience and data analysis.',
                'experience': [
                    {
                        'title': 'Senior Product Manager',
                        'company': 'StartupCo',
                        'duration': '3 years',
                        'description': 'Led product strategy and user research'
                    }
                ],
                'education': [
                    {
                        'school': 'Harvard Business School',
                        'degree': 'MBA',
                        'field': 'Business Administration',
                        'year': 2019
                    }
                ],
                'skills': ['Product Management', 'Data Analysis', 'User Research', 'Agile', 'SQL', 'Python']
            },
            'preferences': {
                'target_companies': ['Google', 'Meta', 'Amazon'],
                'connection_goals': 'Network with product leaders',
                'industry_focus': ['Technology', 'Product Management']
            }
        }
    ]
    
    for user in users_data:
        await conn.execute("""
            INSERT INTO users (email, linkedin_id, profile_data, preferences)
            VALUES ($1, $2, $3, $4)
            ON CONFLICT (email) DO NOTHING
        """, user['email'], user['linkedin_id'], json.dumps(user['profile_data']), json.dumps(user['preferences']))
    
    print("Users seeded successfully")

async def seed_company_employees(conn):
    """Seed company employees table"""
    # Get company IDs
    companies = await conn.fetch("SELECT id, name FROM companies")
    company_map = {company['name']: company['id'] for company in companies}
    
    employees_data = [
        # Google employees
        {
            'company_name': 'Google',
            'linkedin_id': 'google-engineer-1',
            'name': 'Alex Johnson',
            'position': 'Senior Software Engineer',
            'department': 'Engineering',
            'seniority_level': 'Senior',
            'headline': 'Senior Software Engineer at Google',
            'connection_score': 0.85
        },
        {
            'company_name': 'Google',
            'linkedin_id': 'google-pm-1',
            'name': 'Sarah Chen',
            'position': 'Product Manager',
            'department': 'Product',
            'seniority_level': 'Senior',
            'headline': 'Product Manager at Google',
            'connection_score': 0.78
        },
        # Microsoft employees
        {
            'company_name': 'Microsoft',
            'linkedin_id': 'microsoft-engineer-1',
            'name': 'David Wilson',
            'position': 'Principal Software Engineer',
            'department': 'Engineering',
            'seniority_level': 'Principal',
            'headline': 'Principal Software Engineer at Microsoft',
            'connection_score': 0.92
        },
        {
            'company_name': 'Microsoft',
            'linkedin_id': 'microsoft-designer-1',
            'name': 'Emily Rodriguez',
            'position': 'UX Designer',
            'department': 'Design',
            'seniority_level': 'Mid',
            'headline': 'UX Designer at Microsoft',
            'connection_score': 0.73
        },
        # Apple employees
        {
            'company_name': 'Apple',
            'linkedin_id': 'apple-engineer-1',
            'name': 'Michael Brown',
            'position': 'iOS Developer',
            'department': 'Engineering',
            'seniority_level': 'Senior',
            'headline': 'iOS Developer at Apple',
            'connection_score': 0.88
        }
    ]
    
    for employee in employees_data:
        company_id = company_map.get(employee['company_name'])
        if company_id:
            await conn.execute("""
                INSERT INTO company_employees (company_id, linkedin_id, name, position, department, seniority_level, headline, connection_score)
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
                ON CONFLICT (company_id, linkedin_id) DO NOTHING
            """, company_id, employee['linkedin_id'], employee['name'], employee['position'],
            employee['department'], employee['seniority_level'], employee['headline'], employee['connection_score'])
    
    print("Company employees seeded successfully")

async def seed_recommendations(conn):
    """Seed recommendations table"""
    # Get user and company data
    users = await conn.fetch("SELECT id, email FROM users")
    companies = await conn.fetch("SELECT id, name FROM companies")
    employees = await conn.fetch("SELECT id, company_id, linkedin_id, name FROM company_employees")
    
    user_map = {user['email']: user['id'] for user in users}
    company_map = {company['name']: company['id'] for company in companies}
    
    recommendations_data = [
        {
            'user_email': 'john.doe@example.com',
            'company_name': 'Google',
            'target_person_id': 'google-engineer-1',
            'match_score': 0.85,
            'reasoning': [
                {'factor': 'Industry Match', 'score': 0.9, 'description': 'Both in Technology industry'},
                {'factor': 'Skill Compatibility', 'score': 0.8, 'description': 'Shared skills in Python, JavaScript'},
                {'factor': 'Experience Level', 'score': 0.9, 'description': 'Similar experience levels'}
            ]
        },
        {
            'user_email': 'jane.smith@example.com',
            'company_name': 'Google',
            'target_person_id': 'google-pm-1',
            'match_score': 0.78,
            'reasoning': [
                {'factor': 'Industry Match', 'score': 0.9, 'description': 'Both in Technology industry'},
                {'factor': 'Skill Compatibility', 'score': 0.7, 'description': 'Shared skills in Product Management'},
                {'factor': 'Experience Level', 'score': 0.8, 'description': 'Similar experience levels'}
            ]
        }
    ]
    
    for rec in recommendations_data:
        user_id = user_map.get(rec['user_email'])
        company_id = company_map.get(rec['company_name'])
        
        if user_id and company_id:
            await conn.execute("""
                INSERT INTO recommendations (user_id, target_person_id, company_id, match_score, reasoning)
                VALUES ($1, $2, $3, $4, $5)
            """, user_id, rec['target_person_id'], company_id, rec['match_score'], json.dumps(rec['reasoning']))
    
    print("Recommendations seeded successfully")

async def seed_connections(conn):
    """Seed connections table"""
    # Get recommendations data
    recommendations = await conn.fetch("""
        SELECT r.id, r.user_id, r.target_person_id, r.company_id, r.match_score
        FROM recommendations r
        LIMIT 5
    """)
    
    for rec in recommendations:
        await conn.execute("""
            INSERT INTO connections (user_id, target_person_id, company_id, recommendation_id, status, message, sent_at)
            VALUES ($1, $2, $3, $4, $5, $6, $7)
        """, rec['user_id'], rec['target_person_id'], rec['company_id'], rec['id'], 
        'pending', 'Hi! I would like to connect with you.', datetime.now())
    
    print("Connections seeded successfully")

async def main():
    """Main seeding function"""
    print("Starting database seeding...")
    await seed_database()

if __name__ == "__main__":
    asyncio.run(main())

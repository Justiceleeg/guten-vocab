#!/usr/bin/env python3
"""
Test database connection.
"""
import os
import sys
from pathlib import Path
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Load environment variables
load_dotenv(Path(__file__).parent.parent / ".env")

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    print("Error: DATABASE_URL not set in .env file")
    sys.exit(1)

print(f"Testing connection to: {DATABASE_URL.split('@')[-1] if '@' in DATABASE_URL else DATABASE_URL}")

try:
    engine = create_engine(DATABASE_URL)
    with engine.connect() as conn:
        result = conn.execute(text("SELECT version();"))
        version = result.fetchone()[0]
        print(f"✓ Connected successfully!")
        print(f"PostgreSQL version: {version.split(',')[0]}")
        
        # List tables
        result = conn.execute(text("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name;
        """))
        tables = [row[0] for row in result]
        
        if tables:
            print(f"\nFound {len(tables)} tables:")
            for table in tables:
                print(f"  - {table}")
        else:
            print("\nNo tables found. Run setup_database.py to create schema.")
    
    engine.dispose()
    
except Exception as e:
    print(f"✗ Connection failed: {e}")
    print("\nMake sure:")
    print("  1. PostgreSQL is running")
    print("  2. DATABASE_URL in .env is correct")
    print("  3. Database exists (run setup_database.py)")
    sys.exit(1)


#!/usr/bin/env python3
"""
Script to set up the database: create database and schema.
Requires PostgreSQL to be running.

Usage:
    python scripts/setup_database.py
"""
import os
import sys
from pathlib import Path
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Add parent directory to path to import app modules
sys.path.insert(0, str(Path(__file__).parent.parent))

# Load environment variables
load_dotenv(Path(__file__).parent.parent / ".env")

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    print("Error: DATABASE_URL not set in .env file")
    print("Please set DATABASE_URL in backend/.env")
    sys.exit(1)

# Parse database URL to get connection details
# Format: postgresql://user:password@host:port/database
try:
    # Extract database name from URL
    if "@" in DATABASE_URL:
        db_name = DATABASE_URL.split("/")[-1]
        # Get base URL without database name
        base_url = "/".join(DATABASE_URL.split("/")[:-1])
    else:
        print("Error: Invalid DATABASE_URL format")
        sys.exit(1)
except Exception as e:
    print(f"Error parsing DATABASE_URL: {e}")
    sys.exit(1)

print(f"Database name: {db_name}")
print(f"Connecting to PostgreSQL...")

# Connect to PostgreSQL (default database) to create our database
try:
    # Connect to postgres database to create vocab_engine
    admin_url = base_url + "/postgres"
    admin_engine = create_engine(admin_url)
    
    with admin_engine.connect() as conn:
        # Check if database exists
        result = conn.execute(
            text("SELECT 1 FROM pg_database WHERE datname = :db_name"),
            {"db_name": db_name}
        )
        exists = result.fetchone()
        
        if exists:
            print(f"Database '{db_name}' already exists.")
        else:
            # Create database
            conn.execute(text("COMMIT"))  # End any transaction
            conn.execute(text(f'CREATE DATABASE "{db_name}"'))
            print(f"Database '{db_name}' created successfully.")
    
    admin_engine.dispose()
    
    # Now connect to our database and create schema
    print(f"Connecting to database '{db_name}'...")
    engine = create_engine(DATABASE_URL)
    
    # Read and execute schema SQL
    schema_file = Path(__file__).parent / "create_schema.sql"
    if not schema_file.exists():
        print(f"Error: Schema file not found: {schema_file}")
        sys.exit(1)
    
    with open(schema_file, "r") as f:
        schema_sql = f.read()
    
    print("Creating database schema...")
    with engine.connect() as conn:
        # Execute schema SQL
        conn.execute(text(schema_sql))
        conn.commit()
    
    print("Schema created successfully!")
    
    # Verify tables were created
    print("\nVerifying tables...")
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name;
        """))
        tables = [row[0] for row in result]
        
        expected_tables = [
            "students",
            "vocabulary_words",
            "student_vocabulary",
            "books",
            "book_vocabulary",
            "student_recommendations",
            "class_recommendations",
        ]
        
        print(f"Found {len(tables)} tables:")
        for table in tables:
            print(f"  - {table}")
        
        missing = set(expected_tables) - set(tables)
        if missing:
            print(f"\nWarning: Missing tables: {', '.join(missing)}")
        else:
            print("\n✓ All expected tables created!")
    
    engine.dispose()
    print("\nDatabase setup complete!")
    
except Exception as e:
    print(f"\nError: {e}")
    print("\nMake sure PostgreSQL is running and DATABASE_URL is correct.")
    print("For Postgres.app, start the app and ensure it's running.")
    sys.exit(1)


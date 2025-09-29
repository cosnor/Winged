#!/usr/bin/env python3
"""
Database management script for Avedex service.
"""

import asyncio
import sys
import os
from sqlalchemy.ext.asyncio import AsyncSession

# Add the app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from app.infrastructure.database.connection import AsyncSessionLocal, create_tables, drop_tables
from app.infrastructure.database.seed_data import seed_all_data


async def create_and_seed():
    """Create tables and seed with initial data."""
    print("Creating database tables...")
    await create_tables()
    print("Tables created successfully!")
    
    print("Seeding database with initial data...")
    async with AsyncSessionLocal() as session:
        await seed_all_data(session)
    print("Database seeded successfully!")


async def reset_database():
    """Drop all tables and recreate with seed data."""
    print("Dropping all tables...")
    await drop_tables()
    print("Tables dropped successfully!")
    
    await create_and_seed()


async def seed_only():
    """Seed database with initial data (tables must exist)."""
    print("Seeding database with initial data...")
    async with AsyncSessionLocal() as session:
        await seed_all_data(session)
    print("Database seeded successfully!")


def main():
    """Main function."""
    if len(sys.argv) != 2:
        print("Usage: python manage_db.py [create|reset|seed]")
        print("  create: Create tables and seed data")
        print("  reset:  Drop tables, recreate, and seed data")
        print("  seed:   Seed data only (tables must exist)")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "create":
        asyncio.run(create_and_seed())
    elif command == "reset":
        asyncio.run(reset_database())
    elif command == "seed":
        asyncio.run(seed_only())
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
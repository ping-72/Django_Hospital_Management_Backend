# db_connection_test.py

import os
import sys
import django
from django.db import connections
from django.db.utils import OperationalError

# Add the correct path to your settings module
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_dir, 'healthcare_project'))

# Set up Django environment with the correct settings module path
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'healthcare_project.settings')
django.setup()

def check_database_connection():
    try:
        # Try to get cursor from the default database
        db_conn = connections['default']
        db_conn.cursor()
        print("✅ Successfully connected to PostgreSQL database!")
        
        # Get database info
        db_info = connections.databases['default']
        print(f"Database: {db_info['NAME']}")
        print(f"Host: {db_info['HOST']}")
        print(f"User: {db_info['USER']}")
        
        # Query some information
        cursor = db_conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()[0]
        print(f"PostgreSQL version: {version}")
        
        # List tables in database
        cursor.execute("""
            SELECT table_name FROM information_schema.tables
            WHERE table_schema='public'
            ORDER BY table_name;
        """)
        tables = cursor.fetchall()
        print("\nTables in database:")
        for table in tables:
            print(f"- {table[0]}")
        
    except OperationalError as e:
        print(f"❌ Could not connect to PostgreSQL database: {e}")
    except Exception as e:
        print(f"❌ An error occurred: {e}")

if __name__ == "__main__":
    check_database_connection()
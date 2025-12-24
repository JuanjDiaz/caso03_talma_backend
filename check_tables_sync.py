import sys
import os
from sqlalchemy import create_engine, inspect, text

# Add root
sys.path.append(os.getcwd())

from config.database_config import DATABASE_URL

def main():
    print("Checking tables (sync mode)...")
    
    # Convert async url to sync url
    sync_url = DATABASE_URL.replace("postgresql+asyncpg", "postgresql")
    print(f"URL: {sync_url.split('@')[-1]}") # Print host part only
    
    try:
        engine = create_engine(sync_url)
        
        with engine.connect() as conn:
            inspector = inspect(conn)
            tables = inspector.get_table_names()
            
            print("\nTables in public schema:")
            for t in tables:
                print(f" - {t}")
            
            # Case insensitive check
            target = "usuario"
            found = False
            for t in tables:
                if t.lower() == target:
                    found = True
                    print(f"\nFound match: '{t}'")
                    if t != target:
                        print(f"NOTE: Case mismatch! Expected '{target}', found '{t}'")
            
            if not found:
                print(f"\nERROR: Table '{target}' NOT found!")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()

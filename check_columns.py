import sys
import os
from sqlalchemy import create_engine, inspect

# Add root
sys.path.append(os.getcwd())

from config.database_config import DATABASE_URL

def main():
    print("Checking columns (sync mode)...")
    
    # Convert async url to sync url
    if "asyncpg" in DATABASE_URL:
        sync_url = DATABASE_URL.replace("postgresql+asyncpg", "postgresql")
    else:
        sync_url = DATABASE_URL
        
    print(f"URL: {sync_url.split('@')[-1]}") 
    
    try:
        engine = create_engine(sync_url)
        
        with engine.connect() as conn:
            inspector = inspect(conn)
            
            for table in ['rol', 'usuario']:
                print(f"\nColumns in '{table}':")
                try:
                    columns = inspector.get_columns(table)
                    for c in columns:
                        print(f" - {c['name']} ({c['type']})")
                except Exception as e:
                     print(f" - Error getting columns (table might not exist): {e}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()

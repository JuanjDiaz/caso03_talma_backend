import asyncio
import sys
import os
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text

# Add root
sys.path.append(os.getcwd())

from config.database_config import DATABASE_URL

async def main():
    print(f"Connecting to DB...")
    
    try:
        # Use the same args as the app
        engine = create_async_engine(
            DATABASE_URL,
            echo=False,
            connect_args={"statement_cache_size": 0}
        )
        
        async with engine.connect() as conn:
            # Query pg_tables directly
            stmt = text("SELECT schemaname, tablename FROM pg_catalog.pg_tables WHERE schemaname = 'public';")
            result = await conn.execute(stmt)
            rows = result.fetchall()
            
            print("Tables in public schema:")
            found_usuario = False
            for row in rows:
                t = row.tablename
                print(f" - {t}")
                if t.lower() == 'usuario':
                    found_usuario = True
            
            if not found_usuario:
                print("\nWARNING: 'usuario' table NOT found in public schema.")
            else:
                print("\nSUCCESS: 'usuario' table found.")

    except Exception as e:
        print(f"Error connecting: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())

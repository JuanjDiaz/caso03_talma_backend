import sys
import os
import asyncio
import inspect

# Add project root to path
sys.path.append(os.getcwd())

def check_config():
    print("Checking Config...")
    try:
        from config.config import settings
        if settings.DATABASE_URL:
             print("✅ DATABASE_URL loaded correctly from .env")
        else:
             print("❌ DATABASE_URL is missing")
        
        if settings.LLM_API_KEY and settings.LLM_BASE_URL:
             print("✅ LLM Credentials loaded correctly from .env")
        else:
             print("❌ LLM Credentials are missing")
    except Exception as e:
        print(f"❌ Config check failed: {e}")

def check_analyze_service():
    print("\nChecking Analyze Service...")
    try:
        from app.core.services.impl.analyze_service_impl import AnalyzeServiceImpl, process_file_content
        import app.core.services.impl.analyze_service_impl as module
        
        if inspect.isfunction(process_file_content):
            print("✅ process_file_content is a standalone function (good for pickling)")
        
        service = AnalyzeServiceImpl(None)
        if asyncio.iscoroutinefunction(service.upload):
             print("✅ upload is async")
        
    except ImportError as e:
         print(f"❌ Import failed: {e}")
    except Exception as e:
         print(f"❌ Analyze Service check failed: {e}")

def check_pagination():
    print("\nChecking Pagination Signatures...")
    try:
        from app.core.repository.impl.document_repository_impl import DocumentRepositoryImpl
        from app.core.services.impl.document_service_impl import DocumentServiceImpl
        from app.core.facade.impl.document_facade_impl import DocumentFacadeImpl
        from app.core.api.document_router import get_documents

        # Check Repo
        sig_repo = inspect.signature(DocumentRepositoryImpl.find_all)
        if 'skip' in sig_repo.parameters and 'limit' in sig_repo.parameters:
            print("✅ Repository find_all has skip/limit")
        else:
             print(f"❌ Repository find_all signature incorrect: {sig_repo}")

        # Check Router
        sig_router = inspect.signature(get_documents)
        if 'skip' in sig_router.parameters and 'limit' in sig_router.parameters:
             print("✅ Router get_documents has skip/limit")
        else:
             print(f"❌ Router get_documents signature incorrect: {sig_router}")

    except Exception as e:
         print(f"❌ Pagination check failed: {e}")

if __name__ == "__main__":
    check_config()
    check_analyze_service()
    check_pagination()

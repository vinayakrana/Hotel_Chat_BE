"""
Quick verification script to check if everything is set up correctly
Run this before starting the application
"""
import os
import sys

def check_file(filepath, description):
    """Check if a file exists"""
    if os.path.exists(filepath):
        print(f"✅ {description}: {filepath}")
        return True
    else:
        print(f"❌ {description}: {filepath} NOT FOUND")
        return False

def check_env_var(var_name):
    """Check if environment variable is set"""
    value = os.getenv(var_name)
    if value and value != f"your_{var_name.lower()}_here" and not value.startswith("gsk_your"):
        print(f"✅ {var_name}: Configured")
        return True
    else:
        print(f"⚠️  {var_name}: NOT SET (you need to add your actual API key)")
        return False

def main():
    print("="*60)
    print("🔍 Simple Hotel Bot - Setup Verification")
    print("="*60 + "\n")
    
    all_good = True
    
    # Check Python files
    print("📁 Checking Core Files:")
    all_good &= check_file("main.py", "FastAPI Application")
    all_good &= check_file("agent.py", "LangGraph Agent")
    all_good &= check_file("tools.py", "LangChain Tools")
    all_good &= check_file("database.py", "SQLite Database")
    all_good &= check_file("auth.py", "RBAC System")
    all_good &= check_file("vector_store.py", "ChromaDB RAG")
    print()
    
    # Check config files
    print("⚙️  Checking Configuration:")
    all_good &= check_file("requirements.txt", "Dependencies")
    all_good &= check_file(".env", "Environment File")
    all_good &= check_file("data/faqs.txt", "FAQ Data")
    print()
    
    # Check environment variables
    print("🔑 Checking Environment Variables:")
    from dotenv import load_dotenv
    load_dotenv()
    api_key_set = check_env_var("GROQ_API_KEY")
    print()
    
    # Check if packages are installed
    print("📦 Checking Dependencies:")
    try:
        import fastapi
        print(f"✅ fastapi: {fastapi.__version__}")
    except ImportError:
        print("❌ fastapi: NOT INSTALLED")
        all_good = False
    
    try:
        import uvicorn
        print(f"✅ uvicorn: {uvicorn.__version__}")
    except ImportError:
        print("❌ uvicorn: NOT INSTALLED")
        all_good = False
    
    try:
        import langchain
        print(f"✅ langchain: {langchain.__version__}")
    except ImportError:
        print("❌ langchain: NOT INSTALLED")
        all_good = False
    
    try:
        import langgraph
        print(f"✅ langgraph: Installed")
    except ImportError:
        print("❌ langgraph: NOT INSTALLED")
        all_good = False
    
    try:
        import chromadb
        print(f"✅ chromadb: {chromadb.__version__}")
    except ImportError:
        print("❌ chromadb: NOT INSTALLED")
        all_good = False
    
    print()
    print("="*60)
    
    if all_good and api_key_set:
        print("🎉 ALL CHECKS PASSED!")
        print("\n✅ You're ready to run the application:")
        print("   python main.py")
        print("\n📝 API Docs will be at: http://localhost:8000/docs")
    elif not api_key_set:
        print("⚠️  Almost Ready!")
        print("\n❗ ACTION REQUIRED:")
        print("   1. Edit .env file")
        print("   2. Add your Groq API key: GROQ_API_KEY=your_actual_key")
        print("   3. Get a free key at: https://console.groq.com/keys")
        print("\nThen run: python main.py")
    else:
        print("❌ SETUP INCOMPLETE")
        print("\n❗ MISSING STEPS:")
        if not all_good:
            print("   1. Install dependencies: pip install -r requirements.txt")
        if not api_key_set:
            print("   2. Edit .env and add your GROQ_API_KEY")
        print("\nThen run this script again to verify.")
    
    print("="*60)

if __name__ == "__main__":
    main()

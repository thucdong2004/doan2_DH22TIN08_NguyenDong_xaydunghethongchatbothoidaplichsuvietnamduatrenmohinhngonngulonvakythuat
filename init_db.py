from src.vector_store import create_vector_store
import time
import argparse
import sys

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Initialize Vietnamese History Chatbot Database")
    parser.add_argument(
        "--clear", 
        action="store_true", 
        help="Clear existing database before creating new one (WARNING: This will delete all existing data)"
    )
    parser.add_argument(
        "--update",
        action="store_true",
        help="Update existing database (add new documents without clearing)"
    )
    
    args = parser.parse_args()
    
    # Validate arguments
    if args.clear and args.update:
        print("❌ Error: Cannot use both --clear and --update flags together")
        sys.exit(1)
    
    print("🎬 Starting database initialization...")
    
    if args.clear:
        print("⚠️  CLEAR MODE: Existing database will be deleted and recreated")
        clear_existing = True
    elif args.update:
        print("🔄 UPDATE MODE: Adding/updating documents in existing database")
        clear_existing = False
    else:
        print("📝 DEFAULT MODE: Creating database (will fail if already exists)")
        clear_existing = False
    
    start_time = time.time()
    
    try:
        create_vector_store(clear_existing=clear_existing)
        elapsed = time.time() - start_time
        print(f"✅ Database initialized successfully in {elapsed:.2f} seconds!")
        print("🚀 You can now run 'python app.py' to start the chatbot.")
    except Exception as e:
        print(f"\n❌ Error initializing database: {e}")
        print("\n💡 Troubleshooting tips:")
        print("   1. Make sure 'app.py' is NOT running (close it first)")
        print("   2. Close any other Python processes that might be using the database")
        print("   3. Use 'python init_db.py --clear' to force recreate the database")
        print("   4. Check if you have write permissions to the project folder")
        sys.exit(1)

if __name__ == "__main__":
    main()

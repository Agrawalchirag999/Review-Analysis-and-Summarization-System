"""
Configuration Validator for Review Analysis System
Run this script to check if your config.py is properly set up
"""

import sys
import os

def check_config():
    """Validate configuration file"""
    errors = []
    warnings = []
    
    print("=" * 50)
    print("Configuration Validator")
    print("=" * 50)
    print()
    
    # Check if config.py exists
    if not os.path.exists('config.py'):
        print("❌ CRITICAL: config.py not found!")
        print("   Please copy config.template.py to config.py")
        return False
    
    print("✅ config.py found")
    
    # Try to import config
    try:
        import config
        print("✅ config.py can be imported")
    except Exception as e:
        print(f"❌ CRITICAL: Error importing config.py: {e}")
        return False
    
    print()
    print("Checking configuration values...")
    print("-" * 50)
    
    # Check Oxylabs credentials
    if not hasattr(config, 'OXYLABS_USERNAME'):
        errors.append("OXYLABS_USERNAME not defined")
    elif config.OXYLABS_USERNAME == "your_username_here":
        errors.append("OXYLABS_USERNAME is still placeholder - add your actual username")
    else:
        print(f"✅ OXYLABS_USERNAME: {config.OXYLABS_USERNAME}")
    
    if not hasattr(config, 'OXYLABS_PASSWORD'):
        errors.append("OXYLABS_PASSWORD not defined")
    elif config.OXYLABS_PASSWORD == "your_password_here":
        errors.append("OXYLABS_PASSWORD is still placeholder - add your actual password")
    else:
        print(f"✅ OXYLABS_PASSWORD: {'*' * len(config.OXYLABS_PASSWORD)} (hidden)")
    
    # Check scraping limit
    if hasattr(config, 'MAX_PAGES_TO_SCRAPE'):
        pages = config.MAX_PAGES_TO_SCRAPE
        print(f"✅ MAX_PAGES_TO_SCRAPE: {pages}")
        if pages > 5:
            warnings.append(f"MAX_PAGES_TO_SCRAPE is {pages} - this may use many API credits on free trial")
    else:
        errors.append("MAX_PAGES_TO_SCRAPE not defined")
    
    # Check Ollama settings
    if hasattr(config, 'OLLAMA_HOST'):
        print(f"✅ OLLAMA_HOST: {config.OLLAMA_HOST}")
    else:
        errors.append("OLLAMA_HOST not defined")
    
    if hasattr(config, 'OLLAMA_PORT'):
        print(f"✅ OLLAMA_PORT: {config.OLLAMA_PORT}")
    else:
        errors.append("OLLAMA_PORT not defined")
    
    if hasattr(config, 'OLLAMA_URL'):
        print(f"✅ OLLAMA_URL: {config.OLLAMA_URL}")
    else:
        errors.append("OLLAMA_URL not defined")
    
    if hasattr(config, 'OLLAMA_MODEL'):
        print(f"✅ OLLAMA_MODEL: {config.OLLAMA_MODEL}")
    else:
        errors.append("OLLAMA_MODEL not defined")
    
    # Check Flask settings
    if hasattr(config, 'FLASK_HOST'):
        print(f"✅ FLASK_HOST: {config.FLASK_HOST}")
    else:
        errors.append("FLASK_HOST not defined")
    
    if hasattr(config, 'FLASK_PORT'):
        print(f"✅ FLASK_PORT: {config.FLASK_PORT}")
    else:
        errors.append("FLASK_PORT not defined")
    
    # Check session secret
    if hasattr(config, 'SESSION_SECRET'):
        if config.SESSION_SECRET == "your-secret-key-here-change-this-in-production":
            warnings.append("SESSION_SECRET is still default - consider changing for security")
        print(f"✅ SESSION_SECRET: {'*' * 20} (hidden)")
    else:
        errors.append("SESSION_SECRET not defined")
    
    print()
    print("=" * 50)
    
    # Print warnings
    if warnings:
        print()
        print("⚠️  WARNINGS:")
        for warning in warnings:
            print(f"   - {warning}")
    
    # Print errors
    if errors:
        print()
        print("❌ ERRORS:")
        for error in errors:
            print(f"   - {error}")
        print()
        print("Please fix these errors in config.py before running the application")
        return False
    else:
        print()
        print("✅ Configuration looks good!")
        print()
        print("Next steps:")
        print("1. Make sure Ollama is running: ollama serve")
        print("2. Start the app: python app.py")
        print("3. Open browser: http://127.0.0.1:5000")
        return True

if __name__ == "__main__":
    success = check_config()
    print()
    sys.exit(0 if success else 1)

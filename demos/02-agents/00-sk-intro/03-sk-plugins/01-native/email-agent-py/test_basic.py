"""Simple test script to validate basic functionality without external dependencies."""

import os
import sys
sys.path.append('.')

# Test configuration loading
try:
    from common.app_config import AppConfig
    print("✓ Configuration module imported successfully")
    
    # Test configuration loading (will use default values since we don't have real env vars)
    config = AppConfig.from_env()
    print("✓ Configuration loaded successfully")
    print(f"  SK Model: {config.semantic_kernel.model}")
    print(f"  Graph Mail Sender: {config.graph.mail_sender or '(not set)'}")
    
except ImportError as e:
    print(f"✗ Import error: {e}")
except Exception as e:
    print(f"✗ Configuration error: {e}")

# Test plugin import (without actually instantiating due to dependencies)
try:
    from plugins.email_plugin import EmailPlugin
    print("✓ Email plugin module imported successfully")
except ImportError as e:
    print(f"✗ Plugin import error: {e}")

print("\nBasic structure validation complete!")
print("To run the full application, install dependencies with: pip install -r requirements.txt")
print("Then configure your .env file with actual credentials.")
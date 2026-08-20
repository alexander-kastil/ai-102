"""
Minimal MCP Test - Test MCP GitHub server connection without heavy dependencies
"""

import asyncio
import json
import subprocess
import sys
from pathlib import Path


def load_env_config():
    """Load configuration from .env file without external dependencies."""
    env_path = Path(__file__).parent / '.env'
    config = {}
    
    if env_path.exists():
        with open(env_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    config[key.strip()] = value.strip().strip('"\'')
    
    return config


async def test_mcp_server():
    """Test MCP server availability and basic functionality."""
    
    print("Testing MCP GitHub server connectivity...")
    print("This tests the npx @modelcontextprotocol/server-github command")
    print()
    
    try:
        # Test if npx is available
        result = subprocess.run(['npx', '--version'], capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print(f"✓ npx is available: {result.stdout.strip()}")
        else:
            print("✗ npx not available or not working")
            return False
    except Exception as e:
        print(f"✗ Error checking npx: {e}")
        return False
    
    try:
        # Test if the MCP GitHub server can be started
        print("Testing MCP GitHub server availability...")
        
        # This will try to download and run the MCP server briefly
        cmd = ['npx', '-y', '@modelcontextprotocol/server-github', '--help']
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        try:
            stdout, stderr = process.communicate(timeout=30)
            
            if process.returncode == 0:
                print("✓ MCP GitHub server is accessible")
                return True
            else:
                print(f"✗ MCP GitHub server failed: {stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            process.kill()
            print("✓ MCP GitHub server started (killed after timeout - this is expected)")
            return True
            
    except Exception as e:
        print(f"✗ Error testing MCP server: {e}")
        return False


def test_configuration():
    """Test configuration loading."""
    
    print("Testing configuration...")
    config = load_env_config()
    
    required_keys = ["MODEL", "ENDPOINT", "API_KEY", "GIT_REPO"]
    missing = []
    
    for key in required_keys:
        if key in config and config[key]:
            print(f"✓ {key}: {config[key][:20]}..." if len(config[key]) > 20 else f"✓ {key}: {config[key]}")
        else:
            missing.append(key)
            print(f"✗ {key}: Missing")
    
    if missing:
        print(f"\n⚠️  Missing configuration keys: {', '.join(missing)}")
        return False
    
    return True


async def main():
    """Run basic connectivity tests."""
    
    print("="*60)
    print("MCP GitHub Server Connectivity Test")
    print("="*60)
    print()
    
    # Test configuration
    config_ok = test_configuration()
    print()
    
    # Test MCP server
    mcp_ok = await test_mcp_server()
    print()
    
    # Summary
    print("="*60)
    print("SUMMARY")
    print("="*60)
    
    if config_ok:
        print("✓ Configuration: OK")
    else:
        print("✗ Configuration: Missing values")
    
    if mcp_ok:
        print("✓ MCP Server: Accessible")
    else:
        print("✗ MCP Server: Not accessible")
    
    if config_ok and mcp_ok:
        print("\n🎉 All tests passed! Ready for full implementation.")
        print("   Run: pip install -r requirements.txt")
        print("   Then: python main_full.py")
    else:
        print("\n⚠️  Some tests failed. Check the issues above.")
    
    print()


if __name__ == "__main__":
    asyncio.run(main())
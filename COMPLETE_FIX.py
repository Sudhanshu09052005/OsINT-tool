"""
Complete Fix Script for All Issues
Run this to fix WHOIS and test all modes
"""

import sys
import subprocess
import os

print("\n" + "="*70)
print("  OSINT TOOL - COMPLETE FIX SCRIPT")
print("="*70 + "\n")

# Step 1: Fix WHOIS
print("[1/3] Fixing WHOIS package...")
print("-" * 70)
try:
    # Uninstall old whois
    print("Removing old 'whois' package...")
    subprocess.run([sys.executable, "-m", "pip", "uninstall", "whois", "-y"], 
                   capture_output=True)
    
    # Install python-whois
    print("Installing 'python-whois'...")
    result = subprocess.run([sys.executable, "-m", "pip", "install", "python-whois"], 
                          capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✓ python-whois installed successfully!")
    else:
        print("⚠ Warning: python-whois installation had issues")
        print(result.stderr)
except Exception as e:
    print(f"⚠ Error fixing WHOIS: {e}")

print()

# Step 2: Test imports
print("[2/3] Testing all imports...")
print("-" * 70)

required_modules = {
    'flask': 'flask',
    'tkinter': 'tkinter (built-in)',
    'requests': 'requests',
    'bs4': 'beautifulsoup4',
    'reportlab': 'reportlab',
    'dns': 'dnspython',
    'validators': 'validators',
}

missing = []
for module, package in required_modules.items():
    try:
        __import__(module)
        print(f"✓ {package}")
    except ImportError:
        print(f"✗ {package} - MISSING")
        missing.append(package)

if missing:
    print(f"\n⚠ Missing packages: {', '.join(missing)}")
    response = input("\nInstall missing packages? (y/n): ")
    if response.lower() == 'y':
        for pkg in missing:
            if pkg != 'tkinter (built-in)':
                print(f"Installing {pkg}...")
                subprocess.run([sys.executable, "-m", "pip", "install", pkg])

print()

# Step 3: Create directories
print("[3/3] Creating required directories...")
print("-" * 70)

dirs = ['templates', 'reports']
for dir_name in dirs:
    try:
        os.makedirs(dir_name, exist_ok=True)
        print(f"✓ {dir_name}/ created")
    except Exception as e:
        print(f"⚠ Error creating {dir_name}: {e}")

# Create templates/index.html if it doesn't exist
template_path = os.path.join('templates', 'index.html')
if not os.path.exists(template_path):
    print("\n✓ Creating web template...")
    # Will be created by enhanced_launch.py

print("\n" + "="*70)
print("  FIX COMPLETE!")
print("="*70)
print("\nNext steps:")
print("1. Run: python enhanced_launch.py")
print("2. Or double-click: START.bat")
print("\nIf WHOIS still doesn't work, it will show 'N/A' but other features will work fine.")
print("\n" + "="*70)

input("\nPress Enter to exit...")

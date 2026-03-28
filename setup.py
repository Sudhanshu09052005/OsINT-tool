#!/usr/bin/env python3
"""
Setup script for OSINT Tool
Ensures all dependencies are installed and environment is configured
"""

import subprocess
import sys
import os


def install_requirements():
    """Install all required packages"""
    print("🔧 Installing OSINT Tool Dependencies...")
    print("=" * 60)
    
    requirements = [
        'requests==2.31.0',
        'dnspython==2.4.2',
        'whois==0.9.7',
        'certifi==2023.7.22',
        'beautifulsoup4==4.12.2',
        'Pillow==10.0.1',
        'reportlab==4.0.4',
        'validators==0.22.0',
    ]
    
    for req in requirements:
        print(f"📦 Installing {req}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", req])
    
    print("=" * 60)
    print("✓ All dependencies installed successfully!")


def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 7):
        print("❌ Python 3.7 or higher is required!")
        print(f"Current version: {sys.version}")
        sys.exit(1)
    print(f"✓ Python version: {sys.version.split()[0]}")


def main():
    """Main setup function"""
    print("╔" + "=" * 58 + "╗")
    print("║" + " OSINT Tool Setup ".center(58) + "║")
    print("╚" + "=" * 58 + "╝\n")
    
    # Check Python version
    print("🔍 Checking Python version...")
    check_python_version()
    print()
    
    # Install requirements
    try:
        install_requirements()
        print()
        print("🎉 Setup complete! You can now run: python osint_tool.py")
    except Exception as e:
        print(f"❌ Setup failed: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()

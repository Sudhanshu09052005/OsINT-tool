#!/usr/bin/env python3
"""
OSINT Tool Quick Launcher
Handles dependency checking and launches the tool
"""

import sys
import subprocess
import importlib


REQUIRED_PACKAGES = {
    'requests': 'requests',
    'dns': 'dnspython',
    'whois': 'whois',
    'certifi': 'certifi',
    'bs4': 'beautifulsoup4',
    'PIL': 'Pillow',
    'reportlab': 'reportlab',
    'validators': 'validators',
}


def check_dependencies():
    """Check if all required packages are installed"""
    missing = []
    
    for module, package in REQUIRED_PACKAGES.items():
        try:
            importlib.import_module(module)
            print(f"✓ {package}")
        except ImportError:
            print(f"✗ {package} - MISSING")
            missing.append(package)
    
    return missing


def install_packages(packages):
    """Install missing packages"""
    print("\n[!] Installing missing packages...\n")
    for package in packages:
        print(f"[*] Installing {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    print("\n[+] All packages installed!\n")


def main():
    """Main launcher function"""
    print("╔" + "=" * 58 + "╗")
    print("║" + " OSINT Tool Launcher ".center(58) + "║")
    print("╚" + "=" * 58 + "╝\n")
    
    print("[*] Checking dependencies...\n")
    missing = check_dependencies()
    
    if missing:
        response = input(f"\n[?] Install {len(missing)} missing package(s)? (y/n): ").lower()
        if response == 'y':
            install_packages(missing)
        else:
            print("[!] Cannot proceed without dependencies")
            sys.exit(1)
    
    print("\n[+] All dependencies satisfied!")
    print("[*] Launching OSINT Tool...\n")
    
    try:
        import osint_tool
        osint_tool.main()
    except Exception as e:
        print(f"[!] Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()

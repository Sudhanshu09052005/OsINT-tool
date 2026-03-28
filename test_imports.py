"""
Quick WHOIS Fix and Test Script
"""

# Test 1: Check which whois package is installed
print("Testing WHOIS packages...")
print("=" * 60)

try:
    import whois
    print("✓ 'whois' module found")
    print(f"  Location: {whois.__file__}")
    print(f"  Has 'whois' function: {hasattr(whois, 'whois')}")
    print(f"  Has 'query' function: {hasattr(whois, 'query')}")
except ImportError as e:
    print(f"✗ 'whois' module not found: {e}")

print()

try:
    import pythonwhois
    print("✓ 'python-whois' module found")
    print(f"  Location: {pythonwhois.__file__}")
except ImportError as e:
    print(f"✗ 'python-whois' module not found: {e}")

print()
print("=" * 60)
print("\nRecommendation:")
print("Run: pip uninstall whois")
print("Then: pip install python-whois")
print("=" * 60)

# Test 2: Check Flask
print("\n\nTesting Flask...")
print("=" * 60)
try:
    import flask
    print(f"✓ Flask installed: version {flask.__version__}")
except ImportError as e:
    print(f"✗ Flask not found: {e}")
    print("  Run: pip install flask")

# Test 3: Check Tkinter
print("\n\nTesting Tkinter...")
print("=" * 60)
try:
    import tkinter
    print("✓ Tkinter available")
except ImportError as e:
    print(f"✗ Tkinter not found: {e}")
    print("  Tkinter should be built-in with Python")

print("\n\n" + "=" * 60)
print("TESTS COMPLETE")
print("=" * 60)

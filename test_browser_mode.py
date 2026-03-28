"""
Browser Mode Diagnostic Script
Check karo kya problem hai
"""

print("="*70)
print("  BROWSER MODE DIAGNOSTIC")
print("="*70)
print()

# Check 1: Flask
print("[1/5] Checking Flask...")
try:
    import flask
    print(f"✓ Flask installed: v{flask.__version__}")
except ImportError:
    print("✗ Flask NOT installed")
    print("  FIX: pip install flask")
    print()
    import sys
    response = input("Install Flask now? (y/n): ")
    if response.lower() == 'y':
        import subprocess
        subprocess.run([sys.executable, "-m", "pip", "install", "flask"])
        print("✓ Flask installed!")

print()

# Check 2: Templates directory
print("[2/5] Checking templates directory...")
import os
if os.path.exists('templates'):
    print("✓ templates/ folder exists")
    if os.path.exists('templates/index.html'):
        print("✓ templates/index.html exists")
    else:
        print("✗ templates/index.html missing")
        print("  Creating it now...")
        # Will create below
else:
    print("✗ templates/ folder missing")
    print("  Creating it now...")
    os.makedirs('templates', exist_ok=True)

print()

# Check 3: Reports directory
print("[3/5] Checking reports directory...")
if os.path.exists('reports'):
    print("✓ reports/ folder exists")
else:
    print("  Creating reports/ folder...")
    os.makedirs('reports', exist_ok=True)
    print("✓ Created!")

print()

# Check 4: Web app file
print("[4/5] Checking web_app.py...")
if os.path.exists('web_app.py'):
    print("✓ web_app.py exists")
else:
    print("✗ web_app.py missing!")

print()

# Check 5: Port availability
print("[5/5] Checking if port 5000 is free...")
import socket
def is_port_free(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(('', port))
            return True
        except:
            return False

if is_port_free(5000):
    print("✓ Port 5000 is FREE")
else:
    print("⚠ Port 5000 is BUSY")
    print("  Will try port 5001 instead")

print()
print("="*70)
print("  DIAGNOSTIC COMPLETE")
print("="*70)
print()

# Create simple HTML template if missing
if not os.path.exists('templates/index.html'):
    print("Creating simple HTML template...")
    html = '''<!DOCTYPE html>
<html>
<head>
    <title>OSINT Tool</title>
    <style>
        body { font-family: Arial; margin: 40px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
        .container { max-width: 900px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; }
        h1 { color: #333; }
        input { width: 70%; padding: 10px; font-size: 16px; }
        button { padding: 10px 20px; font-size: 16px; background: #667eea; color: white; border: none; cursor: pointer; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔍 OSINT Investigation Tool</h1>
        <p>Browser mode working! Enter a URL to scan.</p>
        <input type="text" id="url" placeholder="https://example.com" value="https://example.com">
        <button onclick="alert('Scanning: ' + document.getElementById('url').value)">Start Scan</button>
    </div>
</body>
</html>'''
    
    os.makedirs('templates', exist_ok=True)
    with open('templates/index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("✓ HTML template created!")

print()
print("Now try running: python web_app.py")
print("Or: python enhanced_launch.py and select option 1")
print()
input("Press Enter to exit...")

#!/usr/bin/env python3
"""
Enhanced OSINT Tool Launcher
Dual Mode: Browser Interface or Desktop Software
For College Project Submission
"""

import sys
import os
import subprocess

def print_banner():
    print("\n" + "="*70)
    print("  ╔═══════════════════════════════════════════════════════════════╗")
    print("  ║           OSINT INVESTIGATION TOOL - ENHANCED VERSION          ║")
    print("  ║         Advanced Website Reconnaissance & Analysis             ║")
    print("  ╚═══════════════════════════════════════════════════════════════╝")
    print("="*70 + "\n")

def check_dependencies():
    """Check and install required dependencies"""
    print("[*] Checking dependencies...\n")
    
    required = {
        'requests': 'requests',
        'dns': 'dnspython',
        'whois': 'python-whois',
        'bs4': 'beautifulsoup4',
        'reportlab': 'reportlab',
        'validators': 'validators',
        'flask': 'flask'
    }
    
    missing = []
    
    for module, package in required.items():
        try:
            __import__(module)
            print(f"✓ {package} - OK")
        except ImportError:
            print(f"✗ {package} - MISSING")
            missing.append(package)
    
    if missing:
        print(f"\n[!] {len(missing)} package(s) missing")
        response = input("\n[?] Do you want to install missing packages? (y/n): ").lower()
        if response == 'y':
            print("\n[*] Installing packages...\n")
            for package in missing:
                print(f"[*] Installing {package}...")
                try:
                    subprocess.check_call([sys.executable, "-m", "pip", "install", package])
                    print(f"✓ {package} installed\n")
                except:
                    print(f"✗ Failed to install {package}\n")
            print("[+] Installation complete!\n")
        else:
            print("[!] Cannot proceed without dependencies")
            input("\nPress Enter to exit...")
            sys.exit(1)
    else:
        print("\n[+] All dependencies satisfied!\n")

def create_directories():
    """Create required directories"""
    dirs = ['templates', 'reports']
    for dir_name in dirs:
        os.makedirs(dir_name, exist_ok=True)

def show_menu():
    """Show main menu"""
    print("\n" + "─"*70)
    print("  SELECT MODE:")
    print("─"*70)
    print("\n  [1] 🌐 Browser Mode  - Modern web interface (Recommended)")
    print("                        Access via web browser at http://localhost:5000")
    print("                        Better UI, responsive design, easy to use")
    print("\n  [2] 💻 Desktop Mode  - Traditional GUI application")
    print("                        Tkinter-based desktop software")
    print("                        Works without internet for local scanning")
    print("\n  [3] ❌ Exit")
    print("\n" + "─"*70)

def launch_browser_mode():
    """Launch Flask web interface"""
    print("\n[*] Starting Browser Mode...")
    print("[*] Creating required files...\n")
    
    create_directories()
    create_html_template()
    
    print("\n" + "="*70)
    print("  🌐 BROWSER MODE STARTING")
    print("="*70)
    print("\n  ✓ Web server initializing...")
    print("  ✓ URL: http://localhost:5000")
    print("  ✓ Open your browser and navigate to the URL above")
    print("\n  [!] Press Ctrl+C to stop the server")
    print("\n" + "="*70 + "\n")
    
    try:
        import web_app
    except Exception as e:
        print(f"\n[!] Error starting browser mode: {str(e)}")
        input("\nPress Enter to return to menu...")

def launch_desktop_mode():
    """Launch Tkinter GUI"""
    print("\n[*] Starting Desktop Mode...")
    print("[*] Loading GUI application...\n")
    
    print("\n" + "="*70)
    print("  💻 DESKTOP MODE STARTING")
    print("="*70)
    print("\n  ✓ Initializing Tkinter GUI...")
    print("  ✓ Application window will open shortly")
    print("\n" + "="*70 + "\n")
    
    try:
        import enhanced_osint_tool
        enhanced_osint_tool.main()
    except Exception as e:
        print(f"\n[!] Error starting desktop mode: {str(e)}")
        input("\nPress Enter to return to menu...")

def create_html_template():
    """Create HTML template if it doesn't exist"""
    template_file = os.path.join('templates', 'index.html')
    
    if not os.path.exists(template_file):
        html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OSINT Investigation Tool</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container { max-width: 1400px; margin: 0 auto; }
        .header { text-align: center; color: white; margin-bottom: 30px; }
        .header h1 { font-size: 2.5em; margin-bottom: 10px; text-shadow: 2px 2px 4px rgba(0,0,0,0.3); }
        .card {
            background: white;
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            margin-bottom: 20px;
        }
        .input-section { display: flex; gap: 10px; margin-bottom: 20px; }
        .input-field {
            flex: 1;
            padding: 15px;
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            font-size: 16px;
        }
        .btn {
            padding: 15px 40px;
            border: none;
            border-radius: 10px;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
        }
        .btn-primary {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        #progressSection { display: none; margin: 20px 0; }
        .progress-bar { width: 100%; height: 30px; background: #e0e0e0; border-radius: 15px; overflow: hidden; }
        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #4caf50 0%, #8bc34a 100%);
            transition: width 0.3s;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: bold;
        }
        #resultsSection { display: none; }
        .info-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 15px;
        }
        .info-item {
            background: #f9f9f9;
            padding: 15px;
            border-radius: 8px;
            border-left: 4px solid #667eea;
        }
        .info-label { font-weight: bold; color: #667eea; margin-bottom: 5px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔍 OSINT Investigation Tool</h1>
            <p>Advanced Website Reconnaissance & Security Analysis</p>
        </div>
        <div class="card">
            <div class="input-section">
                <input type="text" id="urlInput" class="input-field" placeholder="Enter target URL" value="https://">
                <button class="btn btn-primary" onclick="startScan()">Start Investigation</button>
            </div>
            <div id="progressSection">
                <div class="progress-bar">
                    <div id="progressFill" class="progress-fill">0%</div>
                </div>
                <div id="statusText" style="text-align:center;margin-top:10px;color:#666;">Initializing...</div>
            </div>
        </div>
        <div id="resultsSection">
            <div class="card">
                <h2>Investigation Results</h2>
                <div id="resultsContent" class="info-grid"></div>
            </div>
        </div>
    </div>
    <script>
        let currentScanId = null;
        function startScan() {
            const url = document.getElementById('urlInput').value.trim();
            if (!url || url === 'https://') { alert('Please enter a valid URL'); return; }
            document.getElementById('progressSection').style.display = 'block';
            fetch('/api/scan', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({url: url})
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    currentScanId = data.scan_id;
                    checkStatus();
                }
            });
        }
        function checkStatus() {
            fetch(`/api/scan/${currentScanId}/status`)
            .then(response => response.json())
            .then(data => {
                document.getElementById('progressFill').style.width = data.progress + '%';
                document.getElementById('progressFill').textContent = data.progress + '%';
                if (data.status === 'completed') {
                    displayResults(data.data);
                } else {
                    setTimeout(checkStatus, 1000);
                }
            });
        }
        function displayResults(data) {
            document.getElementById('resultsSection').style.display = 'block';
            const html = `
                <div class="info-item"><div class="info-label">Domain</div><div>${data.domain?.domain || 'N/A'}</div></div>
                <div class="info-item"><div class="info-label">IP</div><div>${data.ip?.ip || 'N/A'}</div></div>
                <div class="info-item"><div class="info-label">Security Score</div><div>${data.security_headers?.security_score || 0}%</div></div>
                <div class="info-item"><div class="info-label">Open Ports</div><div>${data.port_scan?.open_ports || 0}</div></div>
            `;
            document.getElementById('resultsContent').innerHTML = html;
        }
    </script>
</body>
</html>'''
        
        with open(template_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"[+] Created HTML template: {template_file}")

def main():
    """Main launcher function"""
    print_banner()
    check_dependencies()
    
    while True:
        show_menu()
        
        try:
            choice = input("\n  Enter your choice (1-3): ").strip()
            
            if choice == '1':
                launch_browser_mode()
            elif choice == '2':
                launch_desktop_mode()
            elif choice == '3':
                print("\n[*] Thank you for using OSINT Investigation Tool!")
                print("[*] Goodbye!\n")
                sys.exit(0)
            else:
                print("\n[!] Invalid choice. Please enter 1, 2, or 3")
                input("\nPress Enter to continue...")
        
        except KeyboardInterrupt:
            print("\n\n[!] Interrupted by user")
            print("[*] Goodbye!\n")
            sys.exit(0)
        except Exception as e:
            print(f"\n[!] Error: {str(e)}")
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()

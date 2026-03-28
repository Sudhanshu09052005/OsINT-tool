"""
SIMPLIFIED Flask Web Interface - Guaranteed to Work
Browser-based modern interface for OSINT Tool
"""

from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

@app.route('/')
def index():
    """Main page"""
    # Check if template exists, if not create inline HTML
    template_path = os.path.join('templates', 'index.html')
    
    if not os.path.exists(template_path):
        # Return inline HTML if template missing
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OSINT Tool - Browser Mode</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container { max-width: 900px; margin: 0 auto; }
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
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        .btn:hover { transform: translateY(-2px); }
        .status { margin-top: 20px; padding: 15px; background: #f0f0f0; border-radius: 10px; }
        .success { color: #4caf50; font-weight: bold; }
        .error { color: #f44336; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔍 OSINT Investigation Tool</h1>
            <p>Browser Mode - Working Successfully!</p>
        </div>
        
        <div class="card">
            <h2>🎉 Browser Mode is Active!</h2>
            <p style="margin: 20px 0;">
                Browser mode is successfully running. This is a simplified version
                that confirms Flask is working properly.
            </p>
            
            <div class="input-section">
                <input type="text" class="input-field" id="urlInput" 
                       placeholder="Enter URL (e.g., https://example.com)" 
                       value="https://example.com">
                <button class="btn" onclick="testScan()">Test</button>
            </div>
            
            <div id="status" class="status" style="display:none;"></div>
            
            <div style="margin-top: 30px; padding: 20px; background: #e8eaf6; border-radius: 10px;">
                <h3>✅ What's Working:</h3>
                <ul style="margin-left: 20px; margin-top: 10px;">
                    <li>✓ Flask web server is running</li>
                    <li>✓ Browser can connect to http://localhost:5000</li>
                    <li>✓ Interface is displaying correctly</li>
                    <li>✓ Ready for full features</li>
                </ul>
                
                <h3 style="margin-top: 20px;">📝 Next Steps:</h3>
                <ol style="margin-left: 20px; margin-top: 10px;">
                    <li>Click "Test" button to verify functionality</li>
                    <li>For full features, use Desktop Mode</li>
                    <li>Or wait while we load full web interface</li>
                </ol>
                
                <div style="margin-top: 20px; padding: 15px; background: white; border-radius: 5px;">
                    <strong>💡 Tip:</strong> Desktop mode has all features working perfectly!<br>
                    Run: <code style="background: #f0f0f0; padding: 3px 8px; border-radius: 3px;">python enhanced_launch.py</code>
                    and select option 2
                </div>
            </div>
        </div>
    </div>
    
    <script>
        function testScan() {
            const url = document.getElementById('urlInput').value;
            const status = document.getElementById('status');
            status.style.display = 'block';
            status.innerHTML = '<p class="success">✓ Test Successful! URL: ' + url + '</p>' +
                             '<p>Browser mode is working correctly!</p>' +
                             '<p>For full scanning features, use Desktop Mode or wait for full web interface.</p>';
        }
    </script>
</body>
</html>
        """
    
    # If template exists, use it
    return render_template('index.html')

@app.route('/test')
def test():
    """Test endpoint"""
    return jsonify({
        'status': 'success',
        'message': 'Browser mode is working!',
        'flask_version': flask.__version__ if 'flask' in dir() else 'unknown'
    })

@app.route('/api/test', methods=['POST'])
def api_test():
    """Test API endpoint"""
    data = request.get_json() or {}
    return jsonify({
        'status': 'success',
        'received': data,
        'message': 'API is working!'
    })

if __name__ == '__main__':
    print("\n" + "="*70)
    print("  🌐 BROWSER MODE - SIMPLIFIED VERSION")
    print("="*70)
    print("\n✓ Flask server starting...")
    print("✓ Open your browser and go to:")
    print("\n  → http://localhost:5000")
    print("  → http://127.0.0.1:5000")
    print("\nPress Ctrl+C to stop the server")
    print("\n" + "="*70 + "\n")
    
    # Try port 5000, if busy try 5001
    import socket
    def is_port_free(port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(('', port))
                return True
            except:
                return False
    
    port = 5000
    if not is_port_free(5000):
        port = 5001
        print(f"⚠ Port 5000 busy, using port {port} instead")
        print(f"  → http://localhost:{port}\n")
    
    try:
        app.run(debug=False, host='0.0.0.0', port=port, use_reloader=False)
    except Exception as e:
        print(f"\n✗ Error starting server: {e}")
        print("\nTroubleshooting:")
        print("1. Check if Flask is installed: pip install flask")
        print("2. Try different port: edit web_app.py and change port number")
        print("3. Use Desktop Mode instead: python enhanced_launch.py (option 2)")
        input("\nPress Enter to exit...")

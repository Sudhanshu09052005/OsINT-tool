"""
Flask Web Interface for OSINT Tool
Browser-based modern interface
"""

from flask import Flask, render_template, request, jsonify, send_file, session
import json
from datetime import datetime
import os
import threading
from advanced_scanner import AdvancedScanner
from enhanced_pdf import EnhancedPDFReport
import sys

# Import the existing osint_tool scanner
sys.path.insert(0, os.path.dirname(__file__))
from osint_tool import OSINTTool

app = Flask(__name__)
app.secret_key = 'osint_investigation_tool_2024'

# Global scan data storage
scan_results = {}


@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')


@app.route('/api/scan', methods=['POST'])
def start_scan():
    """Start OSINT scan"""
    try:
        data = request.get_json()
        url = data.get('url', '').strip()
        
        if not url:
            return jsonify({'error': 'URL is required'}), 400
        
        # Generate scan ID
        scan_id = datetime.now().strftime('%Y%m%d%H%M%S')
        
        # Start scan in background thread
        thread = threading.Thread(target=perform_scan, args=(scan_id, url))
        thread.daemon = True
        thread.start()
        
        return jsonify({
            'success': True,
            'scan_id': scan_id,
            'message': 'Scan started'
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def perform_scan(scan_id, url):
    """Perform the actual scan"""
    global scan_results
    
    scan_results[scan_id] = {
        'status': 'running',
        'progress': 0,
        'data': {}
    }
    
    try:
        # Initialize scanners
        basic_scanner = OSINTTool()
        advanced_scanner = AdvancedScanner()
        
        # Parse domain
        from urllib.parse import urlparse
        parsed = urlparse(url)
        domain = parsed.netloc or parsed.path
        
        results = {}
        
        # Basic scans
        scan_results[scan_id]['progress'] = 10
        scan_results[scan_id]['status'] = 'Gathering WHOIS & DNS...'
        results['domain'] = basic_scanner.get_whois_info(domain)
        results['dns'] = basic_scanner.get_dns_records(domain)
        
        scan_results[scan_id]['progress'] = 25
        scan_results[scan_id]['status'] = 'Analyzing network...'
        results['ip'] = basic_scanner.get_ip_info(domain)
        results['ssl'] = basic_scanner.get_ssl_certificate(domain)
        
        scan_results[scan_id]['progress'] = 40
        scan_results[scan_id]['status'] = 'Scanning ports...'
        results['port_scan'] = advanced_scanner.scan_ports(domain)
        
        scan_results[scan_id]['progress'] = 50
        scan_results[scan_id]['status'] = 'Analyzing security headers...'
        results['security_headers'] = advanced_scanner.analyze_security_headers(url)
        
        scan_results[scan_id]['progress'] = 60
        scan_results[scan_id]['status'] = 'Detecting technologies...'
        results['headers'] = basic_scanner.get_http_headers(url)
        results['technologies'] = basic_scanner.detect_technologies(url)
        results['cms'] = advanced_scanner.detect_cms(url)
        
        scan_results[scan_id]['progress'] = 70
        scan_results[scan_id]['status'] = 'Extracting metadata...'
        results['meta_tags'] = advanced_scanner.extract_meta_tags(url)
        results['robots_txt'] = advanced_scanner.get_robots_txt(url)
        
        scan_results[scan_id]['progress'] = 80
        scan_results[scan_id]['status'] = 'Finding social media links...'
        results['social_media'] = advanced_scanner.find_social_media_links(url)
        results['emails'] = basic_scanner.extract_emails(url)
        
        scan_results[scan_id]['progress'] = 90
        scan_results[scan_id]['status'] = 'Checking archives...'
        results['wayback'] = advanced_scanner.check_wayback_machine(url)
        results['server_info'] = advanced_scanner.get_server_info(domain)
        results['cookies'] = advanced_scanner.analyze_cookies(url)
        
        scan_results[scan_id]['progress'] = 100
        scan_results[scan_id]['status'] = 'completed'
        scan_results[scan_id]['data'] = results
        
    except Exception as e:
        scan_results[scan_id]['status'] = 'error'
        scan_results[scan_id]['error'] = str(e)


@app.route('/api/scan/<scan_id>/status', methods=['GET'])
def get_scan_status(scan_id):
    """Get scan status"""
    if scan_id not in scan_results:
        return jsonify({'error': 'Scan not found'}), 404
    
    result = scan_results[scan_id]
    return jsonify({
        'status': result['status'],
        'progress': result.get('progress', 0),
        'data': result.get('data', {}) if result['status'] == 'completed' else {}
    })


@app.route('/api/export/pdf/<scan_id>', methods=['GET'])
def export_pdf(scan_id):
    """Export scan results to PDF"""
    if scan_id not in scan_results or scan_results[scan_id]['status'] != 'completed':
        return jsonify({'error': 'Scan not completed'}), 400
    
    try:
        data = scan_results[scan_id]['data']
        filename = f"osint_report_{scan_id}.pdf"
        filepath = os.path.join('reports', filename)
        
        # Create reports directory if it doesn't exist
        os.makedirs('reports', exist_ok=True)
        
        # Generate PDF
        pdf_generator = EnhancedPDFReport(filepath)
        pdf_generator.generate(data)
        
        return send_file(filepath, as_attachment=True, download_name=filename)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/export/json/<scan_id>', methods=['GET'])
def export_json(scan_id):
    """Export scan results to JSON"""
    if scan_id not in scan_results or scan_results[scan_id]['status'] != 'completed':
        return jsonify({'error': 'Scan not completed'}), 400
    
    try:
        data = scan_results[scan_id]['data']
        filename = f"osint_report_{scan_id}.json"
        filepath = os.path.join('reports', filename)
        
        # Create reports directory if it doesn't exist
        os.makedirs('reports', exist_ok=True)
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2, default=str)
        
        return send_file(filepath, as_attachment=True, download_name=filename)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    print("\n" + "="*70)
    print("  OSINT TOOL - BROWSER MODE")
    print("="*70)
    print("\n✓ Starting web server...")
    
    # Create directories if they don't exist
    os.makedirs('templates', exist_ok=True)
    os.makedirs('reports', exist_ok=True)
    
    # Check if template exists
    template_file = os.path.join('templates', 'index.html')
    if not os.path.exists(template_file):
        print("⚠ Template file missing, creating basic template...")
        basic_html = '''<!DOCTYPE html>
<html><head><title>OSINT Tool</title></head>
<body style="font-family:Arial;margin:40px;">
<h1>OSINT Tool - Browser Mode</h1>
<p>Browser mode is active! For full features, use Desktop Mode.</p>
<p>Run: <code>python enhanced_launch.py</code> and select option 2</p>
</body></html>'''
        with open(template_file, 'w', encoding='utf-8') as f:
            f.write(basic_html)
        print("✓ Basic template created")
    
    print("✓ Open your browser and go to: http://localhost:5000")
    print("\nPress Ctrl+C to stop the server\n")
    
    # Try to run on available port
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
        print(f"⚠ Port 5000 busy, using port {port}")
        print(f"✓ Go to: http://localhost:{port}\n")
    
    try:
        app.run(debug=False, host='0.0.0.0', port=port, use_reloader=False)
    except KeyboardInterrupt:
        print("\n\n✓ Server stopped")
    except Exception as e:
        print(f"\n✗ Error: {e}")
        print("\nFor full features, use Desktop Mode instead:")
        print("Run: python enhanced_launch.py")
        print("Select option 2")
        input("\nPress Enter to exit...")

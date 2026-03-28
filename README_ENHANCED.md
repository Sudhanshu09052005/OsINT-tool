# OSINT Investigation Tool - Enhanced Edition 🔍

## College Project - Advanced Website Reconnaissance & Security Analysis

### ✨ Features

#### 🎯 **Dual Mode Operation**
- **Browser Mode** - Modern web interface accessible at http://localhost:5000
- **Desktop Mode** - Traditional Tkinter GUI application

#### 🔍 **Investigation Capabilities**

**Basic OSINT:**
- ✅ WHOIS Information
- ✅ DNS Records (A, AAAA, MX, NS, TXT, CNAME, SOA)
- ✅ IP Geolocation
- ✅ SSL Certificate Analysis
- ✅ HTTP Headers
- ✅ Technology Stack Detection
- ✅ Email & Phone Extraction

**Advanced Investigation Features:**
- 🔌 **Port Scanning** - Detect open ports and services
- 🔒 **Security Header Analysis** - Identify missing security headers
- 🤖 **CMS Detection** - WordPress, Joomla, Drupal, etc.
- 📝 **Metadata Extraction** - All meta tags, Open Graph, Twitter Cards
- 🗺️ **robots.txt Analysis** - Restricted paths and sitemaps
- 📱 **Social Media Discovery** - Facebook, Twitter, Instagram, LinkedIn, etc.
- 🔗 **Link Extraction** - Internal and external links
- 🍪 **Cookie Analysis** - Security attributes of cookies
- 📚 **Wayback Machine** - Archive availability check
- 🌐 **Server Fingerprinting** - Detailed server information

#### 📄 **Beautiful PDF Reports**
- Professional design with colors and charts
- Security score visualization
- Comprehensive sections for all findings
- Perfect for college submissions and presentations

#### 📊 **Export Options**
- PDF - Beautiful, formatted reports
- JSON - Raw data for further analysis

---

## 🚀 Installation

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Run the Enhanced Launcher

```bash
python enhanced_launch.py
```

---

## 📖 Usage

### Option 1: Browser Mode (Recommended)

1. Run the launcher: `python enhanced_launch.py`
2. Select option `1` for Browser Mode
3. Open your browser to `http://localhost:5000`
4. Enter target URL and click "Start Investigation"
5. View results in different tabs
6. Export as PDF or JSON

**Advantages:**
- Modern, responsive UI
- Works on any device with a browser
- Beautiful visualization
- Easy to use

### Option 2: Desktop Mode

1. Run the launcher: `python enhanced_launch.py`
2. Select option `2` for Desktop Mode
3. Desktop GUI window will open
4. Enter target URL and click "Start Investigation"
5. Browse results in multiple tabs
6. Export reports

**Advantages:**
- Works offline
- Traditional desktop application feel
- Familiar Tkinter interface

---

## 📁 File Structure

```
OSINT Tool/
│
├── enhanced_launch.py          # Main launcher with dual mode
├── enhanced_osint_tool.py      # Enhanced desktop GUI
├── web_app.py                  # Flask web application
├── advanced_scanner.py         # Advanced investigation modules
├── enhanced_pdf.py             # Beautiful PDF report generator
├── osint_tool.py               # Original OSINT tool (base)
├── requirements.txt            # Python dependencies
│
├── templates/                  # Web templates
│   └── index.html             # Web interface
│
└── reports/                    # Generated reports (auto-created)
    ├── *.pdf                  # PDF reports
    └── *.json                 # JSON exports
```

---

## 🎓 For College Submission

### Key Highlights:

1. **Comprehensive Features**: 20+ investigation techniques
2. **Professional Design**: Beautiful UI in both modes
3. **Detailed Reports**: Professional PDF with charts and colors
4. **Modern Technology**: Flask web framework + Tkinter GUI
5. **Well-Structured Code**: Clean, documented, and modular

### Sample Use Cases:

- **Cybersecurity Analysis**: Assess website security posture
- **Digital Forensics**: Gather digital evidence
- **Threat Intelligence**: Identify potential threats
- **Competitive Analysis**: Understand competitor technology stack
- **Research Projects**: Academic OSINT research

---

## 🔬 Investigation Process

1. **Domain Analysis**
   - WHOIS records
   - DNS configuration
   - Domain age and expiration

2. **Network Investigation**
   - IP address and geolocation
   - Reverse DNS lookup
   - ISP and organization info
   - SSL certificate validation

3. **Security Assessment**
   - Port scanning (21 common ports)
   - Security headers evaluation
   - Security score calculation
   - Vulnerability indicators

4. **Technology Profiling**
   - Web server identification
   - CMS detection
   - Framework discovery
   - Technology stack mapping

5. **Content Analysis**
   - Meta tag extraction
   - Email harvesting
   - Phone number extraction
   - robots.txt parsing
   - Link discovery

6. **Social Intelligence**
   - Social media profile discovery
   - Platform identification
   - Public presence mapping

7. **Historical Data**
   - Wayback Machine archives
   - Historical snapshots

---

## ⚙️ Technical Details

### Technologies Used:

**Backend:**
- Python 3.x
- Flask (Web Framework)
- Tkinter (GUI Framework)
- ReportLab (PDF Generation)

**Libraries:**
- `requests` - HTTP requests
- `beautifulsoup4` - HTML parsing
- `dnspython` - DNS queries
- `python-whois` - WHOIS lookups
- `validators` - URL validation
- `socket` - Network operations

**Features:**
- Multi-threaded scanning
- Progress tracking
- Error handling
- Data validation

---

## 📊 Report Sections

### PDF Report Includes:

1. **Cover Page** - Professional header with target info
2. **Executive Summary** - Key findings overview
3. **Domain Information** - Registration details
4. **Security Analysis** - Security score and headers
5. **Port Scan Results** - Open ports and services
6. **Technology Stack** - Detected technologies
7. **Metadata Analysis** - Website metadata
8. **Social Media** - Discovered profiles
9. **Additional Findings** - Cookies, archives, etc.

---

## 🛡️ Ethical Use

**⚠️ IMPORTANT NOTICE:**

This tool is for **educational and authorized testing purposes only**.

- ✅ Use on websites you own or have permission to test
- ✅ Use for academic research and learning
- ✅ Use for authorized security assessments
- ❌ DO NOT use for unauthorized access
- ❌ DO NOT use for malicious purposes
- ❌ DO NOT violate any laws or regulations

**You are responsible for how you use this tool.**

---

## 🎨 Screenshots

### Browser Mode
- Modern gradient design
- Real-time progress tracking
- Tabbed result viewing
- One-click PDF export

### Desktop Mode
- Clean Tkinter interface
- Multiple result tabs
- Progress bar with status
- Easy export options

---

## 🐛 Troubleshooting

### Issue: Dependencies not installing
**Solution:** 
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Issue: Port 5000 already in use (Browser Mode)
**Solution:** Change port in `web_app.py`:
```python
app.run(debug=False, host='0.0.0.0', port=5001)  # Use different port
```

### Issue: Tkinter not available
**Solution:** Install Tkinter:
```bash
# On Ubuntu/Debian
sudo apt-get install python3-tk

# On Windows (usually pre-installed)
# Reinstall Python with Tkinter option checked
```

---

## 📝 Notes

- Some features require internet connection
- Port scanning may take 30-60 seconds
- Large websites may have longer scan times
- Export reports to `reports/` directory
- Respect robots.txt and rate limits

---

## 👨‍💻 Author

**Cybersecurity Research Project**
- Version: 2.0 Enhanced Edition
- Purpose: College Project / Educational Tool
- License: Educational Use

---

## 🙏 Acknowledgments

- ReportLab for PDF generation
- Flask framework for web interface
- BeautifulSoup for HTML parsing
- Python community for excellent libraries

---

## 📞 Support

For issues or questions:
1. Check the Troubleshooting section
2. Review the code comments
3. Test with example websites (e.g., http://example.com)

---

## ⭐ Features Summary

✅ 20+ Investigation Techniques
✅ Dual Mode (Browser + Desktop)
✅ Beautiful PDF Reports
✅ Security Scoring
✅ Real-time Progress
✅ Multi-threaded Scanning
✅ Professional Design
✅ Well-Documented Code
✅ College-Ready Project
✅ Easy to Use

---

**Made with ❤️ for cybersecurity education**

*Remember: With great power comes great responsibility. Use wisely!*

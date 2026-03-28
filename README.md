# OSINT Web Reconnaissance Tool 🔍

A comprehensive, professional-grade cybersecurity tool for gathering detailed information about websites and exporting intelligence reports in PDF and JSON formats.

## Features ✨

### Information Gathering
- **WHOIS Information**: Domain registrar, creation/expiration dates, registrant details
- **DNS Records**: A, AAAA, MX, NS, TXT, CNAME, SOA records
- **IP Geolocation**: IP address, hostname, reverse DNS lookup
- **SSL/TLS Certificate Analysis**: Certificate issuer, validity period, subject alternative names
- **HTTP Headers Analysis**: Server type, powered-by headers, security headers
- **Technology Detection**: Identifies frameworks (React, Vue, Angular, etc.), CMS (WordPress, Drupal)
- **Email Extraction**: Finds email addresses on the website
- **Subdomain Enumeration**: Discovers accessible subdomains
- **Server Information**: Detailed server and network analysis

### Export Capabilities
- **PDF Reports**: Professional, detailed, formatted reports
- **JSON Export**: Raw data export for programmatic access
- **Organized Tabs**: Categorized information for easy navigation

## Installation 📦

### Prerequisites
- Python 3.7+
- pip (Python package manager)

### Setup Instructions

1. **Clone or download the project**
   ```bash
   cd path/to/osint-tool
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

   Or install individually:
   ```bash
   pip install requests dnspython python-whois certifi beautifulsoup4 
   pip install Pillow reportlab validators email-validator phonenumbers
   ```

3. **Run the tool**
   ```bash
   python osint_tool.py
   ```

## Usage 🚀

### GUI Interface
1. Launch the application: `python osint_tool.py`
2. Enter the target website URL in the input field (e.g., `https://example.com`)
3. Click **"Start Scan"** to begin gathering information
4. Monitor progress with the progress bar
5. View results in organized tabs
6. Export results as PDF or JSON

### Command-Line Arguments (Optional)
```bash
python osint_tool.py --url https://example.com --output report.pdf
```

## Information Collected 📊

### Domain Analysis
- Registrar information
- Domain creation and expiration dates
- Name servers
- Registrant organization
- Domain status

### Network Analysis
- Primary IP address
- Hostname
- Reverse DNS information
- Geolocation data

### SSL/TLS Security
- Certificate issuer
- Subject alternative names (SANs)
- Certificate validity period
- Serial number
- Protocol version

### Web Technologies
- Web server software
- Frameworks and libraries
- CMS detection
- Frontend frameworks
- Backend technologies

### Email Discovery
- Emails found on website and subpages
- Contact information extraction

### Subdomain Enumeration
- Accessible subdomains
- Common subdomain patterns (www, mail, ftp, api, etc.)

## Report Structure 📋

### PDF Report Includes:
1. **Executive Summary** - Key findings table
2. **Domain Information** - Complete WHOIS data
3. **Network Information** - IP and SSL details
4. **Technologies** - Detected tech stack
5. **Subdomains** - Discovered subdomains
6. **Email Addresses** - Extracted contacts
7. **DNS Records** - Detailed DNS analysis

### JSON Export
- Complete raw data in structured JSON format
- Suitable for automated processing
- Can be imported into other tools

## Examples 💡

### Basic Scan
```
Target: https://github.com
- Discovers GitHub's IP address
- Retrieves SSL certificate information
- Analyzes HTTP headers
- Detects technologies (Rails, Octicons, etc.)
- Lists accessible subdomains
- Extracts contact emails
```

### Export Options
```
PDF: Professional report with tables and formatting
JSON: Raw structured data for analysis
```

## Security & Ethical Usage ⚖️

This tool is designed for:
- ✓ Authorized penetration testing
- ✓ Bug bounty hunting
- ✓ Security research
- ✓ OSINT for authorized targets
- ✓ Website reconnaissance for security audits

**Important**:
- Only use this tool on websites you own or have explicit permission to scan
- Respect `robots.txt` and website terms of service
- Use responsibly and ethically
- Always obtain proper authorization before testing
- This tool is for educational and authorized security testing only

## Troubleshooting 🔧

### Issue: "Failed to retrieve WHOIS data"
- Some domains may have restricted WHOIS information
- Try again or check domain availability

### Issue: SSL Certificate Error
- Some websites may not have valid SSL certificates
- The tool will still retrieve available information

### Issue: Subdomain enumeration returns few results
- Uses common subdomain list
- Custom enumeration lists can be added for more results

### Issue: ModuleNotFoundError
- Ensure all requirements are installed: `pip install -r requirements.txt`
- Check Python version (3.7+)

## Architecture 🏗️

```
osint_tool.py
├── OSINTTool (Core scanning engine)
│   ├── get_whois_info()
│   ├── get_dns_records()
│   ├── get_ip_info()
│   ├── get_ssl_certificate()
│   ├── get_http_headers()
│   ├── detect_technologies()
│   ├── extract_emails()
│   ├── enumerate_subdomains()
│   └── generate_pdf_report()
└── OSINTToolGUI (Tkinter interface)
    ├── setup_ui()
    ├── perform_scan()
    ├── update_results()
    ├── export_pdf()
    └── export_json()
```

## Libraries Used 📚

| Library | Purpose |
|---------|---------|
| `requests` | HTTP requests |
| `dnspython` | DNS queries |
| `whois` | WHOIS data retrieval |
| `ssl` | SSL certificate analysis |
| `beautifulsoup4` | HTML parsing |
| `reportlab` | PDF generation |
| `validators` | URL validation |
| `tkinter` | GUI framework |

## Features Roadmap 🚀

Future enhancements:
- [ ] Passive DNS lookups
- [ ] Historical data from archive.org
- [ ] Shodan integration
- [ ] Vulnerability scanner
- [ ] API endpoints discovery
- [ ] Directory brute-forcing
- [ ] Custom scanning profiles
- [ ] Database support for multi-target scans
- [ ] Export to Excel/CSV
- [ ] REST API for automation

## Performance Tips ⚡

1. **Faster Scans**: Disable unnecessary checks
2. **Resource Usage**: Close other applications
3. **Network**: Use stable internet connection
4. **Timeout**: Default timeout is 10 seconds per request

## Common Findings 🎯

Typical OSINT scan reveals:
- Technology stack used by target
- Infrastructure providers (AWS, Cloudflare, etc.)
- Email addresses and contacts
- Related domains and subdomains
- Security configuration issues
- Outdated technologies
- Potential attack surface

## API Reference 🔌

### Core Functions

```python
from osint_tool import OSINTTool

osint = OSINTTool()

# Get domain information
whois_data = osint.get_whois_info("example.com")

# Get DNS records
dns_data = osint.get_dns_records("example.com")

# Get IP information
ip_data = osint.get_ip_info("example.com")

# Get SSL certificate
ssl_data = osint.get_ssl_certificate("example.com")

# Detect technologies
tech = osint.detect_technologies("https://example.com")

# Extract emails
emails = osint.extract_emails("https://example.com")

# Enumerate subdomains
subdomains = osint.enumerate_subdomains("example.com")

# Generate PDF report
osint.generate_pdf_report(data, "report.pdf")
```

## Disclaimer ⚠️

This tool is provided for educational and authorized security testing purposes only. Users are responsible for ensuring they have proper authorization before scanning any websites. Unauthorized use may violate laws in your jurisdiction. The authors assume no liability for misuse.

## License 📄

This project is provided as-is for educational purposes.

## Support 💬

For issues, questions, or improvements:
1. Check the troubleshooting section
2. Review the code documentation
3. Verify all dependencies are installed

## Author Notes 📝

This OSINT tool demonstrates:
- Python GUI development with Tkinter
- Network and security reconnaissance techniques
- API integration and data gathering
- Professional report generation
- Ethical hacking practices

Perfect for:
- Cybersecurity students
- Penetration testers
- Bug bounty hunters
- Security researchers
- System administrators

---

**Remember**: Always scan responsibly and ethically! 🛡️

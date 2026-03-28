# OSINT Tool - Usage Guide & Examples 📖

## Quick Start

### Option 1: Windows Users
Double-click `run.bat` - this will automatically install dependencies and launch the tool.

### Option 2: All Platforms
```bash
# Install dependencies
pip install -r requirements.txt

# Launch the tool
python osint_tool.py
```

### Option 3: Using Launcher
```bash
python launch.py
```

---

## GUI Interface Guide

### Main Window Sections

1. **URL Input Field**
   - Enter the target website URL
   - Format: `https://example.com` (https:// will auto-fill)
   - Examples: `google.com`, `github.com`, `wikipedia.org`

2. **Scan Controls**
   - **Start Scan**: Begins reconnaissance
   - **Stop**: Pauses ongoing scan
   - Progress bar shows scan completion percentage

3. **Results Tabs**
   - **Summary**: Key findings overview
   - **Domain Info**: WHOIS registration data
   - **Network Info**: IP and SSL certificate details
   - **Web Analysis**: HTTP headers and technologies
   - **Subdomains**: Discovered subdomains
   - **Emails**: Extracted email addresses
   - **DNS Records**: Complete DNS information
   - **Raw Data**: Complete JSON output

4. **Export Options**
   - **Export to PDF**: Professional formatted report
   - **Export to JSON**: Raw data for processing
   - **Clear**: Reset all results

---

## Practical Examples

### Example 1: Reconnaissance of GitHub

**Target**: `github.com`

**What You'll Find**:
1. **Domain Info**
   - Registrar: VeriSign Global Registry Services
   - Registrant: GitHub Inc.
   - Created: 2008-02-11
   - Expires: 2026-02-11

2. **Network Information**
   - IP Address: 140.82.113.4
   - SSL Certificate: GitHub, Inc.
   - Valid Until: 2027-XX-XX

3. **Technologies Detected**
   - Jekyll
   - Octicons
   - GitHub Pages
   - Various JavaScript frameworks

4. **Subdomains Found**
   - www.github.com
   - api.github.com
   - gist.github.com
   - pages.github.com
   - And more...

5. **Emails Extracted**
   - support@github.com
   - security@github.com
   - info@github.com

---

### Example 2: Corporate Website Reconnaissance

**Target**: `company-website.com`

**Workflow**:

1. **Initial Scan** (2-3 minutes)
   - Gathers basic domain and network information
   - Identifies hosting provider
   - Gets SSL certificate details

2. **Review Results**
   - Check DNS configuration
   - Note technology stack
   - Review SSL certificate validity

3. **Deep Analysis**
   - Examine subdomains for exposed services
   - Check for leaked emails
   - Identify potential vulnerabilities

4. **Export Report**
   - Generate PDF for documentation
   - Share JSON data with team
   - Keep for security audit records

---

## Report Examples

### PDF Report Structure

**Page 1: Executive Summary**
```
┌─────────────────────────────────────┐
│  OSINT Web Reconnaissance Report    │
│  Report Generated: 2024-03-25       │
│  Target: github.com                 │
├─────────────────────────────────────┤
│ Property           │ Value           │
├─────────────────────────────────────┤
│ Domain             │ github.com      │
│ Registrar          │ VeriSign        │
│ Primary IP         │ 140.82.113.4    │
│ Creation Date      │ 2008-02-11      │
│ SSL Issuer         │ DigiCert        │
│ Technologies       │ 15 detected     │
│ Subdomains         │ 24 found        │
│ Emails Found       │ 8 addresses     │
└─────────────────────────────────────┘
```

**Page 2: Domain Information**
- Registrar details
- Registrant information
- Registration dates
- Name servers
- Domain status

**Page 3: Network Information**
- IP Address
- Hostname
- SSL Certificate Details
- Validity Period
- Certificate Chain

**Page 4+: Detailed Analysis**
- Detected Technologies
- Subdomains List
- Email Addresses
- DNS Records

---

## Advanced Scanning Techniques

### 1. Multi-Target Scanning
```
Scan multiple domains sequentially:
1. Scan domain1.com → Export Results
2. Clear Results → Scan domain2.com → Export Results
3. Compare findings across domains
```

### 2. Vulnerability Assessment
```
Use OSINT findings for deeper testing:
1. Identify subdomains
2. Note technologies (check for known CVEs)
3. Review HTTP headers (security misconfigurations)
4. Check SSL certificates (validity, strength)
5. Extract emails (social engineering prevention)
```

### 3. Competitive Intelligence
```
Gather information about competitors:
1. Compare technology stacks
2. Identify shared hosting providers
3. Analyze infrastructure differences
4. Review security configurations
```

### 4. Security Audit Preparation
```
Use OSINT as first phase of security audit:
1. Document existing infrastructure
2. Identify all services and subdomains
3. Create baseline for vulnerability scanning
4. Prepare report for stakeholders
```

---

## Data Interpretation Guide

### WHOIS Information
- **Registrar**: Company hosting the domain registration
- **Creation Date**: When domain was first registered
- **Expiration Date**: When domain registration expires
- **Registrant Organization**: Official company name
- **Name Servers**: DNS providers

### DNS Records Explained
- **A Record**: Maps domain to IPv4 address
- **AAAA Record**: Maps domain to IPv6 address
- **MX Record**: Mail server configuration
- **NS Record**: Authoritative name servers
- **TXT Record**: Text records (SPF, DKIM, etc.)
- **CNAME Record**: Domain aliases
- **SOA Record**: Start of Authority information

### SSL Certificate Details
- **Issuer**: Certificate Authority (CA)
- **Subject**: Domain the certificate is for
- **Valid Until**: Certificate expiration date
- **Subject Alt Names**: Additional domains covered
- **Serial Number**: Unique certificate identifier

### Technologies Detected
- Web server software (Apache, Nginx, IIS)
- Programming languages (PHP, Python, Node.js)
- Frameworks (React, Vue, Angular)
- CMS platforms (WordPress, Drupal)
- CDN services (CloudFlare, Akamai)

---

## Ethical Considerations

### ✅ Legal & Ethical Uses
- Security research on authorized targets
- Bug bounty hunting (with program participation)
- Penetration testing (with written permission)
- Asset inventory for own organization
- Competitive analysis within legal bounds
- Academic cybersecurity education

### ❌ Prohibited Uses
- Unauthorized scanning
- Collecting data without consent
- Violating terms of service
- Using information for harassment
- Preparing for unauthorized access
- Violating privacy laws (GDPR, CCPA, etc.)

### ⚠️ Best Practices
1. **Obtain Authorization**: Always get explicit permission before scanning
2. **Respect Rate Limits**: Avoid excessive requests that could DoS
3. **Honor Robots.txt**: Follow website crawling guidelines
4. **Protect Results**: Secure reports and data
5. **Document Permission**: Keep records of authorization
6. **Responsible Disclosure**: Report findings ethically

---

## Troubleshooting

### Issue: "Invalid URL"
**Solution**: Ensure URL format is correct
- ✓ https://example.com
- ✓ example.com (auto-formatted)
- ✗ example (incomplete)
- ✗ htp://example.com (typo)

### Issue: "Connection Timeout"
**Causes**: Network issue, target down, rate-limited
**Solution**:
- Check internet connection
- Verify target is accessible
- Try again after delay

### Issue: "WHOIS Data Unavailable"
**Causes**: Restricted WHOIS, private registration
**Solution**: Other data should still be gathered
- DNS records may be available
- SSL certificate information
- Technology detection
- Subdomain enumeration

### Issue: "DNS Resolution Failed"
**Causes**: Server down, DNS issue, incorrect domain
**Solution**:
- Verify domain spelling
- Check if domain is active
- Try adding www. prefix

### Issue: PDF Export Fails
**Causes**: Insufficient permissions, disk space
**Solution**:
- Choose different save location
- Check file permissions
- Ensure disk space available

---

## Performance Tips

### Faster Scanning
1. Use stable internet connection
2. Close unnecessary applications
3. Run during off-peak hours (less network load)
4. Disable firewall temporarily (if safe to do so)

### Slower but Safer
1. Longer timeouts (less aggressive)
2. Respect server response times
3. Add delays between requests
4. Use VPN to rotate IP if needed

### Resource Management
- Tool uses ~50-100MB RAM during scan
- Each scan takes 1-5 minutes typically
- PDF generation is fast (<5 seconds)
- Can scan multiple targets in sequence

---

## Creating Reports

### For Management
- Use PDF export
- Focus on Executive Summary
- Highlight key findings
- Include compliance recommendations

### For Technical Team
- Use JSON export
- Share raw data
- Provide detailed technology listing
- Include all DNS records

### For Security Audit
- Export both PDF and JSON
- Document all findings
- Include timestamps
- Verify all data accuracy

---

## API Usage (Python)

```python
from osint_tool import OSINTTool

# Initialize tool
osint = OSINTTool()

# Gather information
domain = "example.com"
whois_info = osint.get_whois_info(domain)
dns_info = osint.get_dns_records(domain)
ip_info = osint.get_ip_info(domain)
ssl_info = osint.get_ssl_certificate(domain)
tech = osint.detect_technologies(f"https://{domain}")
emails = osint.extract_emails(f"https://{domain}")
subdomains = osint.enumerate_subdomains(domain)

# Generate report
data = {
    'domain': whois_info,
    'dns': dns_info,
    'ip': ip_info,
    'ssl': ssl_info,
    'technologies': tech,
    'emails': emails,
    'subdomains': subdomains
}

osint.generate_pdf_report(data, "report.pdf")
```

---

## Tips & Tricks

1. **Combine with Other Tools**
   - Use OSINT results for Shodan searches
   - Feed subdomains to nmap for port scanning
   - Use emails for OSINT searches on LinkedIn

2. **Track Changes**
   - Scan the same target periodically
   - Compare DNS record changes
   - Monitor SSL certificate updates

3. **Automate Scanning**
   - Use launch.py for batch processing
   - Write Python scripts using core modules
   - Schedule regular scans

4. **Quick Lookups**
   - Bookmark frequently scanned domains
   - Export results for quick reference
   - Keep historical reports

---

## Security Warnings ⚠️

This tool performs real network reconnaissance. Use responsibly:
- ✓ Only scan targets you own or have permission for
- ✓ Comply with all local laws and regulations
- ✓ Respect website terms of service
- ✓ Do not use for unauthorized access preparation
- ✓ Protect reports containing sensitive information
- ✓ Consider privacy implications

---

## Questions or Issues?

1. Check the README.md for general information
2. Review troubleshooting section above
3. Verify all dependencies are installed
4. Check Python version (3.7+)
5. Ensure stable internet connection

---

**Happy Hunting! 🎯 - Use this tool responsibly and ethically**

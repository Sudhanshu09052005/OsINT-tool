# QUICK START GUIDE - OSINT Investigation Tool

## 🚀 Getting Started in 3 Steps

### Step 1: Install Dependencies (First Time Only)

Open Command Prompt in this folder and run:
```
pip install -r requirements.txt
```

This will install all required packages automatically.

### Step 2: Launch the Tool

**Easy Way (Recommended):**
- Double-click `START.bat` file

**OR Manual Way:**
```
python enhanced_launch.py
```

### Step 3: Choose Your Mode

You'll see a menu:
```
[1] 🌐 Browser Mode  - Web interface (Recommended)
[2] 💻 Desktop Mode  - GUI application  
[3] ❌ Exit
```

**For Browser Mode:**
- Press `1` and Enter
- Open browser to `http://localhost:5000`
- Start investigating!

**For Desktop Mode:**
- Press `2` and Enter
- GUI window will open
- Start scanning!

---

## 📖 How to Use

### Browser Mode:

1. **Enter Target URL**
   - Type the website URL (e.g., `https://example.com`)
   - Click "Start Investigation"

2. **Watch Progress**
   - Progress bar shows scan status
   - Wait for completion (usually 30-60 seconds)

3. **View Results**
   - Click different tabs to see results:
     - 📋 Summary - Overview
     - 🌐 Domain - WHOIS info
     - 🔒 Security - Security analysis
     - 🔌 Ports - Open ports
     - ⚙️ Tech - Technologies
     - 📝 Metadata - Website info
     - 📱 Social - Social media links
     - And more...

4. **Export Report**
   - Click "📄 Export Beautiful PDF" for professional report
   - Click "📊 Export JSON" for raw data

### Desktop Mode:

1. **Enter Target URL**
   - Type URL in the input field
   - Click "▶ Start Investigation"

2. **Monitor Progress**
   - Progress bar and status updates
   - Shows current scanning phase

3. **Explore Results**
   - Browse tabs:
     - Summary, Domain, Security, Ports, Technologies, etc.
   - Scroll through detailed findings

4. **Export Results**
   - Click "📄 Export Beautiful PDF"
   - Choose location and save
   - Or export as JSON

---

## 🎯 What Gets Investigated?

### Domain Analysis
- ✅ WHOIS information
- ✅ Domain age and expiration
- ✅ Registrar details
- ✅ DNS records (A, MX, NS, TXT, etc.)

### Network Information
- ✅ IP address and geolocation
- ✅ Hosting provider (ISP)
- ✅ Reverse DNS lookup
- ✅ SSL certificate details

### Security Assessment
- ✅ Port scanning (21 common ports)
- ✅ Security headers check
- ✅ Security score (0-100%)
- ✅ Missing protection identification

### Technology Detection
- ✅ Web server (Apache, Nginx, etc.)
- ✅ CMS (WordPress, Joomla, etc.)
- ✅ JavaScript libraries
- ✅ Frameworks and platforms
- ✅ Analytics tools

### Content Analysis
- ✅ Meta tags (title, description, keywords)
- ✅ Email addresses on page
- ✅ Phone numbers
- ✅ robots.txt file
- ✅ Sitemap locations

### Social Intelligence
- ✅ Facebook profiles/pages
- ✅ Twitter accounts
- ✅ Instagram profiles
- ✅ LinkedIn company pages
- ✅ YouTube channels
- ✅ GitHub repositories

### Additional Features
- ✅ Cookie analysis
- ✅ Internal/external links
- ✅ Wayback Machine archives
- ✅ Open Graph tags
- ✅ Twitter Card data

---

## 📊 Understanding the Results

### Security Score

**75-100% (GOOD) ✅**
- Most security headers present
- Well-protected website
- Low vulnerability risk

**50-74% (MODERATE) ⚠️**
- Some security headers missing
- Moderate protection
- Improvements recommended

**0-49% (POOR) ❌**
- Many security headers missing
- Weak protection
- High vulnerability risk

### Port Scan Results

**Open Port Example:**
```
🔌 Port 443 (OPEN)
   Service: HTTPS
```

**Common Ports:**
- 80 (HTTP), 443 (HTTPS) - Expected for websites
- 21 (FTP), 22 (SSH) - File transfer/admin access
- 25 (SMTP), 110 (POP3), 143 (IMAP) - Email services
- 3306 (MySQL), 5432 (PostgreSQL) - Databases
- 3389 (RDP) - Remote desktop

### Technologies

Shows what the website is built with:
- Programming languages (PHP, Python, etc.)
- Frameworks (Laravel, Django, etc.)
- Libraries (jQuery, React, etc.)
- CDNs (Cloudflare, etc.)
- Analytics (Google Analytics, etc.)

---

## 💡 Pro Tips

### For Best Results:

1. **Use Full URLs**
   - ✅ Good: `https://example.com`
   - ❌ Bad: `example.com` or `www.example.com`

2. **Wait for Completion**
   - Don't interrupt the scan
   - Port scanning takes time
   - Typical scan: 30-90 seconds

3. **Check Multiple Tabs**
   - Each tab has different information
   - Summary gives quick overview
   - Other tabs have detailed data

4. **Export Reports**
   - PDF for presentations
   - JSON for further analysis
   - Save important findings

### For College Presentations:

1. **Use the PDF Report**
   - Professional design
   - Color-coded sections
   - Charts and tables
   - Ready to print/submit

2. **Show Both Modes**
   - Browser mode: modern interface
   - Desktop mode: traditional app
   - Demonstrates versatility

3. **Highlight Features**
   - 20+ investigation techniques
   - Security scoring system
   - Beautiful visualizations
   - Real-time progress tracking

---

## 🐛 Common Issues & Solutions

### Issue: "Module not found"
**Solution:**
```
pip install -r requirements.txt
```

### Issue: "Port 5000 already in use"
**Solution:**
- Close other applications using port 5000
- Or edit `web_app.py` and change port to 5001

### Issue: Scan takes too long
**Reason:**
- Port scanning is thorough
- Large websites have more data
- Network speed affects timing

**Normal Duration:**
- Small sites: 20-40 seconds
- Medium sites: 40-70 seconds
- Large sites: 60-120 seconds

### Issue: Some data shows "N/A"
**Reason:**
- Information not publicly available
- Website blocks certain queries
- WHOIS privacy protection enabled
- This is normal and expected

### Issue: PDF export fails
**Solution:**
```
pip install --upgrade reportlab
```

---

## 🎓 For College Project

### What to Submit:

1. **Source Code**
   - All Python files
   - requirements.txt
   - README files

2. **Sample Reports**
   - 2-3 PDF reports from different websites
   - Show variety of findings

3. **Documentation**
   - README_ENHANCED.md
   - This Quick Start Guide
   - Screenshots of both modes

4. **Presentation**
   - Feature overview
   - Live demonstration
   - Sample results explanation

### Key Points to Mention:

✅ **Technical Skills**
- Python programming
- Web scraping (BeautifulSoup)
- Network programming (sockets)
- Web frameworks (Flask)
- GUI development (Tkinter)
- PDF generation (ReportLab)

✅ **Features Implemented**
- Dual-mode architecture
- Multi-threaded scanning
- Real-time progress tracking
- Professional PDF reports
- Security assessment
- Technology fingerprinting

✅ **Practical Applications**
- Cybersecurity assessments
- Digital forensics
- Threat intelligence
- Competitive analysis
- Academic research

---

## ⚠️ Important Notes

### Ethical Use

- ✅ Only scan websites you own or have permission
- ✅ Use for learning and authorized testing
- ✅ Respect robots.txt
- ❌ Never use for unauthorized access
- ❌ Don't violate laws or regulations

### Legal Disclaimer

This tool is for educational purposes only. You are responsible for how you use it. Always get permission before testing websites.

### Best Practices

1. Test on your own websites first
2. Use example.com for practice
3. Read and understand the results
4. Keep reports confidential
5. Report findings responsibly

---

## 📞 Need Help?

### Debugging Steps:

1. Check Python version: `python --version`
   - Needs Python 3.7 or higher

2. Verify installation:
   ```
   python -c "import flask; import reportlab; print('OK')"
   ```

3. Test basic scan:
   - Try with `http://example.com`
   - Should complete successfully

4. Check logs:
   - Look at terminal/console output
   - Note any error messages

### Test Command:

Run this to test setup:
```
python -c "import sys; print(sys.version); import requests, flask, bs4, reportlab; print('All modules OK!')"
```

---

## 🎉 Success Checklist

Before your presentation/submission:

- [ ] Tool runs without errors
- [ ] Both modes work (Browser + Desktop)
- [ ] Can scan example.com successfully
- [ ] PDF export works
- [ ] JSON export works
- [ ] All tabs show data
- [ ] README documentation reviewed
- [ ] Sample reports generated
- [ ] Screenshots taken
- [ ] Understand all features

---

## 📚 Learn More

### Recommended Reading:

- OSINT Framework
- Web Security Headers
- DNS Record Types
- SSL/TLS Certificates
- Port Number Standards
- WHOIS Protocol

### Practice Websites:

- http://example.com (safe for testing)
- Your own websites
- Authorized test sites

---

**Ready to Start?**

1. Run `START.bat` or `python enhanced_launch.py`
2. Choose your mode
3. Enter a URL
4. Start investigating!

**Good luck with your college project! 🎓**

---

*Remember: Use this tool responsibly and ethically!*

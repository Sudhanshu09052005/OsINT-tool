"""
OSINT Tool - Website Information Gathering & Analysis
A comprehensive cybersecurity tool for gathering detailed information about websites
and exporting reports to PDF format.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import threading
import requests
import socket
import json
import dns.resolver
try:
    import whois
except:
    pass
from datetime import datetime
from urllib.parse import urlparse
import validators
import os
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
import ssl
from bs4 import BeautifulSoup
import re


class OSINTTool:
    """Main OSINT scanning engine"""
    
    def __init__(self):
        self.gathered_data = {}
        self.is_scanning = False
    
    def get_whois_info(self, domain):
        """Get WHOIS information - Fixed version"""
        try:
            domain = domain.replace("http://", "").replace("https://", "").replace("www.", "").split('/')[0]
            
            # Method 1: Try python-whois (most reliable)
            try:
                import pythonwhois
                result = pythonwhois.get_whois(domain)
                
                return {
                    "domain": domain,
                    "registrar": str(result.get('registrar', ['N/A'])[0]) if result.get('registrar') else "N/A",
                    "creation_date": str(result.get('creation_date', ['N/A'])[0]) if result.get('creation_date') else "N/A",
                    "expiration_date": str(result.get('expiration_date', ['N/A'])[0]) if result.get('expiration_date') else "N/A",
                    "updated_date": str(result.get('updated_date', ['N/A'])[0]) if result.get('updated_date') else "N/A",
                    "name_servers": result.get('nameservers', []),
                    "registrant_country": "N/A",
                    "registrant_email": "N/A", 
                    "registrant_organization": "N/A",
                    "status": str(result.get('status', 'N/A')),
                }
            except ImportError:
                # python-whois not installed
                pass
            except Exception as e:
                # python-whois failed, try next method
                pass
            
            # Method 2: Basic fallback - just return domain info
            return {
                "domain": domain,
                "registrar": "WHOIS service unavailable",
                "creation_date": "Install python-whois package",
                "expiration_date": "Run: pip install python-whois",
                "updated_date": "N/A",
                "name_servers": [],
                "registrant_country": "N/A",
                "registrant_email": "N/A",
                "registrant_organization": "N/A",
                "status": "WHOIS data not available - please install python-whois",
                "note": "To get WHOIS data, run: pip uninstall whois && pip install python-whois"
            }
            
        except Exception as e:
            return {
                "domain": domain if 'domain' in locals() else "unknown",
                "registrar": "Error",
                "creation_date": "N/A",
                "expiration_date": "N/A",
                "updated_date": "N/A",
                "name_servers": [],
                "registrant_country": "N/A",
                "registrant_email": "N/A",
                "registrant_organization": "N/A",
                "status": f"Error: {str(e)}"
            }
    
    def get_dns_records(self, domain):
        """Get DNS records"""
        try:
            domain = domain.replace("http://", "").replace("https://", "").replace("www.", "")
            dns_data = {
                "A": [],
                "AAAA": [],
                "MX": [],
                "NS": [],
                "TXT": [],
                "CNAME": [],
                "SOA": []
            }
            
            record_types = ['A', 'AAAA', 'MX', 'NS', 'TXT', 'CNAME', 'SOA']
            
            for record_type in record_types:
                try:
                    answers = dns.resolver.resolve(domain, record_type, raise_on_no_answer=False)
                    for answer in answers:
                        dns_data[record_type].append(str(answer))
                except:
                    pass
            
            return dns_data
        except Exception as e:
            return {"error": f"Failed to retrieve DNS records: {str(e)}"}
    
    def get_ip_info(self, domain):
        """Get IP information and hostname"""
        try:
            domain = domain.replace("http://", "").replace("https://", "").replace("www.", "")
            
            ip_address = socket.gethostbyname(domain)
            
            try:
                hostname = socket.gethostbyaddr(ip_address)[0]
            except:
                hostname = "N/A"
            
            return {
                "ip": ip_address,
                "hostname": hostname,
                "domain": domain,
            }
        except Exception as e:
            return {"error": f"Failed to retrieve IP information: {str(e)}"}
    
    def get_ssl_certificate(self, domain):
        """Get SSL certificate information"""
        try:
            domain = domain.replace("http://", "").replace("https://", "").replace("www.", "")
            
            context = ssl.create_default_context()
            with socket.create_connection((domain, 443), timeout=10) as sock:
                with context.wrap_socket(sock, server_hostname=domain) as ssock:
                    cert = ssock.getpeercert()
                    
                    return {
                        "subject": str(cert.get('subject', 'N/A')),
                        "issuer": str(cert.get('issuer', 'N/A')),
                        "version": str(cert.get('version', 'N/A')),
                        "serial_number": str(cert.get('serialNumber', 'N/A')),
                        "not_before": str(cert.get('notBefore', 'N/A')),
                        "not_after": str(cert.get('notAfter', 'N/A')),
                        "valid_until": str(cert.get('notAfter', 'N/A')),
                        "subjectAltName": str(cert.get('subjectAltName', 'N/A')),
                    }
        except Exception as e:
            return {"error": f"Failed to retrieve SSL certificate: {str(e)}"}
    
    def get_http_headers(self, url):
        """Get HTTP headers"""
        try:
            if not url.startswith("http"):
                url = "https://" + url
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=10, verify=False)
            
            return dict(response.headers)
        except Exception as e:
            return {"error": f"Failed to retrieve HTTP headers: {str(e)}"}
    
    def detect_technologies(self, url):
        """Detect technologies used on the website"""
        try:
            if not url.startswith("http"):
                url = "https://" + url
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=10, verify=False)
            technologies = []
            
            # Check response headers for server info
            if 'Server' in response.headers:
                technologies.append(f"Server: {response.headers['Server']}")
            
            if 'X-Powered-By' in response.headers:
                technologies.append(f"Powered By: {response.headers['X-Powered-By']}")
            
            if 'X-AspNet-Version' in response.headers:
                technologies.append(f"ASP.NET Version: {response.headers['X-AspNet-Version']}")
            
            # Check HTML content for common frameworks
            content = response.text.lower()
            
            if 'react' in content:
                technologies.append("React.js")
            if 'vue' in content:
                technologies.append("Vue.js")
            if 'angular' in content:
                technologies.append("Angular")
            if 'jquery' in content:
                technologies.append("jQuery")
            if 'bootstrap' in content:
                technologies.append("Bootstrap")
            if 'wordpress' in content:
                technologies.append("WordPress")
            if 'drupal' in content:
                technologies.append("Drupal")
            if 'django' in content:
                technologies.append("Django")
            if 'flask' in content:
                technologies.append("Flask")
            if 'nodejs' in content or 'express' in content:
                technologies.append("Node.js/Express")
            
            return list(set(technologies)) if technologies else ["Unable to detect"]
        except Exception as e:
            return [f"Error detecting technologies: {str(e)}"]
    
    def extract_emails(self, url):
        """Extract email addresses from website"""
        try:
            if not url.startswith("http"):
                url = "https://" + url
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=10, verify=False)
            
            # Extract emails using regex
            email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
            emails = list(set(re.findall(email_pattern, response.text)))
            
            return emails[:50]  # Limit to 50
        except Exception as e:
            return []
    
    def enumerate_subdomains(self, domain):
        """Basic subdomain enumeration using common subdomains"""
        try:
            domain = domain.replace("http://", "").replace("https://", "").replace("www.", "")
            
            common_subdomains = [
                'www', 'mail', 'ftp', 'localhost', 'webmail', 'smtp', 'pop', 'ns1', 'webdisk',
                'ns2', 'cpanel', 'whm', 'autodiscover', 'autoconfig', 'test', 'dev', 'staging',
                'admin', 'api', 'blog', 'docs', 'help', 'support', 'contact', 'portal', 'account',
                'accounts', 'auth', 'secure', 'shop', 'store', 'mobile', 'app', 'apps', 'cdn',
                'cdn2', 'cache', 'images', 'static', 'assets', 'media', 'news', 'events', 'jobs'
            ]
            
            subdomains = []
            for subdomain in common_subdomains:
                try:
                    full_domain = f"{subdomain}.{domain}"
                    socket.gethostbyname(full_domain)
                    subdomains.append(full_domain)
                except:
                    pass
            
            return subdomains if subdomains else ["No accessible subdomains found"]
        except Exception as e:
            return [f"Error enumerating subdomains: {str(e)}"]
    
    def generate_pdf_report(self, data, filepath):
        """Generate PDF report from gathered data"""
        try:
            doc = SimpleDocTemplate(filepath, pagesize=A4,
                                   rightMargin=0.5*inch, leftMargin=0.5*inch,
                                   topMargin=0.75*inch, bottomMargin=0.75*inch)
            
            styles = getSampleStyleSheet()
            story = []
            
            # Title
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=24,
                textColor=colors.HexColor('#1a1a1a'),
                spaceAfter=30,
                alignment=1  # Center
            )
            story.append(Paragraph("OSINT Web Reconnaissance Report", title_style))
            story.append(Spacer(1, 0.2*inch))
            
            # Metadata
            meta_text = f"<b>Report Generated:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}<br/>"
            meta_text += f"<b>Target Domain:</b> {data.get('domain', {}).get('domain', 'N/A')}<br/>"
            story.append(Paragraph(meta_text, styles['Normal']))
            story.append(Spacer(1, 0.3*inch))
            
            # Summary Section
            story.append(Paragraph("EXECUTIVE SUMMARY", styles['Heading2']))
            summary_data = [
                ['Property', 'Value'],
                ['Domain', data.get('domain', {}).get('domain', 'N/A')],
                ['Registrar', data.get('domain', {}).get('registrar', 'N/A')],
                ['Primary IP', data.get('ip', {}).get('ip', 'N/A')],
                ['Creation Date', str(data.get('domain', {}).get('creation_date', 'N/A'))[:10]],
                ['Expiration Date', str(data.get('domain', {}).get('expiration_date', 'N/A'))[:10]],
                ['SSL Issuer', data.get('ssl', {}).get('issuer', 'N/A')],
                ['Technologies', str(len(data.get('technologies', [])))],
                ['Subdomains', str(len(data.get('subdomains', [])))],
                ['Emails Found', str(len(data.get('emails', [])))],
            ]
            
            summary_table = Table(summary_data, colWidths=[2*inch, 3.5*inch])
            summary_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a1a1a')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 10),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
            ]))
            story.append(summary_table)
            story.append(Spacer(1, 0.2*inch))
            story.append(PageBreak())
            
            # Domain Information Section
            story.append(Paragraph("DOMAIN INFORMATION", styles['Heading2']))
            domain_info = data.get('domain', {})
            domain_table_data = [['Property', 'Value']]
            for key, value in domain_info.items():
                if key != 'error':
                    domain_table_data.append([str(key).replace('_', ' ').title(), str(value)])
            
            domain_table = Table(domain_table_data, colWidths=[2*inch, 3.5*inch])
            domain_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a1a1a')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 11),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
            ]))
            story.append(domain_table)
            story.append(Spacer(1, 0.2*inch))
            story.append(PageBreak())
            
            # Network Information Section
            story.append(Paragraph("NETWORK INFORMATION", styles['Heading2']))
            ip_info = data.get('ip', {})
            ip_table_data = [['Property', 'Value']]
            for key, value in ip_info.items():
                if key != 'error':
                    ip_table_data.append([str(key).replace('_', ' ').title(), str(value)])
            
            ip_table = Table(ip_table_data, colWidths=[2*inch, 3.5*inch])
            ip_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a1a1a')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
            ]))
            story.append(ip_table)
            story.append(Spacer(1, 0.2*inch))
            
            # SSL Certificate Section
            story.append(Paragraph("SSL CERTIFICATE INFORMATION", styles['Heading3']))
            ssl_info = data.get('ssl', {})
            ssl_table_data = [['Property', 'Value']]
            for key, value in ssl_info.items():
                if key != 'error':
                    ssl_table_data.append([str(key).replace('_', ' ').title(), str(value)[:50]])
            
            ssl_table = Table(ssl_table_data, colWidths=[2*inch, 3.5*inch])
            ssl_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a1a1a')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
            ]))
            story.append(ssl_table)
            story.append(Spacer(1, 0.2*inch))
            story.append(PageBreak())
            
            # Technologies Section
            story.append(Paragraph("DETECTED TECHNOLOGIES", styles['Heading2']))
            tech_list = data.get('technologies', [])
            for tech in tech_list[:20]:
                story.append(Paragraph(f"• {tech}", styles['Normal']))
            story.append(Spacer(1, 0.2*inch))
            
            # Subdomains Section
            story.append(Paragraph("DISCOVERED SUBDOMAINS", styles['Heading2']))
            subdomains = data.get('subdomains', [])
            for subdomain in subdomains[:30]:
                story.append(Paragraph(f"• {subdomain}", styles['Normal']))
            story.append(Spacer(1, 0.2*inch))
            story.append(PageBreak())
            
            # Emails Section
            story.append(Paragraph("EXTRACTED EMAIL ADDRESSES", styles['Heading2']))
            emails = data.get('emails', [])
            for email in emails[:30]:
                story.append(Paragraph(f"• {email}", styles['Normal']))
            
            # Build PDF
            doc.build(story)
            return True
        except Exception as e:
            raise Exception(f"Failed to generate PDF: {str(e)}")


class OSINTToolGUI:
    """GUI for OSINT Tool"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("OSINT Intelligence Tool - Website Reconnaissance")
        self.root.geometry("1100x750")
        self.root.resizable(True, True)
        
        self.osint = OSINTTool()
        self.gathered_data = {}
        self.is_scanning = False
        
        # Configure style
        style = ttk.Style()
        style.theme_use("clam")
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the user interface"""
        # Header
        header_frame = ttk.Frame(self.root)
        header_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Label(header_frame, text="🔍 OSINT Web Reconnaissance Tool", 
                 font=("Arial", 16, "bold")).pack(side="left")
        ttk.Label(header_frame, text="v1.0", 
                 font=("Arial", 10, "bold")).pack(side="right")
        
        # Input frame
        input_frame = ttk.LabelFrame(self.root, text="Target URL", padding=10)
        input_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(input_frame, text="Enter Website URL:").pack(side="left", padx=5)
        self.url_entry = ttk.Entry(input_frame, width=50, font=("Arial", 10))
        self.url_entry.pack(side="left", padx=5, fill="x", expand=True)
        self.url_entry.insert(0, "https://")
        
        self.scan_btn = ttk.Button(input_frame, text="▶ Start Scan", command=self.start_scan)
        self.scan_btn.pack(side="left", padx=5)
        
        self.stop_btn = ttk.Button(input_frame, text="⏹ Stop", command=self.stop_scan, 
                                   state="disabled")
        self.stop_btn.pack(side="left", padx=5)
        
        # Progress frame
        progress_frame = ttk.Frame(self.root)
        progress_frame.pack(fill="x", padx=10, pady=5)
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var, 
                                           maximum=100)
        self.progress_bar.pack(fill="x", padx=5, pady=5)
        
        self.status_label = ttk.Label(progress_frame, text="Ready", 
                                     font=("Arial", 9, "italic"), foreground="blue")
        self.status_label.pack(anchor="w", padx=5)
        
        # Notebook (tabs)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.tabs = {}
        tab_names = ["📋 Summary", "🌐 Domain Info", "🔗 Network Info", "📡 Web Analysis", 
                     "🔍 Subdomains", "📧 Emails", "📊 DNS Records", "📄 Raw Data"]
        
        for tab_name in tab_names:
            frame = ttk.Frame(self.notebook)
            self.notebook.add(frame, text=tab_name)
            
            text_widget = scrolledtext.ScrolledText(frame, wrap="word", font=("Courier", 9),
                                                   bg="white", fg="black")
            text_widget.pack(fill="both", expand=True, padx=5, pady=5)
            
            self.tabs[tab_name] = text_widget
        
        # Export frame
        export_frame = ttk.Frame(self.root)
        export_frame.pack(fill="x", padx=10, pady=10)
        
        self.export_pdf_btn = ttk.Button(export_frame, text="📑 Export to PDF", 
                                        command=self.export_pdf, state="disabled")
        self.export_pdf_btn.pack(side="left", padx=5)
        
        self.export_json_btn = ttk.Button(export_frame, text="📄 Export to JSON", 
                                         command=self.export_json, state="disabled")
        self.export_json_btn.pack(side="left", padx=5)
        
        self.clear_btn = ttk.Button(export_frame, text="🗑️ Clear", 
                                   command=self.clear_results)
        self.clear_btn.pack(side="left", padx=5)
        
        ttk.Label(export_frame, text="💡 Run a scan to see results", 
                 font=("Arial", 9, "italic"), foreground="gray").pack(side="right", padx=5)
    
    def validate_url(self, url):
        """Validate URL format"""
        if not validators.url(url):
            messagebox.showerror("Invalid URL", "Please enter a valid URL (e.g., https://example.com)")
            return False
        return True
    
    def start_scan(self):
        """Start OSINT scan"""
        url = self.url_entry.get().strip()
        
        if not url or url == "https://":
            messagebox.showerror("Error", "Please enter a URL")
            return
        
        if not self.validate_url(url):
            return
        
        self.is_scanning = True
        self.scan_btn.config(state="disabled")
        self.stop_btn.config(state="normal")
        self.export_pdf_btn.config(state="disabled")
        self.export_json_btn.config(state="disabled")
        self.progress_var.set(0)
        self.status_label.config(text="Scan in progress...", foreground="blue")
        
        scan_thread = threading.Thread(target=self.perform_scan, args=(url,))
        scan_thread.daemon = True
        scan_thread.start()
    
    def stop_scan(self):
        """Stop the scan"""
        self.is_scanning = False
        self.scan_btn.config(state="normal")
        self.stop_btn.config(state="disabled")
        self.status_label.config(text="Scan stopped by user", foreground="orange")
    
    def perform_scan(self, url):
        """Perform the OSINT scan"""
        try:
            self.gathered_data = {}
            domain = url.replace("http://", "").replace("https://", "").replace("www.", "").split("/")[0]
            
            # WHOIS & DNS (20%)
            self.update_status("Gathering WHOIS & DNS information...")
            self.update_progress(10)
            self.gathered_data["domain"] = self.osint.get_whois_info(domain)
            self.gathered_data["dns"] = self.osint.get_dns_records(domain)
            
            # Network Info (40%)
            self.update_status("Analyzing network & SSL...")
            self.update_progress(25)
            self.gathered_data["ip"] = self.osint.get_ip_info(domain)
            self.gathered_data["ssl"] = self.osint.get_ssl_certificate(domain)
            
            # Web Analysis (60%)
            self.update_status("Analyzing HTTP headers & technologies...")
            self.update_progress(40)
            self.gathered_data["headers"] = self.osint.get_http_headers(url)
            self.gathered_data["technologies"] = self.osint.detect_technologies(url)
            self.gathered_data["emails"] = self.osint.extract_emails(url)
            
            # Subdomains (80%)
            self.update_status("Enumerating subdomains...")
            self.update_progress(60)
            self.gathered_data["subdomains"] = self.osint.enumerate_subdomains(domain)
            
            # Complete
            self.update_progress(100)
            self.update_status(f"Scan completed successfully at {datetime.now().strftime('%H:%M:%S')}")
            
            self.root.after(0, self.update_results)
            self.root.after(0, self.scan_complete)
            
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Scan Error", 
                f"Error during scan: {str(e)}"))
            self.root.after(0, self.scan_failed)
    
    def update_status(self, message):
        """Update status label"""
        self.root.after(0, lambda: self.status_label.config(text=message, foreground="blue"))
    
    def update_progress(self, value):
        """Update progress bar"""
        self.root.after(0, lambda: self.progress_var.set(value))
    
    def update_results(self):
        """Update results display"""
        # Summary
        summary = self.format_summary()
        self.tabs["📋 Summary"].delete("1.0", "end")
        self.tabs["📋 Summary"].insert("end", summary)
        
        # Domain Info
        domain_info = self.format_dict("DOMAIN INFORMATION", self.gathered_data.get('domain', {}))
        self.tabs["🌐 Domain Info"].delete("1.0", "end")
        self.tabs["🌐 Domain Info"].insert("end", domain_info)
        
        # Network Info
        ip_info = self.format_dict("IP INFORMATION", self.gathered_data.get('ip', {}))
        ssl_info = self.format_dict("SSL CERTIFICATE", self.gathered_data.get('ssl', {}))
        self.tabs["🔗 Network Info"].delete("1.0", "end")
        self.tabs["🔗 Network Info"].insert("end", ip_info + "\n\n" + ssl_info)
        
        # Web Analysis
        headers = self.format_dict("HTTP HEADERS", self.gathered_data.get('headers', {}))
        tech_text = "TECHNOLOGIES DETECTED:\n" + "─" * 50 + "\n"
        for item in self.gathered_data.get('technologies', []):
            tech_text += f"  ✓ {item}\n"
        self.tabs["📡 Web Analysis"].delete("1.0", "end")
        self.tabs["📡 Web Analysis"].insert("end", headers + "\n\n" + tech_text)
        
        # Subdomains
        subdomains_text = self.format_list("SUBDOMAINS", self.gathered_data.get('subdomains', []))
        self.tabs["🔍 Subdomains"].delete("1.0", "end")
        self.tabs["🔍 Subdomains"].insert("end", subdomains_text)
        
        # Emails
        emails_text = self.format_list("EMAIL ADDRESSES", self.gathered_data.get('emails', []))
        self.tabs["📧 Emails"].delete("1.0", "end")
        self.tabs["📧 Emails"].insert("end", emails_text)
        
        # DNS Records
        dns_text = self.format_dict("DNS RECORDS", self.gathered_data.get('dns', {}))
        self.tabs["📊 DNS Records"].delete("1.0", "end")
        self.tabs["📊 DNS Records"].insert("end", dns_text)
        
        # Raw Data
        raw_text = json.dumps(self.gathered_data, indent=2, default=str)
        self.tabs["📄 Raw Data"].delete("1.0", "end")
        self.tabs["📄 Raw Data"].insert("end", raw_text)
    
    def format_summary(self):
        """Format summary report"""
        text = "╔" + "═" * 58 + "╗\n"
        text += "║" + " OSINT SCAN SUMMARY ".center(58) + "║\n"
        text += "╚" + "═" * 58 + "╝\n\n"
        
        text += f"Scan Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        text += f"Target: {self.gathered_data.get('domain', {}).get('domain', 'N/A')}\n\n"
        
        text += "KEY FINDINGS:\n" + "═" * 60 + "\n\n"
        text += f"🌐 Domain Registrar: {self.gathered_data.get('domain', {}).get('registrar', 'N/A')}\n"
        text += f"📅 Created: {str(self.gathered_data.get('domain', {}).get('creation_date', 'N/A'))[:10]}\n"
        text += f"⏰ Expires: {str(self.gathered_data.get('domain', {}).get('expiration_date', 'N/A'))[:10]}\n\n"
        
        text += f"🖥️  IP Address: {self.gathered_data.get('ip', {}).get('ip', 'N/A')}\n"
        text += f"🏠 Hostname: {self.gathered_data.get('ip', {}).get('hostname', 'N/A')}\n\n"
        
        text += f"🔒 SSL Issued By: {self.gathered_data.get('ssl', {}).get('issuer', 'N/A')}\n"
        text += f"📜 Valid Until: {self.gathered_data.get('ssl', {}).get('valid_until', 'N/A')}\n\n"
        
        text += f"⚙️  Technologies: {len(self.gathered_data.get('technologies', []))} detected\n"
        text += f"🌍 Subdomains: {len(self.gathered_data.get('subdomains', []))} found\n"
        text += f"📧 Emails: {len(self.gathered_data.get('emails', []))} extracted\n"
        
        return text
    
    def format_dict(self, title, data):
        """Format dictionary for display"""
        text = f"{title}:\n" + "─" * 60 + "\n"
        if isinstance(data, dict):
            for key, value in data.items():
                if key != 'error':
                    key_display = key.replace('_', ' ').title()
                    if isinstance(value, list):
                        text += f"  {key_display}: {', '.join(map(str, value[:3]))}\n"
                    else:
                        text += f"  {key_display}: {value}\n"
        else:
            text += f"  {data}\n"
        return text
    
    def format_list(self, title, items):
        """Format list for display"""
        text = f"{title} ({len(items)}):\n" + "─" * 60 + "\n"
        for item in items[:40]:
            text += f"  • {item}\n"
        if len(items) > 40:
            text += f"\n  ... and {len(items) - 40} more\n"
        return text
    
    def export_pdf(self):
        """Export to PDF"""
        if not self.gathered_data:
            messagebox.showwarning("No Data", "Please run a scan first")
            return
        
        file_path = filedialog.asksaveasfilename(defaultextension=".pdf",
                                                filetypes=[("PDF files", "*.pdf")])
        if file_path:
            try:
                self.osint.generate_pdf_report(self.gathered_data, file_path)
                messagebox.showinfo("Success", f"PDF saved:\n{file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export: {str(e)}")
    
    def export_json(self):
        """Export to JSON"""
        if not self.gathered_data:
            messagebox.showwarning("No Data", "Please run a scan first")
            return
        
        file_path = filedialog.asksaveasfilename(defaultextension=".json",
                                                filetypes=[("JSON files", "*.json")])
        if file_path:
            try:
                with open(file_path, 'w') as f:
                    json.dump(self.gathered_data, f, indent=2, default=str)
                messagebox.showinfo("Success", f"JSON saved:\n{file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export: {str(e)}")
    
    def clear_results(self):
        """Clear all results"""
        self.gathered_data = {}
        self.url_entry.delete(0, "end")
        self.url_entry.insert(0, "https://")
        self.progress_var.set(0)
        self.status_label.config(text="Ready", foreground="blue")
        
        for tab in self.tabs.values():
            tab.delete("1.0", "end")
        
        self.export_pdf_btn.config(state="disabled")
        self.export_json_btn.config(state="disabled")
    
    def scan_complete(self):
        """Called when scan completes"""
        self.scan_btn.config(state="normal")
        self.stop_btn.config(state="disabled")
        self.export_pdf_btn.config(state="normal")
        self.export_json_btn.config(state="normal")
        self.status_label.config(text="✓ Scan completed successfully", foreground="green")
    
    def scan_failed(self):
        """Called when scan fails"""
        self.scan_btn.config(state="normal")
        self.stop_btn.config(state="disabled")
        self.status_label.config(text="✗ Scan failed", foreground="red")


def main():
    """Main entry point"""
    # Suppress SSL warnings
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    root = tk.Tk()
    app = OSINTToolGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()

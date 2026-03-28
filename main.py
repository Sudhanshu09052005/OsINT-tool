"""
OSINT Tool - Website Information Gathering & Analysis
A comprehensive cybersecurity tool for gathering detailed information about websites
and exporting reports to PDF format.

Features:
- Domain & WHOIS information
- DNS records analysis
- SSL/TLS certificate inspection
- HTTP headers analysis
- Technology stack detection
- IP geolocation
- Email & phone number extraction
- Subdomain enumeration
- Robots.txt & sitemap analysis
- Detailed PDF export

Author: Cybersecurity Team
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import requests
import socket
import json
from datetime import datetime
from urllib.parse import urlparse
import validators
from osint_modules.domain_info import get_whois_info, get_dns_records
from osint_modules.network_info import get_ip_info, get_ssl_certificate
from osint_modules.web_analyzer import get_http_headers, detect_technologies, extract_emails
from osint_modules.subdomain_enum import enumerate_subdomains
from osint_modules.pdf_export import generate_pdf_report


class OSINTToolGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("OSINT Intelligence Tool - Website Reconnaissance")
        self.root.geometry("1000x700")
        self.root.resizable(True, True)
        
        # Configure styles
        style = ttk.Style()
        style.theme_use("clam")
        
        self.gathered_data = {}
        self.is_scanning = False
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the user interface"""
        # Header frame
        header_frame = ttk.Frame(self.root)
        header_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Label(header_frame, text="OSINT Web Reconnaissance Tool", 
                 font=("Arial", 16, "bold")).pack(side="left")
        ttk.Label(header_frame, text="v1.0", 
                 font=("Arial", 10, "gray")).pack(side="right")
        
        # Input frame
        input_frame = ttk.LabelFrame(self.root, text="Target URL", padding=10)
        input_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(input_frame, text="Enter Website URL:").pack(side="left", padx=5)
        self.url_entry = ttk.Entry(input_frame, width=50)
        self.url_entry.pack(side="left", padx=5, fill="x", expand=True)
        self.url_entry.insert(0, "https://")
        
        self.scan_btn = ttk.Button(input_frame, text="Start Scan", command=self.start_scan)
        self.scan_btn.pack(side="left", padx=5)
        
        self.stop_btn = ttk.Button(input_frame, text="Stop", command=self.stop_scan, 
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
                                     font=("Arial", 9))
        self.status_label.pack(anchor="w", padx=5)
        
        # Results notebook (tabs)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.tabs = {}
        tab_names = ["Summary", "Domain Info", "Network Info", "Web Analysis", 
                     "Subdomains", "Emails", "Raw Data"]
        
        for tab_name in tab_names:
            frame = ttk.Frame(self.notebook)
            self.notebook.add(frame, text=tab_name)
            self.tabs[tab_name] = frame
            
            # Add text widget with scrollbar
            text_frame = ttk.Frame(frame)
            text_frame.pack(fill="both", expand=True, padx=5, pady=5)
            
            scrollbar = ttk.Scrollbar(text_frame)
            scrollbar.pack(side="right", fill="y")
            
            text_widget = tk.Text(text_frame, wrap="word", yscrollcommand=scrollbar.set,
                                 font=("Courier", 9))
            text_widget.pack(fill="both", expand=True)
            scrollbar.config(command=text_widget.yview)
            
            self.tabs[tab_name] = text_widget
        
        # Export frame
        export_frame = ttk.Frame(self.root)
        export_frame.pack(fill="x", padx=10, pady=10)
        
        self.export_pdf_btn = ttk.Button(export_frame, text="Export to PDF", 
                                        command=self.export_pdf, state="disabled")
        self.export_pdf_btn.pack(side="left", padx=5)
        
        self.export_json_btn = ttk.Button(export_frame, text="Export to JSON", 
                                         command=self.export_json, state="disabled")
        self.export_json_btn.pack(side="left", padx=5)
        
        self.clear_btn = ttk.Button(export_frame, text="Clear Results", 
                                   command=self.clear_results)
        self.clear_btn.pack(side="left", padx=5)
        
        ttk.Label(export_frame, text="", font=("Arial", 9)).pack(side="right", padx=5)
    
    def validate_url(self, url):
        """Validate the input URL"""
        if not validators.url(url):
            messagebox.showerror("Invalid URL", "Please enter a valid URL")
            return False
        return True
    
    def start_scan(self):
        """Start the OSINT scan"""
        url = self.url_entry.get().strip()
        
        if not url:
            messagebox.showerror("Error", "Please enter a URL")
            return
        
        if not self.validate_url(url):
            return
        
        self.is_scanning = True
        self.scan_btn.config(state="disabled")
        self.stop_btn.config(state="normal")
        self.progress_var.set(0)
        self.status_label.config(text="Scan in progress...")
        
        # Run scan in a separate thread
        scan_thread = threading.Thread(target=self.perform_scan, args=(url,))
        scan_thread.daemon = True
        scan_thread.start()
    
    def stop_scan(self):
        """Stop the ongoing scan"""
        self.is_scanning = False
        self.scan_btn.config(state="normal")
        self.stop_btn.config(state="disabled")
        self.status_label.config(text="Scan stopped by user")
    
    def perform_scan(self, url):
        """Perform the actual OSINT scan"""
        try:
            self.gathered_data = {}
            parsed_url = urlparse(url)
            domain = parsed_url.netloc or parsed_url.path
            
            # Step 1: Domain Information (20%)
            self.status_label.config(text="Gathering WHOIS & DNS information...")
            self.root.after(0, self.progress_var.set, 10)
            
            domain_info = get_whois_info(domain)
            dns_records = get_dns_records(domain)
            self.gathered_data["domain"] = domain_info
            self.gathered_data["dns"] = dns_records
            
            # Step 2: Network Information (40%)
            self.status_label.config(text="Analyzing network & SSL information...")
            self.root.after(0, self.progress_var.set, 25)
            
            ip_info = get_ip_info(domain)
            ssl_info = get_ssl_certificate(domain)
            self.gathered_data["ip"] = ip_info
            self.gathered_data["ssl"] = ssl_info
            
            # Step 3: Web Analysis (60%)
            self.status_label.config(text="Analyzing HTTP headers & technologies...")
            self.root.after(0, self.progress_var.set, 40)
            
            headers = get_http_headers(url)
            technologies = detect_technologies(url)
            emails = extract_emails(url)
            self.gathered_data["headers"] = headers
            self.gathered_data["technologies"] = technologies
            self.gathered_data["emails"] = emails
            
            # Step 4: Subdomain Enumeration (80%)
            self.status_label.config(text="Enumerating subdomains...")
            self.root.after(0, self.progress_var.set, 60)
            
            subdomains = enumerate_subdomains(domain)
            self.gathered_data["subdomains"] = subdomains
            
            # Update UI with results
            self.root.after(0, self.update_results)
            
            # Step 5: Completed (100%)
            self.root.after(0, self.progress_var.set, 100)
            self.root.after(0, lambda: self.status_label.config(
                text=f"Scan completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"))
            self.root.after(0, lambda: messagebox.showinfo("Success", 
                "Scan completed successfully!"))
            
            self.root.after(0, lambda: [self.scan_btn.config(state="normal"),
                                        self.stop_btn.config(state="disabled"),
                                        self.export_pdf_btn.config(state="normal"),
                                        self.export_json_btn.config(state="normal")])
            
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Scan Error", 
                f"Error during scan: {str(e)}"))
            self.root.after(0, lambda: [self.scan_btn.config(state="normal"),
                                        self.stop_btn.config(state="disabled"),
                                        self.status_label.config(text="Error occurred")])
    
    def update_results(self):
        """Update the results tabs with gathered information"""
        # Clear all tabs
        for tab_name in self.tabs:
            if isinstance(self.tabs[tab_name], tk.Text):
                self.tabs[tab_name].config(state="normal")
                self.tabs[tab_name].delete("1.0", "end")
        
        # Summary Tab
        summary = f"""
╔══════════════════════════════════════════════════════════════╗
║                    OSINT SCAN SUMMARY                        ║
╚══════════════════════════════════════════════════════════════╝

Scan Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Target Domain: {self.gathered_data.get('domain', {}).get('domain', 'N/A')}

KEY FINDINGS:
═════════════════════════════════════════════════════════════

Domain Information:
  • Registrar: {self.gathered_data.get('domain', {}).get('registrar', 'N/A')}
  • Creation Date: {self.gathered_data.get('domain', {}).get('creation_date', 'N/A')}
  • Expiration Date: {self.gathered_data.get('domain', {}).get('expiration_date', 'N/A')}

Network Information:
  • Primary IP: {self.gathered_data.get('ip', {}).get('ip', 'N/A')}
  • Hostname: {self.gathered_data.get('ip', {}).get('hostname', 'N/A')}

SSL Certificate:
  • Issuer: {self.gathered_data.get('ssl', {}).get('issuer', 'N/A')}
  • Valid Until: {self.gathered_data.get('ssl', {}).get('valid_until', 'N/A')}

Technologies Detected: {len(self.gathered_data.get('technologies', []))} items

Subdomains Found: {len(self.gathered_data.get('subdomains', []))} subdomains

Emails Found: {len(self.gathered_data.get('emails', []))} email addresses
"""
        self.tabs["Summary"].insert("end", summary)
        
        # Domain Info Tab
        domain_info = self.gathered_data.get('domain', {})
        domain_text = self.format_dict_for_display("DOMAIN INFORMATION", domain_info)
        self.tabs["Domain Info"].insert("end", domain_text)
        
        # Network Info Tab
        ip_info = self.gathered_data.get('ip', {})
        ssl_info = self.gathered_data.get('ssl', {})
        network_text = self.format_dict_for_display("IP INFORMATION", ip_info)
        network_text += "\n\n" + self.format_dict_for_display("SSL CERTIFICATE", ssl_info)
        self.tabs["Network Info"].insert("end", network_text)
        
        # Web Analysis Tab
        headers = self.gathered_data.get('headers', {})
        tech = self.gathered_data.get('technologies', [])
        web_text = self.format_dict_for_display("HTTP HEADERS", headers)
        web_text += "\n\nTECHNOLOGIES DETECTED:\n" + "─" * 50 + "\n"
        for item in tech:
            web_text += f"  • {item}\n"
        self.tabs["Web Analysis"].insert("end", web_text)
        
        # Subdomains Tab
        subdomains = self.gathered_data.get('subdomains', [])
        subdomain_text = f"SUBDOMAINS FOUND ({len(subdomains)}):\n" + "─" * 50 + "\n"
        for subdomain in subdomains[:50]:  # Limit to 50
            subdomain_text += f"  • {subdomain}\n"
        if len(subdomains) > 50:
            subdomain_text += f"\n  ... and {len(subdomains) - 50} more\n"
        self.tabs["Subdomains"].insert("end", subdomain_text)
        
        # Emails Tab
        emails = self.gathered_data.get('emails', [])
        email_text = f"EMAILS FOUND ({len(emails)}):\n" + "─" * 50 + "\n"
        for email in emails[:50]:  # Limit to 50
            email_text += f"  • {email}\n"
        if len(emails) > 50:
            email_text += f"\n  ... and {len(emails) - 50} more\n"
        self.tabs["Emails"].insert("end", email_text)
        
        # Raw Data Tab
        raw_text = json.dumps(self.gathered_data, indent=2, default=str)
        self.tabs["Raw Data"].insert("end", raw_text)
    
    def format_dict_for_display(self, title, data):
        """Format a dictionary for display in text widget"""
        text = f"{title}:\n" + "─" * 50 + "\n"
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, list):
                    text += f"  {key}: {', '.join(map(str, value[:5]))}\n"
                else:
                    text += f"  {key}: {value}\n"
        else:
            text += f"  {data}\n"
        return text
    
    def export_pdf(self):
        """Export results to PDF"""
        if not self.gathered_data:
            messagebox.showwarning("No Data", "Please run a scan first")
            return
        
        file_path = filedialog.asksaveasfilename(defaultextension=".pdf",
                                                filetypes=[("PDF files", "*.pdf")])
        if file_path:
            try:
                generate_pdf_report(self.gathered_data, file_path)
                messagebox.showinfo("Success", f"PDF exported to:\n{file_path}")
            except Exception as e:
                messagebox.showerror("Export Error", f"Failed to export PDF: {str(e)}")
    
    def export_json(self):
        """Export results to JSON"""
        if not self.gathered_data:
            messagebox.showwarning("No Data", "Please run a scan first")
            return
        
        file_path = filedialog.asksaveasfilename(defaultextension=".json",
                                                filetypes=[("JSON files", "*.json")])
        if file_path:
            try:
                with open(file_path, 'w') as f:
                    json.dump(self.gathered_data, f, indent=2, default=str)
                messagebox.showinfo("Success", f"JSON exported to:\n{file_path}")
            except Exception as e:
                messagebox.showerror("Export Error", f"Failed to export JSON: {str(e)}")
    
    def clear_results(self):
        """Clear all results"""
        self.gathered_data = {}
        self.url_entry.delete(0, "end")
        self.url_entry.insert(0, "https://")
        self.progress_var.set(0)
        self.status_label.config(text="Ready")
        self.export_pdf_btn.config(state="disabled")
        self.export_json_btn.config(state="disabled")
        
        for tab_name in self.tabs:
            if isinstance(self.tabs[tab_name], tk.Text):
                self.tabs[tab_name].config(state="normal")
                self.tabs[tab_name].delete("1.0", "end")


def main():
    """Main application entry point"""
    root = tk.Tk()
    app = OSINTToolGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()

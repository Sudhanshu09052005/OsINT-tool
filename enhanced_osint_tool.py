"""
Enhanced OSINT Tool - Desktop Version
Advanced Website Investigation with Beautiful PDF Reports
College Project - Complete Feature Set
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import threading
import json
from datetime import datetime
from urllib.parse import urlparse
import validators
import os

# Import our enhanced modules
from advanced_scanner import AdvancedScanner
from enhanced_pdf import EnhancedPDFReport

# Import original osint_tool for basic functions
from osint_tool import OSINTTool


class EnhancedOSINTGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("OSINT Investigation Tool - Enhanced Edition")
        self.root.geometry("1200x800")
        self.root.resizable(True, True)
        
        # Configure style
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Title.TLabel", font=("Arial", 16, "bold"))
        style.configure("Header.TLabel", font=("Arial", 12, "bold"))
        
        self.gathered_data = {}
        self.is_scanning = False
        self.basic_scanner = OSINTTool()
        self.advanced_scanner = AdvancedScanner()
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup enhanced user interface"""
        # Header frame
        header_frame = ttk.Frame(self.root, style="Header.TFrame")
        header_frame.pack(fill="x", padx=10, pady=10)
        
        title_label = ttk.Label(
            header_frame,
            text="🔍 OSINT Investigation Tool - Enhanced Edition",
            style="Title.TLabel",
            foreground="#1a237e"
        )
        title_label.pack(side="left")
        
        version_label = ttk.Label(header_frame, text="v2.0 - College Edition", font=("Arial", 9))
        version_label.pack(side="right", padx=5)
        
        # Input frame
        input_frame = ttk.LabelFrame(self.root, text="🎯 Target Configuration", padding=15)
        input_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(input_frame, text="Target URL:", font=("Arial", 10, "bold")).grid(
            row=0, column=0, padx=5, pady=5, sticky="w"
        )
        
        self.url_entry = ttk.Entry(input_frame, width=60, font=("Arial", 10))
        self.url_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.url_entry.insert(0, "https://")
        
        self.scan_btn = ttk.Button(
            input_frame,
            text="▶ Start Investigation",
            command=self.start_scan,
            style="Accent.TButton"
        )
        self.scan_btn.grid(row=0, column=2, padx=5, pady=5)
        
        self.stop_btn = ttk.Button(
            input_frame,
            text="⬛ Stop",
            command=self.stop_scan,
            state="disabled"
        )
        self.stop_btn.grid(row=0, column=3, padx=5, pady=5)
        
        input_frame.columnconfigure(1, weight=1)
        
        # Progress frame
        progress_frame = ttk.LabelFrame(self.root, text="📊 Scan Progress", padding=10)
        progress_frame.pack(fill="x", padx=10, pady=5)
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            progress_frame,
            variable=self.progress_var,
            maximum=100,
            mode='determinate',
            length=400
        )
        self.progress_bar.pack(fill="x", padx=5, pady=5)
        
        self.status_label = ttk.Label(
            progress_frame,
            text="Ready to scan",
            font=("Arial", 9),
            foreground="#4caf50"
        )
        self.status_label.pack(anchor="w", padx=5, pady=2)
        
        # Notebook for results
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Create tabs with enhanced categories
        self.tabs = {}
        tab_config = [
            ("📋 Summary", "summary"),
            ("🌐 Domain Info", "domain"),
            ("🔒 Security", "security"),
            ("🔌 Port Scan", "ports"),
            ("⚙️ Technologies", "tech"),
            ("📝 Metadata", "metadata"),
            ("🤖 robots.txt", "robots"),
            ("📱 Social Media", "social"),
            ("🔗 Links", "links"),
            ("🍪 Cookies", "cookies"),
            ("📜 Raw Data", "raw")
        ]
        
        for tab_title, tab_key in tab_config:
            frame = ttk.Frame(self.notebook)
            self.notebook.add(frame, text=tab_title)
            
            # Add text widget with scrollbar
            text_frame = ttk.Frame(frame)
            text_frame.pack(fill="both", expand=True, padx=5, pady=5)
            
            scrollbar = ttk.Scrollbar(text_frame)
            scrollbar.pack(side="right", fill="y")
            
            text_widget = tk.Text(
                text_frame,
                wrap="word",
                yscrollcommand=scrollbar.set,
                font=("Consolas", 9),
                bg="#f5f5f5"
            )
            text_widget.pack(fill="both", expand=True)
            scrollbar.config(command=text_widget.yview)
            
            self.tabs[tab_key] = text_widget
        
        # Export frame
        export_frame = ttk.LabelFrame(self.root, text="📥 Export Options", padding=10)
        export_frame.pack(fill="x", padx=10, pady=10)
        
        self.export_pdf_btn = ttk.Button(
            export_frame,
            text="📄 Export Beautiful PDF",
            command=self.export_pdf,
            state="disabled"
        )
        self.export_pdf_btn.pack(side="left", padx=5)
        
        self.export_json_btn = ttk.Button(
            export_frame,
            text="📊 Export JSON",
            command=self.export_json,
            state="disabled"
        )
        self.export_json_btn.pack(side="left", padx=5)
        
        self.clear_btn = ttk.Button(
            export_frame,
            text="🗑️ Clear Results",
            command=self.clear_results
        )
        self.clear_btn.pack(side="left", padx=5)
        
        # Status info
        info_label = ttk.Label(
            export_frame,
            text="💡 Tip: This tool gathers detailed information for investigation purposes",
            font=("Arial", 8),
            foreground="#666"
        )
        info_label.pack(side="right", padx=5)
    
    def validate_url(self, url):
        """Validate URL"""
        if not validators.url(url):
            messagebox.showerror("Invalid URL", "Please enter a valid URL (e.g., https://example.com)")
            return False
        return True
    
    def start_scan(self):
        """Start comprehensive scan"""
        url = self.url_entry.get().strip()
        
        if not url or url == "https://":
            messagebox.showerror("Error", "Please enter a target URL")
            return
        
        if not self.validate_url(url):
            return
        
        self.is_scanning = True
        self.scan_btn.config(state="disabled")
        self.stop_btn.config(state="normal")
        self.progress_var.set(0)
        self.status_label.config(text="🔄 Initializing scan...", foreground="#2196F3")
        
        # Run scan in background thread
        scan_thread = threading.Thread(target=self.perform_comprehensive_scan, args=(url,))
        scan_thread.daemon = True
        scan_thread.start()
    
    def stop_scan(self):
        """Stop scanning"""
        self.is_scanning = False
        self.scan_btn.config(state="normal")
        self.stop_btn.config(state="disabled")
        self.status_label.config(text="⚠️ Scan stopped by user", foreground="#ff9800")
    
    def perform_comprehensive_scan(self, url):
        """Perform comprehensive OSINT scan with all features"""
        try:
            self.gathered_data = {}
            parsed_url = urlparse(url)
            domain = parsed_url.netloc or parsed_url.path
            
            if not self.is_scanning:
                return
            
            # Phase 1: Basic Information (0-20%)
            self.update_status("📡 Gathering WHOIS & DNS information...", 5)
            self.gathered_data['domain'] = self.basic_scanner.get_whois_info(domain)
            self.gathered_data['dns'] = self.basic_scanner.get_dns_records(domain)
            
            if not self.is_scanning:
                return
            
            # Phase 2: Network Analysis (20-35%)
            self.update_status("🌐 Analyzing network & IP information...", 20)
            self.gathered_data['ip'] = self.basic_scanner.get_ip_info(domain)
            self.gathered_data['ssl'] = self.basic_scanner.get_ssl_certificate(domain)
            self.gathered_data['server_info'] = self.advanced_scanner.get_server_info(domain)
            
            if not self.is_scanning:
                return
            
            # Phase 3: Port Scanning (35-45%)
            self.update_status("🔌 Scanning ports for open services...", 35)
            self.gathered_data['port_scan'] = self.advanced_scanner.scan_ports(domain)
            
            if not self.is_scanning:
                return
            
            # Phase 4: Security Analysis (45-55%)
            self.update_status("🔒 Analyzing security headers...", 45)
            self.gathered_data['security_headers'] = self.advanced_scanner.analyze_security_headers(url)
            
            if not self.is_scanning:
                return
            
            # Phase 5: Web Technologies (55-65%)
            self.update_status("⚙️ Detecting technologies & CMS...", 55)
            self.gathered_data['headers'] = self.basic_scanner.get_http_headers(url)
            self.gathered_data['technologies'] = self.basic_scanner.detect_technologies(url)
            self.gathered_data['cms'] = self.advanced_scanner.detect_cms(url)
            
            if not self.is_scanning:
                return
            
            # Phase 6: Content Analysis (65-75%)
            self.update_status("📝 Extracting metadata & content...", 65)
            self.gathered_data['meta_tags'] = self.advanced_scanner.extract_meta_tags(url)
            self.gathered_data['robots_txt'] = self.advanced_scanner.get_robots_txt(url)
            self.gathered_data['emails'] = self.basic_scanner.extract_emails(url)
            
            if not self.is_scanning:
                return
            
            # Phase 7: Links & Social Media (75-85%)
            self.update_status("🔗 Extracting links & social media...", 75)
            self.gathered_data['social_media'] = self.advanced_scanner.find_social_media_links(url)
            self.gathered_data['page_links'] = self.advanced_scanner.get_page_links(url)
            
            if not self.is_scanning:
                return
            
            # Phase 8: Additional Analysis (85-95%)
            self.update_status("🍪 Analyzing cookies & archives...", 85)
            self.gathered_data['cookies'] = self.advanced_scanner.analyze_cookies(url)
            self.gathered_data['wayback'] = self.advanced_scanner.check_wayback_machine(url)
            
            # Phase 9: Finalization (95-100%)
            self.update_status("✅ Finalizing results...", 95)
            self.root.after(0, self.display_results)
            
            self.update_status("✅ Scan completed successfully!", 100)
            
            self.root.after(0, lambda: [
                messagebox.showinfo("Success", "Investigation completed! Review the results in different tabs."),
                self.scan_btn.config(state="normal"),
                self.stop_btn.config(state="disabled"),
                self.export_pdf_btn.config(state="normal"),
                self.export_json_btn.config(state="normal")
            ])
            
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Scan Error", f"Error during scan:\n{str(e)}"))
            self.root.after(0, lambda: [
                self.scan_btn.config(state="normal"),
                self.stop_btn.config(state="disabled")
            ])
            self.update_status(f"❌ Error: {str(e)}", 0)
    
    def update_status(self, message, progress):
        """Update status and progress"""
        self.root.after(0, lambda: self.progress_var.set(progress))
        self.root.after(0, lambda: self.status_label.config(text=message))
    
    def display_results(self):
        """Display comprehensive results"""
        # Clear all tabs
        for tab_widget in self.tabs.values():
            if isinstance(tab_widget, tk.Text):
                tab_widget.config(state="normal")
                tab_widget.delete("1.0", "end")
        
        # Summary Tab
        self.display_summary()
        
        # Domain Info Tab
        self.display_domain_info()
        
        # Security Tab
        self.display_security_analysis()
        
        # Ports Tab
        self.display_port_scan()
        
        # Technologies Tab
        self.display_technologies()
        
        # Metadata Tab
        self.display_metadata()
        
        # Robots.txt Tab
        self.display_robots()
        
        # Social Media Tab
        self.display_social_media()
        
        # Links Tab
        self.display_links()
        
        # Cookies Tab
        self.display_cookies()
        
        # Raw Data Tab
        self.tabs['raw'].insert("end", json.dumps(self.gathered_data, indent=2, default=str))
    
    def display_summary(self):
        """Display executive summary"""
        data = self.gathered_data
        summary = f"""
╔══════════════════════════════════════════════════════════════════════╗
║                    INVESTIGATION SUMMARY                              ║
╚══════════════════════════════════════════════════════════════════════╝

📅 Scan Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
🎯 Target: {data.get('domain', {}).get('domain', 'N/A')}

═════════════════════════════════════════════════════════════════════════

KEY FINDINGS:
─────────────────────────────────────────────────────────────────────────

🌐 DOMAIN INFORMATION:
   • Registrar: {data.get('domain', {}).get('registrar', 'N/A')}
   • Created: {data.get('domain', {}).get('creation_date', 'N/A')}
   • Expires: {data.get('domain', {}).get('expiration_date', 'N/A')}

🔒 SECURITY ANALYSIS:
   • Security Score: {data.get('security_headers', {}).get('security_score', 'N/A')}%
   • Open Ports: {data.get('port_scan', {}).get('open_ports', 'N/A')}
   • SSL Issuer: {data.get('ssl', {}).get('issuer', 'N/A')}

⚙️ TECHNOLOGY STACK:
   • CMS Detected: {data.get('cms', {}).get('detected', ['N/A'])[0]}
   • Technologies: {len(data.get('technologies', []))} identified
   • Server: {data.get('security_headers', {}).get('server', 'N/A')}

📊 CONTENT ANALYSIS:
   • Social Media Links: {len(data.get('social_media', {}))} platforms found
   • Email Addresses: {len(data.get('emails', []))} discovered
   • Internal Links: {data.get('page_links', {}).get('total_internal', 0)}
   • External Links: {data.get('page_links', {}).get('total_external', 0)}

🔍 ADDITIONAL FINDINGS:
   • Cookies Set: {data.get('cookies', {}).get('total_cookies', 0)}
   • Archive Available: {'Yes' if data.get('wayback', {}).get('available') else 'No'}
   • robots.txt: {'Found' if data.get('robots_txt', {}).get('found') else 'Not Found'}

═════════════════════════════════════════════════════════════════════════
"""
        self.tabs['summary'].insert("end", summary)
    
    def display_domain_info(self):
        """Display domain information"""
        domain_info = self.gathered_data.get('domain', {})
        text = "═" * 70 + "\n"
        text += "DOMAIN INFORMATION\n"
        text += "═" * 70 + "\n\n"
        
        for key, value in domain_info.items():
            text += f"{key.replace('_', ' ').title()}: {value}\n"
        
        self.tabs['domain'].insert("end", text)
    
    def display_security_analysis(self):
        """Display security analysis"""
        sec = self.gathered_data.get('security_headers', {})
        text = "═" * 70 + "\n"
        text += f"SECURITY ANALYSIS - Score: {sec.get('security_score', 0)}%\n"
        text += "═" * 70 + "\n\n"
        
        if sec.get('present'):
            text += "✅ PRESENT SECURITY HEADERS:\n" + "─" * 70 + "\n"
            for header in sec['present']:
                text += f"\n• {header['header']}\n"
                text += f"  Value: {header['value']}\n"
                text += f"  Description: {header['description']}\n"
        
        if sec.get('missing'):
            text += "\n\n⚠️ MISSING SECURITY HEADERS:\n" + "─" * 70 + "\n"
            for header in sec['missing']:
                text += f"\n• {header['header']}\n"
                text += f"  Description: {header['description']}\n"
                text += f"  Risk: {header['risk']}\n"
        
        self.tabs['security'].insert("end", text)
    
    def display_port_scan(self):
        """Display port scan results"""
        ports = self.gathered_data.get('port_scan', {})
        text = f"""
Port Scan Results
═════════════════════════════════════════════════════════════════════════
IP Address: {ports.get('ip', 'N/A')}
Scanned Ports: {ports.get('scanned_ports', 0)}
Open Ports: {ports.get('open_ports', 0)}

OPEN PORTS DETECTED:
─────────────────────────────────────────────────────────────────────────
"""
        if ports.get('details'):
            for port in ports['details']:
                text += f"\n🔌 Port {port['port']} ({port['status']})\n"
                text += f"   Service: {port['service']}\n"
        else:
            text += "\nNo open ports detected or scan failed.\n"
        
        self.tabs['ports'].insert("end", text)
    
    def display_technologies(self):
        """Display technologies"""
        tech = self.gathered_data.get('technologies', [])
        cms = self.gathered_data.get('cms', {})
        
        text = f"""
TECHNOLOGY STACK DETECTED
═════════════════════════════════════════════════════════════════════════

CMS: {cms.get('detected', ['Not Detected'])[0]}
Confidence: {cms.get('confidence', 'N/A')}

TECHNOLOGIES ({len(tech)} found):
─────────────────────────────────────────────────────────────────────────
"""
        for item in tech[:50]:
            text += f"• {item}\n"
        
        if len(tech) > 50:
            text += f"\n... and {len(tech) - 50} more technologies\n"
        
        self.tabs['tech'].insert("end", text)
    
    def display_metadata(self):
        """Display metadata"""
        meta = self.gathered_data.get('meta_tags', {})
        text = "WEBSITE METADATA\n" + "═" * 70 + "\n\n"
        text += f"Title: {meta.get('title', 'N/A')}\n\n"
        text += f"Description: {meta.get('description', 'N/A')}\n\n"
        text += f"Keywords: {meta.get('keywords', 'N/A')}\n\n"
        text += f"Author: {meta.get('author', 'N/A')}\n\n"
        text += f"Generator: {meta.get('generator', 'N/A')}\n\n"
        
        self.tabs['metadata'].insert("end", text)
    
    def display_robots(self):
        """Display robots.txt"""
        robots = self.gathered_data.get('robots_txt', {})
        
        if robots.get('found'):
            text = "ROBOTS.TXT ANALYSIS\n" + "═" * 70 + "\n\n"
            text += "Disallowed Paths:\n"
            for path in robots.get('disallowed_paths', [])[:30]:
                text += f"  • {path}\n"
            
            if robots.get('sitemaps'):
                text += "\nSitemaps:\n"
                for sitemap in robots.get('sitemaps', []):
                    text += f"  • {sitemap}\n"
        else:
            text = "robots.txt not found on this website."
        
        self.tabs['robots'].insert("end", text)
    
    def display_social_media(self):
        """Display social media links"""
        social = self.gathered_data.get('social_media', {})
        text = "SOCIAL MEDIA PRESENCE\n" + "═" * 70 + "\n\n"
        
        if 'message' not in social and social:
            for platform, links in social.items():
                text += f"\n{platform}:\n"
                for link in links[:10]:
                    text += f"  • {link}\n"
        else:
            text += "No social media links found.\n"
        
        self.tabs['social'].insert("end", text)
    
    def display_links(self):
        """Display page links"""
        links = self.gathered_data.get('page_links', {})
        text = f"""
PAGE LINKS ANALYSIS
═════════════════════════════════════════════════════════════════════════

Internal Links: {links.get('total_internal', 0)}
External Links: {links.get('total_external', 0)}

INTERNAL LINKS (Sample):
─────────────────────────────────────────────────────────────────────────
"""
        for link in links.get('internal_links', [])[:20]:
            text += f"• {link}\n"
        
        text += f"\n\nEXTERNAL LINKS (Sample):\n" + "─" * 70 + "\n"
        for link in links.get('external_links', [])[:20]:
            text += f"• {link}\n"
        
        self.tabs['links'].insert("end", text)
    
    def display_cookies(self):
        """Display cookies"""
        cookies = self.gathered_data.get('cookies', {})
        text = f"COOKIES ANALYSIS\n{'═' * 70}\n\n"
        text += f"Total Cookies: {cookies.get('total_cookies', 0)}\n\n"
        
        for cookie in cookies.get('cookies', []):
            text += f"\nCookie: {cookie['name']}\n"
            text += f"  Domain: {cookie['domain']}\n"
            text += f"  Secure: {cookie['secure']}\n"
            text += f"  HttpOnly: {cookie['httponly']}\n"
            text += f"  Expires: {cookie['expires']}\n"
        
        self.tabs['cookies'].insert("end", text)
    
    def export_pdf(self):
        """Export to enhanced PDF"""
        if not self.gathered_data:
            messagebox.showwarning("No Data", "Please run a scan first")
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
            initialfile=f"osint_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        )
        
        if file_path:
            try:
                pdf_generator = EnhancedPDFReport(file_path)
                pdf_generator.generate(self.gathered_data)
                messagebox.showinfo("Success", f"Beautiful PDF report exported to:\n{file_path}")
            except Exception as e:
                messagebox.showerror("Export Error", f"Failed to export PDF:\n{str(e)}")
    
    def export_json(self):
        """Export to JSON"""
        if not self.gathered_data:
            messagebox.showwarning("No Data", "Please run a scan first")
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json")],
            initialfile=f"osint_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )
        
        if file_path:
            try:
                with open(file_path, 'w') as f:
                    json.dump(self.gathered_data, f, indent=2, default=str)
                messagebox.showinfo("Success", f"JSON data exported to:\n{file_path}")
            except Exception as e:
                messagebox.showerror("Export Error", f"Failed to export JSON:\n{str(e)}")
    
    def clear_results(self):
        """Clear all results"""
        self.gathered_data = {}
        self.url_entry.delete(0, "end")
        self.url_entry.insert(0, "https://")
        self.progress_var.set(0)
        self.status_label.config(text="Ready to scan", foreground="#4caf50")
        self.export_pdf_btn.config(state="disabled")
        self.export_json_btn.config(state="disabled")
        
        for tab_widget in self.tabs.values():
            if isinstance(tab_widget, tk.Text):
                tab_widget.config(state="normal")
                tab_widget.delete("1.0", "end")


def main():
    """Main entry point"""
    root = tk.Tk()
    app = EnhancedOSINTGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()

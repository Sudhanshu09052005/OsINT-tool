"""
Advanced OSINT Scanner - Detailed Investigation Features
For college project - Enhanced website reconnaissance
"""

import requests
import socket
import ssl
import json
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import re
from datetime import datetime


class AdvancedScanner:
    """Advanced scanning capabilities for detailed investigation"""
    
    def __init__(self, timeout=10):
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def scan_ports(self, domain, ports=None):
        """
        Scan common ports for open services
        """
        if ports is None:
            # Common ports for investigation
            ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 445, 993, 995, 
                     3306, 3389, 5432, 5900, 8080, 8443, 8888]
        
        try:
            domain = domain.replace("http://", "").replace("https://", "").replace("www.", "")
            ip = socket.gethostbyname(domain)
            
            open_ports = []
            services = {
                21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS",
                80: "HTTP", 110: "POP3", 143: "IMAP", 443: "HTTPS", 445: "SMB",
                993: "IMAPS", 995: "POP3S", 3306: "MySQL", 3389: "RDP",
                5432: "PostgreSQL", 5900: "VNC", 8080: "HTTP-Alt", 
                8443: "HTTPS-Alt", 8888: "HTTP-Proxy"
            }
            
            for port in ports:
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(2)
                    result = sock.connect_ex((ip, port))
                    if result == 0:
                        service = services.get(port, "Unknown")
                        open_ports.append({
                            "port": port,
                            "service": service,
                            "status": "OPEN"
                        })
                    sock.close()
                except:
                    pass
            
            return {
                "ip": ip,
                "scanned_ports": len(ports),
                "open_ports": len(open_ports),
                "details": open_ports
            }
        except Exception as e:
            return {"error": f"Port scan failed: {str(e)}"}
    
    def analyze_security_headers(self, url):
        """
        Analyze security headers for vulnerabilities
        """
        try:
            response = self.session.get(url, timeout=self.timeout, allow_redirects=True)
            headers = response.headers
            
            security_headers = {
                'Strict-Transport-Security': 'HSTS - Forces HTTPS connections',
                'X-Frame-Options': 'Clickjacking protection',
                'X-Content-Type-Options': 'MIME-sniffing protection',
                'X-XSS-Protection': 'XSS attack protection',
                'Content-Security-Policy': 'Content injection protection',
                'Referrer-Policy': 'Controls referrer information',
                'Permissions-Policy': 'Browser feature permissions',
                'X-Permitted-Cross-Domain-Policies': 'Cross-domain policy'
            }
            
            analysis = {
                "security_score": 0,
                "present": [],
                "missing": [],
                "headers_found": {}
            }
            
            for header, description in security_headers.items():
                if header in headers:
                    analysis["present"].append({
                        "header": header,
                        "value": headers[header],
                        "description": description
                    })
                    analysis["security_score"] += 12.5
                else:
                    analysis["missing"].append({
                        "header": header,
                        "description": description,
                        "risk": "Potential security vulnerability"
                    })
            
            # Additional server information
            analysis["server"] = headers.get('Server', 'N/A')
            analysis["powered_by"] = headers.get('X-Powered-By', 'N/A')
            analysis["security_score"] = round(analysis["security_score"], 1)
            
            return analysis
        except Exception as e:
            return {"error": f"Security header analysis failed: {str(e)}"}
    
    def detect_cms(self, url):
        """
        Detect Content Management System (CMS)
        """
        try:
            response = self.session.get(url, timeout=self.timeout)
            content = response.text
            headers = response.headers
            
            cms_signatures = {
                'WordPress': [
                    '/wp-content/',
                    '/wp-includes/',
                    'wp-json',
                    'wordpress'
                ],
                'Joomla': [
                    '/components/com_',
                    '/modules/mod_',
                    'Joomla!'
                ],
                'Drupal': [
                    'Drupal',
                    '/sites/default/',
                    '/modules/system/'
                ],
                'Magento': [
                    'Magento',
                    '/skin/frontend/',
                    'mage/cookies'
                ],
                'Shopify': [
                    'cdn.shopify.com',
                    'Shopify'
                ],
                'Wix': [
                    'wixsite.com',
                    'X-Wix-Request-Id'
                ]
            }
            
            detected = []
            for cms, signatures in cms_signatures.items():
                for sig in signatures:
                    if sig in content or sig in str(headers):
                        detected.append(cms)
                        break
            
            return {
                "detected": detected if detected else ["Not Detected"],
                "confidence": "High" if detected else "N/A"
            }
        except Exception as e:
            return {"error": f"CMS detection failed: {str(e)}"}
    
    def get_robots_txt(self, url):
        """
        Analyze robots.txt for restricted paths
        """
        try:
            parsed = urlparse(url)
            robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
            
            response = self.session.get(robots_url, timeout=self.timeout)
            if response.status_code == 200:
                content = response.text
                
                # Parse robots.txt
                disallowed = []
                allowed = []
                sitemaps = []
                
                for line in content.split('\n'):
                    line = line.strip()
                    if line.lower().startswith('disallow:'):
                        path = line.split(':', 1)[1].strip()
                        if path:
                            disallowed.append(path)
                    elif line.lower().startswith('allow:'):
                        path = line.split(':', 1)[1].strip()
                        if path:
                            allowed.append(path)
                    elif line.lower().startswith('sitemap:'):
                        sitemap = line.split(':', 1)[1].strip()
                        sitemaps.append(sitemap)
                
                return {
                    "found": True,
                    "disallowed_paths": disallowed,
                    "allowed_paths": allowed,
                    "sitemaps": sitemaps,
                    "full_content": content
                }
            else:
                return {"found": False, "message": "robots.txt not found"}
        except Exception as e:
            return {"error": f"robots.txt analysis failed: {str(e)}"}
    
    def extract_meta_tags(self, url):
        """
        Extract all meta tags for investigation
        """
        try:
            response = self.session.get(url, timeout=self.timeout)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            meta_tags = {
                "title": soup.title.string if soup.title else "N/A",
                "description": "",
                "keywords": "",
                "author": "",
                "generator": "",
                "robots": "",
                "viewport": "",
                "og_tags": {},
                "twitter_tags": {},
                "all_meta": []
            }
            
            for meta in soup.find_all('meta'):
                meta_data = {
                    "name": meta.get('name', ''),
                    "property": meta.get('property', ''),
                    "content": meta.get('content', '')
                }
                meta_tags["all_meta"].append(meta_data)
                
                # Extract specific meta tags
                name = meta.get('name', '').lower()
                if name == 'description':
                    meta_tags["description"] = meta.get('content', '')
                elif name == 'keywords':
                    meta_tags["keywords"] = meta.get('content', '')
                elif name == 'author':
                    meta_tags["author"] = meta.get('content', '')
                elif name == 'generator':
                    meta_tags["generator"] = meta.get('content', '')
                elif name == 'robots':
                    meta_tags["robots"] = meta.get('content', '')
                elif name == 'viewport':
                    meta_tags["viewport"] = meta.get('content', '')
                
                # Open Graph tags
                prop = meta.get('property', '').lower()
                if prop.startswith('og:'):
                    meta_tags["og_tags"][prop] = meta.get('content', '')
                elif prop.startswith('twitter:'):
                    meta_tags["twitter_tags"][prop] = meta.get('content', '')
            
            return meta_tags
        except Exception as e:
            return {"error": f"Meta tag extraction failed: {str(e)}"}
    
    def find_social_media_links(self, url):
        """
        Find social media profiles linked on the website
        """
        try:
            response = self.session.get(url, timeout=self.timeout)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            social_patterns = {
                'Facebook': r'(https?://)?(www\.)?facebook\.com/[\w\-\.]+',
                'Twitter': r'(https?://)?(www\.)?twitter\.com/[\w\-\.]+',
                'Instagram': r'(https?://)?(www\.)?instagram\.com/[\w\-\.]+',
                'LinkedIn': r'(https?://)?(www\.)?linkedin\.com/(company|in)/[\w\-\.]+',
                'YouTube': r'(https?://)?(www\.)?youtube\.com/(channel|c|user)/[\w\-\.]+',
                'TikTok': r'(https?://)?(www\.)?tiktok\.com/@[\w\-\.]+',
                'GitHub': r'(https?://)?(www\.)?github\.com/[\w\-\.]+',
                'Pinterest': r'(https?://)?(www\.)?pinterest\.com/[\w\-\.]+',
            }
            
            social_links = {}
            page_content = str(soup)
            
            for platform, pattern in social_patterns.items():
                matches = re.findall(pattern, page_content, re.IGNORECASE)
                if matches:
                    # Clean up matches
                    cleaned = list(set([''.join(m) if isinstance(m, tuple) else m for m in matches]))
                    social_links[platform] = cleaned
            
            return social_links if social_links else {"message": "No social media links found"}
        except Exception as e:
            return {"error": f"Social media extraction failed: {str(e)}"}
    
    def get_server_info(self, domain):
        """
        Advanced server fingerprinting
        """
        try:
            domain = domain.replace("http://", "").replace("https://", "").replace("www.", "")
            
            info = {
                "hostname": domain,
                "ip_address": "",
                "reverse_dns": "",
                "geolocation": {},
                "asn": ""
            }
            
            # Get IP
            try:
                ip = socket.gethostbyname(domain)
                info["ip_address"] = ip
                
                # Reverse DNS
                try:
                    reverse = socket.gethostbyaddr(ip)
                    info["reverse_dns"] = reverse[0]
                except:
                    info["reverse_dns"] = "N/A"
                
                # Try to get geolocation (using ip-api.com - free service)
                try:
                    geo_response = requests.get(f"http://ip-api.com/json/{ip}", timeout=5)
                    if geo_response.status_code == 200:
                        geo_data = geo_response.json()
                        info["geolocation"] = {
                            "country": geo_data.get("country", "N/A"),
                            "region": geo_data.get("regionName", "N/A"),
                            "city": geo_data.get("city", "N/A"),
                            "isp": geo_data.get("isp", "N/A"),
                            "org": geo_data.get("org", "N/A"),
                            "timezone": geo_data.get("timezone", "N/A")
                        }
                except:
                    info["geolocation"] = {"error": "Could not fetch geolocation"}
                
            except Exception as e:
                info["error"] = str(e)
            
            return info
        except Exception as e:
            return {"error": f"Server info failed: {str(e)}"}
    
    def check_wayback_machine(self, url):
        """
        Check Wayback Machine archive availability
        """
        try:
            parsed = urlparse(url)
            domain = f"{parsed.scheme}://{parsed.netloc}"
            
            # Check availability
            api_url = f"http://archive.org/wayback/available?url={domain}"
            response = requests.get(api_url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('archived_snapshots'):
                    closest = data['archived_snapshots'].get('closest', {})
                    if closest:
                        return {
                            "available": True,
                            "timestamp": closest.get('timestamp', 'N/A'),
                            "url": closest.get('url', 'N/A'),
                            "status": closest.get('status', 'N/A')
                        }
            
            return {"available": False, "message": "No archived snapshots found"}
        except Exception as e:
            return {"error": f"Wayback Machine check failed: {str(e)}"}
    
    def analyze_cookies(self, url):
        """
        Analyze cookies set by the website
        """
        try:
            response = self.session.get(url, timeout=self.timeout)
            cookies = response.cookies
            
            cookie_analysis = []
            for cookie in cookies:
                cookie_info = {
                    "name": cookie.name,
                    "value": cookie.value[:50] + "..." if len(cookie.value) > 50 else cookie.value,
                    "domain": cookie.domain,
                    "path": cookie.path,
                    "secure": cookie.secure,
                    "httponly": hasattr(cookie, 'httponly') and cookie.httponly,
                    "expires": cookie.expires if cookie.expires else "Session"
                }
                cookie_analysis.append(cookie_info)
            
            return {
                "total_cookies": len(cookie_analysis),
                "cookies": cookie_analysis
            }
        except Exception as e:
            return {"error": f"Cookie analysis failed: {str(e)}"}
    
    def get_page_links(self, url, max_links=100):
        """
        Extract all internal and external links
        """
        try:
            response = self.session.get(url, timeout=self.timeout)
            soup = BeautifulSoup(response.content, 'html.parser')
            parsed_url = urlparse(url)
            base_domain = parsed_url.netloc
            
            internal_links = set()
            external_links = set()
            
            for link in soup.find_all('a', href=True):
                href = link['href']
                absolute_url = urljoin(url, href)
                parsed_link = urlparse(absolute_url)
                
                if parsed_link.netloc == base_domain:
                    internal_links.add(absolute_url)
                elif parsed_link.netloc:
                    external_links.add(absolute_url)
                
                if len(internal_links) + len(external_links) >= max_links:
                    break
            
            return {
                "total_internal": len(internal_links),
                "total_external": len(external_links),
                "internal_links": list(internal_links)[:50],
                "external_links": list(external_links)[:50]
            }
        except Exception as e:
            return {"error": f"Link extraction failed: {str(e)}"}

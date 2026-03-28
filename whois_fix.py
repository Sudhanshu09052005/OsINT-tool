"""
Fixed WHOIS Module - Works without whois package
"""

import socket
import subprocess
import platform


def get_whois_info_fixed(domain):
    """
    Get WHOIS information - Works even if whois package has issues
    """
    try:
        domain = domain.replace("http://", "").replace("https://", "").replace("www.", "").split('/')[0]
        
        # Method 1: Try python-whois
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
                "status": str(result.get('status', 'N/A')),
            }
        except ImportError:
            pass
        except Exception as e:
            print(f"python-whois failed: {e}")
        
        # Method 2: Try whois command line (Windows/Linux)
        try:
            if platform.system() == "Windows":
                # Windows doesn't have built-in whois, skip
                raise Exception("Windows whois not available")
            else:
                # Linux/Mac
                result = subprocess.run(['whois', domain], capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    return {
                        "domain": domain,
                        "registrar": "Check raw data",
                        "creation_date": "Check raw data",
                        "expiration_date": "Check raw data",
                        "raw_whois": result.stdout[:500]
                    }
        except:
            pass
        
        # Method 3: Return basic info
        return {
            "domain": domain,
            "registrar": "N/A - WHOIS service unavailable",
            "creation_date": "N/A",
            "expiration_date": "N/A",
            "updated_date": "N/A",
            "name_servers": [],
            "status": "Unable to query WHOIS",
            "note": "Install 'python-whois' package: pip install python-whois"
        }
        
    except Exception as e:
        return {
            "domain": domain,
            "error": f"WHOIS lookup failed: {str(e)}",
            "registrar": "N/A",
            "creation_date": "N/A",
            "expiration_date": "N/A"
        }


# Test it
if __name__ == "__main__":
    print("Testing fixed WHOIS function...")
    result = get_whois_info_fixed("example.com")
    print(result)

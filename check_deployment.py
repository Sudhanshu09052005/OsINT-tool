#!/usr/bin/env python3
"""
Railway Deployment Status Checker
Run this to verify your Railway deployment is working
"""

import requests
import sys

def check_deployment(url):
    """Check if the Railway deployment is working"""
    try:
        print(f"🔍 Checking deployment at: {url}")
        response = requests.get(url, timeout=10)

        if response.status_code == 200:
            print("✅ Deployment is LIVE and working!")
            print(f"📊 Response time: {response.elapsed.total_seconds():.2f} seconds")

            # Check if it's the OSINT tool
            if "OSINT" in response.text or "Investigation Tool" in response.text:
                print("🎯 OSINT Tool detected - deployment successful!")
                return True
            else:
                print("⚠️ Page loaded but OSINT tool not detected")
                return False
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            return False

    except requests.exceptions.RequestException as e:
        print(f"❌ Connection Error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Railway Deployment Status Checker")
    print("=" * 50)

    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        url = input("Enter your Railway URL (e.g., https://your-project.up.railway.app): ").strip()

    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url

    success = check_deployment(url)

    if success:
        print("\n🎉 Your OSINT Investigation Tool is successfully deployed!")
        print("📱 You can now access it from any device 24/7")
        print(f"🔗 URL: {url}")
    else:
        print("\n❌ Deployment check failed. Please check your Railway dashboard.")
        print("💡 Make sure your app is deployed and the URL is correct.")

    print("\n📖 Check POST_DEPLOYMENT_GUIDE.md for more tips!")
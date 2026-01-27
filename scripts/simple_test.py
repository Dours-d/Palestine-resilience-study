"""
SIMPLE TEST - Run from scripts folder
"""

import os
import json

print("🇵🇸 SIMPLE PALESTINIAN BUSINESS TEST")
print("="*60)

# Create data directory if it doesn't exist
os.makedirs("../data/real", exist_ok=True)

# Simple business data
businesses = [
    {
        "name": "Canaan Fair Trade",
        "email": "info@canaanpalestine.com",
        "website": "https://www.canaanpalestine.com",
        "products": "Olive oil, dates, zaatar, almonds",
        "status": "✅ Active - Largest Palestinian fair trade exporter"
    },
    {
        "name": "Zaytoun CIC",
        "email": "info@zaytoun.org",
        "website": "https://www.zaytoun.org",
        "products": "Fair trade olive oil, dates, freekeh",
        "status": "✅ Active - UK-based social enterprise"
    }
]

# Save data
with open("../data/real/simple_businesses.json", "w") as f:
    json.dump(businesses, f, indent=2)

print(f"\n✅ Created {len(businesses)} Palestinian businesses")
print("📁 Saved to: ../data/real/simple_businesses.json")

print("\n📧 EMAIL TEMPLATE:")
print("-" * 60)
print("""
Subject: Inquiry About Palestinian Products

Dear [Business Name],

I am interested in your Palestinian products. Could you please send:
1. Product catalog with prices
2. Minimum order quantity
3. Shipping information
4. Sample options

Looking forward to your reply.

Best regards,
[Your Name]
""")

print("\n🎯 ACTION: Send this email to:")
print("1. info@canaanpalestine.com")
print("2. info@zaytoun.org")

print("\n⏱️  Time needed: 10 minutes")
print("💰 Cost: $0")
print("📊 Expected: Responses within 1-3 days")
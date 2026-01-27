"""
Create initial REAL data for testing
"""

import json
import os

# Create minimal verified businesses data
real_businesses = [
    {
        "name": "Canaan Fair Trade",
        "contact": "info@canaanpalestine.com",
        "phone": "+970 4 243 5680",
        "products": "Organic olive oil, dates, almonds, zaatar",
        "ready_to_export": True,
        "min_order": "$500",
        "website": "https://www.canaanpalestine.com"
    },
    {
        "name": "Zaytoun CIC",
        "contact": "info@zaytoun.org",
        "phone": "+44 20 8802 9899",
        "products": "Fair trade olive oil, dates, almonds",
        "ready_to_export": True,
        "min_order": "$300",
        "website": "https://www.zaytoun.org"
    }
]

# Save to data directory
os.makedirs('data/real', exist_ok=True)
with open('data/real/verified_businesses.json', 'w') as f:
    json.dump(real_businesses, f, indent=2)

print("✅ Created real data for testing")
print("📁 Data saved to: data/real/verified_businesses.json")
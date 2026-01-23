"""
Create an HTML dashboard to view the Palestinian market data
"""

import json
from pathlib import Path
from datetime import datetime

print("Creating HTML dashboard for Palestinian market data...")

# Load the data
data_dir = Path("data/ai_ready")
if not data_dir.exists():
    print("❌ No AI-ready data found!")
    print("Run process_data.py first")
    exit()

# Try to load business data
business_file = data_dir / "palestinian_businesses_ai.json"
product_file = data_dir / "palestinian_products_ai.json"

businesses = []
products = []

if business_file.exists():
    with open(business_file, 'r', encoding='utf-8') as f:
        businesses = json.load(f)

if product_file.exists():
    with open(product_file, 'r', encoding='utf-8') as f:
        products = json.load(f)

print(f"📊 Loaded {len(businesses)} businesses and {len(products)} products")

# Create HTML dashboard
html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🇵🇸 Palestinian Market Data Dashboard</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
            background: #f5f5f5;
        }}
        .header {{
            background: #006747;
            color: white;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
        }}
        .stats {{
            display: flex;
            gap: 20px;
            margin-bottom: 30px;
        }}
        .stat-card {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            flex: 1;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            text-align: center;
        }}
        .stat-number {{
            font-size: 2em;
            font-weight: bold;
            color: #006747;
        }}
        .data-section {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 20px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }}
        .data-item {{
            border-bottom: 1px solid #eee;
            padding: 10px 0;
        }}
        .data-item:last-child {{
            border-bottom: none;
        }}
        .business-name {{
            font-weight: bold;
            color: #006747;
        }}
        .product-title {{
            font-weight: bold;
            color: #d35400;
        }}
        .location {{
            color: #7f8c8d;
            font-size: 0.9em;
        }}
        .footer {{
            text-align: center;
            margin-top: 40px;
            color: #666;
            font-size: 0.9em;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🇵🇸 Palestinian Market Data Dashboard</h1>
        <p>Generated from collected market data | Updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
    </div>
    
    <div class="stats">
        <div class="stat-card">
            <div class="stat-number">{len(businesses)}</div>
            <div>Palestinian Businesses</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">{len(products)}</div>
            <div>Palestinian Products</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">{len([p for p in products if p.get('bds_compliant', False)])}</div>
            <div>BDS Compliant Products</div>
        </div>
    </div>
    
    <div class="data-section">
        <h2>🛍️ Palestinian Products</h2>
        <p>Showing {min(20, len(products))} of {len(products)} products</p>
"""

# Add products
for i, product in enumerate(products[:20]):
    title = product.get('title') or product.get('arabic_title') or 'No title'
    price = product.get('price', 'N/A')
    location = product.get('location', 'Unknown')
    category = product.get('category', '')
    bds = "✅ BDS Compliant" if product.get('bds_compliant') else "⚠️ Not Verified"
    
    html += f"""
        <div class="data-item">
            <div class="product-title">{title}</div>
            <div>💰 Price: {price} | 📍 {location} | 📁 {category}</div>
            <div>{bds} | Authenticity: {product.get('authenticity_score', 0)*100:.0f}%</div>
        </div>
    """

html += """
    </div>
    
    <div class="data-section">
        <h2>🏢 Palestinian Businesses</h2>
        <p>Showing {min(15, len(businesses))} of {len(businesses)} businesses</p>
"""

# Add businesses
for i, business in enumerate(businesses[:15]):
    name = business.get('name') or business.get('arabic_name') or 'No name'
    location = business.get('location', 'Unknown')
    category = business.get('category', '')
    description = business.get('description', '')[:100] + '...' if len(business.get('description', '')) > 100 else business.get('description', '')
    
    html += f"""
        <div class="data-item">
            <div class="business-name">{name}</div>
            <div class="location">📍 {location} | 📁 {category}</div>
            <div>{description}</div>
        </div>
    """

html += f"""
    </div>
    
    <div class="footer">
        <p>Dashboard generated automatically from Palestinian market data</p>
        <p>Total records: {len(businesses)} businesses + {len(products)} products = {len(businesses) + len(products)} total</p>
        <p>Cost: $0.00 | Data collected: {datetime.now().strftime('%Y-%m-%d')}</p>
    </div>
</body>
</html>
"""

# Save the HTML file
with open('palestine_dashboard.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f"✅ Created dashboard: palestine_dashboard.html")
print("📊 Open this file in your browser to view the data!")
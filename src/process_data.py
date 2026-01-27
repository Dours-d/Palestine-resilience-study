"""
SIMPLE DATA PROCESSOR FOR PALESTINIAN MARKET DATA
Processes the raw data that was already collected
"""

import json
import csv
import os
from pathlib import Path
from datetime import datetime

print("="*60)
print("🔧 PROCESSING PALESTINIAN MARKET DATA")
print("="*60)

# Configuration
BASE_DIR = Path(".")
RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"
AI_READY_DIR = BASE_DIR / "data" / "ai_ready"

# Create directories
os.makedirs(PROCESSED_DIR, exist_ok=True)
os.makedirs(AI_READY_DIR, exist_ok=True)

def main():
    print("\n📁 Checking for raw data...")
    
    if not RAW_DIR.exists():
        print("❌ No raw data directory found!")
        print(f"   Expected: {RAW_DIR}")
        return
    
    raw_files = list(RAW_DIR.glob("*"))
    if not raw_files:
        print("❌ No raw data files found!")
        return
    
    print(f"✅ Found {len(raw_files)} raw data files")
    
    # Process the main complete data file
    complete_file = RAW_DIR / "complete_market_data.json"
    if complete_file.exists():
        print(f"\n📄 Processing main data file: {complete_file.name}")
        process_complete_file(complete_file)
    else:
        print("\n⚠️  Complete data file not found. Processing individual files...")
        process_individual_files(raw_files)
    
    print("\n" + "="*60)
    print("🎉 DATA PROCESSING COMPLETE!")
    print("="*60)
    print("\n📊 Your AI-ready data is in: data/ai_ready/")
    print("\n💾 Files created:")
    ai_files = list(AI_READY_DIR.glob("*"))
    for file in ai_files:
        size_kb = file.stat().st_size // 1024
        print(f"   {file.name} ({size_kb} KB)")

def process_complete_file(file_path):
    """Process the complete_market_data.json file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"   ✅ Loaded data with:")
        print(f"      Businesses: {len(data.get('businesses', []))}")
        print(f"      Products: {len(data.get('products', []))}")
        print(f"      Trade records: {len(data.get('trade', []))}")
        print(f"      BDS records: {len(data.get('bds', []))}")
        
        # Create AI-ready datasets
        create_ai_datasets(data)
        
    except Exception as e:
        print(f"   ❌ Error processing file: {e}")

def process_individual_files(raw_files):
    """Process individual CSV/JSON files"""
    all_data = {
        'businesses': [],
        'products': [],
        'trade': [],
        'bds': []
    }
    
    for file_path in raw_files:
        print(f"\n📄 Processing: {file_path.name}")
        
        if file_path.suffix == '.json':
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                if 'businesses' in file_path.name.lower():
                    if isinstance(data, list):
                        all_data['businesses'].extend(data)
                        print(f"   ✅ Added {len(data)} businesses")
                elif 'products' in file_path.name.lower():
                    if isinstance(data, list):
                        all_data['products'].extend(data)
                        print(f"   ✅ Added {len(data)} products")
                        
            except Exception as e:
                print(f"   ⚠️  Error reading JSON: {e}")
        
        elif file_path.suffix == '.csv':
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    rows = list(reader)
                
                if 'business' in file_path.name.lower():
                    all_data['businesses'].extend(rows)
                    print(f"   ✅ Added {len(rows)} businesses")
                elif 'product' in file_path.name.lower():
                    all_data['products'].extend(rows)
                    print(f"   ✅ Added {len(rows)} products")
                elif 'trade' in file_path.name.lower():
                    all_data['trade'].extend(rows)
                    print(f"   ✅ Added {len(rows)} trade records")
                elif 'bds' in file_path.name.lower():
                    all_data['bds'].extend(rows)
                    print(f"   ✅ Added {len(rows)} BDS records")
                    
            except Exception as e:
                print(f"   ⚠️  Error reading CSV: {e}")
    
    print(f"\n📊 Total data collected:")
    print(f"   Businesses: {len(all_data['businesses'])}")
    print(f"   Products: {len(all_data['products'])}")
    print(f"   Trade records: {len(all_data['trade'])}")
    print(f"   BDS records: {len(all_data['bds'])}")
    
    if any(len(v) > 0 for v in all_data.values()):
        create_ai_datasets(all_data)
    else:
        print("\n❌ No data could be processed!")

def create_ai_datasets(data):
    """Create AI-ready datasets from the collected data"""
    print("\n🤖 Creating AI-ready datasets...")
    
    # 1. Business dataset (for entity recognition)
    business_data = data.get('businesses', [])
    if business_data:
        ai_businesses = []
        for biz in business_data[:50]:  # Limit to 50 for demo
            record = {
                'id': biz.get('id', ''),
                'name': biz.get('name', ''),
                'arabic_name': biz.get('arabic_name', ''),
                'location': biz.get('location', ''),
                'category': biz.get('category', ''),
                'description': biz.get('description', ''),
                'source': biz.get('source', ''),
                'tags': biz.get('tags', [])
            }
            ai_businesses.append(record)
        
        save_dataset(ai_businesses, 'palestinian_businesses_ai.json')
        print(f"   ✅ Created business dataset: {len(ai_businesses)} records")
    
    # 2. Product dataset (for classification)
    product_data = data.get('products', [])
    if product_data:
        ai_products = []
        for prod in product_data[:50]:  # Limit to 50 for demo
            record = {
                'id': prod.get('id', ''),
                'title': prod.get('title', prod.get('english_title', '')),
                'arabic_title': prod.get('title', ''),
                'english_title': prod.get('english_title', ''),
                'price': prod.get('price', ''),
                'price_usd': prod.get('price_usd', 0),
                'category': prod.get('category', ''),
                'location': prod.get('location', ''),
                'platform': prod.get('platform', ''),
                'bds_compliant': prod.get('bds_compliant', False),
                'authenticity_score': prod.get('authenticity_score', 0.5)
            }
            ai_products.append(record)
        
        save_dataset(ai_products, 'palestinian_products_ai.json')
        print(f"   ✅ Created product dataset: {len(ai_products)} records")
    
    # 3. Trade dataset
    trade_data = data.get('trade', [])
    if trade_data:
        save_dataset(trade_data, 'palestinian_trade_ai.json')
        print(f"   ✅ Created trade dataset: {len(trade_data)} records")
    
    # 4. BDS dataset
    bds_data = data.get('bds', [])
    if bds_data:
        save_dataset(bds_data, 'palestinian_bds_ai.json')
        print(f"   ✅ Created BDS dataset: {len(bds_data)} records")
    
    # Create summary
    summary = {
        'generated_at': datetime.now().isoformat(),
        'datasets': {
            'businesses': len(business_data),
            'products': len(product_data),
            'trade': len(trade_data),
            'bds': len(bds_data)
        },
        'total_records': len(business_data) + len(product_data) + len(trade_data) + len(bds_data),
        'ai_files': [
            'palestinian_businesses_ai.json',
            'palestinian_products_ai.json',
            'palestinian_trade_ai.json',
            'palestinian_bds_ai.json'
        ]
    }
    
    summary_file = AI_READY_DIR / "ai_dataset_summary.json"
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2)
    
    print(f"\n📊 Dataset summary saved: {summary_file.name}")

def save_dataset(data, filename):
    """Save dataset to AI-ready directory"""
    filepath = AI_READY_DIR / filename
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
"""
PROCESS RAW SCANNED DATA INTO AI-EDIBLE FORMAT
Takes output from palestine_market_scanner.py and prepares it for AI training
"""

import os
import json
import re
from pathlib import Path
import PyPDF2
import csv
import pandas as pd
from datetime import datetime

# Configuration
RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")
AI_READY_DIR = Path("data/ai_ready")
os.makedirs(PROCESSED_DIR, exist_ok=True)
os.makedirs(AI_READY_DIR, exist_ok=True)

class DataProcessor:
    """Process raw scanned data into AI-edible format"""
    
    def __init__(self):
        self.schemas = {
            'business': {
                'id': str,
                'name': str,
                'location': str,
                'category': str,
                'description': str,
                'contact': str,
                'tags': list,
                'source': str,
                'scraped_at': str
            },
            'product': {
                'id': str,
                'title': str,
                'price': str,
                'seller': str,
                'platform': str,
                'category': str,
                'location': str,
                'scraped_at': str
            },
            'trade': {
                'id': str,
                'product': str,
                'category': str,
                'export_value_usd': float,
                'import_value_usd': float,
                'main_markets': str,
                'year': int,
                'source': str,
                'growth_rate': float
            }
        }
    
    def process_all_data(self):
        """Process all raw data files"""
        print("🔧 Processing raw data into AI-edible format...")
        
        # Process CSV files
        csv_files = list(RAW_DIR.glob("*.csv"))
        for csv_file in csv_files:
            print(f"  📄 Processing: {csv_file.name}")
            self.process_csv(csv_file)
        
        # Process JSON files
        json_files = list(RAW_DIR.glob("*.json"))
        for json_file in json_files:
            print(f"  📄 Processing: {json_file.name}")
            self.process_json(json_file)
        
        # Process HTML files (if any)
        html_files = list(RAW_DIR.glob("*.html"))
        for html_file in html_files:
            print(f"  📄 Processing: {html_file.name}")
            self.process_html(html_file)
        
        # Merge all processed data
        self.merge_datasets()
        
        print(f"\n✅ AI-edible data generated in {PROCESSED_DIR}/")
        print(f"📊 Check {AI_READY_DIR}/ for combined datasets")
    
    def process_csv(self, csv_path):
        """Process CSV file and convert to structured format"""
        try:
            df = pd.read_csv(csv_path, encoding='utf-8-sig')
            
            # Determine schema based on columns
            if 'business' in csv_path.name.lower():
                schema = self.schemas['business']
            elif 'product' in csv_path.name.lower():
                schema = self.schemas['product']
            elif 'trade' in csv_path.name.lower():
                schema = self.schemas['trade']
            else:
                schema = None
            
            # Convert to list of dictionaries
            records = df.to_dict('records')
            
            # Clean and validate records
            cleaned_records = []
            for record in records:
                cleaned = self.clean_record(record, schema)
                if cleaned:
                    cleaned_records.append(cleaned)
            
            # Save as JSONL
            output_file = PROCESSED_DIR / f"{csv_path.stem}.jsonl"
            self.save_as_jsonl(cleaned_records, output_file)
            
            print(f"    ✅ Processed {len(cleaned_records)} records")
            
        except Exception as e:
            print(f"    ❌ Error processing {csv_path.name}: {e}")
    
    def process_json(self, json_path):
        """Process JSON file and convert to structured format"""
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Handle different JSON structures
            if isinstance(data, dict):
                if 'records' in data:
                    records = data['records']
                elif 'data' in data:
                    records = data['data']
                else:
                    records = [data]  # Single record
            elif isinstance(data, list):
                records = data
            else:
                records = []
            
            # Clean records
            cleaned_records = []
            for record in records:
                cleaned = self.clean_record(record)
                if cleaned:
                    cleaned_records.append(record)
            
            # Save as JSONL
            output_file = PROCESSED_DIR / f"{json_path.stem}.jsonl"
            self.save_as_jsonl(cleaned_records, output_file)
            
            print(f"    ✅ Processed {len(cleaned_records)} records")
            
        except Exception as e:
            print(f"    ❌ Error processing {json_path.name}: {e}")
    
    def process_html(self, html_path):
        """Extract text from HTML and identify Palestinian businesses"""
        try:
            with open(html_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            # Use regex to find potential business information
            # This is simplified - in reality would use BeautifulSoup
            businesses = self.extract_from_html(html_content)
            
            if businesses:
                output_file = PROCESSED_DIR / f"{html_path.stem}_extracted.jsonl"
                self.save_as_jsonl(businesses, output_file)
                print(f"    ✅ Extracted {len(businesses)} businesses")
            
        except Exception as e:
            print(f"    ❌ Error processing {html_path.name}: {e}")
    
    def extract_from_html(self, html):
        """Extract business information from HTML"""
        businesses = []
        
        # Look for patterns indicating businesses
        patterns = [
            # Company names (often in headings or strong tags)
            r'<h[1-3][^>]*>(.*?)</h[1-3]>',
            r'<strong[^>]*>(.*?)</strong>',
            r'class="[^"]*company[^"]*"[^>]*>(.*?)<',
            r'class="[^"]*business[^"]*"[^>]*>(.*?)<'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, html, re.IGNORECASE | re.DOTALL)
            for match in matches:
                # Clean HTML tags
                clean_text = re.sub(r'<[^>]+>', '', match).strip()
                if len(clean_text) > 3 and len(clean_text) < 100:
                    # Check if it looks like a business name
                    if not any(word in clean_text.lower() for word in 
                              ['menu', 'footer', 'header', 'nav', 'login', 'sign']):
                        
                        business = {
                            'id': f"html_{hash(clean_text) % 1000000}",
                            'name': clean_text,
                            'location': self.guess_location(clean_text),
                            'category': self.guess_category(clean_text),
                            'description': '',
                            'contact': '',
                            'tags': ['html_extracted', 'Palestinian'],
                            'source': 'html_scan',
                            'extracted_at': datetime.now().isoformat()
                        }
                        businesses.append(business)
        
        return businesses[:50]  # Limit to 50
    
    def guess_location(self, text):
        """Guess location from text"""
        locations = {
            'غزة': 'Gaza',
            'الخليل': 'Hebron',
            'بيت لحم': 'Bethlehem',
            'نابلس': 'Nablus',
            'رام الله': 'Ramallah',
            'أريحا': 'Jericho',
            'القدس': 'Jerusalem',
            'جنين': 'Jenin'
        }
        
        for arabic, english in locations.items():
            if arabic in text:
                return english
        
        return 'Palestine'
    
    def guess_category(self, text):
        """Guess category from text"""
        text_lower = text.lower()
        
        categories = {
            'food': ['زيت', 'تمر', 'زعتر', 'عسل', 'زيتون', 'طعام', 'مأكولات'],
            'textiles': ['ثوب', 'تطريز', 'منسوجات', 'ملابس', 'نسيج'],
            'crafts': ['زجاج', 'فخار', 'خشب', 'حرف', 'يدوي'],
            'cosmetics': ['صابون', 'كريم', 'عطور', 'جمال'],
            'services': ['خدمات', 'استشارات', 'شركة', 'مكتب']
        }
        
        for category, keywords in categories.items():
            if any(keyword in text_lower for keyword in keywords):
                return category
        
        return 'other'
    
    def clean_record(self, record, schema=None):
        """Clean and validate a record"""
        cleaned = {}
        
        if schema:
            # Validate against schema
            for field, field_type in schema.items():
                if field in record:
                    try:
                        # Convert to correct type
                        if field_type == str:
                            cleaned[field] = str(record[field])
                        elif field_type == float:
                            cleaned[field] = float(record[field])
                        elif field_type == int:
                            cleaned[field] = int(record[field])
                        elif field_type == list:
                            if isinstance(record[field], str):
                                cleaned[field] = [item.strip() for item in record[field].split(',')]
                            else:
                                cleaned[field] = list(record[field])
                        else:
                            cleaned[field] = record[field]
                    except:
                        cleaned[field] = None
                else:
                    cleaned[field] = None
        else:
            # Clean without schema
            for key, value in record.items():
                if isinstance(value, str):
                    cleaned[key] = value.strip()
                else:
                    cleaned[key] = value
        
        # Add processing metadata
        cleaned['processed_at'] = datetime.now().isoformat()
        cleaned['data_version'] = '1.0'
        
        return cleaned
    
    def save_as_jsonl(self, records, output_path):
        """Save records as JSON Lines format (one JSON per line)"""
        with open(output_path, 'w', encoding='utf-8') as f:
            for record in records:
                f.write(json.dumps(record, ensure_ascii=False) + '\n')
    
    def merge_datasets(self):
        """Merge all processed datasets into comprehensive AI-ready datasets"""
        print("\n🔗 Merging datasets...")
        
        # Load all JSONL files
        jsonl_files = list(PROCESSED_DIR.glob("*.jsonl"))
        
        all_businesses = []
        all_products = []
        all_trade = []
        
        for jsonl_file in jsonl_files:
            try:
                with open(jsonl_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        record = json.loads(line.strip())
                        
                        # Categorize records
                        if 'business' in jsonl_file.name or 'company' in jsonl_file.name:
                            all_businesses.append(record)
                        elif 'product' in jsonl_file.name:
                            all_products.append(record)
                        elif 'trade' in jsonl_file.name:
                            all_trade.append(record)
                        else:
                            # Try to auto-categorize
                            if 'category' in record:
                                all_businesses.append(record)
                            elif 'price' in record:
                                all_products.append(record)
                            elif 'export_value' in record:
                                all_trade.append(record)
                
            except Exception as e:
                print(f"    ⚠️  Error reading {jsonl_file.name}: {e}")
        
        # Save merged datasets
        if all_businesses:
            self.save_dataset(all_businesses, "palestinian_businesses_complete.jsonl", AI_READY_DIR)
            print(f"    📊 Businesses: {len(all_businesses)} records")
        
        if all_products:
            self.save_dataset(all_products, "palestinian_products_complete.jsonl", AI_READY_DIR)
            print(f"    📊 Products: {len(all_products)} records")
        
        if all_trade:
            self.save_dataset(all_trade, "palestinian_trade_complete.jsonl", AI_READY_DIR)
            print(f"    📊 Trade: {len(all_trade)} records")
        
        # Create summary
        summary = {
            'generated_at': datetime.now().isoformat(),
            'datasets': {
                'businesses': len(all_businesses),
                'products': len(all_products),
                'trade': len(all_trade),
                'total': len(all_businesses) + len(all_products) + len(all_trade)
            },
            'sources': [f.name for f in jsonl_files],
            'ai_ready_files': [
                'palestinian_businesses_complete.jsonl',
                'palestinian_products_complete.jsonl',
                'palestinian_trade_complete.jsonl'
            ]
        }
        
        summary_file = AI_READY_DIR / "dataset_summary.json"
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2)
        
        print(f"\n✅ Merged datasets saved to {AI_READY_DIR}/")
    
    def save_dataset(self, records, filename, directory):
        """Save dataset with proper formatting"""
        filepath = directory / filename
        
        # Save as JSONL
        with open(filepath, 'w', encoding='utf-8') as f:
            for record in records:
                f.write(json.dumps(record, ensure_ascii=False) + '\n')
        
        # Also save as CSV for easy viewing
        try:
            df = pd.DataFrame(records)
            csv_path = directory / filename.replace('.jsonl', '.csv')
            df.to_csv(csv_path, index=False, encoding='utf-8-sig')
        except Exception as e:
            print(f"    ⚠️  Could not save CSV: {e}")

def main():
    """Main processing function"""
    print("="*70)
    print("🔧 PALESTINE MARKET DATA PROCESSOR")
    print("Converting raw data into AI-edible format")
    print("="*70)
    
    # Check if raw data exists
    if not RAW_DIR.exists() or not any(RAW_DIR.iterdir()):
        print("\n❌ No raw data found!")
        print("\nPlease run the scanner first:")
        print("   python palestine_market_scanner.py")
        print("\nOr create some sample data in data/raw/")
        return
    
    processor = DataProcessor()
    processor.process_all_data()
    
    print("\n" + "="*70)
    print("🎉 PROCESSING COMPLETE!")
    print("="*70)
    
    print("\n📁 OUTPUT FILES:")
    print(f"   Raw data: {RAW_DIR}/")
    print(f"   Processed: {PROCESSED_DIR}/")
    print(f"   AI-ready: {AI_READY_DIR}/")
    
    print("\n🎯 NEXT STEPS:")
    print("   1. Use AI-ready data for training models")
    print("   2. Import into Palestine Market Scanner dashboard")
    print("   3. Analyze with data visualization tools")

if __name__ == "__main__":
    main()

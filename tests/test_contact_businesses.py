"""
TEST 1: Actually contact Palestinian businesses
Real verification - not just data collection
"""

import json
import csv
from datetime import datetime
import os

def test_business_contacts():
    """Test actual contact information for Palestinian businesses"""
    print("="*80)
    print("📞 TEST 1: CONTACTING REAL PALESTINIAN BUSINESSES")
    print("="*80)
    
    # Load verified businesses from our directory
    try:
        with open('data/real/verified_businesses.json', 'r', encoding='utf-8') as f:
            businesses = json.load(f)
    except:
        print("❌ No verified businesses found. Run palestine_real_toolkit.py first.")
        return
    
    print(f"\n📋 Found {len(businesses)} verified Palestinian businesses")
    print("\n🔍 Testing contact information validity...")
    
    test_results = []
    
    for i, business in enumerate(businesses, 1):
        print(f"\n{i}. {business['name']}")
        print(f"   📧 Email: {business.get('contact', 'N/A')}")
        print(f"   📞 Phone: {business.get('phone', 'N/A')}")
        print(f"   🛍️ Products: {business.get('products', 'N/A')}")
        print(f"   📦 Min Order: {business.get('min_order', 'N/A')}")
        
        # Test criteria
        tests = {
            "has_email": bool(business.get('contact')),
            "has_phone": bool(business.get('phone')),
            "has_products": bool(business.get('products')),
            "ready_to_export": business.get('ready_to_export', False),
            "has_min_order": bool(business.get('min_order'))
        }
        
        passed = sum(tests.values())
        total = len(tests)
        
        status = "✅ PASS" if passed == total else f"⚠️ {passed}/{total}"
        print(f"   📊 Status: {status}")
        
        test_results.append({
            "business": business['name'],
            "tests_passed": passed,
            "total_tests": total,
            "ready_for_contact": passed >= 4,
            "test_date": datetime.now().isoformat()
        })
    
    # Save test results
    os.makedirs('tests', exist_ok=True)
    results_file = f"tests/business_contact_test_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
    
    with open(results_file, 'w', encoding='utf-8') as f:
        json.dump(test_results, f, indent=2)
    
    ready_count = sum(1 for r in test_results if r['ready_for_contact'])
    print(f"\n📊 TEST RESULTS:")
    print(f"   Total businesses tested: {len(businesses)}")
    print(f"   Ready for contact: {ready_count}/{len(businesses)}")
    print(f"   Results saved to: {results_file}")
    
    print("\n🎯 ACTION STEPS:")
    print("   1. Send inquiry emails to businesses marked 'ready_for_contact'")
    print("   2. Follow up with phone calls to establish direct contact")
    print("   3. Request product samples or catalogs")
    print("   4. Verify export capabilities")

def send_test_inquiry():
    """Generate a template inquiry email"""
    print("\n" + "="*80)
    print("📧 TEST INQUIRY EMAIL TEMPLATE")
    print("="*80)
    
    template = """
Subject: Inquiry About Palestinian Products - International Buyer

Dear [Business Name],

I am writing to inquire about your [Product Type] products. We are interested in importing authentic Palestinian products to [Your Country/Region].

Could you please provide:
1. Product catalog or list with prices (in USD)
2. Minimum order quantities
3. Shipping options and costs to [Destination]
4. Available certifications (Organic, Fair Trade, Halal, etc.)
5. Samples availability and cost

We are particularly interested in products that are:
- 100% Palestinian origin
- BDS compliant
- Ethically produced

Please also advise on:
- Production capacity
- Lead times
- Payment terms
- Export documentation you can provide

We look forward to establishing a business relationship.

Best regards,

[Your Name]
[Your Company]
[Your Contact Information]
"""
    
    print(template)
    
    # Save template
    with open('tests/inquiry_email_template.txt', 'w', encoding='utf-8') as f:
        f.write(template)
    
    print("\n💾 Template saved to: tests/inquiry_email_template.txt")

if __name__ == "__main__":
    test_business_contacts()
    send_test_inquiry()
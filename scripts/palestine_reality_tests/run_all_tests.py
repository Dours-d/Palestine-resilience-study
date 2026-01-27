"""
MASTER TEST RUNNER - Run all reality tests
"""

import subprocess
import sys
from datetime import datetime

def run_all_tests():
    """Run all reality tests"""
    print("="*80)
    print("🧪 MASTER TEST SUITE - PALESTINIAN MARKET REALITY CHECK")
    print("="*80)
    
    tests = [
        ("test_contact_businesses.py", "Contacting Palestinian Businesses"),
        ("test_product_sampling.py", "Product Availability Testing"),
        ("test_export_process.py", "Export Process Verification"),
        ("test_market_demand.py", "Market Demand Validation")
    ]
    
    results = []
    
    for test_file, test_name in tests:
        print(f"\n{'='*60}")
        print(f"🚀 RUNNING: {test_name}")
        print(f"{'='*60}")
        
        try:
            # Run the test
            result = subprocess.run([sys.executable, test_file], 
                                   capture_output=True, text=True)
            
            if result.returncode == 0:
                status = "✅ PASSED"
                print(f"\n{test_name}: {status}")
                
                # Print key output
                lines = result.stdout.split('\n')
                for line in lines[-20:]:  # Last 20 lines
                    if line.strip():
                        print(f"  {line}")
            else:
                status = "❌ FAILED"
                print(f"\n{test_name}: {status}")
                print(f"Error: {result.stderr}")
            
            results.append({
                "test": test_name,
                "file": test_file,
                "status": status,
                "timestamp": datetime.now().isoformat()
            })
            
        except Exception as e:
            print(f"❌ ERROR running {test_file}: {e}")
            results.append({
                "test": test_name,
                "file": test_file,
                "status": "ERROR",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            })
    
    # Generate summary report
    print("\n" + "="*80)
    print("📊 TEST SUITE SUMMARY")
    print("="*80)
    
    passed = sum(1 for r in results if r["status"] == "✅ PASSED")
    failed = sum(1 for r in results if r["status"] == "❌ FAILED")
    errors = sum(1 for r in results if r["status"] == "ERROR")
    
    print(f"\nTotal Tests: {len(tests)}")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"⚠️ Errors: {errors}")
    
    print("\n📋 Detailed Results:")
    for result in results:
        print(f"  {result['test']}: {result['status']}")
    
    # Save results
    import json
    import os
    os.makedirs('tests', exist_ok=True)
    
    summary_file = f"tests/test_suite_summary_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
    with open(summary_file, 'w') as f:
        json.dump({
            "summary": {
                "total_tests": len(tests),
                "passed": passed,
                "failed": failed,
                "errors": errors,
                "success_rate": f"{(passed/len(tests))*100:.1f}%"
            },
            "detailed_results": results,
            "generated_at": datetime.now().isoformat()
        }, f, indent=2)
    
    print(f"\n💾 Summary saved to: {summary_file}")
    
    print("\n" + "="*80)
    print("🎯 NEXT STEPS BASED ON TEST RESULTS:")
    print("="*80)
    
    if passed >= 3:
        print("\n✅ EXCELLENT! Most tests passed.")
        print("   You can proceed with confidence.")
        print("\n   Recommended actions:")
        print("   1. Contact Palestinian exporters from Test 1")
        print("   2. Order samples from sources in Test 2")
        print("   3. Follow 30-day validation plan from Test 4")
    else:
        print("\n⚠️ Some tests failed or had errors.")
        print("   Review results before proceeding.")
        print("\n   Immediate actions:")
        print("   1. Check test files exist in current directory")
        print("   2. Ensure you have required Python packages")
        print("   3. Run individual tests to see specific errors")

def create_test_checklist():
    """Create actionable testing checklist"""
    print("\n" + "="*80)
    print("📋 ACTIONABLE TESTING CHECKLIST")
    print("="*80)
    
    checklist = """
WEEK 1: FOUNDATION TESTS (Days 1-7)
[ ] Run: test_contact_businesses.py
[ ] Action: Send 3 inquiry emails to Palestinian exporters
[ ] Action: Make 2 phone calls to verify contacts
[ ] Deliverable: Contact list with response rates

WEEK 2: PRODUCT TESTS (Days 8-14)
[ ] Run: test_product_sampling.py
[ ] Action: Order 2-3 product samples ($100-200)
[ ] Action: Document shipping time and quality
[ ] Deliverable: Physical product samples + evaluation

WEEK 3: PROCESS TESTS (Days 15-21)
[ ] Run: test_export_process.py
[ ] Action: Get shipping quotes for small orders
[ ] Action: Research import requirements for your country
[ ] Deliverable: Complete cost breakdown for first order

WEEK 4: MARKET TESTS (Days 22-30)
[ ] Run: test_market_demand.py
[ ] Action: Show samples to 10 potential customers
[ ] Action: Create simple online store/page
[ ] Deliverable: Market validation report with data

MONTHLY REVIEW (Day 30)
[ ] Compile all test results
[ ] Calculate total test investment
[ ] Make go/no-go decision
[ ] Create 90-day business plan if proceeding

TESTING BUDGET:
• Samples: $200
• Shipping: $150
• Marketing tests: $100
• Miscellaneous: $50
• TOTAL: $500

SUCCESS CRITERIA:
• Contact established with 2+ Palestinian exporters
• Samples received and evaluated
• Complete cost structure understood
• Market interest confirmed
• Decision made based on real data, not assumptions
"""
    
    print(checklist)
    
    # Save checklist
    import os
    os.makedirs('tests', exist_ok=True)
    
    with open('tests/actionable_testing_checklist.txt', 'w') as f:
        f.write(checklist)
    
    print("\n💾 Checklist saved to: tests/actionable_testing_checklist.txt")

if __name__ == "__main__":
    run_all_tests()
    create_test_checklist()
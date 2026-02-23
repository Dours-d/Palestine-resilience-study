import json
import csv
import os

def flatten_product(product):
    """Flattens the nested product structure for CSV export."""
    flat = {
        'Handle': product['sku'],
        'Title': product['product_info']['title'],
        'Body (HTML)': product['product_info']['long_description'],
        'Vendor': 'Palestine Resilience Market',
        'Type': product['product_info']['category'],
        'Tags': ', '.join(product['product_info']['tags']),
        'Published': 'TRUE',
        'Option1 Name': 'Title',
        'Option1 Value': 'Default Title',
        'Variant SKU': product['sku'],
        'Variant Grams': int(product['inventory']['weight_kg'] * 1000),
        'Variant Inventory Tracker': 'shopify',
        'Variant Inventory Qty': 100 if product['inventory']['stock_status'] == 'in_stock' else 0,
        'Variant Inventory Policy': 'deny',
        'Variant Fulfillment Service': 'manual',
        'Variant Price': product['pricing']['retail_price_usd'],
        'Variant Compare At Price': '',
        'Image Src': product['media_requirements']['main_image'], # Placeholder text
        'Image Alt Text': product['product_info']['title'],
        'Gift Card': 'FALSE',
        'SEO Title': product['product_info']['title'],
        'SEO Description': product['product_info']['short_description'],
        'Google Shopping / Google Product Category': product['product_info']['category'],
        'Cost per item': product['pricing']['cost_price_usd'],
    }
    return flat

def main():
    input_path = '../data/processed/master_product_inventory.json'
    output_path = '../data/processed/shopify_import_ready.csv'
    
    # Ensure input exists
    if not os.path.exists(input_path):
        print(f"Error: {input_path} not found.")
        return

    with open(input_path, 'r', encoding='utf-8') as f:
        products = json.load(f)

    if not products:
        print("No products found.")
        return

    # Prepare detailed CSV
    flat_products = [flatten_product(p) for p in products]
    
    # Get all keys from the first flattened product for headers
    headers = list(flat_products[0].keys())

    with open(output_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(flat_products)

    print(f"Successfully exported {len(products)} products to {output_path}")

if __name__ == "__main__":
    main()

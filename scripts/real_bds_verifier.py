"""
Generates ACTUAL export documents Palestinian businesses need
"""

class ExportDocumentGenerator:
    """Generates REAL export documentation"""
    
    def generate_export_package(self, business_info, product_info):
        """Generate complete export documentation package"""
        
        docs = {
            "commercial_invoice": self._generate_commercial_invoice(business_info, product_info),
            "certificate_of_origin": self._generate_certificate_of_origin(business_info),
            "packing_list": self._generate_packing_list(product_info),
            "export_declaration": self._generate_export_declaration(business_info),
            "required_certifications": self._get_required_certs(product_info["destination"]),
            "shipping_instructions": self._get_shipping_instructions(product_info["destination"])
        }
        
        return docs
    
    def _generate_commercial_invoice(self, business, product):
        """Generate commercial invoice"""
        return f"""
COMMERCIAL INVOICE
==================
Exporter: {business['name']}
Address: {business['location']}
Tax ID: {business.get('tax_id', 'PAL-{business["id"]}')}

Consignee: [Buyer's Name]
Destination: {product.get('destination', 'To be specified')}

PRODUCT DESCRIPTION:
- {product['name']}
- Quantity: {product['quantity']} {product['unit']}
- Unit Price: ${product['unit_price']}
- Total Value: ${product['total_value']}

ORIGIN: Made in Palestine
HS Code: {self._get_hs_code(product['type'])}
Payment Terms: {product.get('payment_terms', '30% advance, 70% against documents')}

Certified that this invoice shows the actual price of the goods.
        
Signature: ___________________
Date: {datetime.now().strftime('%Y-%m-%d')}
"""
    
    def _generate_certificate_of_origin(self, business):
        """Generate Palestine-specific certificate of origin"""
        return f"""
CERTIFICATE OF ORIGIN
=====================
1. Exporter: {business['name']}
   Address: {business['location']}
   Country: State of Palestine

2. Consignee: [Buyer's Information]

3. Means of transport: [To be specified]

4. Country of origin: State of Palestine

5. For official use (Palestinian Authority stamp):

   I, THE UNDERSIGNED, CERTIFY THAT THE GOODS MENTIONED
   IN THIS CERTIFICATE ORIGINATE IN THE STATE OF PALESTINE
   
   Place: {business['location']}
   Date: {datetime.now().strftime('%Y-%m-%d')}
   Stamp & Signature: _________________________
   
   (Issued by Palestinian Chamber of Commerce)
"""
    
    def _get_required_certs(self, destination):
        """Get certifications needed for specific destinations"""
        requirements = {
            "EU": ["Certificate of Origin", "Phytosanitary Certificate (for agriculture)", 
                   "Organic Certificate (if organic)", "Fair Trade Certificate (if fair trade)"],
            "USA": ["FDA Registration", "Certificate of Origin", 
                    "Commercial Invoice", "Packing List"],
            "Middle East": ["Halal Certificate", "Certificate of Origin", 
                           "Arabic Labeling", "GCC Conformity"],
            "Japan": ["JAS Organic Certificate (if organic)", "Certificate of Origin",
                     "Phytosanitary Certificate", "Commercial Invoice"]
        }
        
        return requirements.get(destination, ["Certificate of Origin", "Commercial Invoice"])
    
    def _get_hs_code(self, product_type):
        """Get Harmonized System codes for Palestinian products"""
        hs_codes = {
            "olive_oil": "1509.10",
            "dates": "0804.10",
            "zaatar": "0910.99",
            "embroidery": "5810.92",
            "olive_wood": "4414.00",
            "glassware": "7013.99",
            "ceramics": "6911.10",
            "soap": "3401.11"
        }
        
        return hs_codes.get(product_type, "9999.99")
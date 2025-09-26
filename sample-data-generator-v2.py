#!/usr/bin/env python3
"""
Generate sample customers.xlsx file for Lumen Email Renderer
Creates one row per product, with 4 products per customer.
"""

import pandas as pd
from datetime import datetime, timedelta
import random

def generate_contract_end_date():
    """Generate realistic contract end dates."""
    dates = [
        "March 15, 2025",
        "April 22, 2025", 
        "May 10, 2025",
        "June 30, 2025"
    ]
    return random.choice(dates)

def create_sample_data():
    """Create sample customer data with one product per row."""
    
    # All customers in single list (normal + edge cases mixed naturally)
    customers = [
        {
            'Customer Name': 'Acme Corporation',
            'Email Address': 'it-admin@acmecorp.com',
            'Physical Address': '1500 Technology Drive, Austin, TX 78701',
            'Account Number': 'LUM001'
        },
        {
            'Customer Name': 'Global Manufacturing Inc',
            'Email Address': 'network.ops@globalmanufacturing.com',
            'Physical Address': '2200 Industrial Blvd, Detroit, MI 48201',
            'Account Number': 'LUM002'
        },
        {
            'Customer Name': 'Metro Healthcare System',
            'Email Address': 'cio@metrohealthcare.org',
            'Physical Address': '',  # Edge case: missing address
            'Account Number': 'LUM003'
        },
        {
            'Customer Name': 'First National Bank',
            'Email Address': 'infrastructure@firstnationalbank.com',
            'Physical Address': '100 Financial Plaza, Charlotte, NC 28202',
            'Account Number': 'LUM004'
        },
        {
            'Customer Name': 'Very Long Business Name Technologies International Group LLC',
            'Email Address': 'very.long.email.address@verylongbusinessname.com',
            'Physical Address': '9999 Very Long Address Name Street, Some Very Long City Name, ST 12345',
            'Account Number': 'LUM005'
        },
        {
            'Customer Name': 'Missing Account Company',
            'Email Address': 'contact@missingaccount.com',
            'Physical Address': '500 Test Street, Test City, TS 12345',
            'Account Number': ''  # Edge case: missing account number
        }
    ]
    
    # Products each customer will have
    products = ['IP VPN', 'DIA', 'IOA', 'Wavelengths']
    
    # Generate rows - one per product per customer
    rows = []
    
    for customer in customers:
        for product in products:
            row = {
                'Customer Name': customer['Customer Name'],
                'Email Address': customer['Email Address'],
                'Physical Address': customer['Physical Address'],
                'Account Number': customer['Account Number'],
                'Product': product,
                'Contract End Date': generate_contract_end_date()
            }
            rows.append(row)
    
    # Create DataFrame
    df = pd.DataFrame(rows)
    
    # Save to Excel file
    filename = 'customers.xlsx'
    df.to_excel(filename, index=False, sheet_name='Sheet1')
    
    print(f"Created sample Excel file: {filename}")

    
    # Display preview
    print("\nData Preview:")

    
    # Show example of one customer's products
    print(f"\nExample - {customers[0]['Customer Name']} (LUM001) products:")
    customer_products = df[df['Account Number'] == 'LUM001'][['Product', 'Contract End Date']]
    print(customer_products.to_string(index=False))
    
    return filename

if __name__ == "__main__":
    create_sample_data()
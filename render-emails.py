#!/usr/bin/env python3
"""
Netflix Email Renderer - Proof of Concept
Reads customer data from Excel and renders personalized HTML emails.
"""

import argparse
import os
import re
import sys
import webbrowser
from pathlib import Path
from typing import Dict, List, Tuple

import pandas as pd
from jinja2 import Template


# Template will be loaded from external file: email_template.html


def simple_filename(text: str) -> str:
    """Simple filename conversion for POC."""
    # Just replace spaces with underscores and limit length
    return str(text).replace(' ', '_')[:30]


def load_customer_data(file_path: str, sheet_name: str) -> Tuple[pd.DataFrame, List[str]]:
    """Load and validate customer data from Excel file."""
    warnings = []
    
    try:
        # Read Excel file
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        print(f"✓ Loaded Excel file: {file_path} (sheet: {sheet_name})")
        
        # Expected columns
        expected_cols = ['Customer Name', 'Email Address', 'Physical Address', 'Account Number']
        missing_cols = [col for col in expected_cols if col not in df.columns]
        
        if missing_cols:
            warnings.append(f"Missing expected columns: {missing_cols}")
            print(f"⚠ Available columns: {list(df.columns)}")
        
        # Basic data cleaning
        initial_rows = len(df)
        
        # Remove completely empty rows
        df = df.dropna(how='all')
        
        # Trim whitespace from string columns
        string_cols = df.select_dtypes(include=['object']).columns
        df[string_cols] = df[string_cols].apply(lambda x: x.str.strip() if x.dtype == "object" else x)
        
        # Convert Account Number to string to handle mixed types
        if 'Account Number' in df.columns:
            df['Account Number'] = df['Account Number'].astype(str)
        
        print(f"✓ Data cleaning: {initial_rows} → {len(df)} rows (removed {initial_rows - len(df)} empty rows)")
        
        return df, warnings
        
    except FileNotFoundError:
        raise FileNotFoundError(f"Excel file not found: {file_path}")
    except Exception as e:
        raise Exception(f"Error reading Excel file: {e}")


def process_customers(df: pd.DataFrame, limit: int = None) -> Tuple[List[Dict], List[str]]:
    """Process customer data and return valid records."""
    valid_customers = []
    processing_log = []
    seen_accounts = set()
    
    # Apply limit if specified
    if limit:
        df = df.head(limit)
        processing_log.append(f"Limited to first {limit} rows")
    
    for idx, row in df.iterrows():
        customer_name = row.get('Customer Name', '').strip()
        email_address = row.get('Email Address', '').strip()
        account_number = str(row.get('Account Number', '')).strip()
        physical_address = row.get('Physical Address', '').strip()
        
        # Skip rows with missing required fields
        if not customer_name:
            processing_log.append(f"Row {idx+2}: Skipped - missing customer name")
            continue
            
        if not account_number or account_number.lower() in ['nan', 'none', '']:
            processing_log.append(f"Row {idx+2}: Skipped - missing account number")
            continue
        
        # Skip duplicate account numbers
        if account_number in seen_accounts:
            processing_log.append(f"Row {idx+2}: Skipped - duplicate account number {account_number}")
            continue
        
        seen_accounts.add(account_number)
        
        # Generate renewal link
        renewal_link = f"https://example.com/renew?acct={account_number}"
        
        # Create customer record
        customer = {
            'customer_name': customer_name,
            'email_address': email_address,
            'account_number': account_number,
            'physical_address': physical_address if physical_address else None,
            'renewal_link': renewal_link,
            'row_number': idx + 2  # Excel row number
        }
        
        valid_customers.append(customer)
        processing_log.append(f"Row {idx+2}: ✓ Processed {customer_name} (Account: {account_number})")
    
    return valid_customers, processing_log


def render_emails(customers: List[Dict], output_dir: Path, open_files: bool = True) -> List[str]:
    """Render HTML emails for each customer."""
    # Load template from external file
    try:
        with open('email_template.html', 'r', encoding='utf-8') as f:
            template_content = f.read()
        template = Template(template_content)
    except FileNotFoundError:
        raise FileNotFoundError("Template file 'email_template.html' not found. Make sure it exists in the current directory.")
    except Exception as e:
        raise Exception(f"Error reading template file: {e}")
    
    rendered_files = []
    
    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)
    print(f"✓ Output directory: {output_dir}")
    
    for customer in customers:
        # Generate simple filename
        simple_name = simple_filename(customer['customer_name'])
        simple_account = simple_filename(customer['account_number'])
        filename = f"customer_{simple_name}_{simple_account}.html"
        file_path = output_dir / filename
        
        # Render template
        try:
            html_content = template.render(
                customer_name=customer['customer_name'],
                account_number=customer['account_number'],
                renewal_link=customer['renewal_link'],
                physical_address=customer['physical_address']
            )
            
            # Write to file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            rendered_files.append(str(file_path))
            print(f"✓ Rendered: {filename}")
            
            # Open in browser
            if open_files:
                webbrowser.open_new_tab(f"file://{file_path.absolute()}")
                
        except Exception as e:
            print(f"✗ Error rendering {customer['customer_name']}: {e}")
            continue
    
    return rendered_files


def main():
    parser = argparse.ArgumentParser(
        description="Render personalized Netflix renewal emails from Excel data",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('--input', default='customers.xlsx', 
                       help='Input Excel file path (default: customers.xlsx)')
    parser.add_argument('--sheet', default='Sheet1',
                       help='Excel sheet name (default: Sheet1)')
    parser.add_argument('--limit', type=int, default=5,
                       help='Limit number of rows to process (default: 5)')
    parser.add_argument('--open', dest='open_files', action='store_true', default=True,
                       help='Open rendered files in browser (default)')
    parser.add_argument('--no-open', dest='open_files', action='store_false',
                       help='Don\'t open rendered files in browser')
    
    args = parser.parse_args()
    
    print("🎬 Netflix Email Renderer")
    print("=" * 50)
    
    try:
        # Load data
        df, warnings = load_customer_data(args.input, args.sheet)
        
        if warnings:
            print("\n⚠ Warnings:")
            for warning in warnings:
                print(f"  - {warning}")
        
        # Process customers
        customers, processing_log = process_customers(df, args.limit)
        
        if not customers:
            print("\n✗ No valid customers found to process!")
            return 1
        
        # Render emails
        print(f"\n📧 Rendering emails for {len(customers)} customers...")
        output_dir = Path('out')
        rendered_files = render_emails(customers, output_dir, args.open_files)
        
        # Summary
        print("\n" + "=" * 50)
        print("📊 PROCESSING SUMMARY")
        print("=" * 50)
        print(f"Total rows in Excel: {len(df)}")
        print(f"Valid customers processed: {len(customers)}")
        print(f"HTML files rendered: {len(rendered_files)}")
        print(f"Skipped: {len(df) - len(customers)}")
        
        if args.open_files and rendered_files:
            print(f"\n🌐 Opened {len(rendered_files)} files in browser tabs")
        
        print(f"\n📁 Output directory: {output_dir.absolute()}")
        
        # Detailed log
        print("\n📝 Processing Details:")
        for log_entry in processing_log:
            print(f"  {log_entry}")
        
        print(f"\n✅ Done! Generated {len(rendered_files)} email files.")
        
        return 0
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
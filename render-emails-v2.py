import argparse
import sys
import threading
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from typing import Dict, List, Tuple

import pandas as pd
from jinja2 import Template


def load_customer_data(file_path: str, sheet_name: str) -> Tuple[pd.DataFrame, List[str]]:
    """
    Load customer data from Excel and do some light cleaning.
    Returns a DataFrame + warnings if required columns are missing.
    """
    warnings = []
    df = pd.read_excel(file_path, sheet_name=sheet_name)

    # Make sure we have at least the basics
    expected = ['Customer Name', 'Email Address', 'Physical Address', 'Account Number']
    missing = [c for c in expected if c not in df.columns]
    if missing:
        warnings.append(f"Missing expected columns: {missing}")

    # Drop empty rows and strip whitespace
    df = df.dropna(how='all')
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].astype(str).str.strip()

    # Normalize account numbers to strings (avoids Excel number weirdness)
    if 'Account Number' in df.columns:
        df['Account Number'] = df['Account Number'].astype(str)

    return df, warnings


def process_customers(df: pd.DataFrame) -> Tuple[List[Dict], List[str]]:
    """
    Group rows by Account Number, combine product info,
    and build a clean list of customers.
    """
    logs, customers = [], []
    for acct, group in df.groupby('Account Number'):
        # Skip empty/invalid accounts
        if not acct or str(acct).strip().lower() in ('', 'none', 'nan'):
            logs.append(f"Skipped invalid account: {acct}")
            continue

        # Use first row for base customer details
        first = group.iloc[0]
        name = str(first.get('Customer Name', '')).strip()
        email = str(first.get('Email Address', '')).strip()
        addr = str(first.get('Physical Address', '')).strip()

        if not name:
            logs.append(f"Account {acct}: Skipped - missing customer name")
            continue

        # Collect all products tied to this account
        products = [
            {
                'name': str(r.get('Product', '')).strip(),
                'contract_end_date': (str(r.get('Contract End Date', '')).strip() or 'N/A')
            }
            for _, r in group.iterrows()
            if str(r.get('Product', '')).strip().lower() not in ('', 'none', 'nan')
        ]
        if not products:
            logs.append(f"Account {acct}: Skipped - no valid products")
            continue

        # Build final customer dict
        customers.append({
            'customer_name': name,
            'email_address': email,
            'account_number': str(acct),
            'physical_address': addr or None,
            'renewal_link': f"https://example.com/renew?acct={acct}",
            'products': products,
        })
        logs.append(f"Account {acct}: Processed {name} with {len(products)} products")
    return customers, logs


class EmailHandler(BaseHTTPRequestHandler):
    # Class variable holds rendered HTML strings
    emails: List[str] = []

    def do_GET(self):
        """
        Serve one email per URL:
        /0 → first customer
        /1 → second customer, etc.
        """
        try:
            idx = int(self.path.strip("/")) if self.path.strip("/") else 0
            if 0 <= idx < len(self.emails):
                html = self.emails[idx]
                self.send_response(200)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(html.encode("utf-8"))
            else:
                self.send_error(404, "Email not found")
        except Exception as e:
            self.send_error(500, f"Server error: {e}")


def serve_emails(customers: List[Dict]) -> int:
    """
    Render emails for all customers,
    start a small localhost web server,
    and open each email in a new browser tab.
    """
    template = Template(Path('email_template.html').read_text(encoding='utf-8'))

    # Render HTML for each customer
    rendered = [
        template.render(
            customer_name=c['customer_name'],
            account_number=c['account_number'],
            renewal_link=c['renewal_link'],
            physical_address=c['physical_address'],
            products=c['products']
        )
        for c in customers
    ]
    EmailHandler.emails = rendered

    # Run HTTP server in background thread
    server = HTTPServer(("localhost", 8000), EmailHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()

    # Open each customer email in its own browser tab
    for i in range(len(rendered)):
        webbrowser.open_new_tab(f"http://localhost:8000/{i}")

    return len(rendered)


def main() -> int:
    parser = argparse.ArgumentParser(description="Preview Lumen renewal emails in browser (no files)")
    parser.add_argument('--input', default='customers.xlsx', help='Input Excel file path')
    args = parser.parse_args()

    try:
        df, warnings = load_customer_data(args.input, "Sheet1")
        for w in warnings:
            print(f"Warning: {w}")

        customers, logs = process_customers(df)
        if not customers:
            print("No valid customers found.")
            return 1

        opened = serve_emails(customers)

        print("\nSummary")
        print(f"Rows in Excel: {len(df)}")
        print(f"Customers processed: {len(customers)}")
        print(f"Browser tabs opened: {opened}")
        print("Server running at: http://localhost:8000/ (Ctrl+C to stop)")
        for line in logs:
            print(f"- {line}")

        # Keep server alive until user manually interrupts
        try:
            while True:
                pass
        except KeyboardInterrupt:
            print("\nShutting down server.")
            return 0

    except Exception as e:
        print(f"Error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())

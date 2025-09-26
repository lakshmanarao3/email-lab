# main.py
import argparse
import sys

from data import load_and_prepare_customer_df, process_customers
from server import render_emails, start_server_and_open_tabs

def main() -> int:
    """
    Entry point: load/clean data, build customers, render emails,
    start the local server, and open browser tabs.
    """
    parser = argparse.ArgumentParser(description="Preview renewal emails in browser (no files)")
    parser.add_argument('--input', default='customers.xlsx', help='Input Excel file path')
    args = parser.parse_args()

    try:
        # Load and validate once (Sheet1 is assumed)
        df, warnings = load_and_prepare_customer_df(args.input, "Sheet1")
        for w in warnings:
            print(f"Warning: {w}")

        # Build customer objects (assumes required fields exist)
        customers, logs = process_customers(df)
        if not customers:
            print("No valid customers found.")
            return 1

        # Render -> serve -> open tabs
        rendered = render_emails(customers)
        opened = start_server_and_open_tabs(rendered)  # localhost:8000 by default

        # Console summary
        print("\nSummary")
        print(f"Rows in Excel: {len(df)}")
        print(f"Customers processed: {len(customers)}")
        print(f"Browser tabs opened: {opened}")
        print("Server running at: http://localhost:8000/ (Ctrl+C to stop)")
        for line in logs:
            print(f"- {line}")

        # Keep process alive so the server can serve pages
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

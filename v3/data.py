# data.py
from typing import Dict, List, Tuple
import pandas as pd

def _s(x) -> str:
    """
    Normalize any value to a trimmed string.
    - None -> ""
    - Ensures consistent comparisons and safe string ops.
    """
    return "" if x is None else str(x).strip()

def _nonempty(x) -> bool:
    """
    True if the value is meaningfully present.
    Treats "", "none", and "nan" (case-insensitive) as empty placeholders.
    """
    v = _s(x).lower()
    return v not in ("", "none", "nan")

def load_and_prepare_customer_df(file_path: str, sheet_name: str) -> Tuple[pd.DataFrame, List[str]]:
    """
    Read Excel, validate required columns, normalize strings, and
    drop rows missing any required field (single source of truth for validation/cleanup).

    Returns:
      - Cleaned DataFrame ready for processing
      - List of human-readable warnings
    """
    warnings: List[str] = []

    # Read Excel sheet
    df = pd.read_excel(file_path, sheet_name=sheet_name)

    # 1) Validate schema (once)
    required_cols = ['Customer Name', 'Email Address', 'Physical Address', 'Account Number']
    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        # Missing schema means we can't proceed meaningfully
        raise ValueError(f"Missing required columns: {missing}")

    # 2) Clean section — make data predictable and uniform
    # - Drop rows that are entirely empty
    df = df.dropna(how='all')

    # - Normalize strings: for every object column, stringify + strip
    for col in df.columns:
        if df[col].dtype == object:
            df[col] = df[col].apply(_s)

    # - Normalize Account Number (Excel can store it as float; we need a clean string)
    df['Account Number'] = df['Account Number'].astype(str).apply(_s)

    # 3) Enforce required values (single place)
    # Build a mask that keeps only rows with all required fields non-empty
    mask = (
        df['Customer Name'].apply(_nonempty) &
        df['Email Address'].apply(_nonempty) &
        df['Physical Address'].apply(_nonempty) &
        df['Account Number'].apply(_nonempty)
    )
    dropped = int((~mask).sum())
    if dropped:
        warnings.append(f"Dropped {dropped} row(s) missing required fields.")

    df = df[mask].copy()
    return df, warnings

def process_customers(df: pd.DataFrame) -> Tuple[List[Dict], List[str]]:
    """
    Convert cleaned DataFrame into structured customer records.
    Assumes required fields are already enforced by load_and_prepare_customer_df.

    Logic:
      - Group rows by Account Number (one customer per account)
      - Take the first row's identity fields (name/email/address)
      - Aggregate products for that account (skip blank/placeholder products)
      - Skip accounts with no valid products (no email to render)
    """
    logs: List[str] = []
    customers: List[Dict] = []

    for acct, group in df.groupby('Account Number'):
        first = group.iloc[0]
        name  = _s(first['Customer Name'])
        email = _s(first['Email Address'])
        addr  = _s(first['Physical Address'])

        # Collect valid products within this account
        products = []
        for _, r in group.iterrows():
            prod_name = _s(r.get('Product', ''))
            if not _nonempty(prod_name):
                continue
            end = _s(r.get('Contract End Date', '')) or 'N/A'
            products.append({'name': prod_name, 'contract_end_date': end})

        if not products:
            logs.append(f"Account {acct}: Skipped - no valid products")
            continue

        customers.append({
            'customer_name': name,
            'email_address': email,
            'account_number': acct,
            'physical_address': addr,
            'renewal_link': f"https://example.com/renew?acct={acct}",
            'products': products,
        })
        logs.append(f"Account {acct}: Processed {name} with {len(products)} products")

    return customers, logs

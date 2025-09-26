import pandas as pd
from pathlib import Path

def create_sample_data():
    """Create sample customer data for testing."""
    
    # Sample customer data
    customers = [
        {
            'Customer Name': 'John Smith',
            'Email Address': 'john.smith@email.com',
            'Physical Address': '123 Main Street, New York, NY 10001',
            'Account Number': 'ACC001'
        },
        {
            'Customer Name': 'Jane Doe',
            'Email Address': 'jane.doe@gmail.com',
            'Physical Address': '456 Oak Avenue, Los Angeles, CA 90210',
            'Account Number': 'ACC002'
        },
        {
            'Customer Name': 'Alice Johnson',
            'Email Address': 'alice.johnson@yahoo.com',
            'Physical Address': '789 Pine Road, Chicago, IL 60601',
            'Account Number': 'ACC003'
        },
        {
            'Customer Name': 'Bob Wilson',
            'Email Address': 'bob.wilson@outlook.com',
            'Physical Address': '321 Elm Street, Houston, TX 77001',
            'Account Number': 'ACC004'
        },
        {
            'Customer Name': 'Carol Davis',
            'Email Address': 'carol.davis@hotmail.com',
            'Physical Address': '654 Maple Drive, Phoenix, AZ 85001',
            'Account Number': 'ACC005'
        },
        {
            'Customer Name': 'David Miller',
            'Email Address': 'david.miller@email.com',
            'Physical Address': '987 Cedar Lane, Philadelphia, PA 19101',
            'Account Number': 'ACC006'
        },
        {
            'Customer Name': 'Emma Garcia',
            'Email Address': 'emma.garcia@gmail.com',
            'Physical Address': '147 Birch Street, San Antonio, TX 78201',
            'Account Number': 'ACC007'
        },
        {
            'Customer Name': 'Frank Brown',
            'Email Address': 'frank.brown@yahoo.com',
            'Physical Address': '258 Spruce Avenue, San Diego, CA 92101',
            'Account Number': 'ACC008'
        },
        {
            'Customer Name': 'Grace Lee',
            'Email Address': 'grace.lee@outlook.com',
            'Physical Address': '369 Willow Road, Dallas, TX 75201',
            'Account Number': 'ACC009'
        },
        {
            'Customer Name': 'Henry Martinez',
            'Email Address': 'henry.martinez@email.com',
            'Physical Address': '741 Ash Street, San Jose, CA 95101',
            'Account Number': 'ACC010'
        },
        # Add some edge cases for testing
        {
            'Customer Name': 'Test User With Long Name',
            'Email Address': 'longname@test.com',
            'Physical Address': '999 Very Long Address Name Street, Some Very Long City Name, ST 12345',
            'Account Number': 'ACC011'
        },
        {
            'Customer Name': 'No Address User',
            'Email Address': 'noaddress@test.com',
            'Physical Address': '',  # Empty address to test conditional display
            'Account Number': 'ACC012'
        },
        # Add a row with missing data to test validation
        {
            'Customer Name': '',  # Missing name - should be skipped
            'Email Address': 'missing@test.com',
            'Physical Address': '123 Test St',
            'Account Number': 'ACC013'
        },
        {
            'Customer Name': 'Missing Account User',
            'Email Address': 'missingacct@test.com',
            'Physical Address': '456 Test Ave',
            'Account Number': ''  # Missing account - should be skipped
        }
    ]
    
    # Create DataFrame
    df = pd.DataFrame(customers)
    
    # Save to Excel file
    filename = 'customers.xlsx'
    df.to_excel(filename, index=False, sheet_name='Sheet1')
    
    print(f"✅ Created sample Excel file: {filename}")
    print(f"📊 Contains {len(customers)} sample customers")
    print(f"📝 Includes test cases for:")
    print("   - Normal customer data")
    print("   - Long names and addresses")
    print("   - Missing address (to test conditional display)")
    print("   - Missing required fields (to test validation)")
    print()
    print("🚀 Ready to run: python render_emails.py")
    
    # Display preview
    print("\n📋 Data Preview:")
    print("-" * 80)
    print(df[['Customer Name', 'Account Number', 'Physical Address']].head(8).to_string(index=False))
    
    return filename

if __name__ == "__main__":
    create_sample_data()
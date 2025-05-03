import os
from db.database_helper import Database
from email_parser import parse_emails
from report_generator import generate_report
from datetime import datetime

def setup_database():
    # Create Database helper instance
    db = Database()
    
    # Run SQL setup if database does not exist
    db.execute_sql_from_file('db/create_database.sql')


# Main function entry point

def main():
    """ Main function for application workflow """
    # Step 1: Setup database for first time users
    setup_database()

    # Step 2: Parse emails to collect transaction data
    print("Running email parser...")
    parse_emails(use_sample_emails=False)

    # Step 3: Generate desired report
    print("Welecome to Xavier's personal FINANCIAL TRAKCER!")
    
    try:
        # Prompt user for month and year for desired report
        month = int(input("Enter the month (1-12) for the report: "))
        year = int(input("Enter the year (e.g., 2024) for the report: "))
        # Check for valid inputs
        if not (1 <= month <= 12):
            raise ValueError("Month must be between 1 and 12.")
        
        date_str = f"{datetime(year, month, 1).strftime('%B')} 1, {year}"
        print("Generating report...")

        generate_report(date_str)

    except ValueError as ve:
        print(f"Invalid input: {ve}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    print("Process completed.")

if __name__ == "__main__":
    main()


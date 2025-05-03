import os
import argparse
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
    # Introduction
    print("Welecome to Xavier's personal FINANCIAL TRAKCER!")
    
    parser = argparse.ArgumentParser(description="Xavier's Personal Financial Tracker")
    parser.add_argument('-p','--parse-only', action='store_true', help='Only parse emails, do not generate a report')
    parser.add_argument('-r', '--report-only', action='store_true', help='Only generate a report, do not parse emails')
    args = parser.parse_args()

    """ Main function for application workflow """

    # with flag -p: Parse emails to collect transaction data
    if not args.report_only:
        setup_database() # Setup database for first time users
        print("Running email parser...")
        parse_emails(use_sample_emails=False)
    
    # with flag -r: generates report only
    if not args.parse_only:
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


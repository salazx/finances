from db.database_helper import Database
from datetime import datetime

def generate_report(date_str=None):
    """
    Generates and prints a monthly summary of transactions by category.

    :param month: The month for which to generate report (default: current month)
    :parma year: The year for which to generate report (default: current year)
    """

    # Default value for report will be current month and year
    if date_str is None:
        today = datetime.today()
        month = today.month
        year = today.year

    else:
        try:
            parsed_date = datetime.strptime(date_str, "%B %d, %Y")
            month = parsed_date.month
            year = parsed_date.year
        except ValueError:
            print(f"Error: The date '{date_str} is not in the expected format")
            return

    db = Database()
    total_spent = 0

    try:
        summary = db.get_monthly_summary(str(month).zfill(2), year)

        print(f"Monthly Summary for {month}/{year}")
        print("-" * 40)

        if summary:
            for category, total in summary:
                print(f"{category}: ${total:.2f}")
                total_spent += total
        else:
            print("No transactions found for this period.")

        print("-" * 40)
        print(f"Total Spent: ${total_spent:.2f}")

    except Exception as e:
        print(f"Error generating report: {e}")
    finally:
        db.close_connection()


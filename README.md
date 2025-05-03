# CS50 Final Project Xavier Salazar

## Introduction
This README.md file documents my final project, a **Finance Tracker**, which generates monthly summary reports to help users easily track and document personal finances and spending habits. 

## Features
- **Email Parsing**: Automatically retrieves transaction details from emails. 
- **Database**: Stores transaction data in an SQLite database.
- **Monthly Reports**: Generates financial reports for any given month and year.

## Requirements

Before running the application, ensure that you have the following dependencies installed:

- Python 3.x
- SQLite3 (for the database)
- Google API Python Client (for Gmail integration)

You can install the necessary Python dependencies using 'pip' by running:

'''bash
pip install -r requirements.txt

# Usage
The main entry point for the application resides in the "main.py" file, where 3 main steps are outlined:
Step 1: Setup database for first time users
Step 2: Parse emails to collect transaction data
Step 3: Generate desired report

The three steps will use a combination of python scripts to accomplish various tasks.

## Email Parsing
The intended functionality is to use email notifications from credit card accounts, and assign the appropriate labels to those emails. The email parser then retrieves transaction details from unread emails with assigned labels (e.g., "Chase", "VentureX", "Discover", etc.) and creates 'transactions' as defined in the transaction.py file. To ensure proper functionality, the desired labels must be created and assigned to a Gmail email account. It is possible to automatically assign labels to received emails with filters that rely on criteria specific to the email.

Currently, the application only parses emails from Chase credit accounts, as this was the primary testing account used. The parsing relies on standardized patterns in the emails to pull appropriate data. 

## Generating Reports
When running the program, you will be prompted to input a month and year for which you want the report to be created. The application will generate a financial report based on the transactions for that period. The report will include sums for each category that was retrieved from the database query and present them. 

## Database PreSets
The database is preset to have the following categories: Eating Out, Education, Gas, Groceries, Clothes, House Supplies, Loans, Insurance, Misc., Debt Payments, Travel, Entertainment, and Car Supplies. It also has presets for accounts: Wells Fargo, 'Asset', Capital One, 'Asset', Chase, 'Liability', VentureX, 'Liability', Discover, 'Liability', Quicksilver, 'Liability', and Macys Amex, 'Liability'. Currently, the only way to adjust desired categories or accounts is to change it directly in the database, or update the 'create_database.sql' file before the first time running the program ensuring the desired changes are included when the database is created.

## Vendor to Category Mappings
Vendor to category mappings are also preset and new vendors with unassigned categories are defaulted to the Misc. category. These mappings are stored within a dictionary in the category.py file. This was a decision made to save time in the developing phase, with the hope to adjust at a later date utilizing AI to assign category mappings per vendor. 

## Link to Youtube Project Demo
https://youtu.be/TO71gp07L7I


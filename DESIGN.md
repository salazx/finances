# Design.md - CS50 Final Project: Finance Tracker

## Overview
The Finance Tracker is designed as a modular, Python-based application to automate the process of gathering, categorizing, and reporting personal financial transactions. It is structured around core components that work together seamlessly to ensure flexibility, scalability, and maintainability.

---

## Project Structure

core/
├── db/
│   ├── database_helper.py
│   └── create_database.sql
├── models/
│   ├── category.py
│   └── transaction.py
├── authentication.py
├── email_parser.py
├── report_generator.py
├── main.py
└── client_secret.json

---

## Key Components

### 1. **Database Management**
- **Module**: 'db/database_helper.py'
- **Responsibilities**:
    - Handles database connection and transaction operations
    - Manages schema setup using 'create_database.sql'
    - Facilitates CRUD (Create, Read, Update, Delete) operations for transactions and vendors
    - References 'create_database.sql' file to create a database with the correct schema for first time users
- **Design Considerations**:
    - SQLite database ('db/finances.db') is lightweight and sufficient for single-user applications
    - The database schema is designed to store normalized data for transactions, categories, and vendors

---

### 2. **Email Parsing**
- **Module**: 'email_parser.py'
- **Responsibilities**: 
    - Integrates with Gmail API to fetch and parse transactional emails
    - Extracts key details (e.g., data, vendor, amount) using regular expressions
    - Imports new vendors into database
    - Converts email data into structured 'Transaction' objects
- **Design Considerations**:
    - Based email parsing off of standardized patterns from email notifications of credit card account
    - Checks vendor-to-category dictionary in categories.py for known vendors, otherwise assigns category to misc.

---

### 3. **Transaction Modeling**
- **Module**: 'models/transaction.py' 'models/category.py'
- **Responsibilities**:
    - Represents financial transactions and categories as objects
    - Facilitates hard coded vendor-to-category mapping
- **Design Considerations**:
    - Abstracts business logic for transactions, making it reusable in email parsing and report generation
    - Hard coded vendor-to-category mapping due to lack of time in development, further developements should look to automate vendor-to-category mappings

---

### 4. **Report Generation**
- **Module**: 'report_generator.py'
- **Responsibilities**:
    - Creates financial report based on database data showing categorized spending
- **Design Considerations**:
    - Prompts user for desired month and year at runtime
    - Easily extensible to include additional report formats or visualization

---

### 5. **Authentication**
- **Module**: 'authentication.py'
- **Responsibilities**:
    - Handles OAuth 2.0 authentication with Google API
    - Manages token storage ('token.json') for secure and persistent access
- **Design Considerations**:
    - Ensures secure, token-based interactions with Gmail API
    - Simplifies first-time setup by automating credential validation

---

## Workflow

1. **Database Setup**:
    - On the first run, the program will check for the existence of the database
    - If absent, it initializes the database schema using 'create_database.sql'

2. **Email Parsing**:
    - The user allows email notifications for credit card accounts and assigns specific labels to notification emails in Gmail
    - The parser fetches and processes these emails, storing transaction details in the database

3. **Report Generation**:
    - The user specifies the month and year for the report
    - The program queries the database and generates a final summary

---

## Future Enhancements

- **Enhanced Email Parsing**:
    - Support for additional credit card accounts, email providers, or custom parsers
- **Advanced Reporting**:
    - Inclusion of visualizations (e.g., charts and graphs)
    - Export options (e.g., PDF, Excel)
- **Increase dynamic attributes within program**:
    - Use AI to take vendors as input and provide an educated guess on which category to assign it to
    - Add configuration options for various categories, and transaction accounts rather than setting default values for both inside of the database

---

## Conclusion

The Finance Tracker is built with a focus on simplicity and modularity, making it a reliable tool for personal financial management. Its current design lays the foundation for future enhancements and adaptations.



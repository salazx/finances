# db/database.py
import os
import sqlite3

class Database:
    def __init__(self):
        # Initializes database object and connects to SQLite database
        self.db_name = "/home/profx/Documents/Code/Finances/finances/db/finances.db" 
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
    
    def connect(self):
        """ Connect to the SQLite database."""
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()

    def close_connection(self):
        # Closes database connection
        self.conn.close()

    def execute_sql_from_file(self, sql_file):
        """ Run SQL commands from provided files to adjust database"""
        if not os.path.exists(self.db_name) or os.path.getsize(self.db_name) == 0:
            print(f"Database '{self.db_name}' does not exist. Creating database...")
            self.connect()
            
            if os.path.exists(sql_file):
                with open(sql_file, 'r') as file:
                    sql_script = file.read()
                    try:
                        self.cursor.executescript(sql_script)
                        print("Database created and schema applied.")
                    except Exception as e:
                        print(f"Error applying schema: {e}")
            else:
                print(f"SQL file '{sql_file}' not found. Please check the path.")

            self.close_connection()
        else:
            print(f"Database '{self.db_name}' already exists. Skipping creation.")

    def execute_query(self, query, params=None):
        """
        Executes a query (SELECT, INSERT, UPDATE, DELETE) on the database
        :param query: The SQL query string
        :param params: The parameters to use with the query (default is None)
        :return: The resutl of the query (if applicable)
        """
        try:
            if params is None:
                self.cursor.execute(query)
            else:
                self.cursor.execute(query,params)
            
            # Commit changes for INSERT/UPDATE/DELETE queries
            if query.strip().upper().startswith(('INSERT', 'UPDATE', 'DELETE')):
                self.conn.commit()

            # If query is SELECT, return results
            if query.strip().upper().startswith('SELECT'):
                return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error executing query: {e}")
            return None

    def insert_vendors(self, vendors):
        # Inserts unique vendors into vendor table of database

        for vendor in vendors:
            # Uses insert or ignore into to insert new vendors into database
            query = "INSERT OR IGNORE INTO vendors (vendor_name) VALUES (?)"
            self.execute_query(query, (vendor,))

    def get_vendor_id(self, vendor_name):
        query = "SELECT vendor_id FROM vendors WHERE vendor_name = ?"
        result = self.execute_query(query, (vendor_name, ))
        return result[0][0] if result else None # Return vendor_id if found, else None

    def get_category_id(self, category):
        query = "SELECT category_id FROM categories WHERE category_name = ?"
        result = self.execute_query(query, (category, ))
        return result[0][0] if result else None # Return category_id if found, else None

    def get_account_id(self, account_name):
        query = "SELECT account_id FROM accounts WHERE account_name = ?"
        result = self.execute_query(query, (account_name, ))
        return result[0][0] if result else None # Return account_id if found, else None


    def insert_transactions(self, transactions):
        # Inserts found transactions from email parser
        
        query = """ 
        INSERT INTO transactions (date, amount, vendor_id, category_id, account_id)
        VALUES (?, ?, ?, ?, ?)
        """   

        for transaction in transactions:
            # Retrieve ID's

            vendor_id = self.get_vendor_id(transaction.vendor)
            category_id = self.get_category_id(transaction.category)
            account_id = self.get_account_id(transaction.account)

            if not (vendor_id and category_id and account_id):
                missing_ids = []
                if not vendor_id:
                    missing_ids.append("vendor_id")
                if not category_id:
                    missing_ids.append("category_id")
                if not account_id:
                    missing_ids.append("account_id")


                print(f"Error: Missing {', '.join(missing_ids)} for transaction: {transaction}")
                continue

            self.execute_query(
                query, 
                (transaction.date, transaction.amount, vendor_id, category_id, account_id)
                )



    def get_monthly_summary(self, month, year):
        
        month_str = str(month).zfill(2)
        year_str = str(year)

        query = """
        SELECT c.category_name, SUM(t.amount) as total
        FROM transactions t
        JOIN categories c on t.category_id = c.category_id
        WHERE strftime('%m', t.date) = ? and strftime('%Y', t.date) = ?
        GROUP BY c.category_name
        ORDER BY total DESC;
        """
        
        return self.execute_query(query, (month_str, year_str))


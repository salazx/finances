# Create the Transaction class to handle all functionality related to transactions

class Transaction:

    def __init__(self, date, amount, vendor, category, account):
        
        self.date = date
        self.amount = amount
        self.vendor = vendor
        self.category = category
        self.account = account
    
    def __str__(self):
        return f"Date: {self.date}, Amount: {self.amount}, Vendor: {self.vendor}, Category: {self.category}, Account: {self.account}"

    def import_transactions(self, cursor): 

        # SQL Query to import transactions to transaction table
        query = """
        INSERT INTO transactions (date, amount, vendor, category, account)
        VALUES (?, ?, ?, ?, ?)
        """
        # Execute the query
        cursor.execute(query, (self.date, self.amount, self.vendor, self.category, self.account))


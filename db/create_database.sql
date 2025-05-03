CREATE TABLE transactions (
    transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
    date DATETIME,
    amount REAL NOT NULL,
    vendor_id TEXT NOT NULL,
    category_id INTEGER NOT NULL,
    account_id TEXT NOT NULL,
    FOREIGN KEY (category_id) REFERENCES categories(category_id),
    FOREIGN KEY (account_id) REFERENCES accounts(account_id),
    FOREIGN KEY (vendor_id) REFERENCES vendors(vendor_id)
);

CREATE TABLE categories (
    category_id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_name TEXT UNIQUE NOT NULL
);

CREATE TABLE vendors (
	vendor_id INTEGER PRIMARY KEY AUTOINCREMENT,
	vendor_name TEXT UNIQUE NOT NULL
);

CREATE TABLE vendor_categories (
	category_id INTEGER NOT NULL,
	vendor_id INTEGER NOT NULL,
	FOREIGN KEY (category_id) REFERENCES categories(category_id),
	FOREIGN KEY (vendor_id) REFERENCES vendors(vendor_id),
	PRIMARY KEY (category_id, vendor_id) -- Ensures unique combinations
);

CREATE TABLE accounts (
	account_id INTEGER PRIMARY KEY AUTOINCREMENT,
	account_name TEXT NOT NULL,
	type TEXT CHECK(type IN ('Asset', 'Liability')) NOT NULL
);


INSERT INTO categories (category_name) VALUES 
        ('Eating Out'), 
        ('Education'),
        ('Gas'), 
        ('Groceries'), 
        ('Clothes'), 
        ('House Supplies'), 
        ('Loans'), 
        ('Insurance'), 
        ('Misc.'), 
        ('Debt Payments'), 
        ('Travel'), 
        ('Entertainment'),
        ('Car Supplies');

INSERT INTO accounts (account_name, type) VALUES
        ('Wells Fargo', 'Asset'),
        ('Capital One', 'Asset'),
        ('HSBC', 'Asset'),
	('Chase', 'Liability'),
        ('VentureX', 'Liability'),
        ('Discover', 'Liability'),
        ('Quicksilver', 'Liability'),
        ('Macys Amex', 'Liability');


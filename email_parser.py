from authentication import get_credentials
from googleapiclient.discovery import build
from db.database_helper import Database
from models.transaction import Transaction
from models.category import Category
from simplegmail import Gmail
from simplegmail.query import construct_query
from datetime import datetime
import re
import os
from openai import OpenAI
from dotenv import load_dotenv
import json


# ChatGPT Parsing

load_dotenv()
api_key=os.getenv("OPENAI_API_KEY")

if api_key:
    client = OpenAI(api_key=api_key)
else:
    raise ValueError("OPENAI_API_KEY is not set in the .env file")

def gpt_batch_prompt(email_texts):
    return [
        {"role": "system", "content": "You are a helpful assistant that extracts structured data from multiple credit card transaction emails."},
        {"role": "user", "content": f"""Extract the following details from each email:
    - Vendor name
    - Amount
    - Date

    Return the results as a JSON array in the same order as the emails.

    Emails:
    {format_email_batch(email_texts)}
    """}
            ]

def format_email_batch(email_texts):
    return "\n\n".join(
                f"Email {i+1}:\n\"\"\"\n{email}\n\"\"\"" for i, email in enumerate(email_texts)
            )

def parse_emails(gmail=None, use_sample_emails=False):

    # Get credentials from authentication.py
    creds = get_credentials()
    if creds:
        print(f"Valid: {creds.valid}, Expired: {creds.expired}")
    else:
        print("Failed to retrieve credentials.")

    # Build the gmail api client with the credentials

    gmail_service = build('gmail', 'v1', credentials=creds)
    gmail = Gmail()

    # Labels for different sources of personal transactions
    desired_labels = ["Chase", "VentureX", "Quicksilver", "Macys", "Discover"] 

    transaction_data = []

    # Initializes a connection to database
    db = Database() 
    
    # Create batches to limit API requests
    BATCH_SIZE = 10 

    # Sets query parameters for each label in desired labels
    for label in desired_labels:
        query_params = {
                "labels":[[label]],
                "unread": True
                }

        # Grabs messages for current label of loop
        messages = gmail.get_messages(query=construct_query(query_params))

        # Grabs individual values for necessary attributes of the transaction class
        for i in range(0, len(messages), BATCH_SIZE):
            batch = messages[i:i + BATCH_SIZE]
            email_texts = [msg.plain for msg in batch]
            try:
                prompt = gpt_batch_prompt(email_texts)
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo", 
                    messages=prompt,
                    temperature=0.2
                    )
                
                print(f"Tokens used: {response.usage.total_tokens}")
                response_text = response.choices[0].message.content.strip()
                if response_text.startswith("```json"):
                    response_text = response_text[len("```json"):].strip()
                if response_text.endswith("```"):
                    response_text = response_text[:-3].strip()

                print("GPT response:", response_text)

                try:
                    results = json.loads(response_text)
                except json.JSONDecodeError as e:
                    print(f"Failed to parse JSON from GPT: {e}")
                    continue

                for message, data in zip(batch, results):
                    # Set transaction class attributes based on parsed data from chatgpt
                    vendor = data.get("Vendor name")
                    category = Category.get_category_for_vendor(vendor)
                    account = label

                    # Amount format conversion
                    raw_amount = data.get("Amount", "").replace("$","").replace(",","").strip()
                    amount = float(raw_amount)
                    # Date format conversion
                    date_str = data.get("Date")
                    date_obj = datetime.strptime(date_str, "%B %d, %Y")
                    date = date_obj.strftime("%Y-%m-%d")

                    # Change email status to read to prevent repeat transactionsi
                    try:
                        message.mark_as_read()
                    except Exception as e:
                        print(f"Error marking email as read: {e}")

                    # Import vendors into vendor table of database for catgorizing
                    if vendor:
                        db.insert_vendors([vendor])

                    # creates a transaction of the transaction class to be appended to transaction_data
                    transaction = Transaction(date, amount, vendor, category, account)
                    transaction_data.append(transaction)

            except Exception as e:
                print(f"Error parsing batch for label {label}: {e}")

    # Insert Transactions into database
    db.insert_transactions(transaction_data)

    # Close database connection
    db.close_connection()
    print("Email parsing and transaction import completed.")




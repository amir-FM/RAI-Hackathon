import json
from dataclasses import dataclass
from typing import List, Optional

# Define data classes for the JSON structure
@dataclass
class Amount:
    amount: float
    currency: str

@dataclass
class Transaction:
    transactionId: str
    endToEndId: str
    mandateId: str
    bookingDate: str
    valueDate: str
    transactionAmount: Amount
    creditorName: str
    remittanceInformationUnstructured: str

@dataclass
class Transactions:
    booked: List[Transaction]
    viewAccount: Optional[str] = None  # Link to view account (optional)

@dataclass
class TotalSalary:
    amount: float
    currency: str

@dataclass
class User:
    totalSalary: TotalSalary
    transactions: Transactions

@dataclass
class Root:
    user: User

# Function to parse JSON from a file into data classes
def parse_json_from_file(file_path: str) -> Root:
    def convert_transaction(trans: dict) -> Transaction:
        return Transaction(
            transactionId=trans["transactionId"],
            endToEndId=trans["endToEndId"],
            mandateId=trans["mandateId"],
            bookingDate=trans["bookingDate"],
            valueDate=trans["valueDate"],
            transactionAmount=Amount(**trans["transactionAmount"]),
            creditorName=trans["creditorName"],
            remittanceInformationUnstructured=trans["remittanceInformationUnstructured"]
        )

    def convert_transactions(transactions: dict) -> Transactions:
        booked = [convert_transaction(trans) for trans in transactions["booked"]]
        viewAccount = transactions["_links"]["viewAccount"]["href"] if "_links" in transactions and "viewAccount" in transactions["_links"] else None
        return Transactions(booked=booked, viewAccount=viewAccount)

    # Read JSON data from the file
    with open(file_path, 'r') as file:
        json_obj = json.load(file)
    
    # Extract the user data and construct the Root object
    user_data = json_obj["user"]
    return Root(
        user=User(
            totalSalary=TotalSalary(**user_data["totalSalary"]),
            transactions=convert_transactions(user_data["transactions"])
        )
    )

# Path to your JSON file
file_path = 'input.json'

# Parse the JSON file
parsed_data = parse_json_from_file(file_path)



import os
from openai import AzureOpenAI



client = AzureOpenAI(
  azure_endpoint = "https://rbro-openai-hackatlon.openai.azure.com/openai/deployments/gpt-4o/chat/completions?api-version=2024-08-01-preview", # insert the provided endpoint here 
api_key = os.getenv("OPENAI_API_KEY"), # insert the provided api key here  
  api_version="2024-08-01-preview"
)

import re

def get_string_between_quotes(text):
    # Use regex to find content between single quotes
    match = re.search(r"'(.*?)'", text)
    if match:
        return match.group(1)  # Return the content between the quotes
    return None  # Return None if no match is found

def classify_transaction(transaction_description, client):
    response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
            {"role": "system", "content": "You are a helpful assistant that classifies transactions."},
            {"role": "user", "content": f"Classify the following transaction into one of these categories: 'Healthcare', 'Education','FoodAndDrinks', 'RestaurantsOrCoffeShops 'Shopping', 'Transport', 'Bills', 'Transfer', 'Entertainment'.\n\nTransaction: {transaction_description}"}
        ],
        max_tokens=400,
        temperature=0.2,
)
    return response.choices[0].message.content

from Spendings import Spendings


cheltuieli = Spendings()

cheltuieli.salary = parsed_data.user.totalSalary.amount


for tx in parsed_data.user.transactions.booked:
    category = None
    while True:
        category = classify_transaction(tx.creditorName, client)
        if(get_string_between_quotes(category) != None):
            break
    print(f"Transaction: {tx.creditorName} -> Category: {get_string_between_quotes(category)}")
    # tx.transaction_amount.currency

    cheltuieli.add_to_field(get_string_between_quotes(category), (float)(tx.transactionAmount.amount))


cheltuieli.free = cheltuieli.salary - cheltuieli.totalSpent

print(cheltuieli.free)


print(cheltuieli.str())
cheltuieli.update_percentages()
print(cheltuieli.percentages_str())


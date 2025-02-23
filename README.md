# Currency_conversion-Tool-Python

import requests
import json
import sys
from pprint import pprint

# Replace with your own API key (store it securely!)
API_KEY = "33ec7c73f8a4eb6b9b5b5f95118b2275"
url = f"http://data.fixer.io/api/latest?access_key={API_KEY}"

# Fetch exchange rate data
response = requests.get(url)
data = response.json()

# Check if API request was successful
if not data.get("success"):
    print("Error fetching exchange rates. Please check your API key.")
    sys.exit()

fx = data["rates"]

currencies = {c.split(" : ")[0]: c for c in [
    "USD : US Dollar",
    "EUR : Euro",
    "GBP : British Pound",
    "INR : Indian Rupee",
    "AUD : Australian Dollar",
    "CAD : Canadian Dollar",
    "JPY : Japanese Yen",
    "CNY : Chinese Yuan Renminbi",
    "NZD : New Zealand Dollar",
    "SGD : Singapore Dollar",
    "CHF : Swiss Franc",
    "ZAR : South African Rand",
    "SEK : Swedish Krona",
    "NOK : Norwegian Krone",
    "MXN : Mexican Peso",
    "HKD : Hong Kong Dollar",
]}  # You can expand this list


def convert_currency():
    while True:
        query = input(
            "Enter amount, from currency, to currency (e.g., '100 USD EUR').\n"
            "Type 'SHOW' to list available currencies or 'Q' to quit: "
        ).strip().upper()
 if query == "Q":
            print("Goodbye!")
            sys.exit()
   elif query == "SHOW":
            pprint(list(currencies.values()))
            continue

   try:
            qty, fromC, toC = query.split()
            qty = float(qty)

   if fromC not in fx or toC not in fx:
                print("Invalid currency code. Try again.")
                continue

  amount = round(qty * fx[toC] / fx[fromC], 2)
            print(f"{qty} {fromC} = {amount} {toC}")

 except ValueError:
            print("Invalid input                 format. Use: '100 USD EUR'.")

  except KeyError:
            print("Currency not found. Try again.")


# Run the function
convert_currency()

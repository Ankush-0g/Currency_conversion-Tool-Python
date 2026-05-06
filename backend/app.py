import requests
import time
import traceback
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Cache configuration
rates_cache = {"data": None, "timestamp": 0}
CACHE_TTL = 600  # 10 minutes

# Hardcoded fallback rates (updated approximately)
FALLBACK_RATES = {
    "USD": 1.0,
    "EUR": 0.92,
    "GBP": 0.79,
    "INR": 83.12,
    "AUD": 1.52,
    "CAD": 1.36,
    "JPY": 149.85,
    "CNY": 7.24,
    "NZD": 1.62,
    "SGD": 1.34,
    "CHF": 0.88,
    "ZAR": 18.73,
    "SEK": 10.45,
    "NOK": 10.62,
    "MXN": 17.10,
    "HKD": 7.82,
}

# Available currencies (must match keys in the rates)
CURRENCY_NAMES = {
    "USD": "US Dollar",
    "EUR": "Euro",
    "GBP": "British Pound",
    "INR": "Indian Rupee",
    "AUD": "Australian Dollar",
    "CAD": "Canadian Dollar",
    "JPY": "Japanese Yen",
    "CNY": "Chinese Yuan Renminbi",
    "NZD": "New Zealand Dollar",
    "SGD": "Singapore Dollar",
    "CHF": "Swiss Franc",
    "ZAR": "South African Rand",
    "SEK": "Swedish Krona",
    "NOK": "Norwegian Krone",
    "MXN": "Mexican Peso",
    "HKD": "Hong Kong Dollar",
}


def fetch_rates_from_api(url):
    """Try to fetch rates from a given URL. Returns dict or raises."""
    resp = requests.get(url, timeout=10)
    data = resp.json()
    if "rates" not in data:
        raise Exception("Response missing 'rates'")
    return data["rates"]


def get_rates():
    """Return live rates if possible, otherwise fallback to hardcoded rates."""
    now = time.time()
    # If cache is still valid, return it
    if rates_cache["data"] and (now - rates_cache["timestamp"]) < CACHE_TTL:
        return rates_cache["data"]

    # Attempt multiple free APIs
    apis = [
        "https://api.exchangerate-api.com/v4/latest/USD",
        "https://open.er-api.com/v6/latest/USD",
    ]

    for api_url in apis:
        try:
            rates = fetch_rates_from_api(api_url)
            rates_cache["data"] = rates
            rates_cache["timestamp"] = now
            print(f"✅ Rates fetched from {api_url}")
            return rates
        except Exception as e:
            print(f"⚠️ API {api_url} failed: {e}")
            traceback.print_exc()
            continue

    # All APIs failed – use fallback
    print("❌ All external APIs failed. Using fallback rates (offline mode).")
    rates_cache["data"] = FALLBACK_RATES
    rates_cache["timestamp"] = now
    return FALLBACK_RATES


@app.route("/api/currencies", methods=["GET"])
def list_currencies():
    """Return the list of supported currencies."""
    cur_list = [{"code": code, "name": name} for code, name in CURRENCY_NAMES.items()]
    return jsonify(cur_list)


@app.route("/api/convert", methods=["GET"])
def convert():
    """Convert amount from one currency to another."""
    # Get parameters safely without chaining .upper() on None
    amount = request.args.get("amount", type=float)
    from_cur = request.args.get("from", type=str)
    to_cur = request.args.get("to", type=str)

    # Validate presence of all parameters
    if not all([amount, from_cur, to_cur]):
        return jsonify({"error": "Missing parameters. Use amount, from, to."}), 400

    # Additional validation
    if amount <= 0:
        return jsonify({"error": "Amount must be positive."}), 400

    # Now it's safe to uppercase
    from_cur = from_cur.upper()
    to_cur = to_cur.upper()

    if from_cur not in CURRENCY_NAMES or to_cur not in CURRENCY_NAMES:
        return jsonify({"error": "Invalid currency code."}), 400

    # Fetch rates (live or fallback)
    try:
        rates = get_rates()
    except Exception as e:
        return jsonify({"error": f"Failed to fetch exchange rates: {str(e)}"}), 502

    # Final validation: ensure the currencies exist in the rates we got
    if from_cur not in rates or to_cur not in rates:
        return jsonify({"error": "Currency not supported by current rates."}), 400

    # Perform conversion
    converted = round(amount * (rates[to_cur] / rates[from_cur]), 2)
    rate = round(rates[to_cur] / rates[from_cur], 6)

    return jsonify({
        "amount": amount,
        "from": from_cur,
        "to": to_cur,
        "result": converted,
        "rate": rate
    })


if __name__ == "__main__":
    app.run(debug=True, port=5000)
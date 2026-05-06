# 💱 Currency Converter

A full-stack currency converter web application with a **Python (Flask) backend** and a **vanilla HTML/CSS/JavaScript frontend**. The backend fetches live exchange rates from free APIs and falls back to hardcoded rates if offline, ensuring the converter always works.



## Features

- Convert between 16 major currencies (USD, EUR, GBP, INR, AUD, CAD, JPY, CNY, NZD, SGD, CHF, ZAR, SEK, NOK, MXN, HKD)
- Live exchange rates from multiple free, no-key APIs
- Automatic fallback to offline rates when the internet is unavailable
- In‑memory caching to stay within API rate limits
- Simple, responsive UI with dropdowns for currency selection
- Error handling for invalid inputs and network issues
- Cross‑origin resource sharing (CORS) enabled


  

## Tech Stack

| Layer      | Technology                |
|------------|---------------------------|
| Backend    | Python, Flask, Flask‑CORS |
| Frontend   | HTML5, CSS3, JavaScript (vanilla) |
| APIs used  | [ExchangeRate-API](https://www.exchangerate-api.com/), [Open ER API](https://open.er-api.com/) |
| Caching    | Python dictionary with TTL (10 min) |



## Project Structure

currency-converter/
├── backend/
│   ├── app.py              # Flask API server
│   └── requirements.txt    # Python dependencies
├── frontend/
│   └── index.html          # User interface
└── README.md




## Getting Started

### Prerequisites

- Python 3.7 or higher
- pip
- A modern web browser (Chrome, Firefox, Edge, etc.)


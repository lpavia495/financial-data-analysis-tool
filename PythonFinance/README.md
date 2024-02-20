# Financial Data Analysis Tool

This Flask application provides an interactive way to visualize and analyze financial data for S&P 500 companies. Users can select a stock symbol from the S&P 500 list, and the application will display various financial indicators including Closing Price, Relative Strength Index (RSI), Volatility, and Trading Volume.

## Features

- **Stock Data Fetching**: Fetches historical stock data using the `yfinance` API.
- **Data Visualization**: Generates and displays plots for closing prices, RSI, volatility, and trading volume.
- **Search Functionality**: Allows users to filter through the S&P 500 stock symbols.
- **Responsive Design**: Adapts to different screen sizes for an optimal viewing experience.

## Installation

Run this command to install all packages:
pip install -r requirements.txt

To start, type this into terminal at correct directory:
python -u app.py
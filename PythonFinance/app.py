from flask import Flask, render_template, request
from datetime import datetime, timedelta
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

# Define the function to fetch stock data
def fetch_stock_data(stock_symbol):
    # Calculate the date range for exactly one year
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)

    # Format dates in YYYY-MM-DD format
    start_date_str = start_date.strftime('%Y-%m-%d')
    end_date_str = end_date.strftime('%Y-%m-%d')

    # Fetch historical data for the stock
    data = yf.download(stock_symbol, start=start_date_str, end=end_date_str)
    return data

def get_sp500_symbols():
    table = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    sp500 = table[0]  # The first table is typically the S&P 500 list
    return sp500['Symbol'].tolist()

@app.route('/')
def index():
    sp500_symbols = get_sp500_symbols()
    return render_template('index.html', symbols=sp500_symbols)

@app.route('/analyze', methods=['POST'])
def analyze():
    symbol = request.form['symbol']
    data = fetch_stock_data(symbol)  # Use the function to fetch stock data
    imgs = create_plots(data)  # Function to create and return plot images
    return render_template('analysis.html', symbol=symbol, imgs=imgs)

def create_plots(data):
    plots = {}

    # Calculate additional metrics for the plots
    data['RSI'] = calculate_rsi(data)
    data['Volatility'] = data['Close'].pct_change().rolling(window=20).std() * (252 ** 0.5)
    data['20_day_ma'] = data['Close'].rolling(window=20).mean()

    # Plot for Closing Prices
    plt.figure(figsize=(10, 5))
    plt.plot(data['Close'], label='Close Price')
    plt.plot(data['20_day_ma'], label='20-Day Moving Average')
    plt.title('Closing Price and Moving Average')
    plt.legend()
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    plots['close_price'] = base64.b64encode(buf.getvalue()).decode('utf8')

    # Plot for RSI
    plt.figure(figsize=(10, 5))
    plt.plot(data['RSI'])
    plt.axhline(70, linestyle='--', alpha=0.5, color='red')
    plt.axhline(30, linestyle='--', alpha=0.5, color='green')
    plt.title('Relative Strength Index')
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    plots['rsi'] = base64.b64encode(buf.getvalue()).decode('utf8')

    # Plot for Volatility
    plt.figure(figsize=(10, 5))
    plt.plot(data['Volatility'])
    plt.title('Volatility (20-day rolling std dev)')
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    plots['volatility'] = base64.b64encode(buf.getvalue()).decode('utf8')

    # Plot for Volume
    plt.figure(figsize=(10, 5))
    plt.bar(data.index, data['Volume'], color='gray')
    plt.title('Trading Volume')
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    plots['volume'] = base64.b64encode(buf.getvalue()).decode('utf8')

    plt.close('all')  # Close all the figures to free memory
    return plots

def calculate_rsi(data, window=14):
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()

    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

if __name__ == '__main__':
    app.run(debug=True)

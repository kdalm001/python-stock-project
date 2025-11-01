import yfinance as yf
import pandas as pd
import time
import os

# --- 1. Define the High-Performance Stock Tickers ---
# NOTE: This is a curated list of tickers that have shown high returns in recent years.
# In a real-world financial application, this list would be dynamically generated
# using a stock screener API based on a specific ROI formula (e.g., 1-year total return).
TOP_PERFORMERS = [
    'NVDA',  # NVIDIA
    'TSLA',  # Tesla
    'MSFT',  # Microsoft
    'GOOGL', # Alphabet (Google)
    'AMZN',  # Amazon
    'AAPL',  # Apple
    'AMD',   # Advanced Micro Devices
    'PLTR',  # Palantir Technologies
    'META',  # Meta Platforms (Facebook)
    'COST'   # Costco Wholesale
]

def clear_console():
    """Clears the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def get_real_time_prices(tickers):
    """
    Fetches the latest stock information using the yfinance Ticker module.
    
    Args:
        tickers (list): A list of stock ticker symbols (e.g., ['NVDA', 'TSLA']).
        
    Returns:
        pandas.DataFrame: A DataFrame with the current price, previous close, and daily change.
    """
    data = []
    
    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            # Fetch latest price data for the current trading day
            history = stock.history(period="1d", interval="1m")
            
            # Check if market is open and data is available
            if history.empty:
                # Use regularMarketPrice if available for off-hours data
                info = stock.info
                current_price = info.get('regularMarketPrice')
                previous_close = info.get('regularMarketPreviousClose')
            else:
                # Get the latest price from the minute-interval data
                current_price = history['Close'].iloc[-1]
                previous_close = history['Close'].iloc[0] # Using the Open of the day as previous close reference
            
            if current_price and previous_close:
                # Calculate the daily change in percentage
                change_percent = ((current_price - previous_close) / previous_close) * 100
            else:
                current_price, previous_close, change_percent = 'N/A', 'N/A', 'N/A'
                
            data.append({
                'Ticker': ticker,
                'Current Price (USD)': f"${current_price:.2f}" if isinstance(current_price, float) else current_price,
                'Daily Change (%)': f"{change_percent:.2f}%" if isinstance(change_percent, float) else change_percent,
            })
            
        except Exception as e:
            data.append({
                'Ticker': ticker,
                'Current Price (USD)': 'Error',
                'Daily Change (%)': 'Error',
            })
            # print(f"Error fetching data for {ticker}: {e}") # Uncomment for debugging

    # Create and sort the DataFrame
    df = pd.DataFrame(data)
    
    # Attempt to sort by Daily Change, handling 'N/A' and 'Error'
    # For portfolio display, sorting by a key metric is a great feature
    try:
        df['Sort_Key'] = df['Daily Change (%)'].str.replace('%', '').replace('N/A', '-999').replace('Error', '-1000').astype(float)
        df = df.sort_values(by='Sort_Key', ascending=False).drop(columns=['Sort_Key'])
    except:
        pass # If sorting fails, just display the unsorted data
        
    return df

def main():
    """Main function to run the stock tracker loop."""
    interval = 10 # Update every 10 seconds
    
    try:
        while True:
            clear_console()
            
            print("🚀 Real-Time Top Performer Stock Tracker (Simulated)")
            print("-----------------------------------------------------")
            print(f"Last Updated: {time.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"Update Interval: {interval} seconds\n")
            
            # Fetch and display the data
            stock_data_df = get_real_time_prices(TOP_PERFORMERS)
            print(stock_data_df.to_markdown(index=False)) # Use markdown for neat console display
            
            time.sleep(interval)
            
    except KeyboardInterrupt:
        print("\n\nTracker stopped by user. Thank you for using the Stock Tracker!")

if __name__ == "__main__":
    main()
import time

import matplotlib.pyplot as plt
import requests
import pandas as pd
from io import StringIO
print('*********************************************************************************************************************')
print('                                 WELCOME TO THE STOCK ANALYSIS PROGRAM ')
print('It’s important to consider additional factors in conjunction with this analysis to make informed trading decisions.')
print('**********************************************************************************************************************')
time.sleep(2)

def user_inputs():
 stock_name = input("Enter stock symbol (e.g. AAPL): ")
 print(f"{stock_name} data is being retrieved...")
 month = input("Enter month to retrieve data from (e.g. 2009-01): ")
 api_key = '5HLSV8QII2XLZ9Y2'
 url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={stock_name}&interval=60min&apikey={api_key}&month={month}&datatype=csv'
 response = requests.get(url)
 return stock_name, month, response


def check_response(response,stock_name,month):
 if response.status_code == 200:
    data = pd.read_csv(StringIO(response.text))
    print("Data retrieved successfully:")
    print(data)
 else:
    print(f"Data retrieval failed for {stock_name} in {month}. Please check the stock symbol and date format.")

def decision(response,stock_name):
 decision = input("Would you like to know if investing in this stock at the time would have been a good decision? (YES/NO):" ).upper()
 if decision == 'NO':
    print("Thank you for using the program.")
 elif decision == 'YES':
    print("")
    time.sleep(5)
    if response.status_code == 200:
        data = pd.read_csv(StringIO(response.text))
        data.columns = data.columns.str.lower()
        #'Typical Price' (average of high, low, and close)
        data['typical_price'] = (data['high'] + data['low'] + data['close']) / 3
        # VWAP calculation
        data['price_volume'] = data['typical_price'] * data['volume']  # Price * Volume
        cumulative_vwap = data['price_volume'].cumsum() / data['volume'].cumsum()
        data['vwap'] = cumulative_vwap
        print(data[['timestamp', 'vwap']])
        if data['vwap'].iloc[-1] > data['vwap'].iloc[-2]:
          print("Good indicator to invest in stock at the time based on VMAP.")
          visuals(data, stock_name)
        else:
            print("Not ideal time to invest based on VWAP")
    else:
        print("Failed to retrieve data")
 else:
    print("Invalid input.")

def visuals(data, stock_name):
    plt.figure(figsize=(10, 7))
    plt.plot(data['timestamp'], data['vwap'], label='VWAP', color='red')
    plt.xlabel('Date')
    plt.ylabel('VWAP')
    plt.title(f'{stock_name} VWAP Trend')
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
def outro():
 time.sleep(4)
 print('*********************************************************************************************************************')
 print('                               THANK YOU FOR USING THE STOCK ANALYSIS PROGRAM')
 print('It’s important to consider additional factors in conjunction with this analysis to make informed trading decisions.')
 print('**********************************************************************************************************************')


def main():
    stock_name, month, response = user_inputs()
    check_response(response, stock_name, month)
    decision(response, stock_name)
    outro()

if __name__ == "__main__":
    main()


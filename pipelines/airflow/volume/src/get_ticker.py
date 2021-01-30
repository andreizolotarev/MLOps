import pandas as pd
import os
import time
import yfinance as yf
import argparse

def cli_args():
    """Return input argument/s for a script via CLI."""
    parser = argparse.ArgumentParser()
    parser.add_argument('-o_f', '--output_folder', type=str, default='data/',
                        help='Define the name for the output folder')
    parser.add_argument('-t_n', '--ticker_name', type=str, default='MSFT',
                        help="Ticker name")
    parser.add_argument('-i', '--interval', type=str, default='60m',
                        help="Interval for ticker values")
    parser.add_argument('-d_t', '--date_time', type=str, default='2021-01-01',
                        help="Date time in format 2020-01-01")
    return parser.parse_args()

def download_ticker(ticker_name: str,
                    date_time: str,
                    interval: str,
                    output_folder: str) -> None:
    df = yf.download(tickers=ticker_name,
                     start=date_time,
                     end=(pd.to_datetime(date_time)+pd.DateOffset()).strftime('%Y-%m-%d'),
                     interval=interval,
                     progress=False)
    if not df.empty:
        df.index = pd.to_datetime(df.index, format='%Y-%m-%d').strftime('%Y-%m-%d %H:%M:%S')
        df['Avg'] = df[['High', 'Low']].mean(axis=1)
        out_path = f'{output_folder}/{ticker_name}/df/{ticker_name}_{date_time}.csv'
        os.makedirs(out_path.rsplit('/', 1)[0], exist_ok=True)
        df.to_csv(out_path)
        print(f'Saved: {out_path}')

    
if __name__ == "__main__":
    args = cli_args()
    download_ticker(ticker_name=args.ticker_name,
                    date_time=args.date_time,
                    interval=args.interval,
                    output_folder=args.output_folder)
	
'''    
python get_ticker.py --ticker_name AAPL \
                 --date_time 2020-10-12 \
                 --interval 60m \
                 --output_folder ./data
'''

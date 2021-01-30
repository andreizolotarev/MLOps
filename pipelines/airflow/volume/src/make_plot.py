import pandas as pd
import os
import time
import matplotlib.pyplot as plt
import argparse

def cli_args():
    """Return input argument/s for a script via CLI."""
    parser = argparse.ArgumentParser()
    parser.add_argument('-o_f', '--output_folder', type=str, default='data/',
                        help='Define the name for the output folder')
    parser.add_argument('-t_n', '--ticker_name', type=str, default='MSFT',
                        help="Ticker name")
    parser.add_argument('-d_t', '--date_time', type=str, default='2021-01-01',
                        help="Date time in format 2020-01-01")
    return parser.parse_args()


def make_plot(ticker_name: str,
              output_folder: str,
              date_time: str) -> None:
    in_path = f'{output_folder}/{ticker_name}/df/{ticker_name}_{date_time}.csv'
    df = pd.read_csv(in_path,
                     index_col='Unnamed: 0')
    plt.figure(figsize=(12, 6))
    plt.plot(df.index, df['High'], c='blue')
    plt.plot(df.index, df['Avg'], c='red')
    plt.plot(df.index, df['Low'], c='blue')
    plt.title(f'{ticker_name} {date_time}\nDaily plot', fontsize=18)
    plt.xlabel('Date', fontsize=14)
    plt.xticks(rotation=90)
    plt.ylabel('Value', fontsize=14)
    plt.legend(['High, Low', 'Avg'])
    plt.grid(True)
    out_path = f'{output_folder}/{ticker_name}/plot/{ticker_name}_{date_time}.png'
    os.makedirs(out_path.rsplit('/', 1)[0], exist_ok=True)
    plt.savefig(out_path, bbox_inches='tight')
    print(f'Saved: {out_path}')
    
if __name__ == "__main__":
    args = cli_args()
    make_plot(ticker_name=args.ticker_name,
              output_folder=args.output_folder,
              date_time=args.date_time)
	
'''    
python make_plot.py --ticker_name AAPL \
                 --date_time 2020-10-12 \
                 --output_folder ./data
'''

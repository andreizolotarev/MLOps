'''
WORKFLOW MANAGEMENT WITH LUIGI
'''
import logging
import datetime
import pandas as pd
import numpy as np
import os
import time
import luigi
import yfinance as yf
import matplotlib.pyplot as plt
import argparse

logging.basicConfig(filename='pipeline_log.log', level=logging.INFO)
logger = logging.getLogger()
fh = logging.FileHandler('pipeline_log.log', 'w')
ff = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(message)s')
fh.setFormatter(ff)
logger.addHandler(fh)

def cli_args():
    """Return input argument/s for a script via CLI."""
    parser = argparse.ArgumentParser()
    parser.add_argument('-d_d', '--data_dir', type=str, default='data/',
                        help='Define the name for the output folder')
    parser.add_argument('-t_n', '--ticker_name', type=str, default='MSFT',
                        help="Ticker name")
    parser.add_argument('-s_d', '--start_date', type=str, default='2020-06-06',
                        help="Starting date")
    parser.add_argument('-w', '--workers', type=int, default=4,
                        help="N of workers")
    return parser.parse_args()

def dates_to_do(ticker_name='MSFT', start_date='2021-01-01'):
    df = yf.download(ticker_name, start=start_date)
    dates = [i.strftime('%Y-%m-%d') for i in list(df.index)]
    return dates[7:]

def prepare_df(df, ticker_name, output_path, date):
    df = df[df.index<=date]
    df = df[-7:]
    df['Avg'] = df[['High', 'Low']].mean(axis=1)
    os.makedirs(output_path.rsplit('/', 1)[0], exist_ok=True)
    df.to_csv(output_path)


def line_plot(df, ticker_name, output_path, date):
    plt.figure(figsize=(12, 6))
    plt.plot(df.index, df['High'], c='blue')
    plt.plot(df.index, df['Avg'], c='red')
    plt.plot(df.index, df['Low'], c='blue')
    plt.title(f'{ticker_name}\n7days plot', fontsize=18)
    plt.xlabel('Date', fontsize=14)
    plt.xticks(rotation=90)
    plt.ylabel('Value', fontsize=14)
    plt.legend(['High, Low', 'Avg'])
    plt.grid(True)
    os.makedirs(output_path.rsplit('/', 1)[0], exist_ok=True)
    plt.savefig(output_path, bbox_inches='tight')


class PrepareDataframe(luigi.Task):
    '''
    Prepare a df for further plotting
    '''
    logger.info('class PrepareDataframe')
    item = luigi.Parameter()

    def output(self):
        return luigi.LocalTarget(f'{DATA_DIR}{TICKER_NAME}/{self.item}/{self.item}.csv')

    def run(self):
        prepare_df(df=yf.download(TICKER_NAME, start=START),
                   ticker_name=TICKER_NAME,
                   output_path=self.output().path,
                   date=self.item)
        

class MakePlot(luigi.Task):
    logger.info('class MakePlot')
    """
    Make a plot
    """
    item = luigi.Parameter()

    def requires(self):
        return PrepareDataframe(item=self.item)

    def output(self):
        return luigi.LocalTarget(f'{DATA_DIR}{TICKER_NAME}/{self.item}/{self.item}.jpg')

    def run(self):

        line_plot(df=pd.read_csv(self.input().path, index_col='Date'),
                  ticker_name=TICKER_NAME,
                  output_path=self.output().path,
                  date=self.item)


class FullPipeline(luigi.WrapperTask):
    logger.info('FullPipeline')
    '''
    This is a wrapper luigi task, use it when there is no output
    '''
    def requires(self):
        return [MakePlot(item=date) for date in dates_to_do(ticker_name=TICKER_NAME, start_date=START)]


if __name__ == "__main__":
    args = cli_args()
    DATA_DIR = args.data_dir
    TICKER_NAME = args.ticker_name
    START = args.start_date
    WORKERS = args.workers
    start_time = time.time()
    luigi.build([FullPipeline()], workers=WORKERS)
    elapsed_time = time.time() - start_time
    logger.info(f'Elapsed time: {elapsed_time}')
    
# python pipeline.py --workers 14 --ticker_name AAPL --start_date 2020-10-10

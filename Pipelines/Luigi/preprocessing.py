'''
WORKFLOW MANAGEMENT WITH LUIGI
'''

import logging
import datetime
import requests
import boto3
from zipfile import ZipFile
import pandas as pd
import numpy as np
import os
import time
import luigi
from sklearn.model_selection import train_test_split

DATA_DIR = 'data/'
URL = 'https://mlstud.s3-us-west-2.amazonaws.com/task4/data/'


logging.basicConfig(filename='test_log.log', level=logging.INFO)
logger = logging.getLogger()
fh = logging.FileHandler('test_log.log', 'w')
ff = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(message)s')
fh.setFormatter(ff)
logger.addHandler(fh)


def save_df(df_in, df_path):
    df_in.to_csv(df_path, sep=';', index=False)


def get_bucket_list(bucketname='mlstud'):
    '''
    This function returns list of items from the bucket
    based on condition
    '''
    s3 = boto3.resource('s3')
    my_bucket = s3.Bucket(bucketname)
    prefix = 'task4/data/'
    buck_list = [file.key.replace('task4/data/', '')
                 for file in my_bucket.objects.filter(Prefix=prefix)]
    buck_list = list(filter(None, buck_list))
    final = [s for s in buck_list if len(s) > 15]
    return final


class DownloadData(luigi.Task):
    """
    Download raw dataset
    """
    logger.info('class DownloadData')
    item_name = luigi.Parameter()
    folder_name = luigi.Parameter(default='zips/')

    def output(self):
        res = f'{DATA_DIR}{self.folder_name}{self.item_name}'
        return luigi.LocalTarget(res, luigi.format.Nop)

    def run(self):
        file_zip = requests.get(f'{URL}{self.item_name}')
        with self.output().open('wb') as new_file:
            new_file.write(file_zip.content)


class UnzipData(luigi.Task):
    '''
    Unzip items
    '''
    logger.info('class UnzipData')
    item = luigi.Parameter()
    folder_name = luigi.Parameter(default='csv/')

    def requires(self):
        return DownloadData(self.item)

    def output(self):
        n = self.item.replace('.zip', '')
        return luigi.LocalTarget(f'{DATA_DIR}{self.folder_name}{n}.csv')

    def run(self):
        with ZipFile(self.input().path, 'r') as f:
            for filename in f.namelist():
                f.extract(filename, f'{DATA_DIR}{self.folder_name}')


class MergeData(luigi.Task):
    '''
    Join all dfs into one
    '''
    logger.info('class MergeData')
    items = luigi.ListParameter()
    folder_name = luigi.Parameter(default='final/')

    def requires(self):
        return [UnzipData(item=i) for i in self.items]

    def output(self):
        return luigi.LocalTarget(f'{DATA_DIR}{self.folder_name}merged_df.csv')

    def run(self):
        os.makedirs(f'{DATA_DIR}{self.folder_name}', exist_ok=True)

        df_first = pd.read_csv(self.input()[0].path, delimiter=';')

        for i in self.input()[1:]:

            # print(i.path)
            df_in = str(i.path)
            df_new = pd.read_csv(df_in, delimiter=';')
            df_first = df_first.append(df_new, ignore_index=True)
        save_df(df_first, self.output().path)


class BasicPreprocessing(luigi.Task):

    '''
    Basic preprocessing 
    '''
    logger.info('class BasicPreprocessing')
    items = luigi.ListParameter()
    item_name = luigi.Parameter(default='preprocessed.csv')
    folder_name = luigi.Parameter(default='final/')

    def requires(self):
        return MergeData(self.items)

    def output(self):
        return luigi.LocalTarget(f'{DATA_DIR}{self.folder_name}{self.item_name}')

    def run(self):
        # Read data
        df_1 = pd.read_csv(self.input().path, sep=';')

        # Get rid off commas within df
        for i in df_1.iloc[:, 2:]:
            df_1[i] = df_1[i].replace(',', '.', regex=True).astype('float64')

            # Combine 'Date' and 'Time'
        df_combined = df_1['Date'].str.cat(df_1['Time'], sep=' ')

        # Create new column with right datetime format
        df_1['DateTime'] = pd.to_datetime(
            df_combined, format='%d/%m/%Y %H.%M.%S')

        # Drop columns 'Date' & 'Time', because we don't need them anymore
        df_1.drop(columns=['Date', 'Time'], inplace=True)

        # Convert -200 to NANs
        df_1.replace(to_replace=-200, value=np.NaN, inplace=True)

        # Drop columns with high share (90%) of NANs
        df_1 = df_1.loc[:, df_1.isna().mean() < 0.9]

        # Name target column explicitly
        df_1 = df_1.rename(columns={'C6H6(GT)': 'Target'})

        # Drop NANs from target
        df_1.dropna(subset=['Target'], inplace=True)

        # Sort by DateTime
        df_1.sort_values(by=['DateTime'], inplace=True)

        os.makedirs(f'{DATA_DIR}{self.folder_name}', exist_ok=True)
        save_df(df_1, self.output().path)


class SplitData(luigi.Task):
    logger.info('class SplitData')
    """
    Split dataset
    """
    items = luigi.ListParameter()
    folder_name = luigi.Parameter(default='final/')

    def requires(self):
        return BasicPreprocessing(self.items)

    def output(self):
        return [luigi.LocalTarget(f'{DATA_DIR}{self.folder_name}train_df.csv'),
                luigi.LocalTarget(f'{DATA_DIR}{self.folder_name}test_df.csv')]

    def run(self):

        df_before = pd.read_csv(self.input().path, sep=';')

        # Split
        train_df, test_df = train_test_split(df_before, test_size=0.25,
                                             random_state=0, shuffle=False)

        train_df.to_csv(self.output()[0].path, sep=';', index=False)
        test_df.to_csv(self.output()[1].path, sep=';', index=False)


class FullPipeline(luigi.WrapperTask):
    logger.info('FullPipeline')
    '''
    This is a wrapper luigi task, that's why there is no output
    '''

    def requires(self):
        items = get_bucket_list()
        return SplitData(items)


if __name__ == "__main__":
    start_time = time.time()
    luigi.run()
    elapsed_time = time.time() - start_time
    logger.info(f'Elapsed time: {elapsed_time}')


# python preprocessing.py FullPipeline --local-scheduler
# luigid --background --logdir tmp --port 12345
# python preprocessing.py FullPipeline --workers 20

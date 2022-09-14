import logging
import time
import requests
from io import StringIO

import glob
import tqdm
import numpy as np
import pandas as pd

COL_NAMES = '''C/A,UNIT,SCP,
DATE1,TIME1,DESC1,ENTRIES1,EXITS1,DATE2,TIME2,DESC2,ENTRIES2,EXITS2,
DATE3,TIME3,DESC3,ENTRIES3,EXITS3,DATE4,TIME4,DESC4,ENTRIES4,EXITS4,
DATE5,TIME5,DESC5,ENTRIES5,EXITS5,DATE6,TIME6,DESC6,ENTRIES6,EXITS6,
DATE7,TIME7,DESC7,ENTRIES7,EXITS7,DATE8,TIME8,DESC8,
ENTRIES8,EXITS8'''.replace('\n', '').split(',')

def _get_links_to_raw_data(links=None):
    """Prepares `list of links` to access the dataset stored online,
        Storage is here web.mta.info/developers/turnstile.html ,
        files are Saturday to Saturday.

    Parameters
    links : list
        Custom list of links which to reach with `get` requests to access data
    ----------
    """

    if links is None: # if no links provided, use hardcoded list
        links = ['http://web.mta.info/developers/data/nyct/turnstile/turnstile_130105.txt',
                 'http://web.mta.info/developers/data/nyct/turnstile/turnstile_130112.txt',
                 'http://web.mta.info/developers/data/nyct/turnstile/turnstile_130119.txt',
                 'http://web.mta.info/developers/data/nyct/turnstile/turnstile_130126.txt',
                 'http://web.mta.info/developers/data/nyct/turnstile/turnstile_130202.txt',
                 'http://web.mta.info/developers/data/nyct/turnstile/turnstile_130209.txt',
                 'http://web.mta.info/developers/data/nyct/turnstile/turnstile_130216.txt',
                 'http://web.mta.info/developers/data/nyct/turnstile/turnstile_130223.txt',
                 'http://web.mta.info/developers/data/nyct/turnstile/turnstile_130302.txt',
                 'http://web.mta.info/developers/data/nyct/turnstile/turnstile_130309.txt',
                 'http://web.mta.info/developers/data/nyct/turnstile/turnstile_130316.txt',
                 'http://web.mta.info/developers/data/nyct/turnstile/turnstile_130323.txt',
                 'http://web.mta.info/developers/data/nyct/turnstile/turnstile_130330.txt',
                 # 'http://web.mta.info/developers/data/nyct/turnstile/turnstile_121229.txt',
                 'http://web.mta.info/developers/data/nyct/turnstile/turnstile_130406.txt'
                ]

    return links

def download_raw_data(links, download=False):
    """Downloads files from online storage - http://web.mta.info/developers/turnstile.html.
        Returns a list of paths to downloaded files.

    Parameters
    ----------
    links : int
        list of links which to reach with `get` requests to access data
    download : bool
        if true - downloads files, if false - uses existing files from hardcoded raw data folder
    """
    if download:
        path = []
        for indx, link in enumerate(tqdm.tqdm(links, desc='Downloading raw files')):
            try:
                response = requests.get(link)

                path_i = f'./data/raw/{link[-20:]}'
                # response to pd.DataFrame
                response_data = StringIO(response.text)
                response_data_df = pd.read_csv(response_data, sep=',', names=COL_NAMES)
                # save file
                response_data_df.to_csv(path_i)

                path.append(path_i)

            except response.status_code != 200:
                print('Error:', link, response.status_code)

            time.sleep(0.5)

        print(f'Raw files downloaded, {indx} files downloaded')

    else:
        path = glob.glob('./data/raw/turnstile*.txt')
        print(f'Raw files found, {len(path)} files found')

    return path

def reorganize_raw_files(files, custom_parse=True):
    """Transforms (re-orginezes) format of fields of raw pre-2014 files.
        Basicly transform from wide to long table.
        Returns a list of paths to files with transformed format.

    *** NOTE: Data provider changed format of data set after 10/18/14
        from one-wide-row-for-eight-audits to one-row-for-one-audit ***

    We have two ways to do it - with pandas built-in functions or with custom-written  'parser'.
        Custom parses performs about 10% faster on my tests, but it is custom

    Parameters
    ----------
    files : list
        list of raw files which to reach and read to transform dataset format
    custom_parse : bool
        if true - uses custom function, if false - uses `wide_to_long` built-in function
    """
    columns_target = ['C/A', 'UNIT', 'SCP', 'DATE', 'TIME', 'DESC', 'ENTRIES', 'EXIT']
    path = []

    for indx, file in enumerate(tqdm.tqdm(files, desc='Making long files')):

        # open wide table
        df = pd.read_csv(file, index_col=0)

        if custom:
            # use custom row split
            reshaped_list = []
            for indx, row in df.iterrows():
                row_splited = row.values.tolist()

                row_key_data = row_splited[:3]; del row_splited[:3]
                rows_updating_data = np.reshape(row_splited, (-1, 5)).tolist()

                [reshaped_list.append(row_key_data + row_updating_data) for row_updating_data in rows_updating_data]
                #break
            df = pd.DataFrame(reshaped_list, columns=columns_target)

        else:
            # use wide_to_long method from pandas
            df['id'] = df.index.astype(str) + "-" + df['C/A'] + "-" + df['UNIT'] + "-" + df['SCP']
            #display(df.head(2))

            df = pd.wide_to_long(df,
                            stubnames=['DATE', 'TIME', 'DESC', 'ENTRIES', 'EXITS'],
                            i=['id'],
                            j='row',
                            suffix='.+').reset_index()

            df = df.sort_values(['C/A','UNIT','SCP', 'DATE', 'TIME']).reset_index(drop=True)

            df.drop('id', axis=1, inplace=True)

        # somethimes columns from wide format are not populated for each and every row
        df = df.dropna()
        # save long table
        save_path = file.replace('raw', 'interim').replace('txt', 'csv')
        path.append(save_path)

        df.to_csv(save_path)

    return path

def _concat_files(files, save_path='./data/interim/turnstile_Q1_2013.csv'):
    """Concatenates weekly data-files ('batches') into one big, long table.
        ☆ We might use 'batches' too, but it will require some additional loops & logics every-time
        to access the data and calculate things. On other hand, we already have enough resources
        to work with whole dataset in premier speed.
        ☆ We would need batch-processing staff, as well as a different data-storage model,
        if we had significantly bigger dataset and some tricky modeling goals

        ! Check memory usage. Sometimes garbage collector works wrong with concatenating/unionizing files

    Parameters
    ----------
    files : list
        list of transformed files (batches) which to reach and read to concatenate into big file (table)
    save_path :
        path where to save concatenated table
    df : pd.DataFrame
        temp dataframe behaving as a bone for a concatenating files
    """
    df = pd.DataFrame([])
    for indx, file in enumerate(tqdm.tqdm(files, desc='Concatenating long files')):
        # concat weekly "batches" to big table
        df_small = pd.read_csv(file, index_col=0)
        df = pd.concat([df, df_small], ignore_index=True, axis=0)
        del df_small

    # df = df.sort_values(['C/A','UNIT','SCP', 'DATE', 'TIME']).reset_index(drop=True)
    df.to_csv(save_path)

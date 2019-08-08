#! python3
# COSC 505: Summer 2019
# ProjectC - Group 14
# Damilola Olayinka Akamo
# Nicole Callais
# Shane Christopher Henderson
# Stephen Opeyemi Fatokun
#
# 08/01/2019
import argparse
import pandas as pd
from itertools import product
from urllib.error import URLError

### Code for output ###
#Should expect to get the sequence and the position

### Code for Data Analysis ###
#Need something to check identified patients ailments
def check_Correlations(df,base_string):
    match = False
    base = base_string + 'A'
    for n in range(len(df.dna.iloc[0])-len(base_string)):
        reg_exper = r'(^[AB]{'+str(n)+'}'+base+')'
        ds = df.dna.str.match(reg_exper)
        cnts = ds.value_counts()
        if cnts.get(True) and cnts.get(True) > 2:
            print(reg_exper)
            print(cnts.get(True))
            match = True
    if match:
        check_Correlations(df,base)

    match = False
    base = base_string + 'B'
    for n in range(len(df.dna.iloc[0])-len(base_string)):
        reg_exper = r'(^[AB]{'+str(n)+'}'+base+')'
        ds = df.dna.str.match(reg_exper)
        cnts = ds.value_counts()
        if cnts.get(True) and cnts.get(True) > 2:
            print(reg_exper)
            print(cnts.get(True))
            match = True
    if match:
        check_Correlations(df,base)

### Code for for serving http request and getting data ###
#shende25
def get_dataset(url):
    try:
        df = pd.read_json(url)
    except URLError as e:
        # Catch errors related to the URL
        if hasattr(e, 'reason'):
            print('Connection failed!')
            print('Reason: ', e.reason)

        # Catch errors related to the server
        elif hasattr(e, 'code'):
            print('Server Error!')
            print('Error code: ', e.code)
        return None
    else:
        return df

### Code for parsing input ###
#shende25
def setup():
    parser = argparse.ArgumentParser(description="Scans sample medical data \
            for correlations, input data should be in .JSON format.", \
            add_help=False)
    parser.add_argument('data',metavar='<URL>', nargs=1, \
            type=lambda x: get_dataset(x),\
            help="The url where the data file can be found")
    parser.add_argument('output',metavar='<output file or ->', nargs=1, \
            type=argparse.FileType('w'), \
            help="Location for writing output, '-' will direct to stdout")
    args = parser.parse_args()
    return args.data[0],args.output[0]

### Default usage
#shend25
if __name__ == "__main__":
    df,outfile = setup()
    for x in product('AB',repeat=2):
        check_Correlations(df,''.join(x))

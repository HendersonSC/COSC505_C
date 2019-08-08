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
#Need something to come up with all possible sequences
    #should also end sequences once the become non viable
def check_Correlations(base_string):
    print(base_string)
#Need something to iterate over all positions
#Need something to check identified patients ailments
#Would decrease memory footprint if the output was tied to the search

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
    print(args.output)
    print(args.data,file=args.output[0])
    return args.data,args.output[0]

### Default usage
#shend25
if __name__ == "__main__":
    df,outfile = setup()
    for x in product('AB',repeat=2):
        check_Correlations(''.join(x))

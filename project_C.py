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
from urllib.error import URLError

### Code for Data Analysis ###

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

### Code for output ###



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

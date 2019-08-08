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
import re
from itertools import product
from urllib.error import URLError

ailment_map = {
        "a" : "Pancreatic Cancer",
        "b" : "Breast Cancer",
        "c" : "Lung Cancer",
        "d" : "Lymphoma",
        "e" : "Leukemia",
        "A" : "Gastro-Reflux",
        "B" : "Hyperlipidemia",
        "C" : "High Blood Pressure",
        "D" : "Macular Degeneration"
              }

### Code for output ###
def write_Output(dna,n,all_ids,ailments):
    global outfile
    print(dna,n,all_ids,ailments,file=outfile)

### Code for Data Analysis ###
# This is O(n) on the number of diseases considered
# It is also O(m) on the number of IDs. Total this is O(mn)
def get_Correlations(ids,df):
    global ailment_map
    corr = {}
    for i in ailment_map.keys():
        scratch = {i:[]}
        for j in ids:
            if re.search(i,df.at[j,'emr']):
                scratch[i].append(j)
        pct = len(scratch[i]) / len(ids)
        if pct >= 0.8:
            corr[ailment_map[i]] = {"Significantly Correlated" : scratch[i]}
        elif pct >= 0.6:
            corr[ailment_map[i]] = {"Moderately Correlated" : scratch[i]}
        elif pct >= 0.4:
            corr[ailment_map[i]] = {"Slightly Correlated" : scratch[i]}
    return corr

# This recursively searches the possible sequences of DNA appending to the
# sequence as necessary and aborting the sequence when no matches are found
# Each recurrence of this method is O(n) on dna where n is 120-len(subset)
#    Which does have an n-1 relation between recurrences
# It is also O(m) on matches, since n and m are independent it is O(mn)
def get_Matches(df,base_string):
    # Flag if a match was found
    match = False
    # Append to the search string
    base = base_string + 'A'
    # Loop over available locations
    for n in range(len(df.dna.iloc[0])-len(base_string)):
        # regex on the search string and check for matches
        ds = df.dna.str.match(r'(^[AB]{'+str(n)+'}'+base+')')
        cnts = ds.value_counts()
        # make a container for ids
        ids = []
        if cnts.get(True) and cnts.get(True) > 2:
            # For the matches that were made store ids in the container
            for i in ds.index:
                if ds.get(i):
                    ids.append(i)
            # Send findings to the outputter
            write_Output(base,n,ids,get_Correlations(ids,df))
            match = True
    # Recursion to add to the string
    if match:
        get_Matches(df,base)

    # Flag if a match was found
    match = False
    # Append to the search string
    base = base_string + 'B'
    # Loop over available locations
    for n in range(len(df.dna.iloc[0])-len(base_string)):
        # regex on the search string and check for matches
        ds = df.dna.str.match(r'(^[AB]{'+str(n)+'}'+base+')')
        cnts = ds.value_counts()
        # make a container for ids
        ids = []
        if cnts.get(True) and cnts.get(True) > 2:
            # For the matches that were made store ids in the container
            for i in ds.index:
                if ds.get(i):
                    ids.append(i)
            # Send findings to the outputter
            write_Output(base,n,ids,get_Correlations(ids,df))
            match = True
    # Recursion to add to the string
    if match:
        get_Matches(df,base)

### Code for for serving http request and getting data ###
#shende25
# This operates only on the supplied URL
# O(1)
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
# This is over the arugment list, which is required to be two
# O(2)
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
#shende25
# This has one loop which rolls over the combinations 'AA','AB','BA','BB'
# We will call this O(n) but n is really just 4
if __name__ == "__main__":
    df,outfile = setup()
    for x in product('AB',repeat=2):
        get_Matches(df,''.join(x))

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

### Dictionary for looking up ailments
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

### Function for outputing results
#sfatokun
# Function Analysis:
# Nested for loop.
# First loop is O(n) for the worst case
# Second loop iterates O(m) per n in the first loop
# but m is promised to be 1 in this implementation
# Timing: O(n)
def write_Output(dna,n, all_ids, ailments):
    global outfile
    # Printing the DNA sequence
    print(f'\t\tSequence : {dna:{25}} location : {n:{3}}', file=outfile)
    for disea in ailments:
        for corre in ailments[disea]:
            # Printing the disease and the related correlation
            print(f'{disea:{20}} {corre:{30}}', file=outfile)
            # Identities that correlate to each disease
            print(f'{str(ailments[disea][corre]).strip("[]"):{80}}\n', file=outfile)
    # Printing all IDs associated with the search sequence
    print(f'All IDs with sequence :', file=outfile)
    print(f'{str(all_ids).strip("[]"):{80}}\n\n', file=outfile)

### Code for Data Analysis ###
#dakamo
# This is O(n) on the number of diseases considered
# It is also O(m) on the number of IDs. Total this is O(mn)
# Since the number of diseases is constant, then in a large data set n << m,
# which would be O(m)
def get_Correlations(ids,df):
    global ailment_map
    # Set a container for the return variable -> dictionary makes most sense
    corr = {}
    # Roll through all possible ailments
    for i in ailment_map.keys():
        scratch = {i:[]}
        # Check to see if anyone in the list has that ailment
        for j in ids:
            if re.search(i,df.at[j,'emr']):
                scratch[i].append(j)
        # Select the appropriate correlation and store in the return dictionary
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
#shende25
# Each recurrence of this method is O(n) on dna where n is 120-len(subset)
#    Which does have an n-1 relation between recurrences
# It is also O(m) on matches, since n and m are independent it is O(mn)
# Not sure how to define worst case sense if m=n for O(n^2), and there are no
# duplicates then m=n=1, I think.
def get_Matches(df,base):
    # Flag if a match was found
    match = False
    # Loop over available locations
    for n in range(120-len(base)):
        # regex on the search string and check for matches
        ds = df.dna.str.match(r'(^[AB]{'+str(n)+'}'+base+')')
        cnts = ds.value_counts()
        # make a container for ids
        ids = []
        if cnts.get(True) and cnts.get(True) > 1:
            # For the matches that were made store ids in the container
            for i in ds.index:
                if ds.get(i):
                    ids.append(i)
            # Send findings to the outputter
            write_Output(base,n,ids,get_Correlations(ids,df))
            match = True
    # Recursion to add to the string
    if match:
        get_Matches(df,base+"A")
        get_Matches(df,base+"B")

### Code for for serving http request and getting data ###
#dakamo
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

#### Test function
#ncallais
#O(n) actually n is constant
def test(df):
    if not "emr" in df:
        print ("Error: No 'emr' column.")
        return False
    if not "dna" in df:
        print ("Error: No 'dna' column.")
        return False
    if not (df.dna.str.len() == 120).all():
        print ("DNA sequences do not contain the correct number of values.")
        return False
    if not (df.dna.str.contains('^[AB]{120}$')).all():
        print ("DNA sequences do not contain the correct characters.")
        return False
    return True

### Code for parsing input ###
#shende25
# This is over the arugment list, which is required to be two
# O(n)  n in this case equals 2 for the worst case
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
#ncallais
# This has one loop which rolls over the combinations 'AA','AB','BA','BB'
# We will call this O(n) but n is defined to be 4 and it is done twice
if __name__ == "__main__":
    df,outfile = setup()
    if test(df):
        for x in product('AB',repeat=2):
            get_Matches(df,"".join(x)+"A")
            get_Matches(df,"".join(x)+"B")

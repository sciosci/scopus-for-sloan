""" This is an example of how to implement the modified elsapy module to search authors and papers."""

import pandas as pd
from scopus.scopus import *
from scopus.utils import read_keys


# A sample function that shows how to assemble the query
# Please rewrite the function according to your specific search fields
def assemble_query(file):
    df = pd.read_csv(file)
    subjects = list(df['subjects'])

    # assign indices and names from data source, for naming and tracking results
    names = [[str(i)] for i in range(len(subjects))]
    queries = [
        ' AND '.join([f'SUBJAREA({i})' for i in line.split(',')]) for line in subjects
    ]

    # 'names' is a list of lists
    return names, subjects, queries


if __name__ == '__main__':

    """If you have multiple queries, just read them from a file like csv or json,
        then you can write a loop to search all of them.

        For multiple search fields, their documentation will teach you how to 
        combine different keywords into one query."""

    search = ScopusSearch(
        keys=read_keys('./keys.csv'),
        names=[['scopus', 'test']],
        queries=['AU-ID(6504318313)'],
        subject='scopus'
    )
    search.search()

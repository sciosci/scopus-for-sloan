""" Test cases for author retrieval and abstract retrieval.
    Make sure you have the author ids first. """

import json
from pathlib import Path
from scopus.author_retrieval import retrieve_author
from scopus.abstract_retrieval import retrieve_abstract
from scopus.utils import read_keys, key_generator


keys = read_keys('keys.csv')
authors = [6701368453, 7005699374, 12139841900]  # sample ids

# abstract retrieval
destination = Path('result/abstract')  # specify the result folder
if not destination.exists():
    destination.mkdir(parents=True)
for author in authors:
    filename = destination / f'{str(author)}.json'
    keygen = key_generator(keys[1:])
    retrieve_abstract(author, str(filename), keygen=keygen)


# author retrieval
destination = Path('result/author')
if not destination.exists():
    destination.mkdir(parents=True)
for author in authors:
    filename = destination / f'{str(author)}.json'
    keygen = key_generator(keys[1:])
    retrieve_author(author, str(filename), keygen=keygen)

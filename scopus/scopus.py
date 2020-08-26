import json, os, time
from pathlib import Path

from elsapy.elsclient import ElsClient
from elsapy.elssearch import ElsSearch
from . import log

search_log = log.get_logger('search')
error_log = log.get_logger('error')

class ScopusSearch:
    """Customized Scopus API implementation class"""

    def __init__(self, keys, names, queries, subject='scopus', view='STANDARD'):
        self.keys = keys
        self.subject = subject
        self.view = view

        """self.names are used to name the result files, normally with multiple fields like
            author name and author id, so they are lists"""
        self.names = iter(names)
        self.queries = iter(queries)
        self.length = len(queries)

    def key_generator(self):
        for key in self.keys:
            yield key
        return 'Keys Exhausted'

    def write_json(self, data, name, folder):
        filename = name
        i = 1
        while f'{filename}.json' in os.listdir(folder):
            search_log.info(f'Duplicate file: {filename}')
            filename = f'{filename}-{i}'
            i += 1
        with open(f'{str(folder)}/{filename}.json', 'w') as writer:
            json.dump(data, writer, indent=4)

    def search(self):
        # initialize the keys
        keygen = self.key_generator()
        init_key = next(keygen)

        # Initialize the elsapy client
        client = ElsClient(init_key, view=self.view)
        count = 0

        folder = Path('result') / f'{self.subject}_{time.strftime("%Y%m%d")}'
        if not folder.exists():
            folder.mkdir(parents=True)

        for query in self.queries:

            try:
                name = next(self.names)
                name = '_'.join(name)
            except:
                # this could happen if your file name contains unexpected characters
                error_log.info(f'Name error at {query}.')
                break

            try:
                srch =ElsSearch(query, index=self.subject, keygen=keygen)
                srch.execute(client, get_all=True)
                count += 1
                print(f'Progress: {count}/{self.length}, {query}')
                if srch.status_code == 400:
                    error_log.info(f'Bad query: {name}')
                else:
                    search_log.info(f'Results found: {name}, # of results: {len(srch.results)}')
                    self.write_json(srch.results, name, folder)
            except Exception as e:
                error_log.info(f'Search error: {name}, {str(e)}')

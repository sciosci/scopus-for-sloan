"""The search module of elsapy.
    Additional resources:
    * https://github.com/ElsevierDev/elsapy
    * https://dev.elsevier.com
    * https://api.elsevier.com"""

from . import log_util
from urllib.parse import quote_plus as url_encode
import json

logger = log_util.get_logger(__name__)

class ElsSearch():
    """Represents a search to one of the search indexes accessible
         through api.elsevier.com. Returns True if successful; else, False."""

    # static / class variables
    _base_url = u'https://api.elsevier.com/content/search/'
    _cursored_indexes = [
        'scopus',
    ]

    def __init__(self, query, index, keygen):
        """Initializes a search object with a query and target index."""
        self.query = query
        self.index = index
        self.keygen = keygen
        self.status_code = None
        self._cursor_supported = (index in self._cursored_indexes)
        self._uri = self._base_url + self.index + '?query=' + url_encode(
                self.query)

    # properties
    @property
    def query(self):
        """Gets the search query"""
        return self._query

    @query.setter
    def query(self, query):
        """Sets the search query"""
        self._query = query

    @property
    def index(self):
        """Gets the label of the index targeted by the search"""
        return self._index

    @index.setter
    def index(self, index):
        """Sets the label of the index targeted by the search"""
        self._index = index

    @property
    def results(self):
        """Gets the results for the search"""
        return self._results

    @property
    def tot_num_res(self):
        """Gets the total number of results that exist in the index for
            this query. This number might be larger than can be retrieved
            and stored in a single ElsSearch object (i.e. 5,000)."""
        return self._tot_num_res

    @property
    def num_res(self):
        """Gets the number of results for this query that are stored in the 
            search object. This number might be smaller than the number of 
            results that exist in the index for the query."""
        return len(self.results)

    @property
    def uri(self):
        """Gets the request uri for the search"""
        return self._uri

    def _upper_limit_reached(self):
        """Determines if the upper limit for retrieving results from of the
            search index is reached. Returns True if so, else False. Upper 
            limit is 5,000 for indexes that don't support cursor-based 
            pagination."""
        if self._cursor_supported:
            return False
        else:
            return self.num_res >= 5000

    
    def execute(self, els_client = None, get_all = False):
        """Executes the search. If get_all = False (default), this retrieves
            the default number of results specified for the API. If
            get_all = True, multiple API calls will be made to iteratively get 
            all results for the search, up to a maximum of 5,000."""

        request = els_client.exec_request(self._uri)
        self.status_code = request[1]

        # This part is added by myself for HTTP error handling and key cycling.
        # TODO: the current key cycler generates redundant messages, will try to fix it later
        while not self.status_code == 200:
            # status code 400 represents an invalid query
            if self.status_code == 400:
                return None
            # 401 or 429 is returned when key quota exhausts
            elif self.status_code in [401, 429]:
                try:
                    els_client.api_key = next(self.keygen)
                    request = els_client.exec_request(self._uri)
                    self.status_code = request[1]
                    print(f'Key Switched to {els_client.api_key}')
                except Exception as e:
                    print(e.args[0])
                    break
            else:
                print(f'Status code: {self.status_code}')
                break

        api_response = request[0]

        self._tot_num_res = int(api_response['search-results']['opensearch:totalResults'])
        self._results = api_response['search-results']['entry']
        if get_all is True:
            while (self.num_res < self.tot_num_res) and not self._upper_limit_reached():
                for e in api_response['search-results']['link']:
                    if e['@ref'] == 'next':
                        next_url = e['@href']
                request = els_client.exec_request(next_url)
                status_code = request[1]
                while status_code in [401, 429]:
                    try:
                        els_client.api_key = next(self.keygen)
                        request = els_client.exec_request(next_url)
                        status_code = request[1]
                        print(f'Key Switched to {els_client.api_key}')
                    except Exception as e:
                        print(e.args[0])
                        break
                api_response = request[0]
                self._results += api_response['search-results']['entry']
        with open('dump.json', 'w') as f:
            f.write(json.dumps(self._results))

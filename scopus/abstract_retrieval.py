""" This script only considered scenarios for abstract retrieval.
    You must have the exact Scopus ids of the papers because it's not 'searching'.
    Abstract retrieval API only supports id-based retrieval."""

import json
import requests
from scopus.utils import write_json
from urllib.parse import quote_plus as url_encode


def search(url, api='scopus', key='8ad236116ff835cfc52d52530132383e'):
    headers = {
        "X-ELS-APIKey": key,
        "User-Agent": "elsapy-v%s" % '0.5.0',
        "Accept": 'application/json'
    }

    # search function is used in both steps so the 'view' option should be specified.
    view = 'FULL' if api == 'abstract' else 'COMPLETE'

    try:
        r = requests.get(url=url, headers=headers, params={'view': view})
        return r
    except Exception as e:
        print(str(e))


def retrieve_abstract(author, filename, keygen=None):
    key = next(keygen) if keygen else '8ad236116ff835cfc52d52530132383e'

    query = f'AU-ID({author})'
    url = f"https://api.elsevier.com/content/search/scopus?query={url_encode(query)}"

    try:
        response = search(url, key=key)
        while response.status_code in [401, 429]:
            key = next(keygen)
            response = search(url, key=key)

        r = json.loads(response.text)
        entry = r['search-results']['entry']
        total = int(r['search-results']['opensearch:totalResults'])
        length = len(entry)

        # get all the pages available
        while length < total:
            for e in r['search-results']['link']:
                if e['@ref'] == 'next':
                    next_url = e['@href']

            response = search(next_url, key=key)
            while response.status_code in [401, 429]:
                key = next(keygen)
                response = search(next_url, key=key)
            r = json.loads(response.text)
            entry += r['search-results']['entry']
            length = len(entry)

        data = []
        for e in entry:
            try:
                abs_url = e['prism:url']
                abs_response = search(abs_url, api='abstract', key=key)
                while abs_response.status_code in [401, 429]:
                    key = next(keygen)
                    abs_response = search(abs_url, api='abstract', key=key)

                abs_r = json.loads(abs_response.text)
                content = abs_r['abstracts-retrieval-response']['coredata']['dc:description']
            except:
                content = 'Not found'
            d = dict({'info': e, 'abstract': content})
            data.append(d)

        write_json(data, filename)
    except Exception as e:
        print(filename, str(e))

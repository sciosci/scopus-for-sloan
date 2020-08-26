""" This script only considered scenarios for author profile retrieval.
    You must have the exact author ids because it's not 'searching'.
    Author retrieval API only supports id-based retrieval."""

import requests, json
from scopus.utils import write_json


def search(url, key='8ad236116ff835cfc52d52530132383e'):
    headers = {
        "X-ELS-APIKey": key,
        "User-Agent": "elsapy-v%s" % '0.5.0',
        "Accept": 'application/json'
    }
    try:
        r = requests.get(url=url, headers=headers, params={'view': 'ENHANCED'})
        return r
    except Exception as e:
        print(str(e))


def retrieve_author(author, filename, keygen=None):
    key = next(keygen) if keygen else '8ad236116ff835cfc52d52530132383e'
    url = f'https://api.elsevier.com/content/author/author_id/{author}'
    try:
        response = search(url, key=key)
        while response.status_code in [401, 429]:
            key = next(keygen)
            response = search(url, key=key)
        r = json.loads(response.text)
        write_json(r, filename)
    except Exception as e:
        print(filename, str(e))

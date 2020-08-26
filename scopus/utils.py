import csv, json


def read_keys(file):
    with open(file, 'r') as reader:
        r = csv.reader(reader)
        next(r)
        return [key[0] for key in r]


def key_generator(keys):
    for key in keys:
        yield key
    return 'Keys Exhausted'


def write_json(data, filename):
    with open(filename, 'w') as writer:
        json.dump(data, writer, indent=4)
import json, pprint


def read_json_from_file(sample_file):
    with open(sample_file, 'r') as in_file:
        sample_json=json.load(in_file)
    return sample_json

def dumpsutf8(data):
    return json.dumps(data, ensure_ascii=False).encode('utf8')


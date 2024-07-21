import json


def parse_json_data(file_path, object):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data[object]

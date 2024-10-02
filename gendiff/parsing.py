import json
import yaml
import os.path as osp


def read_file(file_path):
    _, ext = osp.splitext(file_path)
    if ext == '.json':
        return json.load(open(file_path))
    elif ext == '.yml' or ext == '.yaml':
        return yaml.safe_load(open(file_path))
    else:
        raise Exception(f'Uknown file extension: {ext}!')

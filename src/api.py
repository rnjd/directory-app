from flask import Flask, jsonify, request
import json
import os
from os.path import join
from pwd import getpwuid
import sys

app = Flask(__name__)

file_type = 'file'
dir_type = 'dir'

root = sys.argv[1]


@app.route('/', methods=['GET', 'POST', 'PUT', 'DELETE'])
@app.route('/<path:file_path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def contents(file_path=None):
    full_path = join(root, file_path) if file_path else root
    try:
        if request.method == 'GET':
            return get_contents(full_path), 200
        if request.method == 'POST':
            return post_contents(full_path)
        if request.method == 'PUT':
            return put_contents(full_path)
        if request.method == 'DELETE':
            return delete_contents(full_path)
    except ValueError as err:
        return str(err), 400


def get_contents(full_path):
    if not os.path.exists(full_path):
        raise ValueError("This path does not exist.")

    if os.path.isfile(full_path):
        with open(full_path) as f:
            file_contents = f.read()
            f.close()
        return file_contents

    path_contents = []
    for sub_dir in os.listdir(full_path):
        sub_dir_details = __get_content_details(join(full_path, sub_dir))
        path_contents.append(json.dumps(sub_dir_details))
    return path_contents


def post_contents(full_path):
    contents_name = request.json['name']
    contents_type = request.json['type']

    if contents_type not in (file_type, dir_type):
        return jsonify('Invalid  type.')
    new_path = join(full_path, contents_name)

    if os.path.exists(new_path):
        raise ValueError('Path already exists.')

    if contents_type == file_type:
        open(new_path, 'w').close()
    else:
        os.makedirs(new_path, exist_ok=True)
    return json.dumps(__get_content_details(new_path))


def put_contents(full_path):
    old_name = request.json['old_name']
    new_name = request.json['new_name']
    contents_type = request.json['type']

    if contents_type not in (file_type, dir_type):
        return jsonify('Invalid  type.')

    old_path = join(full_path, old_name)
    new_path = join(full_path, new_name)

    if os.path.exists(new_path):
        raise ValueError('Path already exists.\\n')

    if not os.path.exists(old_path):
        if contents_type == file_type:
            open(new_path, 'w').close()
        else:
            os.mkdir(new_path)
    else:
        os.rename(old_path, new_path)
    return json.dumps(__get_content_details(new_path))


def delete_contents(full_path):
    if not os.path.exists(full_path):
        raise ValueError('Path does not exist.')

    details = __get_content_details(full_path)

    if os.path.isfile(full_path):
        os.remove(full_path)
    else:
        os.rmdir(full_path)
    return json.dumps(details)


class ContentsDto(dict):
    def __init__(self, name: str, owner: str, size: int, permissions: str) -> None:
        dict.__init__(self, name=name, owner=owner, size=size, permissions=permissions)


def __get_content_details(path) -> ContentsDto:
    sub_dir_stat = os.stat(path)
    return ContentsDto(path, getpwuid(sub_dir_stat.st_uid).pw_name, sub_dir_stat.st_size,
                       oct(sub_dir_stat.st_mode))


if __name__ == '__main__':
    app.run(debug=True)

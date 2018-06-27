import sys
import json
import os
import functools
import bson
import bson.json_util
from .query import query


def get_format(filename, format=None):
    '''
    Get the file format from filename or provided format.
    '''
    if format is not None:
        return format
    else:
        lower_filename = filename.lower()
        if lower_filename.endswith('.bson'):
            format = 'bson'
        elif lower_filename.endswith('.json'):
            format = 'json'
        else:
            format = 'bson'
    return format


def get_output_fileobj(output, output_format):
    '''
    Get output file object based on output filename and output_format.
    '''
    output_format = get_format(output, output_format)
    if output and output_format == 'bson':
        fd = open(output, 'wb')
    elif output and output_format == 'json':
        fd = open(output, 'w')
    elif (not output) and output_format == 'json': 
        fd = sys.stdout
    else:
        fd = sys.stdout.buffer
    return fd


def as_output_format(dict_obj, output_format):
    '''
    Convert dict object to str or byte format w.r.t. output_format.
    '''
    if output_format == 'json':
        return '%s\n' % (bson.json_util.dumps(dict_obj))
    else:
        return bson.BSON.encode(dict_obj)


def decode_json_file_iter(filename, *args, **kw):
    '''
    Decode newline splitted json file.
    '''
    for line in open(filename).readlines():
        if not line:
            continue
        yield bson.json_util.loads(line, *args, **kw)


def query_son(filename, file_format=None, filters=None):
    '''
    Query a file with mongo like query filters.
    '''
    if isinstance(filters, str):
        filters = json.loads(filters)
    filters = filters or {}
    file_format = get_format(filename, format=file_format)
    if file_format == 'bson':
        for obj in query(bson.decode_file_iter(open(filename, 'rb')), filters):
            yield obj
    elif file_format == 'json':
        for obj in query(decode_json_file_iter(filename, filters)):
            yield obj
    else:
        raise Exception('Unknown file format "%s".' % file_format)

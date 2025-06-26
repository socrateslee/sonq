import gzip
import sys
import json
import os
import functools
import bson
import bson.json_util
import contextlib
from .query import query

SUPPORTED_FORMATS = ('.bson', '.json', '.jsonl')
SUPPORTED_COMPRESS_EXTS = ('.gz', '.bz2')


def supported_suffix():
    '''
    Get the supported file suffixes.
    '''
    for format in SUPPORTED_FORMATS:
        for compress_ext in ['', *SUPPORTED_COMPRESS_EXTS]:
            yield format + compress_ext


def get_format(filename, format=None):
    '''
    Get the file format from filename or provided format.
    '''
    suported = list(supported_suffix())
    if format:
        if format not in suported and ('.%s' % format) not in suported:
            raise ValueError('Unsupported format: %s' % format)
        return format
    else:
        lower_filename = filename.lower()
        for suffix in suported:
            if lower_filename.endswith(suffix):
                format = suffix[1:]
                break
        else:
            if filename == '-':
                format = 'json'
            else:
                format = 'bson'
    return format


def get_output_fileobj(output, output_format):
    '''
    Get output file object based on output filename and output_format.
    '''
    file_format = get_format(output, output_format)
    open_func = open
    if file_format.endswith('.gz'):
        import gzip
        open_func = gzip.open
    elif file_format.endswith('.bz2'):
        import bz2
        open_func = bz2.open
    if output:
        if file_format.startswith('bson'):
            fd = open_func(output, 'wb')
        else:
            fd = open_func(output, 'wt', encoding='utf-8', newline='\n')
    elif output_format.startswith('bson'):
        fd = sys.stdout.buffer
    else:
        fd = sys.stdout
    return fd


def as_output_format(dict_obj, output_format, json_options=None):
    '''
    Convert dict object to str or byte format w.r.t. output_format.
    '''
    if output_format.startswith('bson'):
        return bson.BSON.encode(dict_obj)
    else:
        if json_options is None:
            json_options = {}
        return '%s\n' % (bson.json_util.dumps(dict_obj, **json_options))


def decode_json_file_iter(fd, *args, **kw):
    '''
    Decode newline splitted json file.
    '''
    for line in fd.readlines():
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
    file_mode = 'rb' if file_format.startswith('bson') else 'rt'
    open_func = open
    if file_format.endswith('.gz'):
        import gzip
        open_func = gzip.open
    elif file_format.endswith('.bz2'):
        import bz2
        open_func = bz2.open
    if filename == '-':
        get_fd = lambda: contextlib.nullcontext(sys.stdin)
    else:
        get_fd = lambda: open_func(filename, file_mode)
    decode_iter = bson.decode_file_iter if file_format.startswith('bson') else decode_json_file_iter
    with get_fd() as fd:
        for obj in query(decode_iter(fd), filters):
            yield obj

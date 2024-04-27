'''
Command line interface.
'''
import argparse
import signal
from . import operation

signal.signal(signal.SIGPIPE, signal.SIG_DFL)

SUPPORTED_FORMATS = [i[1:] for i in operation.supported_suffix()]

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--filter", default={},
                        help="The mongo like query filter over .bson or .json file.")
    parser.add_argument("-o", "--output", default="",
                        help="The output .bson or .json file, default to STDOUT if ignored.")
    parser.add_argument("--output-format", default="", choices=SUPPORTED_FORMATS,
                        help="The output format.")
    parser.add_argument("--input-format", default="", choices=SUPPORTED_FORMATS,
                        help="The input format.")
    parser.add_argument("-n", default=None, type=int,
                        help="The number of entries to output.")
    parser.add_argument("--json-indent",
                        default=None,
                        type=lambda x: int(x) if x.isdigit() else x,
                        help="Whether to indent the output json/jsonl file.")
    parser.add_argument("--json-ensure-ascii",
                        action=argparse.BooleanOptionalAction, default=True,
                        help="Whether to enable the `ensure_ascii` option for output json/jsonl file.")
    parser.add_argument("--json-skipkeys", action=argparse.BooleanOptionalAction, default=False,
                        help="Whether to enable the `skipkeys` option for output json/jsonl file.")
    parser.add_argument("--json-allow-nan", action=argparse.BooleanOptionalAction, default=True,
                        help="Whether to enable the `allow_nan` option for output json/jsonl file.")
    parser.add_argument("--json-sort-keys", action=argparse.BooleanOptionalAction, default=False,
                        help="Whether to enable the `sort_keys` option for output json/jsonl file.")
    parser.add_argument("options", default=[], nargs="*")
    return parser.parse_args()


def main():
    args = vars(parse_args())
    options = args['options']
    if not args['output']:
        output_format = args['output_format'] or 'json'
    else:
        output_format = args['output_format'] or operation.get_format(args['output'])
    json_options = {k[5:]: v for k, v in args.items() if k.startswith('json_') and v is not None}
    out_fd = operation.get_output_fileobj(args['output'], output_format)
    n = args['n']
    for idx, entry in enumerate(operation.query_son(options[0],
                                                    file_format=args['input_format'],
                                                    filters=args['filter'])):
        if n is not None and idx >= n:
            break
        out_fd.write(operation.as_output_format(entry, output_format, json_options=json_options))


if __name__ == '__main__':
    main()

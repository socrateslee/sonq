'''
Command line interface.
'''
import argparse
from . import operation


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--filter", default={},
                        help="The mongo like query filter over .bson or .json file.")
    parser.add_argument("-o", "--output", default="",
                        help="The output .bson or .json file, default to STDOUT if ignored.")
    parser.add_argument("--output-format", default="",
                        help="The output format.")
    parser.add_argument("options", default=[], nargs="*")
    return parser.parse_args()


def main():
    args = vars(parse_args())
    options = args['options']
    if not args['output']:
        output_format = args['output_format'] or 'json'
    else:
        output_format = args['output_format'] or operation.get_format(args['output'])
    out_fd = operation.get_output_fileobj(args['output'], output_format)
    for i in operation.query_son(options[0], filters=args['filter']):
        out_fd.write(operation.as_output_format(i, output_format))


if __name__ == '__main__':
    main()

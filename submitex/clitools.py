"""
Helper functions for CLI usage.
"""
import argparse
import sys

def get_parsed_args(parser):
    """Returns parser.parse_args()"""
    return parser.parse_args()

def parse_input(args):
    """
    Check if a filename was given in the args. If yes,
    return contents of the file, otherwise return the
    input from sys.stdin
    """
    if args.filename is None:
        s = sys.stdin.read()
    else:
        if not args.filename.endswith('.tex'):
            fn = args.filename + '.tex'
        else:
            fn = args.filename

        with open(fn,'r',encoding=args.enc) as f:
            s = f.read()
    return s

def get_default_parser(description):
    """
    Returns an argparse.ArgumentParser object
    with two default arguments (filename and enc(oding))
    """
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('filename', type=str, nargs='?',
                        help='Files to convert',default=None)
    parser.add_argument('-e','--enc',
                        type=str,
                        default='utf8',
                        help='encoding')

    return parser

def write_output(output):
    """Write string `output` to sys.stdout"""
    sys.stdout.write(output)

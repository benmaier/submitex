import argparse
import sys

def get_parsed_args(parser):
    return parser.parse_args()

def parse_input(args):
    if args.filename is None:
        s = sys.stdin.read()
    else:
        with open(args.filename,'r',encoding=args.enc) as f:
            s = f.read()
    return s

def get_default_parser():
    parser = argparse.ArgumentParser(description='Convert \input{|command} to the output of command.')
    parser.add_argument('filename', type=str, nargs='?',
                        help='Files to convert',default=None)
    parser.add_argument('-e','--enc',
                        default='utf8',
                        help='encoding')

    return parser

def write_output(output):
    sys.stdout.write(output)

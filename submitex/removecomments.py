"""
Functions to find all non-escaped "%" and remove what ever comes after.
Afterwards, squash consecutive empty lines to a single empty line.
"""

import re

from submitex.clitools import (
        get_default_parser,
        parse_input,
        get_parsed_args,
        write_output,
    )

def remove_unescaped_percent_comments(text: str) -> str:
    """
    Remove everything from the first *unescaped* '%' to the end of each line,
    keeping what comes before it.
    Works in Python without variable-length lookbehind.
    """
    # ^((?:[^\\]|\\{2})*?)  -> capture the shortest prefix that ends before the first unescaped %
    # %.*$                  -> from that % to end of line
    return re.sub(r'^((?:[^\\]|\\{2})*?)%.*$', r'\1', text, flags=re.M)

def collapse_empty_lines(text: str) -> str:
    """
    Replace any run of 2+ consecutive empty/whitespace-only lines with a single empty line.
    Handles \n and \r\n.
    """
    # Match one empty/whitespace-only line followed by one or more more of the same
    return re.sub(r'(?m)^[ \t\f\v]*\r?\n(?:[ \t\f\v]*\r?\n)+', '\n', text)

def clean_text(text: str) -> str:
    text = remove_unescaped_percent_comments(text)
    text = collapse_empty_lines(text)
    return text

def cli():

    description = r'Replace all comments with an empty string and squash all empty lines to one empty line'
    parser = get_default_parser(description)
    #parser.add_argument('-d','--dontcopyfigs',
    #                    action='store_true',
    #                    default=False,
    #                    help='Per default, the figures that are found will be copied to the current '\
    #                         "working directory, but you can turn that off with this flag.")
    #parser.add_argument('-F','--figprefix',
    #                    type=str,
    #                    default='Fig',
    #                    help='The prefix for the renamed figures (default: "Fig", such that Fig01, Fig02, ...)')
    args = get_parsed_args(parser)
    tex = parse_input(args)

    converted = clean_text(tex)

    write_output(converted)

if __name__ == "__main__":
    sample = r"""code % comment
                 code with escaped \% percent stays
                 path with backslashes \\% not a comment
                 line with no comment



                 next line % another comment
               """
    print(clean_text(sample))


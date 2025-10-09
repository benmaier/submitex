"""
Functions to find all non-escaped "%" and remove what ever comes after.
Afterwards, squash consecutive empty lines to a single empty line.
"""

import re
from typing import List

from submitex.clitools import (
        get_default_parser,
        parse_input,
        get_parsed_args,
        write_output,
    )


# Regex to find the FIRST unescaped '%' on a line.
# It tokenizes as: (escaped char) OR (any char that isn't % or \), repeated, then a %
FIRST_UNESCAPED_PERCENT = re.compile(r'^((?:\\.|[^%\\])*)%.*$')

def _process_line(line: str) -> str:
    """
    Apply rules (1) and (2) to a single line:
      1) If there's an unescaped '%' and there is a non-whitespace char before it,
         strip from that '%' to the end (keep the prefix).
      2) If there's an unescaped '%' and only whitespace before it,
         turn the whole line into a single '%'.
      Otherwise, leave the line unchanged.
    """
    m = FIRST_UNESCAPED_PERCENT.search(line)
    if not m:
        return line

    prefix = m.group(1)
    if re.search(r'\S', prefix):   # has any non-whitespace
        return prefix
    else:
        return '%'

def _collapse_lines(lines: List[str]) -> List[str]:
    """
    Apply rules (3) and (4):
      3) Collapse consecutive empty/whitespace-only lines to a single empty line.
      4) Collapse consecutive lines that are exactly '%' (ignoring surrounding whitespace) to a single '%'.
    """
    out = []
    prev_was_empty = False
    prev_was_percent = False

    for raw in lines:
        line = raw  # already processed by _process_line
        stripped = line.strip()

        is_empty = (stripped == '')
        is_percent_only = (stripped == '%')

        if is_empty:
            if not prev_was_empty:
                out.append('')  # keep a single empty line
            prev_was_empty = True
            prev_was_percent = False
            continue

        if is_percent_only:
            if not prev_was_percent:
                out.append('%')  # keep a single '%' line
            prev_was_empty = False
            prev_was_percent = True
            continue

        # normal content line
        out.append(line)
        prev_was_empty = False
        prev_was_percent = False

    return out

def clean_text(text: str) -> str:
    """
    Applies all rules:
      1) Remove from the first unescaped '%' when there is non-whitespace before it.
      2) If only whitespace precedes the first unescaped '%', replace that whole line with '%'.
      3) Collapse consecutive empty lines.
      4) Collapse consecutive '%' lines.
    Notes:
      - Operates line-by-line; treats '\\n' and '\\r\\n' inputs equivalently and outputs with '\\n'.
      - Handles escaped percent '\\%' correctly (kept as literal percent).
    """
    # Normalize newlines to '\n' for consistent processing
    text_norm = text.replace('\r\n', '\n').replace('\r', '\n')

    # Step 1 & 2: line-wise processing
    processed = [_process_line(line) for line in text_norm.split('\n')]

    # Step 3 & 4: collapsing sequences
    collapsed = _collapse_lines(processed)

    # Rejoin using '\n'
    return '\n'.join(collapsed)


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

    \includegraphics[width=0.5\textwidth]{Fig35.pdf} % original file: example.pdf


               """
    print(clean_text(sample))

    sample = (
        r"\includegraphics[width=0.5\textwidth]{Fig35.pdf} % original file: example.pdf" "\n"
        r"\asd\%\\%" "\n"
        r"   % spacing line" "\n"
        r"   % another spacing line" "\n"
        r"" "\n"
        r"" "\n"
        r"content % comment" "\n"
        r"content continued" "\n"
    )

    print("INPUT:\n------")
    print(sample)
    print("\nOUTPUT:\n-------")
    print(clean_text(sample))


"""
Functions to find all input commands and replace
them with the content of the respective files.
"""

import sys
import re
from pathlib import Path
from subprocess import Popen, PIPE
from submitex.clitools import (
        get_default_parser,
        parse_input,
        get_parsed_args,
        write_output,
    )
from submitex.tools import (
        iterate_matches,
        search_pattern_and_replace,
    )

def _extract_filepath_from_within_brackets(text):

    before, fn = text.split('{')
    fn = fn[:-1]

    fn = Path(fn.strip())
    if fn.suffix == '' and not fn.exists():
        fn = Path( str(fn) + '.tex')
    return fn

def _read_file_content(fn,enc='utf-8'):
    with open(fn,'r',encoding=enc) as f:
        output = f.read()
    return output

def convert(tex):
    r"""
    Finds all instances of a tex-command input in a
    string, runs the contained commands as subprocesses
    and replaces the tex-commands with the respective
    results of the run.

    Explicitly, it matches the input against
    the regexp (\\inp|\\input)\s*{\s*\|.*?}.

    For an explanation of the regexp, check
    https://regexr.com/72k51

    Prints out all errors by commands and raises
    a ValueError at the end if there was any errors
    in the commands.

    Parameters
    ==========
    tex : str
        The string containing tex source.

    Returns
    =======
    new_tex : str
        String that matches ``tex``, but every
        occurrence of an ``\input{|command}`` was
        replaced by the output of ``command``.
    """
    input_regexp = r"\\input\s*{.*?}"
    pattern = re.compile(input_regexp)
    pos = 0
    newtex = str(tex)

    found_matches = set()
    for m in iterate_matches(tex, pattern):
        span = m.span()
        this_match = str(m.group())
        if this_match not in found_matches:
            found_matches.add(this_match)
            fp = _extract_filepath_from_within_brackets(this_match)
            try:
                output = _read_file_content(fp)
            except FileNotFoundError:
                continue
            newtex = search_pattern_and_replace(newtex, re.compile(re.escape(this_match)), output)




    return newtex


def cli():
    description = 'Replace `\input{filename}` with the content of `filename`'
    parser = get_default_parser(description)
    args = get_parsed_args(parser)
    tex = parse_input(args)

    converted = convert(tex)
    write_output(converted)

if __name__ == "__main__":

    tex = r"""
        This is a {\bf test}.

        I'll try converting this \input{ /Users/bfmaier/.zshrc } {"

    """
    result = convert(tex)
    print(result)

    tex3 = r"\input{|python ../cookbook/example.py}dingdongwallawallabingbanf\input{|python ../cookbook/example.py}"
    result = convert(tex3)
    print(result)

    tex2 = r"""
        This is a {\bf test}.

        I'll try converting this \input{|python -c "print('hi(input)')"}

        I'll try converting this \inp{|python -c "print('hi(inp)')"}
        I'll try converting this \inp{|python "print('hi(inp)')"}
        I'll try converting this \inp  { |  python   "print('hi(inp)')"   }
    """
    convert(tex2)

import sys
import re

from submitex.clitools import (
        get_default_parser,
        parse_input,
        get_parsed_args,
        write_output,
    )

from submitex.tools import (
        iterate_matches,
        match_is_comment,
        search_pattern_and_replace,
    )

def convert(tex,bib):

    # delete \bibliographystyle{...}
    pattern_style = re.compile(r'\\bibliographystyle{.*}')
    pos = 0
    newtex = str(tex)
    while True:
        match = pattern_style.search(newtex,pos=pos)
        if match is None:
            break
        if match_is_comment(newtex,match):
            pos = match.span()[1]
            continue
        start, end = match.span()
        before = newtex[:start]
        after = newtex[end:]
        newtex = before + after

    pattern_bib = re.compile(r'\\bibliography{.*}')
    pos = 0
    while True:
        match = pattern_bib.search(newtex,pos=pos)
        if match is None:
            break
        if match_is_comment(newtex,match):
            pos = match.span()[1]
            continue

        start, end = match.span()
        before = newtex[:start]
        after = newtex[end:]
        newtex = before + bib + after
        pos = len(before)+len(bib)

    return newtex

def cli():

    parser = get_default_parser()
    args = get_parsed_args(parser)

    if args.filename is not None:
        if args.filename.endswith('.tex'):
            args.filename = args.filename[:-4]
    else:
        raise ValueError('No filename given!')

    fn = args.filename

    with open(fn+'.bbl','r',encoding=args.encoding) as f:
        bib = f.read()

    with open(fn+'.tex','r',encoding=args.encoding) as f:
        tex = f.read()

    converted = convert(tex,bib)
    write_output(converted)

if __name__ == "__main__":
    tex = r"""%\bibliographystyle{deimuddi}
    \bibliographystyle{deinemudder}
    %\bibliographystyle{deimuddi}
    %\bibliography{luemmel.bib}
    abc\bibliography{luemmel.bib}def

    \bibliography{luemmel.bib}
    """
    bib = r"""
    \begin{thebibliography}
    \end{thebibliography}
    """
    converted = convert(tex,bib)
    print(converted)



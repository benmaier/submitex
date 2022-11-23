"""
Functions to replace the bibliography-command
with the contents of the generated .bbl-file.
"""
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

from pathlib import Path

def convert(tex,bib):

    # delete \bibliographystyle{...}
    pattern_style = re.compile(r'\\bibliographystyle\s*{.*?}')
    tex = search_pattern_and_replace(tex, pattern_style, '')

    # replace \bibliography{} with the text in parameter `bib`
    pattern_bib = re.compile(r'\\bibliography\s*{.*?}')
    tex = search_pattern_and_replace(tex, pattern_bib, bib)

    return tex

def cli():

    description = r'Put the content of the bbl-file into the section where previouly laid `\biblipgraphystyle{...}\bibliography{filename}`'
    parser = get_default_parser(description)
    parser.add_argument('-b','--bib',
                        type=str,
                        default=None,
                        help="We'll try to deduce a bib-file from the passed filename of the TeX-source, "+\
                             "but in case the bib-file is named differently, you can provided it here"
                        )
    args = get_parsed_args(parser)

    if args.filename is not None:
        if args.filename.endswith('.tex'):
            args.filename = args.filename[:-4]
    else:
        raise ValueError('No filename given!')

    fn = args.filename

    if args.bib is not None:
        fn_bib = args.bib
    else:
        fn_bib = fn

    if not Path(fn_bib).exists():
        fn_bib = fn + '.bbl'

    with open(fn_bib,'r',encoding=args.enc) as f:
        bib = f.read()

    with open(fn+'.tex','r',encoding=args.enc) as f:
        tex = f.read()

    converted = convert(tex,bib)
    write_output(converted)

if __name__ == "__main__":
    tex = r"""%\bibliographystyle {deimuddi}
    \bibliographystyle{deinemudder}
    \bibliographystyle {deinemudder}
    %\bibliographystyle{deimuddi}
    %\bibliography{luemmel.bib}
    abc\bibliography{luemmel.bib}def

    \bibliography {luemmel.bib}
    """
    bib = r"""
    \begin{thebibliography}
    \end{thebibliography}
    """
    converted = convert(tex,bib)
    print(converted)



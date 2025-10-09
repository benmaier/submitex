"""
Functions to find all "figure"- and
"includegraphics"-environments and replace the listed
files with generic filenames that are on cwd-level.
"""

import sys
import re
import shutil
from string import ascii_lowercase as abc


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
from math import log10

def get_next_figure_range(tex,pos):

    begin_figure = re.compile(r'\\begin\s*{\s*figure[\s\*]*?}')
    match_begin = begin_figure.search(tex,pos=pos)
    if match_begin is None:
        return None
    end_figure = re.compile(r'\\end\s*{\s*figure[\s\*]*?}')
    match_end = end_figure.search(tex,pos=match_begin.span()[-1])
    if match_end is None:
        return None

    return match_begin.span()[-1], match_end.span()[0]

def iterate_includegraphics_in_figure(tex,pos,endpos,fig_str):
    includegraphics_pattern = re.compile(r"\\includegraphics.*?{.*?}")
    brackets_pattern = re.compile(r"{.*?}")
    has_more_than_one_graphics = _count_includegraphics(tex[pos:endpos]) > 1

    i = 0
    fig_paths = []
    added_chars = 0
    while True:
        #print(tex[pos:pos+10])
        match = includegraphics_pattern.search(tex,pos=pos,endpos=endpos)
        if match is None:
            break
        if match_is_comment(tex,match):
            pos = match.span()[1]
            continue
        start, end = match.span()
        before = tex[:start]
        after = tex[end:]
        #print("""=======before====""""")
        #print(before)
        #print("""=======match====""""")
        #print(match)
        #print("""=======after====""""")
        #print(after)

        s = match.group()
        incl, fn = s.split('{')
        fn = fn[:-1]
        source = Path(fn)
        if has_more_than_one_graphics:
            this_fig = fig_str + abc[i]
        else:
            this_fig = fig_str
        if source.suffix != '':
            this_fig += source.suffix
        if str(source) != this_fig:
            fig_paths.append((str(source), this_fig))
            repl = incl + '{' + this_fig + '}' + ' % original file: '+str(source) + '\n'
        else:
            repl = s
        added_chars += len(repl)

        diff = len(repl) - len(s)
        tex = before + repl + after
        pos = len(before) + len(repl)
        endpos += diff
        i += 1


    return tex, fig_paths, endpos

def _count_occ(tex,pattern):
    # use iterate_matches to disregarded out-commented
    return len([*iterate_matches(tex, pattern)])

def _count_figures(tex):
    pattern = re.compile(r'\\begin\s*{\s*figure[\s\*]*?}')
    return _count_occ(tex, pattern)

def _count_includegraphics(tex):
    pattern = re.compile(r'\\includegraphics')
    return _count_occ(tex, pattern)

def convert_and_get_figure_paths(tex,figure_prefix='Fig'):

    n_figs = _count_figures(tex)
    places = max([int(log10(n_figs)) + 1,2])
    fmt_string = figure_prefix+'{0:0'+str(places)+'d}'

    pos = 0
    i = 1
    fig_paths = []
    while True:
        span = get_next_figure_range(tex, pos)
        if span is None:
            break
        tex, new_fig_paths, pos = iterate_includegraphics_in_figure(tex, span[0], span[1], fmt_string.format(i))
        fig_paths.extend(new_fig_paths)
        #print("========",tex[span[0]:pos],"---------")
        i += 1


    return tex, fig_paths

def clone_figures(fig_paths,fileendings=['.pdf','.png','.eps','.jpg','.jpeg'],debug=False):

    debug_out = []

    for source, target in fig_paths:
        src = Path(source)
        suffix = src.suffix
        if suffix == '':
            if not src.exists():
                for suffix in fileendings:
                    src = Path(source + suffix)
                    if src.exists():
                        break

        trg = Path(target)
        trg = trg.parents[0] / (trg.stem + suffix)

        if debug:
            debug_out.append((src, trg))
        else:
            shutil.copy2(src, trg)

    if debug:
        return debug_out



def cli():

    description = r'Rename all figure files in the `\includegraphics`-environment to generic enumerated names and copy the respective files with the new names to top-level.'
    parser = get_default_parser(description)
    parser.add_argument('-d','--dontcopyfigs',
                        action='store_true',
                        default=False,
                        help='Per default, the figures that are found will be copied to the current '\
                             "working directory, but you can turn that off with this flag.")
    parser.add_argument('-F','--figprefix',
                        type=str,
                        default='Fig',
                        help='The prefix for the renamed figures (default: "Fig", such that Fig01, Fig02, ...)')
    args = get_parsed_args(parser)
    tex = parse_input(args)

    converted, fig_paths = convert_and_get_figure_paths(tex,figure_prefix=args.figprefix)
    if not args.dontcopyfigs:
        clone_figures(fig_paths)
    write_output(converted)

if __name__ == "__main__":

    figure_paths = [
                ('foo/bar', 'Fig01'),
                ('foo/bar', 'Fig02.pdf'),
                ('foo/bar/lump.eps', 'Fig03.jpg'),
                ('./foo/bar/lump.pdf', './Fig03.jpg'),
            ]

    output = clone_figures(figure_paths,debug=True)
    for s, t in output:
        print(s, t)


    print(_count_figures(r"\begin {figure } \end{figure}  \n   \begin{figure} %\begin{figure}"))

    newtex, figpaths = convert_and_get_figure_paths(r"""
            \begin{figure}
                    \includegraphics[width=\textwidth]{figures/result.pdf} \includegraphics{a}
                    %\includegraphics[width=\textwidth]{figures/result.pdf}
                    \includegraphics[width=\textwidth]{figures/result.pdf}
            \end{figure}

            \begin{figure}
                    \includegraphics[width=\textwidth]{figures/result2}
            \end{figure}

            \begin{figure}[p]
                    \includegraphics[width=\textwidth]{figures/result3.pdf} \includegraphics{b}
            \end{figure}

            \begin{figure*}[p]
                    \includegraphics[width=\textwidth]{figures/result4.pdf} \includegraphics{c}
            \end{figure*}



            \begin{figure}
    """)

    print(newtex)
    for s, t in clone_figures(figpaths,debug=True):
        print(s, t)




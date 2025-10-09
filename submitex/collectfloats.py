"""
Functions to collect figures and tables and list
them at the end of the document on their own pages.
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
        search_pattern_and_replace,
    )

def convert(tex):

    figures, tables, newtex = extract_floats(tex)

    concat_floats = ""
    for _float in figures + tables:
        concat_floats += "\\afterpage{%\n" + _float + "\n\\clearpage}\n\n"

    concat_floats += '\\end{document}\n'

    pattern_enddoc = re.compile(r'\\end\s*{\s*document\s*?}')
    newtex = search_pattern_and_replace(newtex, pattern_enddoc,concat_floats)

    return newtex


def extract_floats(tex):
    """
    https://regexr.com/72slr
    https://regexr.com/72smm
    """
    fig_pattern = re.compile(r"\\begin\s*{\s*figure[\s\*]*}(.|\n)*?\\end\s*{\s*figure[\s\*]*}")
    table_pattern = re.compile(r"\\begin\s*{\s*table[\s\*]*}(.|\n)*?\\end\s*{\s*table[\s\*]*}")

    newtex = str(tex)
    figures = []
    for match in iterate_matches(tex, fig_pattern):
        newtex = newtex.replace(match.group(), '')
        figures.append(match.group())

    tables = []
    for match in iterate_matches(newtex, table_pattern):
        newtex = newtex.replace(match.group(), '')
        tables.append(match.group())

    return figures, tables, newtex


def cli():

    description = 'Remove all figure- and table-environments from their respective place in the document body and put them on their own page at the end of the document, first figures, then tables.'
    parser = get_default_parser(description)
    args = get_parsed_args(parser)
    tex = parse_input(args)

    converted = convert(tex)
    write_output(converted)

if __name__ == "__main__":


    print(convert(r"""
            \begin{document}


                  This is a parapgraph.

            \begin{figure}
                    \includegraphics[width=\textwidth]{figures/result.pdf} \includegraphics{a}
                    %\includegraphics[width=\textwidth]{figures/result.pdf}
                    \includegraphics[width=\textwidth]{figures/result.pdf}
            \end{figure}

            \begin{table}
                  \begin{tabulate}
                    yello
                  \end{tabulate}
            \end{table}

            \begin{table*}
                  \begin{tabulate}
                    hallo :D
                  \end{tabulate}
            \end{table*}



                  This is another paragraph

            \begin{figure}
                    \includegraphics[width=\textwidth]{figures/result2}
            \end{figure}

            \begin{figure*}
                    \includegraphics[width=\textwidth]{figures/result3}
            \end{figure*}

            %\begin{figure}
            %\begin{figure}
            %        \includegraphics[width=\textwidth]{figures/result2}
            %\end{figure}


            \end{document}
    """))

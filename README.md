# submitex

Python tools and CLIs to automatically convert your LaTeX-project into a
structure in which it can be easily submitted to a journal.

For instance for `manuscript.tex` with bibtex-generated `manuscript.bbl`:

    replacebib manuscript | replacefigs | collectfloats | resolveinputs | resolvepipes > newmanuscript.tex

## Install

    pip install submitex

## Examples

Check out the [cookbook section](https://github.com/benmaier/submitex/tree/main/cookbook) or further below.

## Modules/CLIs

Functionality is given by functions in the respective `submitex.modulename`, e.g. `submitex.replacefigs`.

The same modulename can be used to evoke the functionality from the command line.

| module/CLI | description |
|------------|-------------|
| replacefigs | Rename all figure files in the `\includegraphics`-environment to generic enumerated names and copy the respective files with the new names to top-level. |
| collectfloats | Remove all figure- and table-environments from their respective place in the document body and put them on their own page at the end of the document, first figures, then tables. |
| replacebib | Put the content of the bbl-file into the section where previously laid `\bibliographystyle{...}\bibliography{filename}` |
| resolveinputs | Replace `\input{filename}` with the content of `filename` |
| resolvepipes | Replace `\input{\|command}` with the output of the process `command` |

### Python examples

#### replacefigs

```python
import submitex.replacefigs as rf

tex = r"""
\begin{figure} \includegraphics[width=1in]{foo/bar} \includegraphics{result.png} \end{figure}

\begin{figure} \includegraphics[width=1in]{foo/bong.jpg} \end{figure}
"""

newtex, figpaths = rf.convert_and_get_figure_paths(tex, figure_prefix='figure_')

print(newtex)
for src, trg in figpaths:
    print(src, trg)
```

Output:

    \begin{figure} \includegraphics[width=1in]{figure_01a} % original file: foo/bar
     \includegraphics{figure_01b.png} % original file: result.png
     \end{figure}
    
    \begin{figure} \includegraphics[width=1in]{figure_02.jpg} % original file: foo/bong.jpg
     \end{figure}
    
    foo/bar figure_01a
    result.png figure_01b.png
    foo/bong.jpg figure_02.jpg

#### collectfloats

```python
import submitex.collectfloats as cf

tex = r"""\begin{document}
\begin{figure} \end{figure}
Test
\begin{figure} \end{figure} \begin{ table} \end{table }
This is another paragraph
\end{document}
"""

print(cf.convert(tex))
```

Output:

    \begin{document}
    
    Test
    
    This is another paragraph
    \afterpage{%
    \begin{figure} \end{figure}
    \clearpage}
    
    \afterpage{%
    \begin{figure} \end{figure}
    \clearpage}
    
    \afterpage{%
    \begin{ table} \end{table }
    \clearpage}
    
    \end{document}

#### replacebib

```python
import submitex.replacebib as rb

tex = r"""
\bibliographystyle{vancouver}
%\bibliographystyle{chicago}
%\bibliography{main.bib}
\bibliography {main.bib}
"""
bib = r"""
\begin{thebibliography}
\end{thebibliography}
"""
print(rb.convert(tex,bib))
```


Output:

    %\bibliographystyle{chicago}
    %\bibliography{main.bib}
    
    \begin{thebibliography}
    \end{thebibliography}

#### resolveinputs

File `section1.tex`:

```latex
\section{Section 1}
This is Section 1.
```

```python
import submitex.resolveinputs as ri

tex = r"""
\input{ section01.tex}
%\input{ section01.tex}
"""

print(ri.convert(tex))
```

Output:


    \section{Section 1}
    This is Section 1.
    
    %\input{ section01.tex}


#### resolvepipes

```python
import submitex.resolvepipes as rp

tex = "There's \inp{|python -c 'print(int(24*60*60*365.25))'} seconds in a year."
print("source:", tex)
print("out   :", rp.convert(tex), '\n')

tex = "There's $\input { | ls -al ~ | wc -l }$ files/directories in your user directory."
print("source:", tex)
print("out   :", rp.convert(tex))

```

Output:

    source: There's \inp{|python -c 'print(int(24*60*60*365.25))'} seconds in a year.
    out   : There's 31557600 seconds in a year.

    source: There's $\input { | ls -al ~ | wc -l }$ files/directories in your user directory.
    out   : There's $      62$ files/directories in your user directory.



### CLI usage

Almost all of the CLIs work like this:

    resolvepipes oldmanuscript.tex > newmanuscript.tex
    cat oldmanuscript.tex | resolvepipes > newmanuscript.tex

An exception is `replacebib` which needs another file to work. Typically, the file is called the same as the input file, so for 

    replacebib oldmanuscript > newmanuscript.tex

the procedure assumes that both `oldmanuscript.tex` and `oldmanuscript.bbl` exist in the cwd. Alternatively, provided it explicitly with the `--bib` flag. Then you can pipe. For instance

    cat oldmanuscript.tex | replacebib -b otherbibfile.bbl > newmanuscript.tex

Note that that means you can pipe several or all of the commands together, for instance like so:

    replacebib manuscript | replacefigs | collectfloats | resolveinputs | resolvepipes > newmanuscript.tex

#### replacefigs

    usage: replacefigs [-h] [-e ENC] [-d] [-F FIGPREFIX] [filename]
    
    Rename all figure files in the `\includegraphics`-environment to generic
    enumerated names and copy the respective files with the new names to top-
    level.
    
    positional arguments:
      filename              Files to convert
    
    options:
      -h, --help            show this help message and exit
      -e ENC, --enc ENC     encoding
      -d, --dontcopyfigs    Per default, the figures that are found will be copied
                            to the current working directory, but you can turn
                            that off with this flag.
      -F FIGPREFIX, --figprefix FIGPREFIX
                            The prefix for the renamed figures (default: "Fig",
                            such that Fig01, Fig02, ...)

#### collectfloats

    usage: collectfloats [-h] [-e ENC] [filename]
    
    Remove all figure- and table-environments from their respective place in the
    document body and put them on their own page at the end of the document, first
    figures, then tables.
    
    positional arguments:
      filename           Files to convert
    
    options:
      -h, --help         show this help message and exit
      -e ENC, --enc ENC  encoding

#### replacebib

    usage: replacebib [-h] [-e ENC] [-b BIB] [filename]
    
    Put the content of the bbl-file into the section where previouly laid
    `\biblipgraphystyle{...}\bibliography{filename}`
    
    positional arguments:
      filename           Files to convert
    
    options:
      -h, --help         show this help message and exit
      -e ENC, --enc ENC  encoding
      -b BIB, --bib BIB  We'll try to deduce a bib-file from the passed filename
                         of the TeX-source, but in case the bib-file is named
                         differently, you can provided it here

#### resolveinputs

    usage: resolveinputs [-h] [-e ENC] [filename]
    
    Replace `\input{filename}` with the content of `filename`
    
    positional arguments:
      filename           Files to convert
    
    options:
      -h, --help         show this help message and exit
      -e ENC, --enc ENC  encoding


#### resolvepipes

    usage: resolvepipes [-h] [-e ENC] [filename]

    Convert \input{|command} to the output of `command`.

    positional arguments:
      filename           Files to convert

    options:
      -h, --help         show this help message and exit
      -e ENC, --enc ENC  encoding

Example:

    resolvepipes manuscript.tex > manuscript_with_executed_commands.tex
    cat manuscript.tex | resolvepipes > manuscript_cmds.tex


## Dependencies

`submitex` only uses the Python standard library.

## License

This project is licensed under the [MIT License](https://github.com/benmaier/submitex/blob/main/LICENSE).

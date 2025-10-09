submitex
========

Python tools and CLIs to automatically convert your LaTeX-project into a
structure in which it can be easily submitted to a journal.

For instance for ``manuscript.tex`` with bibtex-generated
``manuscript.bbl``:

.. code:: bash

   replacebib manuscript | replacefigs | collectfloats | resolveinputs | resolvepipes > newmanuscript.tex

Install
-------

.. code:: bash

   pip install submitex

Examples
--------

Check out the `cookbook
section <https://github.com/benmaier/submitex/tree/main/cookbook>`__ or
further below.

Workflow for the arXiv
----------------------

Modules/CLIs
------------

Functionality is given by functions in the respective
``submitex.modulename``, e.g. ``submitex.replacefigs``.

The same modulename can be used to evoke the functionality from the
command line.

+---------------------------------+----------------------------------------------------+
| module/CLI                      | description                                        |
+=================================+====================================================+
| replacefigs                     | Rename all figure files in the                     |
|                                 | ``\includegraphics``-environment to generic        |
|                                 | enumerated names and copy the respective files     |
|                                 | with the new names to top-level.                   |
+---------------------------------+----------------------------------------------------+
| collectfloats                   | Remove all figure- and table-environments from     |
|                                 | their respective place in the document body and    |
|                                 | put them on their own page at the end of the       |
|                                 | document, first figures, then tables.              |
+---------------------------------+----------------------------------------------------+
| replacebib                      | Put the content of the bbl-file into the section   |
|                                 | where previously laid                              |
|                                 | ``\bibliographystyle{...}\bibliography{filename}`` |
+---------------------------------+----------------------------------------------------+
| resolveinputs                   | Replace ``\input{filename}`` with the content of   |
|                                 | ``filename``                                       |
+---------------------------------+----------------------------------------------------+
| resolvepipes                    | Replace ``\input{\|command}`` with the output of   |
|                                 | the process ``command``                            |
+---------------------------------+----------------------------------------------------+
| removecomments                  | Remove comments (beginning with unescaped ``%``)   |
|                                 | on non-whitespace lines, squash lines comments to  |
|                                 | a single line on white-space lines. Squash         |
|                                 | white-space lines to a single line.                |
+---------------------------------+----------------------------------------------------+

.. _workflow-for-the-arxiv-1:

Workflow for the arXiv
----------------------

For the arxiv, it's nice to copy all figures to top-level, resolve all
inputs, replace the bibliography with the bbl file, and remove comments.
Then in the end, you want a zip that you can upload. What follows is a
Makefile that takes care of that.

Make sure to have `diff-pdf <https://github.com/vslavik/diff-pdf>`__
installed! On MacOS:

.. code:: bash

   brew install diff-pdf

Here is the Makefile:

.. code:: makefile

   # ============================
   # Configurable parameters
   # ============================

   # Input directory (copied from Overleaf)
   INPUT_DIR := /path/to/manuscript/directory

   # Local working directories
   PAPER_DIR := paper
   ARXIV_DIR := arxiv
   ARXIV_TEST := arxiv_test

   # Manuscript base name (without .tex)
   MAIN := main

   # Tool to open a file (on Mac, just `open`)
   OPEN := open

   # ============================
   # Targets
   # ============================

   default: init arxiv

   init: clean copy latex

   arxiv: processtex test zip

   latex:
       cd $(PAPER_DIR); pdflatex $(MAIN); bibtex $(MAIN); pdflatex $(MAIN); pdflatex $(MAIN)

   processtex:
       cd $(PAPER_DIR); replacebib $(MAIN) | resolveinputs | replacefigs | removecomments > $(MAIN)_for_arxiv.tex
       mkdir -p $(ARXIV_DIR)
       mkdir -p $(ARXIV_TEST)
       cp ./$(PAPER_DIR)/$(MAIN)_for_arxiv.tex ./$(ARXIV_DIR)
       cp ./$(PAPER_DIR)/Fig* ./$(ARXIV_DIR)
       cp ./$(PAPER_DIR)/$(MAIN)_for_arxiv.tex ./$(ARXIV_TEST)
       cp ./$(PAPER_DIR)/Fig* ./$(ARXIV_TEST)

   copy:
       cp -r $(INPUT_DIR)/ ./$(PAPER_DIR)

   clean:
       rm -rf ./$(ARXIV_DIR)
       rm -rf ./$(ARXIV_TEST)
       rm -rf ./$(PAPER_DIR)
       rm -f texput.log arxiv.zip diff.pdf

   softclean:
       rm -rf ./$(ARXIV_TEST)
       rm -rf ./$(PAPER_DIR)
       rm -f texput.log diff.pdf

   zip:
       zip -r arxiv.zip ./$(ARXIV_DIR)

   test:
       cd $(ARXIV_TEST) &&\
               rm -f $(MAIN)_for_arxiv.pdf &&\
               pdflatex $(MAIN)_for_arxiv.tex &&\
               pdflatex $(MAIN)_for_arxiv.tex
       rm -f $(ARXIV_TEST)/$(MAIN)_for_arxiv
       diff-pdf $(ARXIV_TEST)/$(MAIN)_for_arxiv.pdf $(PAPER_DIR)/$(MAIN).pdf --output-diff=diff.pdf --skip-identical
       $(OPEN) diff.pdf

Python examples
---------------

replacefigs
^^^^^^^^^^^

.. code:: python

   import submitex.replacefigs as rf

   tex = r"""
   \begin{figure} \includegraphics[width=1in]{foo/bar} \includegraphics{result.png} \end{figure}

   \begin{figure} \includegraphics[width=1in]{foo/bong.jpg} \end{figure}
   """

   newtex, figpaths = rf.convert_and_get_figure_paths(tex, figure_prefix='figure_')

   print(newtex)
   for src, trg in figpaths:
       print(src, trg)

Output:

.. code:: bash

   \begin{figure} \includegraphics[width=1in]{figure_01a} % original file: foo/bar
    \includegraphics{figure_01b.png} % original file: result.png
    \end{figure}

   \begin{figure} \includegraphics[width=1in]{figure_02.jpg} % original file: foo/bong.jpg
    \end{figure}

   foo/bar figure_01a
   result.png figure_01b.png
   foo/bong.jpg figure_02.jpg

collectfloats
^^^^^^^^^^^^^

.. code:: python

   import submitex.collectfloats as cf

   tex = r"""\begin{document}
   \begin{figure} \end{figure}
   Test
   \begin{figure} \end{figure} \begin{ table} \end{table }
   This is another paragraph
   \end{document}
   """

   print(cf.convert(tex))

Output:

.. code:: bash

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

replacebib
^^^^^^^^^^

.. code:: python

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

Output:

.. code:: bash

   %\bibliographystyle{chicago}
   %\bibliography{main.bib}

   \begin{thebibliography}
   \end{thebibliography}

resolveinputs
^^^^^^^^^^^^^

File ``section1.tex``:

.. code:: latex

   \section{Section 1}
   This is Section 1.

.. code:: python

   import submitex.resolveinputs as ri

   tex = r"""
   \input{ section01.tex}
   %\input{ section01.tex}
   """

   print(ri.convert(tex))

Output:

.. code:: bash

   \section{Section 1}
   This is Section 1.

   %\input{ section01.tex}

resolvepipes
^^^^^^^^^^^^

.. code:: python

   import submitex.resolvepipes as rp

   tex = r"There's \inp{|python -c 'print(int(24*60*60*365.25))'} seconds in a year."
   print("source:", tex)
   print("out   :", rp.convert(tex), '\n')

   tex = r"There's $\input { | ls -al ~ | wc -l }$ files/directories in your user directory."
   print("source:", tex)
   print("out   :", rp.convert(tex))

Output:

.. code:: bash

   source: There's \inp{|python -c 'print(int(24*60*60*365.25))'} seconds in a year.
   out   : There's 31557600 seconds in a year.

   source: There's $\input { | ls -al ~ | wc -l }$ files/directories in your user directory.
   out   : There's $      62$ files/directories in your user directory.

removecomments
^^^^^^^^^^^^^^

.. code:: python

   import submitex.removecomments as rc
   sample = r"""
   code % comment
   code with escaped \% percent stays
   path with backslashes \\% not a comment
   line with no comment



   next line % another comment

   \includegraphics[width=0.5\textwidth]{Fig35.pdf} % original file: example.pdf
      %
   %
   %
   """
   print(rc.clean_text(sample))

Output:

.. code:: bash


   code
   code with escaped \% percent stays
   path with backslashes \\
   line with no comment

   next line

   \includegraphics[width=0.5\textwidth]{Fig35.pdf}
   %

CLI usage
~~~~~~~~~

Almost all of the CLIs work like this:

.. code:: bash

   resolvepipes oldmanuscript.tex > newmanuscript.tex
   cat oldmanuscript.tex | resolvepipes > newmanuscript.tex

An exception is ``replacebib`` which needs another file to work.
Typically, the file is called the same as the input file, so for

.. code:: bash

   replacebib oldmanuscript > newmanuscript.tex

the procedure assumes that both ``oldmanuscript.tex`` and
``oldmanuscript.bbl`` exist in the cwd. Alternatively, provided it
explicitly with the ``--bib`` flag. Then you can pipe. For instance

.. code:: bash

   cat oldmanuscript.tex | replacebib -b otherbibfile.bbl > newmanuscript.tex

Note that that means you can pipe several or all of the commands
together, for instance like so:

.. code:: bash

   replacebib manuscript | replacefigs | collectfloats | resolveinputs | resolvepipes | removecomments > newmanuscript.tex

.. _replacefigs-1:

replacefigs
^^^^^^^^^^^

.. code:: bash

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

.. _collectfloats-1:

collectfloats
^^^^^^^^^^^^^

.. code:: bash

   usage: collectfloats [-h] [-e ENC] [filename]

   Remove all figure- and table-environments from their respective place in the
   document body and put them on their own page at the end of the document, first
   figures, then tables.

   positional arguments:
     filename           Files to convert

   options:
     -h, --help         show this help message and exit
     -e ENC, --enc ENC  encoding

.. _replacebib-1:

replacebib
^^^^^^^^^^

.. code:: bash

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

.. _resolveinputs-1:

resolveinputs
^^^^^^^^^^^^^

.. code:: bash

   usage: resolveinputs [-h] [-e ENC] [filename]

   Replace `\input{filename}` with the content of `filename`

   positional arguments:
     filename           Files to convert

   options:
     -h, --help         show this help message and exit
     -e ENC, --enc ENC  encoding

.. _resolvepipes-1:

resolvepipes
^^^^^^^^^^^^

.. code:: bash

   usage: resolvepipes [-h] [-e ENC] [filename]

   Convert \input{|command} to the output of `command`.

   positional arguments:
     filename           Files to convert

   options:
     -h, --help         show this help message and exit
     -e ENC, --enc ENC  encoding

Example:

.. code:: bash

   resolvepipes manuscript.tex > manuscript_with_executed_commands.tex
   cat manuscript.tex | resolvepipes > manuscript_cmds.tex

.. _removecomments-1:

removecomments
^^^^^^^^^^^^^^

.. code:: bash

   usage: removecomments [-h] [-e ENC] [filename]

   Replace all comments with an empty string and squash all empty lines to one empty line

   positional arguments:
     filename           Files to convert

   options:
     -h, --help         show this help message and exit
     -e ENC, --enc ENC  encoding

Example:

.. code:: bash

   removecomments manuscript.tex > manuscript_with_removed_comments.tex
   cat manuscript.tex | removecomments > manuscript_clean.tex

Dependencies
------------

``submitex`` only uses the Python standard library.

License
-------

This project is licensed under the `MIT
License <https://github.com/benmaier/submitex/blob/main/LICENSE>`__.

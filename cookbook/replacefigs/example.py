import submitex.replacefigs as rf

tex = r"""
\begin{figure} \includegraphics[width=1in]{foo/bar} \includegraphics{result.png} \end{figure}

\begin{figure} \includegraphics[width=1in]{foo/bong.jpg} \end{figure}
"""

newtex, figpaths = rf.convert_and_get_figure_paths(tex, figure_prefix='figure_')

print(newtex)
for src, trg in figpaths:
    print(src, trg)


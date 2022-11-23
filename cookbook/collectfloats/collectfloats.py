import submitex.collectfloats as cf

tex = r"""\begin{document}
This is a parapgraph.

\begin{figure}
        \includegraphics[width=\textwidth]{figures/result.pdf}
        \includegraphics{a}
\end{figure}

This is another paragraph

\begin{table}
      \begin{tabulate}
      \end{tabulate}
\end{table}

\begin{figure}
        \includegraphics{b}
\end{figure}
%\begin{table}
%\end{table}

\end{document}
"""

print(cf.convert(tex))

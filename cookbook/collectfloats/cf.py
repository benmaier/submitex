import submitex.collectfloats as cf

tex = r"""\begin{document}
\begin{figure} \end{figure}
Test
\begin{figure} \end{figure} \begin{ table} \end{table }
This is another paragraph
\end{document}
"""

print(cf.convert(tex))

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



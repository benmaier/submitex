import submitex.resolveinputs as ri

tex = r"""
\input{ section01.tex}
%\input{ section01.tex}
"""

print(ri.convert(tex))

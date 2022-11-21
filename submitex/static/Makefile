mainin=main
mainout=manuscript
mainfinal=$(mainout)_final
suppin=SM
suppout=supplementary
suppfinal=$(suppout)_final

all:
	make clean
	make conversion
	make manuscript
	make supplementary

allwoutconv:
	make clean
	make manuscript
	make supplementary

conversion:
	cat $(mainin).tex | pipetex2tex > $(mainout).tex
	cat $(suppin).tex | pipetex2tex > $(suppout).tex

manuscript:
	pdflatex $(mainout)
	bibtex $(mainout)
	pdflatex $(mainout)
	pdflatex $(mainout)
	python replacebib.py $(mainout) > $(mainfinal).tex
	pdflatex $(mainfinal)
	pdflatex $(mainfinal)
	make clean

supplementary:
	pdflatex $(suppout)
	bibtex $(suppout)
	pdflatex $(suppout)
	pdflatex $(suppout)
	python replacebib.py $(suppout) > $(suppfinal).tex
	pdflatex $(suppfinal)
	pdflatex $(suppfinal)
	make clean

clean:
	rm -f *.log
	rm -f *.aux
	rm -f *.blg
	rm -f *.bbl
	rm -f $(suppout)Notes.bib 
	rm -f $(mainout)Notes.bib 
	rm -f $(suppout)_finalNotes.bib 
	rm -f $(mainout)_finalNotes.bib 



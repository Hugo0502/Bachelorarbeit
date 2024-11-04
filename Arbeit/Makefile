
all: pdf

pdf:
	pdflatex thesis.tex
	bibtex thesis.aux
	pdflatex thesis.tex
	pdflatex thesis.tex
	rm thesis.aux thesis.bbl thesis.blg thesis.log thesis.out thesis.toc

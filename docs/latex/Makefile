
CMD_LATEX = pdflatex
CMD_BIBER = biber

FILE_START = clinguin
FILE_TEX = $(FILE_START).tex
FILE_BIBER = clinguin.bib


compile:
	$(CMD_LATEX) $(FILE_TEX)
	$(CMD_BIBER) $(FILE_START)
	$(CMD_LATEX) $(FILE_TEX)
	$(CMD_LATEX) $(FILE_TEX)

clean:
	rm $(FILE_START).aux
	rm $(FILE_START).bbl
	rm $(FILE_START).bcf
	rm $(FILE_START).blg
	rm $(FILE_START).log
	rm $(FILE_START).out
	rm $(FILE_START).run.xml

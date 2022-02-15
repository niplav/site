all: finite_groups_i_huppert_1967.pdf

finite_groups_i_huppert_1967.pdf: finite_groups_i_huppert_1967.tex
	latex finite_groups_i_huppert_1967.tex
	bibtex finite_groups_i_huppert_1967.aux
	latex finite_groups_i_huppert_1967.tex
	latex finite_groups_i_huppert_1967.tex
	pdflatex finite_groups_i_huppert_1967.tex

clean:
	rm -f *.aux *.bbl. *.bcf *.blg *.dvi *.log *.run.xml *.toc *.nav *.out *.snm

.PHONY: clean

# Makefile
TEXFILES = $(wildcard *.tex)
PDFFILES = $(TEXFILES:.tex=.pdf)

all: pdflatex 

pdf: $(PDFFILES)

%.pdf: %.tex
	@if [ -d publish ];then mv *.pdf publish; else mkdir publish; mv *.pdf publish/;fi
#	@rubber --pdf $<

pdflatex: $(TEXFILES)
	$(foreach x,$(TEXFILES:.tex=),pdflatex $(x);)
	$(foreach x,$(TEXFILES:.tex=),bibtex $(x);)
	$(foreach x,$(TEXFILES:.tex=),pdflatex $(x);)
	$(foreach x,$(TEXFILES:.tex=),pdflatex $(x);)
	@if [ -d publish ];then mv *.pdf publish; else mkdir publish; mv *.pdf publish/;fi

#clean:
#	@rubber --clean $(TEXFILES:.tex=)

distclean: clean
	@rm -rf publish
	@rm -f $(PDFFILES)
#	@rubber --clean --pdf $(TEXFILES:.tex=)

x:
	@open publish/$(PDFFILES) &> /dev/null &

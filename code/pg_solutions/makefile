include config.mk

.SUFFIXES: .rc .kg .eps .png

all: $(IMG)

puttit: $(IMG)
	mv $(IMG) ../../img/pg_solutions

.eps.png:
	convert $< $@
	rm $<

%.eps: draw_all.kg
	kg -l ./$< -e '.x(0)'

clean:
	rm -f $(IMG)

.PHONY: puttit clean

include config.mk

.SUFFIXES: .rc .kg .eps .png

all: $(IMG)

puttit: $(IMG)
	mv $(IMG) ../../img/99_klong

.eps.png:
	convert $< $@
	rm $<

.rc.eps:
	./$< >$@

.kg.eps:
	kg -l ./$< -e '.x(0)' >$@

clean:
	rm -f $(IMG)

.PHONY: puttit clean

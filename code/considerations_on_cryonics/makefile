include config.mk

.SUFFIXES: .rc .kg .eps .png

all: $(IMG)

puttit: $(IMG)
	mv $(IMG) ../../img/considerations_on_cryonics

.eps.png:
	convert -chop 0x180 $< $@
	rm $<

.rc.eps:
	./$< >$@

.kg.eps:
	kg -l ./$< -e '.x(0)' >$@

clean:
	rm -f $(IMG)

.PHONY: puttit clean

include config.mk

.SUFFIXES: .kg .eps .png

all: $(IMG)

puttit: $(IMG)
	mv $(IMG) ../../img/masturbation

.eps.png:
	convert -chop 0x180 $< $@
	rm $<

.kg.eps:
	kg -l ./$< -e '.x(0)' >$@

clean:
	rm -f $(IMG)

.PHONY: puttit clean

include config.mk

.SUFFIXES: .kg .eps .png

all: $(IMG)

puttit: $(IMG)
	mv $(IMG) ../../estimated_life_expectancy

.eps.png:
	convert $< $@
	convert -chop 12x192 $@ $@

.kg.eps:
	kg -l ./$< -e '.x(0)' >$@

clean:
	rm -f $(IMG)

.PHONY: puttit clean

include config.mk

.SUFFIXES: .dot .png

all: $(IMG)

puttit: $(IMG)
	mv $(IMG) ../../img/turning

.dot.png:
	dot -Tpng $< >$@

clean:
	rm -f $(IMG)

.PHONY: puttit clean

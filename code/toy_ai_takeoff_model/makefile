include config.mk

.SUFFIXES: .kg .eps .png

all: $(IMG)

.eps.png:
	convert -chop 0x180 $< $@
	rm $<

%.eps: draw_all.kg
	kg -l ./$< -e '.x(0)'

clean:
	rm -f $(IMG)
	rm -f $(CSV)

.PHONY: all clean

include config.mk

.SUFFIXES: .kg .eps .png

all: $(IMG)

$(EPS): draw_all.kg
	kg -l ./$< -e '.x(0)'

.eps.png: $(EPS)
	convert $< $@
	rm $<

clean:
	rm -f $(IMG)

.PHONY: all clean

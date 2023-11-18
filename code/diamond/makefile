include config.mk

.SUFFIXES: .kg .eps .png

all: $(IMG)

onedim.eps: draw_all.kg
	kg -l ./$< -e '.x(0)'

onedim.png: onedim.eps
	convert -chop 0x180 $< $@
	rm $<

twodim.png: twodim.py
	python3 twodim.py

threedim.png: threedim.py
	python3 threedim.py

clean:
	rm -f $(IMG)

.PHONY: all clean

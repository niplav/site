include config.mk

.SUFFIXES: .kg .eps .png

all: $(IMG)

puttit: $(CSV) $(IMG)
	mv pb.csv ../../data
	mv met.csv ../../data

pb.csv:
	./pbdata.py >pb.csv

met.csv:
	./metdata.py <../../data/metaculus.json >met.csv

.eps.png:
	convert $< $@
	rm $<

%.eps: draw_all.kg
	kg -l ./$< -e '.x(0)'

clean:
	rm -f $(IMG)
	rm -f $(CSV)

.PHONY: clean

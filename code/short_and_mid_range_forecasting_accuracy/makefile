include config.mk

all: $(CSV)

puttit: all
	mv pb.csv ../../data
	mv met.csv ../../data

pb.csv:
	./pbdata.py >pb.csv

met.csv:
	./metdata.py <../../data/metaculus.json >met.csv

clean:
	rm -f pb.csv
	rm -f met.csv

.PHONY: clean

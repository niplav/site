all:
	./pbdata.py >pb.csv
	./metdata.py <../../data/metaculus.json >met.csv

puttit: all
	mv pb.csv ../../data
	mv met.csv ../../data

clean:
	rm -f pb.csv
	rm -f met.csv

.PHONY: clean

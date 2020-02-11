all:
	python2 pbdata.py >pb.csv

puttit: all
	mv pb.csv ../../data

clean:
	rm -f pb.csv

.PHONY: clean

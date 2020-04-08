all: bp_chrono.md

puttit: all
	mv bp_chrono.md ../../

bp_chrono.md:
	./gen_chrono bp_chrono.md

clean:
	rm -f bp_chrono.md

.PHONY: clean

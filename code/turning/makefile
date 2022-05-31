include config.mk

.SUFFIXES: .dot .png

all: $(IMG)

puttit: $(IMG)
	mv $(IMG) ../../img/turning

.dot.png:
	dot -Tpng $< >$@

incomplete.png: incomplete.dot
	dot -Tpng $< >$@

intransitive.png: intransitive.dot
	circo -Tpng $< >$@

unbalanced_cycle.png: unbalanced_cycle.dot
	dot -Tpng $< >$@

resubc_hyp.png: resubc_hyp.dot
	dot -Tpng $< >$@

resubc_hyp_trans.png: resubc_hyp_trans.dot
	dot -Tpng $< >$@

se_comp.png: se.png ser_1.png ser_2.png
	montage se.png ser_1.png ser_2.png ser_3.png -adjoin -geometry 192x252 se_comp.png

se.png: se.dot
	dot -Tpng $< >$@

ser_1.png: ser_1.dot
	dot -Tpng $< >$@

ser_2.png: ser_2.dot
	dot -Tpng $< >$@

clean:
	rm -f $(IMG)

.PHONY: puttit clean

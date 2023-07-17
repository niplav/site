include config.mk

.SUFFIXES: .dot .png

all: $(IMG)

puttit: $(IMG)
	mv $(IMG) ../../img/turning

counter_comp.png: counter_min.png turn_counter_min.png
	montage counter_min.png turn_counter_min.png -adjoin -geometry 192x252 counter_comp.png

shift.png: before_shift.png after_shift.png
	montage before_shift.png s_arrow.png after_shift.png -adjoin -geometry 192x252 shift.png

se_comp.png: se.png ser_1.png ser_2.png
	montage se.png ser_1.png ser_2.png ser_3.png -adjoin -geometry 192x252 se_comp.png

.dot.png:
	dot -Tpng $< >$@

incomplete.png: incomplete.dot
	dot -Tpng $< >$@

intransitive.png: intransitive.dot
	circo -Tpng $< >$@

unbalanced_cycle.png: unbalanced_cycle.dot
	dot -Tpng $< >$@

turnubc_hyp.png: turnubc_hyp.dot
	dot -Tpng $< >$@

turnubc_hyp_trans.png: turnubc_hyp_trans.dot
	dot -Tpng $< >$@

medium_hodge.png: medium_hodge.dot
	dot -Tpng $< >$@

se.png: se.dot
	dot -Tpng $< >$@

ser_1.png: ser_1.dot
	dot -Tpng $< >$@

ser_2.png: ser_2.dot
	dot -Tpng $< >$@

counter_min.png: counter_min.dot
	dot -Tpng $< >$@

turn_counter_min.png: turn_counter_min.dot
	dot -Tpng $< >$@

before_shift.png: before_shift.dot
	dot -Tpng $< >$@

after_shift.png: after_shift.dot
	dot -Tpng $< >$@

clean:
	rm -f $(IMG)

.PHONY: puttit clean

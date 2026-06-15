include config.mk

JULIA=/usr/local/etc/julia/juliaup/julia-1.12.6+0.x64.linux.gnu/bin/julia

.SUFFIXES: .rc .kg .eps .png

all: $(IMG)

julia: daygame.jl
	$(JULIA) daygame.jl

puttit: $(IMG)
	mv $(IMG) ../../img/daygame_cost_benefit

.eps.png:
	convert -chop 0x180 $< $@
	rm $<

%.eps: draw_all.kg
	kg -l ./$< -e '.x(0)'

clean:
	rm -f $(IMG)

.PHONY: puttit clean julia

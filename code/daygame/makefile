include config.mk

JULIA=julia

.SUFFIXES: .rc .kg .eps .png

# Images with a Julia plotter: build these via Julia by default, not Klong.
# Everything else in $(IMG) (complete.png, cost.png, &c.) has no Julia port
# yet, so it still falls through to the .eps.png/draw_all.kg rules below.
PLOTS_IMG=layratio_data.png layratio_data_reduced.png \
          dateratio_data.png dateratio_data_reduced.png \
          ratio_data.png ratio_data_reduced.png
SCALING_IMG=scaling_fertility.png scaling_value_m.png \
            scaling_heatmap.png scaling_Ne.png

all: $(IMG)

$(PLOTS_IMG) &: plots.jl
	$(JULIA) plots.jl

$(SCALING_IMG) &: scaling.jl
	$(JULIA) scaling.jl

puttit: $(IMG)
	mv $(IMG) ../../img/daygame

.eps.png:
	convert -chop 0x180 $< $@
	rm $<

%.eps: draw_all.kg
	kg -l ./$< -e '.x(0)'

clean:
	rm -f $(IMG)

.PHONY: puttit clean

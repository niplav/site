include config.mk

.SUFFIXES: .png

all: $(IMG)

onedim.png: onedim.py generalized_o3_pro.py
	python3 onedim.py

onedim_multi.png: onedim_multi.py generalized_o3_pro.py
	python3 onedim_multi.py

twodim.png: twodim.py generalized_o3_pro.py
	python3 twodim.py

twodim_multi.png: twodim_multi.py generalized_o3_pro.py
	python3 twodim_multi.py

threedim.png: threedim.py generalized_o3_pro.py
	python3 threedim.py

threedim_multi.png: threedim_multi.py generalized_o3_pro.py
	python3 threedim_multi.py

threedim_isosurface_2.png threedim_isosurface_3.png threedim_isosurface_4.png: threedim_isosurface.py generalized_o3_pro.py
	ulimit -v 6291456 && python3 threedim_isosurface.py

threedim_animation_0.gif threedim_animation_1.gif threedim_animation_2.gif: threedim_animation.py generalized_o3_pro.py
	ulimit -v 6291456 && python3 threedim_animation.py

fourdim_isosurface_animation_33_stitch0_2shells.gif fourdim_isosurface_animation_33_stitch1_2shells.gif fourdim_isosurface_animation_33_stitch2_2shells.gif fourdim_isosurface_animation_33_stitch3_2shells.gif fourdim_isosurface_animation_33_stitch0_3shells.gif fourdim_isosurface_animation_33_stitch1_3shells.gif fourdim_isosurface_animation_33_stitch2_3shells.gif fourdim_isosurface_animation_33_stitch3_3shells.gif: fourdim_isosurface_animation.py generalized_o3_pro.py
	ulimit -v 6291456 && python3 fourdim_isosurface_animation.py

clean:
	rm -f $(IMG)

.PHONY: all clean

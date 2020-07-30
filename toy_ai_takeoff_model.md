[home](./index.md)
------------------

*author: niplav, created: 2020-07-22, modified: 2020-07-26, language: english, status: draft, importance: 7, confidence: unlikely*

> __In [AI safety](https://en.wikipedia.org/wiki/AI_control_problem),
significant time has been spent on the question of
the intelligence of AI systems over time, especially during
[takeoff](https://en.wikipedia.org/wiki/Technological_singularity#Hard_vs._soft_takeoff).
An underappreciated argument in the debate has been the idea that the more
intelligent an AI system becomes, the better it can search the space of
possible optimization algorithms. This post proposes a computational model
of this process by creating a search space using the [diamond-square
algorithm](https://en.wikipedia.org/wiki/Diamond-square_algorithm)
generalized to n dimensions and then running a very simple
[hill-climbing](https://en.wikipedia.org/wiki/Hill_climbing) algorithm
and brute-force search on that space. Possible further improvements to
the model are suggested.__

An Exploratory Toy AI Takeoff Model
===================================

> Libre de la metáfora y del mito  
labra un arduo cristal: el infinito  
mapa de Aquel que es todas Sus estrellas.

*– [Jorge Luis Borges](https://en.wikipedia.org/wiki/Jorge_Luis_Borges), [“Spinoza”](https://thefunambulist.net/literature/litterature-spinoza-by-borges), 1964*

> Paraphrasing Roache (2008) the state of play is such that nobody
believes the result of a simulation, except the person who performed
the simulation, and everybody believes the result of an experiment,
except the person who ran the experiment.

*– Ryan G. McClarren, “Uncertainty Quantification and Predictive Computational Science“ p. 9, 2018*

(Although the quote apparently goes back to Einstein, see “The
advancement of science, and its burdens” p. 13, only there with "theory"
instead of "simulation").

<!--Articles:
* https://aiimpacts.org/historical-growth-trends/
* https://aiimpacts.org/likelihood-of-discontinuous-progress-around-the-development-of-agi/
* https://intelligence.org/ai-foom-debate/
* https://intelligence.org/files/IEM.pdf
* https://longtermrisk.org/the-future-of-growth-near-zero-growth-rates/
* https://sideways-view.com/2018/02/24/takeoff-speeds/
* https://www.lesswrong.com/posts/5WECpYABCT62TJrhY/will-ai-undergo-discontinuous-progress
* https://www.lesswrong.com/posts/66FKFkWAugS8diydF/modelling-continuous-progress
* https://www.lesswrong.com/posts/77xLbXs6vYQuhT8hq/why-ai-may-not-foom
* https://www.lesswrong.com/posts/CjW4axQDqLd2oDCGG/misconceptions-about-continuous-takeoff
* https://www.lesswrong.com/posts/JBadX7rwdcRFzGuju/recursive-self-improvement
* https://www.lesswrong.com/posts/YgNYA6pj2hPSDQiTE/distinguishing-definitions-of-takeoff
* https://www.lesswrong.com/posts/cxgtQXnH2uDGBJJGa/redefining-fast-takeoff
* https://www.lesswrong.com/posts/tjH8XPxAnr6JRbh7k/hard-takeoff
-->

<!--
https://en.wikipedia.org/wiki/Brownian_surface
https://en.wikipedia.org/wiki/Fractal_landscape
https://en.wikipedia.org/wiki/Fractional_Brownian_motion
https://en.wikipedia.org/wiki/Gradient_descent
https://en.wikipedia.org/wiki/Hill_climbing
https://en.wikipedia.org/wiki/Newton%27s_method
https://en.wikipedia.org/wiki/OpenSimplex_noise
https://en.wikipedia.org/wiki/Perlin_noise
https://en.wikipedia.org/wiki/Simplex_noise
https://github.com/buckinha/DiamondSquare
https://nullprogram.com/blog/2007/11/20/
-->

Introduction
------------

### Existing Approaches

The Argument
------------

The Model
---------

### Generating the Search Space

#### Desiderata for the Search Space

#### N-Dimensional Diamond Square

##### Square

##### Diamond

#### Results

### Searching the Space

#### Hill Climbing

#### Brute Force Search

Results
--------

### Uniform Values

### Lognormal Values

Limitations
-----------

Conclusion
----------

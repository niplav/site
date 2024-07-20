[home](./index.md)
------------------

*author: niplav, created: 2023-11-18, modified: 2024-07-05, language: english, status: in progress, importance: 2, confidence: likely*

> __I finally make use of my [daygame data](./data.html#Daygame) by
writing some code that implements a multi-armed bandit with Thompson
sampling on beta-distributed estimates of what proportion of approaches
in a particular location yield contact information.__

Using A Multi-Armed Bandit to Select Daygame Locations
=======================================================

Given the [data of my daygame approaches](./data.html#Daygame), I've
wondered for quite a while how I could use that data to make improve
my game. I don't think I've found anything solid yet, so instead I'm
going to try to use that data to estimate where I should do my next
daygame session. Beliefs are for action, after all.

For this, I trick ChatGPT into writing code for a [multi-armed
bandit](https://en.wikipedia.org/wiki/Multi-armed_bandit) using
[Thompson sampling](https://en.wikipedia.org/wiki/Thompson_sampling) of
[beta-distributed](https://en.wikipedia.org/wiki/Beta-distribution) value
in [Julia](https://en.wikipedia.org/wiki/Julia_\(programming_language\)),
with getting a contact information as a reward of 1 and not getting any
contact information as a reward of 0.

(I know that this is a super impoverished view on what makes a good
daygame approach, but this is an exploratory exercise. I might add more &
different factors later.)

Of course, I can't tell ChatGPT that I am doing pickup, so I instead
say that I'm looking to optimize the quality of icecream I'm eating by
selecting different icecream shops. (Title of conversation: "Bayesian
Icecream Bandit").

The resulting code is is wholly confused and *bad*, with multiple subtle
and not so subtle bugs, and unelegant too—I reckon there's just not
enough Julia training data to make it capable enough, but I haven't
checked with the most recent models.

So after more than a year of procrastination, I decide to rewrite
the code, the result is [here](./code/bandit/location.jl).

If first loads the data, collects the number of successes (got contact
info) and failures (didn't get contact info), builds the corresponding
Beta distribution and past success ratio, throws it all into the DataFrame
`bandit` and then samples from the distribution. (The Beta distribution
is useful here because the more samples have been collected, the smaller
the variance—and this is exactly what we want, since less-explored
locations should be sampled more often.)

So the output of the script can look something like this, where the most
preferred option is at the bottom:

	julia> sort(bandit, :sample)
	34×6 DataFrame
	 Row │ location  successes  failures  success_prob  dist                          sample
	     │ Int64     Int64      Int64     Float64       Beta…                         Float64
	─────┼──────────────────────────────────────────────────────────────────────────────────────
	   1 │   300211          0         3      0.0       Beta{Float64}(α=1.0, β=4.0)   0.0170241
	   2 │   438791          0         6      0.0       Beta{Float64}(α=1.0, β=7.0)   0.0448562
	   3 │    52055          0         1      0.0       Beta{Float64}(α=1.0, β=2.0)   0.0678704
	   4 │    10939          3        27      0.1       Beta{Float64}(α=4.0, β=28.0)  0.0684485
	   5 │   956569          4        16      0.2       Beta{Float64}(α=5.0, β=17.0)  0.0853593
	  ⋮  │    ⋮          ⋮         ⋮           ⋮                     ⋮                    ⋮
	  31 │   817198          1         0      1.0       Beta{Float64}(α=2.0, β=1.0)   0.670436
	  32 │   295748          1         0      1.0       Beta{Float64}(α=2.0, β=1.0)   0.71711
	  33 │    76108          1         1      0.5       Beta{Float64}(α=2.0, β=2.0)   0.724031
	  34 │   702595          1         0      1.0       Beta{Float64}(α=2.0, β=1.0)   0.864322
	                                                                             25 rows omitted

The top option (namely 692431) is, unfortunately, in another city hundreds kilometers from where I live.

So I might want to filter out irrelevant locations, so I create a set
of locations that are amenable to weekday/weekend and good/bad weather
daygame:

	weekday_good_weather=[548236, 175735, 709269, 76108, 956569, 132388, 449256, 591664, 449052, 119752, 868084]
	weekday_bad_weather=[449052, 709269, 76108, 548236, 422985]
	weekend_good_weather=[692404,10939,548236,35322,175735,702595,709269,803955,76108,276017,52055,422985,956569,300211,132388,449256,531828,433507,591664,868084,371851,32441,119752,449052]
	weekend_bad_weather=[449052, 709269, 76108, 548236, 422985, 10939, 702595, 531828]

Then, on a weekday with good weather (as it often is, at the time of
writing), I can then filter for locations in my current city with such
conditions:

	julia> filter(x->x[:location] in weekday_good_weather, sort(bandit, :sample))
	12×6 DataFrame
	 Row │ location  successes  failures  success_prob  dist                           sample
	     │ Int64     Int64      Int64     Float64       Beta…                          Float64
	─────┼───────────────────────────────────────────────────────────────────────────────────────
	   1 │   956569          4        16     0.2        Beta{Float64}(α=5.0, β=17.0)   0.0853593
	   2 │   868084          6        20     0.230769   Beta{Float64}(α=7.0, β=21.0)   0.122411
	   3 │   591664          9        69     0.115385   Beta{Float64}(α=10.0, β=70.0)  0.144931
	   4 │   422985          3        36     0.0769231  Beta{Float64}(α=4.0, β=37.0)   0.178057
	   5 │   119752          1         5     0.166667   Beta{Float64}(α=2.0, β=6.0)    0.180755
	   6 │   548236         21        86     0.196262   Beta{Float64}(α=22.0, β=87.0)  0.191124
	   7 │   175735          0         5     0.0        Beta{Float64}(α=1.0, β=6.0)    0.191262
	   8 │   709269          3        37     0.075      Beta{Float64}(α=4.0, β=38.0)   0.200749
	   9 │   132388          2        12     0.142857   Beta{Float64}(α=3.0, β=13.0)   0.382025
	  10 │   449052          1         3     0.25       Beta{Float64}(α=2.0, β=4.0)    0.485961
	  11 │   449256          1         3     0.25       Beta{Float64}(α=2.0, β=4.0)    0.559443
	  12 │    76108          1         1     0.5        Beta{Float64}(α=2.0, β=2.0)    0.724031

The approach of using a multi-armed bandit here is nice because, if I
follow it, it avoids both situations where I undervalue really great
opportunities (because they're so crowded nobody goes there anymore), and
I can notice when locations *do* get worse. I had for example thought that
422985 was a great location, but the statistics definitely say otherwise,
and similar with 709269.

Additional variables I could take into account would be my enjoyment
of the approach, the attractiveness of the woman I'm speaking to, the
amount of time I'm spending between approaches, …

I will, however, exercise my judgement: I will *probably* take a closer
look at 76108, even if I don't feel very enthusiastic about it.

<!--
### Adding Unexplored Locations

I have some locations I haven't looked at in my city.
-->

### Beyond the Bandit

And if I wanted to be really fancy, I could use a 2-dimensional
[Gaussian process](https://en.wikipedia.org/wiki/Gaussian_Process), in
[kriging](https://en.wikipedia.org/wiki/Kriging) fashion, to interpolate
geographical data and find the best daygame locations that way. *Probably*
overkill.

<!--TODO: Fatebook predictions-->

### See Also

* [The Multi-Armed Bandit Problem and Its Solutions (Lilian Weng, 2018)](https://lilianweng.github.io/posts/2018-01-23-multi-armed-bandit/)
* [A penguin fish-recommender systems using multi-armed bandit pt. 1 (Sebastian Callh, 2020)](https://sebastiancallh.github.io/post/multi-armed-bandit-and-penguins/)

[home](./index.md)
------------------

*author: niplav, created: 2023-11-18, modified: 2024-09-30, language: english, status: in progress, importance: 2, confidence: likely*

> __I finally make use of my [daygame data](./data.html#Daygame) by
writing some code that implements a multi-armed bandit with Thompson
sampling on beta-distributed estimates of what proportion of approaches
in a particular location yield contact information.__

Using A Multi-Armed Bandit to Select Daygame Locations
=======================================================

> Glattes Eis  
Ein Paradeis  
Für den, der gut zu tanzen weiß.

*—Friedrich Nietzsche, “Für Tänzer”, 1882*

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
	32×7 DataFrame
	 Row │ location  successes  failures  success_prob  dist                           sample     name
	     │ Float64   Int64      Int64     Float64       Beta…                          Float64    String
	─────┼──────────────────────────────────────────────────────────────────────────────────────────────────
	   1 │ 571077.0          0         1     0.0        Beta{Float64}(α=1.0, β=2.0)    0.0202956  [REDACTED]
	   2 │ 371851.0          1        10     0.0909091  Beta{Float64}(α=2.0, β=11.0)   0.0311173  [REDACTED]
	   3 │ 449256.0          3        37     0.075      Beta{Float64}(α=4.0, β=38.0)   0.0320887  [REDACTED]
	   4 │ 785084.0          2        35     0.0540541  Beta{Float64}(α=3.0, β=36.0)   0.0338077  [REDACTED]
	   5 │  98955.0          1         7     0.125      Beta{Float64}(α=2.0, β=8.0)    0.0493673  [REDACTED]
	  ⋮  │    ⋮          ⋮         ⋮           ⋮                      ⋮                    ⋮      [REDACTED]
	  29 │ 817198.0          1         1     0.5        Beta{Float64}(α=2.0, β=2.0)    0.619935   [REDACTED]
	  30 │ 276017.0          3         5     0.375      Beta{Float64}(α=4.0, β=6.0)    0.787144   [REDACTED]
	  31 │ 692404.0          0         1     0.0        Beta{Float64}(α=1.0, β=2.0)    0.826964   [REDACTED]
	  32 │ 295748.0          1         0     1.0        Beta{Float64}(α=2.0, β=1.0)    0.982625   [REDACTED]
	                                                                                         23 rows omitted

The top option (namely 702595) is, unfortunately, in another city hundreds
kilometers from where I live.

So I want to filter out irrelevant locations, so I create a set of
locations that are amenable to weekday/weekend and good/bad weather
daygame:

	weekday_good_weather=[709269, 449256, 76108, 449052, 175735, 276017, 796877, 835159, 823073, 696163, 843941, 132388, 496077, 32441, 399686, 793915]
	weekday_bad_weather=[709269, 449256, 76108, 449052]
	weekend_good_weather=[692404, 10939, 709269, 157691, 175735, 276017, 702595, 449256, 76108, 793915, 796877, 835159, 823073, 696163, 531828, 781627, 843941, 132388, 496077, 371851, 32441, 399686, 449052]
	weekend_bad_weather=[709269, 449256, 76108, 449052, 702595, 531828]

Then, on a weekday with good weather (as it often is, at the time of
writing), I can then filter for locations in my current city with such
conditions:

	julia> filter(x->x[:location] in weekday_good_weather, sort(bandit, :sample))
	14×7 DataFrame
	 Row │ location  successes  failures  success_prob  dist                           sample     name
	     │ Float64   Int64      Int64     Float64       Beta…                          Float64    String
	─────┼──────────────────────────────────────────────────────────────────────────────────────────────────
	   1 │ 449256.0          3        37     0.075      Beta{Float64}(α=4.0, β=38.0)   0.0320887  [REDACTED]
	   2 │ 132388.0          9        71     0.1125     Beta{Float64}(α=10.0, β=72.0)  0.0543564  [REDACTED]
	   3 │ 175735.0          0         7     0.0        Beta{Float64}(α=1.0, β=8.0)    0.0923418  [REDACTED]
	   4 │ 823073.0          2        13     0.133333   Beta{Float64}(α=3.0, β=14.0)   0.11243    [REDACTED]
	   5 │ 449052.0          1        10     0.0909091  Beta{Float64}(α=2.0, β=11.0)   0.130813   [REDACTED]
	   6 │ 796877.0          0         3     0.0        Beta{Float64}(α=1.0, β=4.0)    0.153522   [REDACTED]
	   7 │ 696163.0          1         3     0.25       Beta{Float64}(α=2.0, β=4.0)    0.207392   [REDACTED]
	   8 │ 399686.0          2         5     0.285714   Beta{Float64}(α=3.0, β=6.0)    0.221436   [REDACTED]
	   9 │ 709269.0         22        87     0.201835   Beta{Float64}(α=23.0, β=88.0)  0.249274   [REDACTED]
	  10 │ 835159.0          5        16     0.238095   Beta{Float64}(α=6.0, β=17.0)   0.256881   [REDACTED]
	  11 │ 843941.0          0         1     0.0        Beta{Float64}(α=1.0, β=2.0)    0.272473   [REDACTED]
	  12 │ 496077.0         12        28     0.3        Beta{Float64}(α=13.0, β=29.0)  0.313311   [REDACTED]
	  13 │  76108.0          1         1     0.5        Beta{Float64}(α=2.0, β=2.0)    0.617513   [REDACTED]
	  14 │ 276017.0          3         5     0.375      Beta{Float64}(α=4.0, β=6.0)    0.787144   [REDACTED]

The approach of using a multi-armed bandit here is nice because, if I
follow it, it avoids both situations where I undervalue really great
opportunities (because they're so overgamed nobody goes there anymore),
and I can notice when locations *do* get worse. I had for example thought
that 449256 was a great location, but the statistics definitely say
otherwise, and similar with 449052.

Additional variables I could take into account would be my enjoyment
of the approach, the attractiveness of the woman I'm speaking to, the
amount of time I'm spending between approaches, …

I will, however, exercise my judgement: I'll *probably* take a closer
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

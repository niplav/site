[home](./index.md)
-------------------

*author: niplav, created: 2023-01-06, modified: 2023-06-21, language: english, status: notes, importance: 3, confidence: log*

> __Modeled after [Gwern 2018](https://www.gwern.net/Nootropics) I've
decided to log my nootropics usage and its effects.__

Nootropics
===========

You could put randomized substances in your body and find out what they
do by recording the outcomes. That's what I did.

<table>
<tbody>
	<tr>
		<td></td>
		<td>Log-score of predictions of substance</td>
		<td>Mindfulness effect size [d](https://en.wikipedia.org/wiki/Effect_size#Cohen's_d) (λ, p, σ increase)</td>
		<td>Absorption effect size [d](https://en.wikipedia.org/wiki/Effect_size#Cohen's_d) (λ, p, σ increase)</td>
		<td>Productivity effect size [d](https://en.wikipedia.org/wiki/Effect_size#Cohen's_d) (λ, p, σ increase)</td>
		<td>Creativity effect size [d](https://en.wikipedia.org/wiki/Effect_size#Cohen's_d) (λ, p, σ increase)</td>
		<td>Happiness effect size [d](https://en.wikipedia.org/wiki/Effect_size#Cohen's_d) (λ, p, σ increase)</td>
		<td>Contentment effect size [d](https://en.wikipedia.org/wiki/Effect_size#Cohen's_d) (λ, p, σ increase)</td>
		<td>Relaxation effect size [d](https://en.wikipedia.org/wiki/Effect_size#Cohen's_d) (λ, p, σ increase)</td>
		<td>Horniness effect size [d](https://en.wikipedia.org/wiki/Effect_size#Cohen's_d) (λ, p, σ increase)</td>
	</tr>
	<tr>
		<td>200mg Caffeine (n=1, m=40)</td>
		<td>-0.61</td>
		<td>0.61 (λ=10.12, p=0.0033, -0.019)</td>
		<td>0.56 (λ=9.32, p=0.0065, -0.071)</td>
		<td>0.78 (λ=58.50, p=1.8<sup>-32</sup>, 0.156)</td>
		<td>0.37 (λ=24.73, p=3.2<sup>-10</sup>, 0.095)</td>
		<td>0.47 (λ=15.83, p=1.22<sup>-5</sup>, 0.1)</td>
		<td>0.266 (λ=5.17, p=0.14, 0.141)</td>
		<td>-0.13 (λ=6.71, p=0.05, 0.61)</td>
		<td>-0.17 (λ=2.89, p=0.449, -0.28)</td>
	</tr>
</tbody>
</table>

Caffeine
---------

[Examine](https://examine.com/supplements/caffeine/).

### Experiment A: Self-Blinded RCT

Cost:

* Time
	* Time for filling: 35 minutes
	* Time for preparing envelopes: 40 minutes
* Cost of caffeine pills:
* Cost of empty capsules:
* Cost of sugar:

200mg caffeine pills, placebo pills filled with sugar, of each 25.
Put each pill with a corresponding piece of paper ("C" for caffeine,
"P" for placebo) into an unlabeled envelope.  Used `seq 1 50 | shuf`
to number the envelopes, and sorted them accordingly.

Variables tracked:

* Meditation: 45 minutes of ānāpānasati, started 0-60 minutes after taking the dose, tracking two variables.
	* __Mindfulness__: How aware I was of what was going on in my head, modulo my ability to influence it.
	* __Absorption__ (often called concentration): How "still" my mind was, how easily I was swept away by my thoughts.
* __Arm Prediction__: I tried to predict whether the substance I'd taken was placebo or caffeine.
* [Mood](./data.html#Mood): Tracking 4 different variables at random points during the day, namely
	* __Happiness/Sadness__
	* __Contentment/Discontentment__
	* __Relaxation/Stress__
	* __Horniness/Chastity__: Chastity being simply the opposite of horniness in this case.
* __Productivity__ and __creativity__, recorded at the end of the day.
* __Flashcard performance__: Did my daily flashcards for ~20 minutes, started 0-60 minutes after finishing meditation.

Notes on the experiment:

* 3rd dose: Out of fear that the placebo pills have some sugar stuck
outside of them, which could de-blind the dose, I take a bit (~10 g)
of sugar with each pill.
* 7th dose: Increase time between consumption and starting to meditate to
~45 minutes, after finding out that the onset of action is 45 minutes-1
hour.
* 14th dose: Noticed that during meditation, sharpness/clarity of
attention is ~high, and relaxing after becoming mindful is easy, but
attention strays just as easily.
* 49th dose: Took the pill, meditated, lay down during meditation and fell asleep. Likely<sub>10%</sub> placebo.

#### Statistical Method

In general, I'll be working with the [likelihood ratio
test](https://en.wikipedia.org/wiki/Likelihood-ratio_Test). For this,
let `$\mathbf{v}_P$` be the distribution of values of a variable
for the placebo arm, and `$\mathbf{v}_C$` the distribution of
values for a variable of the caffeine arm. (I apologise for the
`$C$` being ambiguous, since it could also refer to the [control
arm](https://en.wikipedia.org/wiki/Control_arm)).

Then let `$\theta_0=(\mu_0, \sigma_0)=MLE_{\mathcal{N}}(\mathbf{v}_P)$`
be the Gaussian maximum likelihood estimator for our placebo values,
and `$\theta=(\mu, \sigma)=MLE_{\mathcal{N}}(\mathbf{v}_C)$` be the MLE
for our caffeine values.

Then the likelihood ratio statistic `$\lambda$` is defined as

<div>
	$$\lambda=2 \log \frac{\mathcal{L}_C(\theta)}{\mathcal{L}_C(\theta_0)}$$
</div>

where `$\mathcal{L}_C(\theta)$` is the likelihood the caffeine distribution
assigns to the parameters `$\theta$`. This test is useful here because we
fix all values of `$\theta_0$`. See [Wassermann 2003 ch. 10.6]()<!--TODO:
link--> for more.

If `$\lambda \approx 0$`, then the MLE for the placebo arm is very close
to the MLE for the caffeine arm, the distributions are similar. If
`$\lambda>0$`, then the MLE for the placebo arm is quite different from
the caffeine arm (though there is no statement about which has *higher*
values). `$\lambda<0$` is not possible, since that would mean that
the MLE of the placebo distribution has a higher likelihood for the
caffeine data than the MLE of the caffeine distribution itself—not
very likely<!--TODO: sunglasses emoji?-->.

<!--TODO: effect sizes!-->

Note that I'm not a statistician, this is my first serious statistical
analysis, so please correct me if I'm making some important
mistakes. Sorry.

#### Predictions on the Outcomes of the Experiment

After collecting the data, but before analysing it,
I want to make some predictions about the outcome
of the experiment, similar to another attempt
[here](./range_and_forecasting_accuracy.html#Some_Predictions_About_The_Results).

<!--TODO: convert into a table?-->

* __Prediction of Arm__
	* My prediction about the content of the pill is more accurate than random guesses<sub>[80%](https://predictionbook.com/predictions/211893)</sub>.
	* My prediction about the content of the pill has a log score of more than -0.5<sub>[60%](https://predictionbook.com/predictions/211894)</sub>.
* __Meditation__
	* On days with caffeine, my average mindfulness during meditation was higher than days with placebo<sub>[60%](https://predictionbook.com/predictions/211895)</sub>.
	* On days with caffeine, my average absorption during meditation was higher than days with placebo<sub>[40%](https://predictionbook.com/predictions/211896)</sub>.
	* On days with caffeine, the variance of values for mindfulness during meditation was lower than on placebo days<sub>[55%](https://predictionbook.com/predictions/211897)</sub>.
	* On days with caffeine, the variance of values for absorption during meditation was lower than on placebo days<sub>[35%](https://predictionbook.com/predictions/211898)</sub>.
	* `$\lambda<1$` for the mindfulness values<sub>[20%](https://predictionbook.com/predictions/211899)</sub>.
	* `$\lambda<1$` for the absorption values<sub>[25%](https://predictionbook.com/predictions/211900)</sub>.
	* `$\lambda<4$` for the mindfulness values<sub>[82%](https://predictionbook.com/predictions/211901)</sub>.
	* `$\lambda<4$` for the absorption values<sub>[88%](https://predictionbook.com/predictions/211902)</sub>.
* __Mood__
	* On days with caffeine, my average happiness during the day was higher than days with placebo<sub>[65%](https://predictionbook.com/predictions/211903)</sub>.
	* On days with caffeine, my average contentment during the day was higher than days with placebo<sub>[45%](https://predictionbook.com/predictions/211904)</sub>.
	* On days with caffeine, my average relaxation during the day was higher than days with placebo<sub>[35%](https://predictionbook.com/predictions/211905)</sub>.
	* On days with caffeine, my average chastity during the day was higher than days with placebo<sub>[50%](https://predictionbook.com/predictions/211906)</sub>.
	* On days with caffeine, the variance of values for happiness during the day was lower than on placebo days<sub>[55%](https://predictionbook.com/predictions/211907)</sub>.
	* On days with caffeine, the variance of values for contentment during the day was lower than on placebo days<sub>[30%](https://predictionbook.com/predictions/211908)</sub>.
	* On days with caffeine, the variance of values for relaxation during the day was lower than on placebo days<sub>[30%](https://predictionbook.com/predictions/211909)</sub>.
	* On days with caffeine, the variance of values for chastity during the day was lower than on placebo days<sub>[50%](https://predictionbook.com/predictions/211910)</sub>.
	* `$\lambda<1$` for the happiness values<sub>[45%](https://predictionbook.com/predictions/211911)</sub>.
	* `$\lambda<1$` for the contentment values<sub>[40%](https://predictionbook.com/predictions/211912)</sub>.
	* `$\lambda<1$` for the relaxation values<sub>[37%](https://predictionbook.com/predictions/211913)</sub>.
	* `$\lambda<1$` for the chastity values<sub>[60%](https://predictionbook.com/predictions/211914)</sub>.
	* `$\lambda<4$` for the happiness values<sub>[85%](https://predictionbook.com/predictions/211915)</sub>.
	* `$\lambda<4$` for the contentment values<sub>[90%](https://predictionbook.com/predictions/211916)</sub>.
	* `$\lambda<4$` for the relaxation values<sub>[90%](https://predictionbook.com/predictions/211917)</sub>.
	* `$\lambda<4$` for the chastity values<sub>[95%](https://predictionbook.com/predictions/211918)</sub>.
* __Productivity and Creativity__
	* On days with caffeine, my average productivity during the day was higher than days with placebo<sub>52%</sub>.
	* On days with caffeine, my average creativity during the day was higher than days with placebo<sub>55%</sub>.
	* On days with caffeine, the variance of values for productivity during the day was lower than on placebo days<sub>40%</sub>.
	* On days with caffeine, the variance of values for creativity during the day was lower than on placebo days<sub>65%</sub>.
	* `$\lambda<1$` for the productivity values<sub>[40%](https://predictionbook.com/predictions/211919)</sub>.
	* `$\lambda<1$` for the creativity values<sub>[45%](https://predictionbook.com/predictions/211920)</sub>.
	* `$\lambda<4$` for the producitvity values<sub>[75%](https://predictionbook.com/predictions/211921)</sub>.
	* `$\lambda<4$` for the creativity values<sub>[80%](https://predictionbook.com/predictions/211922)</sub>.

I also recorded my predictions about the content of the pill on PredictionBook ([1](https://predictionbook.com/predictions/211311) [2](https://predictionbook.com/predictions/211312) [3](https://predictionbook.com/predictions/211313) [4](https://predictionbook.com/predictions/211314) [5](https://predictionbook.com/predictions/211857) [6](https://predictionbook.com/predictions/211858) [7](https://predictionbook.com/predictions/211859) [8](https://predictionbook.com/predictions/211860) [9](https://predictionbook.com/predictions/211861) [10](https://predictionbook.com/predictions/211862) [11](https://predictionbook.com/predictions/211863) [12](https://predictionbook.com/predictions/211864) [13](https://predictionbook.com/predictions/211865) [14](https://predictionbook.com/predictions/211866) [15](https://predictionbook.com/predictions/211867) [16](https://predictionbook.com/predictions/211868) [17](https://predictionbook.com/predictions/211869) [18](https://predictionbook.com/predictions/211870) [19](https://predictionbook.com/predictions/211871) [20](https://predictionbook.com/predictions/211872) [21](https://predictionbook.com/predictions/211873) [22](https://predictionbook.com/predictions/211874) [23](https://predictionbook.com/predictions/211875) [24](https://predictionbook.com/predictions/211876) [25](https://predictionbook.com/predictions/211877) [26](https://predictionbook.com/predictions/211878) [27](https://predictionbook.com/predictions/211879) [28](https://predictionbook.com/predictions/211880) 29 30 31 32 33 34 35 36 37 38 [39](https://predictionbook.com/predictions/211881) [40](https://predictionbook.com/predictions/211882) [41](https://predictionbook.com/predictions/211883) [42](https://predictionbook.com/predictions/211884) [43](https://predictionbook.com/predictions/211885) [44](https://predictionbook.com/predictions/211886) [45](https://predictionbook.com/predictions/211887) [46](https://predictionbook.com/predictions/211888) [47](https://predictionbook.com/predictions/211889) [48](https://predictionbook.com/predictions/211890) [49](https://predictionbook.com/predictions/211891) [50](https://predictionbook.com/predictions/211892)).

#### Analysis

We start by setting everything up and loading the data.

	import math
	import numpy as np
	import pandas as pd
	import scipy.stats as scistat

	substances=pd.read_csv('../..//data/substances.csv')

	meditations=pd.read_csv('../../data/meditations.csv')
	meditations['meditation_start']=pd.to_datetime(meditations['meditation_start'], unit='ms', utc=True)
	meditations['meditation_end']=pd.to_datetime(meditations['meditation_end'], unit='ms', utc=True)

	creativity=pd.read_csv('../../data/creativity.csv')
	creativity['datetime']=pd.to_datetime(creativity['datetime'], utc=True)

	productivity=pd.read_csv('../../data/productivity.csv')
	productivity['datetime']=pd.to_datetime(productivity['datetime'], utc=True)

	expa=substances.loc[substances['experiment']=='A'].copy()
	expa['datetime']=pd.to_datetime(expa['datetime'], utc=True)

The mood data is a bit special, since it doesn't have timezone info,
but that is easily remedied.

	mood=pd.read_csv('../../data/mood.csv')
	alarms=pd.to_datetime(pd.Series(mood['alarm']), format='mixed')
	mood['alarm']=pd.DatetimeIndex(alarms.dt.tz_localize('CET', ambiguous='infer')).tz_convert(tz='UTC')
	dates=pd.to_datetime(pd.Series(mood['date']), format='mixed')
	mood['date']=pd.DatetimeIndex(dates.dt.tz_localize('CET', ambiguous='infer')).tz_convert(tz='UTC')

##### Summary Statistics

We can first test how well my predictions fared:

	probs=np.array(expa['prediction'])
	outcomes=np.array([0 if substances[i]=='sugar' else 1 for i in substances.index])

*drumroll*

	>>> np.mean(list(map(lambda x: math.log(x[0]) if x[1]==1 else math.log(1-x[0]), zip(probs, outcomes))))
	-0.6142394580267694

At least this time I was better than chance:

	>>> np.mean(list(map(lambda x: math.log(x[0]) if x[1]==1 else math.log(1-x[0]), zip([0.5]*40, outcomes))))
	-0.6931471805599453

###### Meditation

Merging the meditations closest (on the right) to the consumption and
selecting the individual variables of interest:

	meditations.sort_values("meditation_start", inplace=True)
	meditations_a=pd.merge_asof(expa, meditations, left_on='datetime', right_on='meditation_start', direction='forward')
	caffeine_mindfulness=meditations_a.loc[meditations_a['substance']=='caffeine']['mindfulness_rating']
	placebo_mindfulness=meditations_a.loc[meditations_a['substance']=='sugar']['mindfulness_rating']
	caffeine_concentration=meditations_a.loc[meditations_a['substance']=='caffeine']['concentration_rating']
	placebo_concentration=meditations_a.loc[meditations_a['substance']=='sugar']['concentration_rating']

So, does it help?

	>>> (caffeine_concentration.mean()-placebo_concentration.mean())/meditations['concentration_rating'].std()
	0.5609411379318844
	>>> (caffeine_mindfulness.mean()-placebo_mindfulness.mean())/meditations['mindfulness_rating'].std()
	0.6171233170326925

Indeed! [Cohen's d](https://en.wikipedia.org/wiki/Effect_size#Cohen's_d)
here looks pretty good. Taking caffeine also reduces the variance of
both variables:

	>>> caffeine_mindfulness.std()-placebo_mindfulness.std()
	-0.01898430416807584
	>>> caffeine_concentration.std()-placebo_concentration.std()
	-0.07119944142518708

###### Productivity and Creativity

We repeat the same procedure for the productivity and creativity data:

	prod_a=pd.merge_asof(expa, productivity, left_on='datetime', right_on='datetime', direction='forward')
	creat_a=pd.merge_asof(expa, creativity, left_on='datetime', right_on='datetime', direction='forward')
	caffeine_productivity=prod_a.loc[meditations_a['substance']=='caffeine']['productivity']
	placebo_productivity=prod_a.loc[meditations_a['substance']=='sugar']['productivity']
	caffeine_creativity=creat_a.loc[meditations_a['substance']=='caffeine']['creativity']
	placebo_creativity=creat_a.loc[meditations_a['substance']=='sugar']['creativity']

And the result is…

	>>> (caffeine_productivity.mean()-placebo_productivity.mean())/prod_a['productivity'].std()
	0.7847612611667064
	>>> (caffeine_creativity.mean()-placebo_creativity.mean())/creat_a['creativity'].std()
	0.3684366228871795

Again surprisingly good! The creativity values are small enough to be
a fluke, but the productivity values seem cool.

In this case, though, caffeine *increases* variance in the variables
(not by very much):

	>>> caffeine_productivity.std()-placebo_productivity.std()
	0.1557773175491261
	>>> caffeine_creativity.std()-placebo_creativity.std()
	0.09479532961921128

###### Mood

Some unimportant pre-processing, in which we filter
for mood recordings 0-10 hours after caffeine intake, since
[`pd.merge_asof`](https://devdocs.io/pandas~1/reference/api/pandas.merge_asof)
doesn't do cartesian product:

	mood_a=expa.join(mood, how='cross')
	mood_a=mood_a.loc[(mood_a['alarm']-mood_a['datetime']<pd.Timedelta('10h'))&(mood_a['alarm']-mood_a['datetime']>pd.Timedelta('0h'))]
	caffeine_mood=mood_a.loc[mood_a['substance']=='caffeine']
	placebo_mood=mood_a.loc[mood_a['substance']=='sugar']

And now the analysis:

	>>> caffeine_mood[['happy', 'content', 'relaxed', 'horny']].describe()
	           happy    content    relaxed       horny
	count  64.000000  64.000000  64.000000   64.000000
	mean   52.484375  51.515625  50.718750   46.843750
	std     2.145443   2.581941   3.382817    2.912582
	[…]
	>>> placebo_mood[['happy', 'content', 'relaxed', 'horny']].describe()
	           happy    content    relaxed       horny
	count  57.000000  57.000000  57.000000   57.000000
	mean   51.473684  50.842105  51.122807   47.368421
	std     2.045075   2.440649   2.771476    3.188325
	[…]

Which leads to [d](https://en.wikipedia.org/wiki/Effect_size#Cohen's_d)
of ~0.47 for happiness, ~0.266 for contentment, -0.13 for relaxation
and -0.17 for horniness.

##### Likelihood Ratios

We assume (at first) that the data is distributed normally<!--TODO:
link-->. The we can define a function for the gaussian likelihood
of a distribution given some parameters:

	def normal_likelihood(data, mu, std):
		return np.product(scistat.norm.pdf(data, loc=mu, scale=std))

And now we can compute the likelihood ratio
`$\frac{\mathcal{L}{θ}}{\mathcal{L}{θ_0}}$` for the null hypothesis
`$θ_0=\text{MLE}(\mathbf{v}_P)$` for the placebo data `$\mathbf{v}_P$`,
and also the result of the likelihood ratio test:

	def placebo_likelihood(active, placebo):
		placebo_mle_lh=normal_likelihood(active, placebo.mean(), placebo.std())
		active_mle_lh=normal_likelihood(active, active.mean(), active.std())
		return active_mle_lh/placebo_mle_lh

	def likelihood_ratio_test(lr):
		return 2*np.log(lr)

And this gives us surprisingly large values:

	>> placebo_likelihood_ratio(caffeine_mindfulness, placebo_mindfulness)
	157.37572997585897
	>>> likelihood_ratio_test(placebo_likelihood_ratio(caffeine_mindfulness, placebo_mindfulness))
	10.11727226160484
	>>> placebo_likelihood_ratio(caffeine_concentration, placebo_concentration)
	105.8473930980437
	>>> likelihood_ratio_test(placebo_likelihood_ratio(caffeine_concentration, placebo_concentration))
	9.323996738023183
	>>> placebo_likelihood_ratio(caffeine_productivity, placebo_productivity)
	5053632067240.518
	>>> likelihood_ratio_test(placebo_likelihood_ratio(caffeine_productivity, placebo_productivity))
	58.50225664387183
	>>> placebo_likelihood_ratio(caffeine_creativity, placebo_creativity)
	234560.28379684332
	>>> likelihood_ratio_test(placebo_likelihood_ratio(caffeine_creativity, placebo_creativity))
	24.7309358151824

And, if one is interested in p-values, those correspond to (with 2 degrees of freedom each):

	def llrt_pval(lmbda, df=2):
		return scistat.chi2.cdf(df, lmbda)

	>>> llrt_pval([10.11727226160484, 9.323996738023183, 58.50225664387183, 24.7309358151824])
	array([3.30451079e-03, 6.51771165e-03, 1.83724663e-32, 3.27886988e-10])

I find these results surprisingly strong, and am still kind of mystified
why. Surely caffeine isn't *that* reliable!

And, the same, for mood:

	>>> placebo_likelihood_ratio(caffeine_mood['happy'], placebo_mood['happy'])
	2743.9269008532096
	>>> likelihood_ratio_test(placebo_likelihood_ratio(caffeine_mood['happy'], placebo_mood['happy']))
	15.83429069772036
	>>> placebo_likelihood_ratio(caffeine_mood['content'], placebo_mood['content'])
	13.301378181774787
	>>> likelihood_ratio_test(placebo_likelihood_ratio(caffeine_mood['content'], placebo_mood['content']))
	5.175735305098163
	>>> placebo_likelihood_ratio(caffeine_mood['relaxed'], placebo_mood['relaxed'])
	28.57583615444588
	>>> likelihood_ratio_test(placebo_likelihood_ratio(caffeine_mood['relaxed'], placebo_mood['relaxed']))
	6.7051229420012906
	>>> placebo_likelihood_ratio(caffeine_mood['horny'], placebo_mood['horny'])
	4.23238893275755
	>>> likelihood_ratio_test(placebo_likelihood_ratio(caffeine_mood['horny'], placebo_mood['horny']))
	2.8855331863174007

Creatine
---------

[Examine](https://examine.com/supplements/creatine/). I
follow the loading procedure detailed
[here](https://examine.com/supplements/creatine/#NJj4E2e-do-i-need-to-load-creatine):

> [Creatine](https://examine.com/supplements/creatine/) is a supplement that is known for having a 'loading' phase followed by a 'maintenance' phase. A typical creatine cycle has three parts to it.
>  
> * Take 20-25g (or 0.3g/kg) for 5-7 days (Loading)
> * Then take 5g daily for 3-4 weeks (Maintenance)
> * Take a week or two off creatine, and then repeat (Wash-out)

First dose was taken on 2023-01-06.

I'm especially interested in the effects of
creatine on my cognition (it [might increase IQ in
vegetarians](https://examine.com/supplements/creatine/)
(or it [might not](https://gwern.net/creatine)?), and I'm a
[lacto-vegetarian](https://en.wikipedia.org/wiki/Lacto-vegetarianism)),
my exercising performance and my meditation ability.

L-Theanine
-----------

> L-Theanine is synergistic with caffeine in regards to attention
switching<sup>[\[318\]](https://examine.com/supplements/caffeine/research/#ref-318)</sup>
and
alertness<sup>[\[319\]](https://examine.com/supplements/caffeine/research/#ref-319)[\[320\]](https://examine.com/supplements/caffeine/research/#ref-320)</sup>
and reduces susceptibility to distractions
(focus).<sup>[\[320\]](https://examine.com/supplements/caffeine/research/#ref-320)[\[321\]](https://examine.com/supplements/caffeine/research/#ref-320)</sup>
However, alertness seems to be relatively subjective
and may not be a reliable increase between these two
compounds,<sup>[\[318\]](https://examine.com/supplements/caffeine/research/#ref-318)</sup>
and increases in mood are either present or<!--TODO: correct?-->
absent.<sup>[\[322\]](https://examine.com/supplements/caffeine/research/#ref-322)[\[318\]](https://examine.com/supplements/caffeine/research/#ref-318)[\[323\]](https://examine.com/supplements/caffeine/research/#ref-323)</sup>
This may be due to theanine being a relatively subpar
nootropic in and of itself pertaining to the above parameters,
but augmenting caffeine's effects; some studies do note
that theanine does not affect the above parameters in and of
itself.<sup>[\[324\]](https://examine.com/supplements/caffeine/research/#ref-324)</sup>
Due to this, any insensitivity or habituation to caffeine would reduce
the effects of the combination as L-theanine may work through caffeine.
>
> L-Theanine does not appear to be synergistic with caffeine
in regards to attention to a prolonged and monotonous
task.<sup>[\[325\]](https://examine.com/supplements/caffeine/research/#ref-325)</sup>
<!--Foxe JJ, et al. Assessing the effects of caffeine and theanine on the maintenance of vigilance during a sustained attention task.-->

*—Kamal Patel, [“Caffeine”](https://examine.com/supplements/caffeine/research/#3JD9zlr-nutrient-nutrient-interactions_3JD9zlr-l-theanine), 2023*

### Experiment B: Self-Blinded RCT

* Time for preparation: 93 minutes
* Cost of l-theanine pills:
* Cost of empty capsules:

Melatonin
----------

See [my report on my melatonin consumption](./reports.html#Melatonin).

<!--TODO: describe the weird sometimes-insomnia effects-->

Nicotine
---------

I started taking nicotine (in the form of nicotine chewing gum with 2mg of
active ingredient) in high-pressure situations (e.g. I'm procrastinating
on an important task and have anxiety around it, or during exams). So
far, it seems especially useful to break me out of an akratic rut.
~0.47 for happiness, ~0.266 for contentment, -0.13 for relaxation and
-0.17 for horniness.

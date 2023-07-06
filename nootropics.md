[home](./index.md)
-------------------

*author: niplav, created: 2023-01-06, modified: 2023-07-05, language: english, status: notes, importance: 3, confidence: log*

> __Modeled after [Gwern 2018](https://www.gwern.net/Nootropics) I've
decided to log my nootropics usage and its effects.__

Nootropics
===========

<!--Nootropics and meditation:
*Caffeine
	* https://skemman.is/handle/1946/41957
	* Maybe https://www.frontiersin.org/articles/10.3389/fpsyg.2020.610156/full accidentally reveals some info on caffeine effect on mindfulness? But probably not.
* Caffeine & L-Theanine
	* http://cafeesaude.com/wp-content/uploads/2012/01/Humor-J-Bryan-et-al-Appetite-Volume-58-2012.pdf
* L-Theanine
	* https://citeseerx.ist.psu.edu/document?repid=rep1&type=pdf&doi=6899536c95f528308ab27810cfd17f4ba3a96d9e
-->

You could put randomized substances in your body and find out what they
do by recording the outcomes. That's what I did.

<table>
<tbody>
	<tr>
		<td></td>
		<td>Log-score of predictions of substance</td>
		<td>Absorption effect size d (λ, p, σ increase)</td>
		<td>Mindfulness effect size d (λ, p, σ increase)</td>
		<td>Productivity effect size d (λ, p, σ increase)</td>
		<td>Creativity effect size d (λ, p, σ increase)</td>
		<td>Happiness effect size d (λ, p, σ increase)</td>
		<td>Contentment effect size d (λ, p, σ increase)</td>
		<td>Relaxation effect size d (λ, p, σ increase)</td>
		<td>Chastity effect size d (λ, p, σ increase)</td>
	</tr>
	<tr>
		<td>200mg Caffeine (n=1, m=50)</td>
		<td>-0.6</td>
		<td>0.61 (λ=13.3, p=0.00017, -0.072)</td>
		<td>0.58 (λ=11.8, p=0.0007, 0.021)</td>
		<td>0.58 (λ=28.9, p=1.3<sup>-12</sup>, 0.11)</td>
		<td>0.38 (λ=32.9, p=5.2<sup>-15</sup>, 0.09)</td>
		<td>0.27 (λ=10.6, p=0.002, 0.3)</td>
		<td>0.13 (λ=7.66, p=0.02, 0.47)</td>
		<td>-0.11 (λ=5, p=0.15, 0.42)</td>
		<td>-0.14 (λ=1.9, p=0.64, 0.11)</td>
	</tr>
</tbody>
</table>

I am especially interested in testing many different substances for
their effect on meditation, while avoiding negative side effects. The
benefits from high meditational attainments valuable to me, and seem
especially likely to benefit from chemical intervention, since the
[Algernon argument](https://gwern.net/drug-heuristic#loopholes)
likely doesn't apply: Meditative attainments might've
not led to a fitness advantage (even, by [opportunity
cost](https://en.wikipedia.org/wiki/Opportunity_cost), to a fitness
disadvantage), and so were likely selected against, but most of us
don't care *that* much about inclusive genetic fitness and more about
psychological well-being. Evolutionary dynamics favor being like
[Dschingis Khan](https://en.wikipedia.org/wiki/Dschinghis_Khan)
([dozens to hundreds of
offspring](https://en.wikipedia.org/wiki/Family_and_descendants_of_Genghis_Khan))
over [Siddharta Gautama](https://en.wikipedia.org/wiki/Siddharta_Gotama)
([one son](https://en.wikipedia.org/wiki/R%C4%81hula)), but I'd rather
attain [sotāpanna](https://en.wikipedia.org/wiki/Sotāpanna) than
pillage and murder.

And meditative attainments are *costly*: they take tens to
hundreds to thousands of hours to reach, which would make simple
psychopharmacological interventions worthwhile. I also don't buy
that they miss the point of meditation—most people already struggle
enough, so some help doesn't make it a cakewalk; ["reach heaven through
fraud"](https://pastebin.com/xuVuVnhw). One must be careful not to fall
into the trap of taking substances that feel good but lessen sensory
clarity (which I believe was the original intent behind the [fifth
precept](https://en.wikipedia.org/wiki/Five_precepts#Fifth_precept),
and so I'll exclude e.g. opiates from the substances to test).

Caffeine
---------

I won't dig too deep into the effects of caffeine, as other people have
done that already ([Examine](https://examine.com/supplements/caffeine/),
[Gwern](https://gwern.net/nootropic/nootropics#caffeine),
[Wikipedia](https://en.wikipedia.org/wiki/Caffeine)).

### Experiment A: Self-Blinded RCT

Variables tracked (see more [here](./data.html)):

* Meditation: 45 minutes of ānāpānasati, started 0-60 minutes after taking the dose, tracking two variables.
	* __Mindfulness__: How aware I was of what was going on in my head, modulo my ability to influence it.
	* __Absorption__ (often called concentration): How "still" my mind was, how easily I was swept away by my thoughts.
* __Flashcard performance__: Did my daily flashcards for ~20 minutes, started 0-60 minutes after finishing meditation.
* __Arm Prediction__: I tried to predict whether the substance I'd taken was placebo or caffeine.
* [Mood](./data.html#Mood): Tracking 4 different variables at random points during the day, namely
	* __Happiness/Sadness__
	* __Contentment/Discontentment__
	* __Relaxation/Stress__
	* __Horniness/Chastity__: Chastity being simply the opposite of horniness in this case.
* __Productivity__ and __creativity__, recorded at the end of the day.

The total cost of the experiment is at least 21.5€:

* Time: The [Clearer Thinking tool](https://programs.clearerthinking.org/what_is_your_time_really_worth_to_you.html) for the value of my time returns 15€/hour, which gives a time cost of 18.75€ for preparing the experiment.
	* Time for filling: 35 minutes
	* Time for preparing envelopes: 40 minutes
* Cost of caffeine pills: `$\frac{0.0825€}{\text{200mg caffeine pill}} \cdot \text{ 200mg caffeine pills}=2.0625€$`
* Cost of empty capsules: `$\frac{0.03€}{\text{capsule}} \cdot 25 \text{ capsules}=0.75€$`
* Cost of sugar: Negligible.

200mg caffeine pills, placebo pills filled with sugar, of each 25.
Put each pill with a corresponding piece of paper ("C" for caffeine,
"P" for placebo) into an unlabeled envelope.  Used `seq 1 50 | shuf`
to number the envelopes, and sorted them accordingly.

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
test](https://en.wikipedia.org/wiki/Likelihood-ratio_Test) (encouraged by
[this article]((https://arbital.com/p/likelihoods_not_pvalues/)). For
this, let `$\mathbf{v}_P$` be the distribution of values of a
variable for the placebo arm, and `$\mathbf{v}_C$` the distribution
of values for a variable of the caffeine arm. (I apologise for the
`$C$` being ambiguous, since it could also refer to the [control
arm](https://en.wikipedia.org/wiki/Control_arm)).

Then let `$\theta_0=(\mu_0, \sigma_0)=MLE_{\mathcal{N}}(\mathbf{v}_P)$`
be the Gaussian [maximum likelihood
estimator](https://en.wikipedia.org/wiki/Maximum_likelihood_estimation)
for our placebo values, and
`$\theta=(\mu, \sigma)=MLE_{\mathcal{N}}(\mathbf{v}_C)$`
be the MLE for our caffeine values.

Then the likelihood ratio statistic `$\lambda$` is defined as

<div>
	$$\lambda=2 \log \frac{\mathcal{L}_C(\theta)}{\mathcal{L}_C(\theta_0)}$$
</div>

where `$\mathcal{L}_C(\theta)$` is the likelihood the caffeine
distribution assigns to the parameters `$\theta$`. This test is useful
here because we fix all values of `$\theta_0$`. See [Wasserman 2003
ch. 10.6](https://www.goodreads.com/book/show/411722.All_of_Statistics)
for more.

If `$\lambda \approx 0$`, then the MLE for the placebo arm is very close
to the MLE for the caffeine arm, the distributions are similar. If
`$\lambda>0$`, then the MLE for the placebo arm is quite different from
the caffeine arm (though there is no statement about which has *higher*
values). `$\lambda<0$` is not possible, since that would mean that
the MLE of the placebo distribution has a higher likelihood for the
caffeine data than the MLE of the caffeine distribution itself—not
very likely<!--TODO: sunglasses emoji?-->.

Note that I'm not a statistician, this is my first serious statistical
analysis, so please correct me if I'm making some important
mistakes. Sorry.

#### Predictions on the Outcomes of the Experiment

After collecting the data, but before analysing it,
I want to make some predictions about the outcome
of the experiment, similar to another attempt
[here](./range_and_forecasting_accuracy.html#Some_Predictions_About_The_Results).

Moved [here](#Caffeine_1).

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
	substances=np.array(expa['substance'])
	outcomes=np.array([0 if i=='sugar' else 1 for i in substances])

*drumroll*

	>>> np.mean(list(map(lambda x: math.log(x[0]) if x[1]==1 else math.log(1-x[0]), zip(probs, outcomes))))
	-0.5991670759554912

At least this time I was better than chance:

	>>> np.mean(list(map(lambda x: math.log(x[0]) if x[1]==1 else math.log(1-x[0]), zip([0.5]*40, outcomes))))
	-0.6931471805599453

###### Meditation

Merging the meditations closest (on the right) to the consumption and
selecting the individual variables of interest:

	meditations.sort_values("meditation_start", inplace=True)
	meditations_a=pd.merge_asof(expa, meditations, left_on='datetime', right_on='meditation_start', direction='forward')
	caffeine_concentration=meditations_a.loc[meditations_a['substance']=='caffeine']['concentration_rating']
	placebo_concentration=meditations_a.loc[meditations_a['substance']=='sugar']['concentration_rating']
	caffeine_mindfulness=meditations_a.loc[meditations_a['substance']=='caffeine']['mindfulness_rating']
	placebo_mindfulness=meditations_a.loc[meditations_a['substance']=='sugar']['mindfulness_rating']

So, does it help?

	>>> (caffeine_concentration.mean()-placebo_concentration.mean())/meditations['concentration_rating'].std()
	0.6119357868347828
	>>> (caffeine_mindfulness.mean()-placebo_mindfulness.mean())/meditations['mindfulness_rating'].std()
	0.575981762563846

Indeed! [Cohen's d](https://en.wikipedia.org/wiki/Effect_size#Cohen's_d)
here looks pretty good. Taking caffeine also reduces the variance of
both variables:

	>>> caffeine_concentration.std()-placebo_concentration.std()
	-0.0720877290884765
	>>> caffeine_mindfulness.std()-placebo_mindfulness.std()
	0.02186797288826836

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
	0.5784143673702401
	>>> (caffeine_creativity.mean()-placebo_creativity.mean())/creat_a['creativity'].std()
	0.38432393552829164

Again surprisingly good! The creativity values are small enough to be
a fluke, but the productivity values seem cool.

In this case, though, caffeine *increases* variance in the variables
(not by very much):

	>>> caffeine_productivity.std()-placebo_productivity.std()
	0.1139221931098384
	>>> caffeine_creativity.std()-placebo_creativity.std()
	0.08619686235791152

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
	           happy    content    relaxed      horny
	count  88.000000  88.000000  88.000000  88.000000
	mean   52.193182  51.227273  50.704545  46.568182
	std     2.396635   2.911441   3.115254   3.117601
	[…]
	>>> placebo_mood[['happy', 'content', 'relaxed', 'horny']].describe()
	           happy    content    relaxed      horny
	count  73.000000  73.000000  73.000000  73.000000
	mean   51.575342  50.876712  51.041096  47.000000
	std     2.101043   2.437811   2.699992   3.009245
	[…]

Which leads to [d](https://en.wikipedia.org/wiki/Effect_size#Cohen's_d)
of ~0.27 for happiness, ~0.13 for contentment, ~-0.11 for relaxation
and ~-0.14 for horniness.

##### Likelihood Ratios

We assume (at first) that the data is [distributed
normally](https://en.wikipedia.org/wiki/Normal_distribution). Then we
can define a function for the gaussian likelihood of a distribution
given some parameters:

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

	>>> placebo_likelihood_ratio(caffeine_concentration, placebo_concentration)
	776.6147119766716
	>>> likelihood_ratio_test(placebo_likelihood_ratio(caffeine_concentration, placebo_concentration))
	13.309888722406932
	>> placebo_likelihood_ratio(caffeine_mindfulness, placebo_mindfulness)
	363.3984201164464
	>>> likelihood_ratio_test(placebo_likelihood_ratio(caffeine_mindfulness, placebo_mindfulness))
	11.790999616893938
	>>> placebo_likelihood_ratio(caffeine_productivity, placebo_productivity)
	1884090.6347491818
	>>> likelihood_ratio_test(placebo_likelihood_ratio(caffeine_productivity, placebo_productivity))
	28.8979116811553
	>>> placebo_likelihood_ratio(caffeine_creativity, placebo_creativity)
	14009015.173307568
	>>> likelihood_ratio_test(placebo_likelihood_ratio(caffeine_creativity, placebo_creativity))
	32.910423242578126

And, if one is interested in p-values, those correspond to (with 2 degrees of freedom each):

	def llrt_pval(lmbda, df=2):
		return scistat.chi2.cdf(df, lmbda)

	>>> llrt_pval([13.309888722406932,11.790999616893938, 28.8979116811553, 32.910423242578126])
	array([1.66559304e-04, 7.23739116e-04 ,1.34836408e-12, 5.17222209e-15])

I find these results surprisingly strong, and am still kind of mystified
why. Surely caffeine isn't *that* reliable!

And, the same, for mood:

	>>> placebo_likelihood_ratio(caffeine_mood['happy'], placebo_mood['happy'])
	204.81283712162838
	>>> likelihood_ratio_test(placebo_likelihood_ratio(caffeine_mood['happy'], placebo_mood['happy']))
	10.644193144917832
	>>> placebo_likelihood_ratio(caffeine_mood['content'], placebo_mood['content'])
	46.08310645632934
	>>> likelihood_ratio_test(placebo_likelihood_ratio(caffeine_mood['content'], placebo_mood['content']))
	7.6608928570645105
	>>> placebo_likelihood_ratio(caffeine_mood['relaxed'], placebo_mood['relaxed'])
	12.229945616108525
	>>> likelihood_ratio_test(placebo_likelihood_ratio(caffeine_mood['relaxed'], placebo_mood['relaxed']))
	5.007775005855661
	>>> placebo_likelihood_ratio(caffeine_mood['horny'], placebo_mood['horny'])
	2.670139324155222
	>>> likelihood_ratio_test(placebo_likelihood_ratio(caffeine_mood['horny'], placebo_mood['horny']))
	1.9642613047646074

And the p-values of those are:

	>>> llrt_pval([10.644193144917832, 7.6608928570645105, 5.007775005855661, 1.9642613047646074])
	array([0.0020736 , 0.02462515, 0.15015613, 0.63984027])

#### Conclusion

Caffeine appears helpful for everything except relaxation (and it makes
me hornier, which I'm neutral about). I'd call this experiment a success
and will be running more in the future, while in the meantime taking
caffeine before morning meditations.

Full code for the experiment [here](./code/experiment_a/load.py).

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

See again [Examine](https://examine.com/supplements/theanine/research/),
[Wikipedia](https://en.wikipedia.org/wiki/Theanine) and
[Gwern](https://gwern.net/Nootropics#L-Theanine).

### Experiment B: Self-Blinded RCT

* Time for preparation: 93 minutes
* Cost of l-theanine pills: `$\frac{~0.25€}{\text{500mg L-theanine pill}} \cdot 25 \text{ 500mg L-theanine pills}=6.25€$`
* Cost of empty capsules: `$0.75€$`

Notes during consumption:

* 1st dose: Made a mistake while filling the envelopes, accidentally deblinded myself.

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

Appendix A: Predictions on Self-Blinded RCTs
---------------------------------------------

Predicting the outcomes of personal experiments give a useful way to
train ones own calibration, I take it a step further and record the
predictions for the world to observe my idiocy.

### Caffeine

<!--TODO: convert into a table?-->

* __Prediction of Arm__
	* My prediction about the content of the pill is more accurate than random guesses<sub>[80%](https://predictionbook.com/predictions/211893)</sub>: Yes.
	* My prediction about the content of the pill has a log score of more than -0.5<sub>[60%](https://predictionbook.com/predictions/211894)</sub>: No.
* __Meditation__
	* On days with caffeine, my average mindfulness during meditation was higher than days with placebo<sub>[60%](https://predictionbook.com/predictions/211895)</sub>: Yes.
	* On days with caffeine, my average absorption during meditation was higher than days with placebo<sub>[40%](https://predictionbook.com/predictions/211896)</sub>: Yes.
	* On days with caffeine, the variance of values for mindfulness during meditation was lower than on placebo days<sub>[55%](https://predictionbook.com/predictions/211897)</sub>: No.
	* On days with caffeine, the variance of values for absorption during meditation was lower than on placebo days<sub>[35%](https://predictionbook.com/predictions/211898)</sub>: Yes.
	* `$\lambda<1$` for the mindfulness values<sub>[20%](https://predictionbook.com/predictions/211899)</sub>: No.
	* `$\lambda<1$` for the absorption values<sub>[25%](https://predictionbook.com/predictions/211900)</sub>: No.
	* `$\lambda<4$` for the mindfulness values<sub>[82%](https://predictionbook.com/predictions/211901)</sub>: No.
	* `$\lambda<4$` for the absorption values<sub>[88%](https://predictionbook.com/predictions/211902)</sub>: No.
* __Mood__
	* On days with caffeine, my average happiness during the day was higher than days with placebo<sub>[65%](https://predictionbook.com/predictions/211903)</sub>: Yes.
	* On days with caffeine, my average contentment during the day was higher than days with placebo<sub>[45%](https://predictionbook.com/predictions/211904)</sub>: Yes.
	* On days with caffeine, my average relaxation during the day was higher than days with placebo<sub>[35%](https://predictionbook.com/predictions/211905)</sub>: No.
	* On days with caffeine, my average chastity during the day was higher than days with placebo<sub>[50%](https://predictionbook.com/predictions/211906)</sub>: No.
	* On days with caffeine, the variance of values for happiness during the day was lower than on placebo days<sub>[55%](https://predictionbook.com/predictions/211907)</sub>: No.
	* On days with caffeine, the variance of values for contentment during the day was lower than on placebo days<sub>[30%](https://predictionbook.com/predictions/211908)</sub>: No.
	* On days with caffeine, the variance of values for relaxation during the day was lower than on placebo days<sub>[30%](https://predictionbook.com/predictions/211909)</sub>: No.
	* On days with caffeine, the variance of values for chastity during the day was lower than on placebo days<sub>[50%](https://predictionbook.com/predictions/211910)</sub>: No.
	* `$\lambda<1$` for the happiness values<sub>[45%](https://predictionbook.com/predictions/211911)</sub>: No.
	* `$\lambda<1$` for the contentment values<sub>[40%](https://predictionbook.com/predictions/211912)</sub>: No.
	* `$\lambda<1$` for the relaxation values<sub>[37%](https://predictionbook.com/predictions/211913)</sub>: No.
	* `$\lambda<1$` for the chastity values<sub>[60%](https://predictionbook.com/predictions/211914)</sub>: No.
	* `$\lambda<4$` for the happiness values<sub>[85%](https://predictionbook.com/predictions/211915)</sub>: No.
	* `$\lambda<4$` for the contentment values<sub>[90%](https://predictionbook.com/predictions/211916)</sub>: No.
	* `$\lambda<4$` for the relaxation values<sub>[90%](https://predictionbook.com/predictions/211917)</sub>: No.
	* `$\lambda<4$` for the chastity values<sub>[95%](https://predictionbook.com/predictions/211918)</sub>: Yes.
* __Productivity and Creativity__
	* On days with caffeine, my average productivity during the day was higher than days with placebo<sub>[52%](https://predictionbook.com/predictions/211991)</sub>: Yes.
	* On days with caffeine, my average creativity during the day was higher than days with placebo<sub>[55%](https://predictionbook.com/predictions/211992)</sub>: Yes.
	* On days with caffeine, the variance of values for productivity during the day was lower than on placebo days<sub>[40%](https://predictionbook.com/predictions/211993)</sub>: No.
	* On days with caffeine, the variance of values for creativity during the day was lower than on placebo days<sub>[65%](https://predictionbook.com/predictions/211994)</sub>: No.
	* `$\lambda<1$` for the productivity values<sub>[40%](https://predictionbook.com/predictions/211919)</sub>: No.
	* `$\lambda<1$` for the creativity values<sub>[45%](https://predictionbook.com/predictions/211920)</sub>: No.
	* `$\lambda<4$` for the productivity values<sub>[75%](https://predictionbook.com/predictions/211921)</sub>: No.
	* `$\lambda<4$` for the creativity values<sub>[80%](https://predictionbook.com/predictions/211922)</sub>: No.

I also recorded my predictions about the content of the pill on PredictionBook ([1](https://predictionbook.com/predictions/211311) [2](https://predictionbook.com/predictions/211312) [3](https://predictionbook.com/predictions/211313) [4](https://predictionbook.com/predictions/211314) [5](https://predictionbook.com/predictions/211857) [6](https://predictionbook.com/predictions/211858) [7](https://predictionbook.com/predictions/211859) [8](https://predictionbook.com/predictions/211860) [9](https://predictionbook.com/predictions/211861) [10](https://predictionbook.com/predictions/211862) [11](https://predictionbook.com/predictions/211863) [12](https://predictionbook.com/predictions/211864) [13](https://predictionbook.com/predictions/211865) [14](https://predictionbook.com/predictions/211866) [15](https://predictionbook.com/predictions/211867) [16](https://predictionbook.com/predictions/211868) [17](https://predictionbook.com/predictions/211869) [18](https://predictionbook.com/predictions/211870) [19](https://predictionbook.com/predictions/211871) [20](https://predictionbook.com/predictions/211872) [21](https://predictionbook.com/predictions/211873) [22](https://predictionbook.com/predictions/211874) [23](https://predictionbook.com/predictions/211875) [24](https://predictionbook.com/predictions/211876) [25](https://predictionbook.com/predictions/211877) [26](https://predictionbook.com/predictions/211878) [27](https://predictionbook.com/predictions/211879) [28](https://predictionbook.com/predictions/211880) [29](https://predictionbook.com/predictions/211967) [30](https://predictionbook.com/predictions/211968) [31](https://predictionbook.com/predictions/211969) [32](https://predictionbook.com/predictions/211970) [33](https://predictionbook.com/predictions/211971) [34](https://predictionbook.com/predictions/211972) [35](https://predictionbook.com/predictions/211973) [36](https://predictionbook.com/predictions/211974) [37](https://predictionbook.com/predictions/211975) [38](https://predictionbook.com/predictions/211976) [39](https://predictionbook.com/predictions/211881) [40](https://predictionbook.com/predictions/211882) [41](https://predictionbook.com/predictions/211883) [42](https://predictionbook.com/predictions/211884) [43](https://predictionbook.com/predictions/211885) [44](https://predictionbook.com/predictions/211886) [45](https://predictionbook.com/predictions/211887) [46](https://predictionbook.com/predictions/211888) [47](https://predictionbook.com/predictions/211889) [48](https://predictionbook.com/predictions/211890) [49](https://predictionbook.com/predictions/211891) [50](https://predictionbook.com/predictions/211892)).

This comes out badly for me, again:

	>>> import math
	>>> import numpy as np
	>>> probs=np.array([0.8, 0.6, 0.6, 0.4, 0.55, 0.35, 0.2, 0.25, 0.82, 0.88, 0.65, 0.45, 0.35, 0.5, 0.55, 0.3, 0.3, 0.5, 0.45, 0.4, 0.37, 0.6, 0.85, 0.9, 0.9, 0.95, 0.52, 0.55, 0.4, 0.65, 0.4, 0.45, 0.75, 0.8])
	>>> outcomes=np.array([1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0])
	>>> np.mean(list(map(lambda x: math.log(x[0]) if x[1]==1 else math.log(1-x[0]), zip(probs, outcomes))))
	-0.8610697622640346
	>>> np.mean(list(map(lambda x: math.log(x[0]) if x[1]==1 else math.log(1-x[0]), zip([0.5]*40, outcomes))))
	-0.6931471805599452

I am significantly *worse* than chance in my predictions.

> Die Welt gibt dir viel falsche Zeichen,  
> dem tückischen Geist zu vergleichen,  
> Du bist, alle Zeichen verachtend,  
> zu dem ohne Zeichen gegangen.

*—Dschelāladdīn Rūmī, “Am Ende bist du entschwunden”, 1256*

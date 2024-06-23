[home](./index.md)
------------------

*author: niplav, created: 2024-01-29, modified: 2024-01-29, language: english, status: draft, importance: 3, confidence: possible*

> __In which I investigate whether not masturbating makes my mind clear.__

Does Recent Masturbation Decrease Meditation Quality?
=======================================================

<!--TODO: maybe replace correlations with linear regressions, which give
p-values too.-->

Maybe<sub>65%</sub>? Correlations between mindfulness and time since
last masturbation are generally <0.2, and sometimes negative.
But there seems to be a pretty clear trend of positive correlation with
concentration if we only look at sessions with >20 days of abstinence.

There is some received wisdom that ejaculation and masturbation
in particular decreases meditation quality: The retreats of
[dhamma.org](http://www.dhamma.org/en/) in the tradition of
[S.N. Goenka](https://en.wikipedia.org/wiki/S.N.Goenka) forbid
any sexual activity, and [Taoist sexual practices recommend semen
retention](https://en.wikipedia.org/wiki/Taoist_sexual_practices#Male_control_of_ejaculation).
Since I track both [my meditations](./data.html#Meditation) and
[(a.m.a.b.) masturbations](./data.html#Masturbation), I can check whether
this is observationally true. Of course results from observational data
can be due to confounders, but such results are more valuable than pure
speculation, and may point to possible experimental investigations.

First, I load both meditation data and masturbation data (using my
loading code from [here](./code/experiments/load.py)):

        >>> meditations=get_meditations()
        >>> masturbations=get_masturbations()

Since I only started tracking my masturbations on 2021-01-15, I have to
filter out all meditation I did before that:

        tohu=masturbations['datetime'].min()
        meditations=meditations.loc[meditations['meditation_start']>tohu]

And then I merge `meditations` and `masturbations` so that each meditation
is relation to the masturbation last before it:

        meditations=meditations.sort_values('meditation_start')
        masturbations=masturbations.sort_values('datetime')
        combined=pd.merge_asof(meditations, masturbations, left_on='meditation_start', right_on='datetime', direction='backward')
        ['diff']=combined['meditation_start']-combined['datetime']

All hail `merge_asof`!<!--TOOO: meme with Elmo?-->

Just to check whether the difference computed is the right one, I do a
quick sanity check:

        >>> combined['diff'].describe()
        count                         1462
        mean     3 days 21:46:44.564929548
        std      6 days 10:27:57.403873207
        min         0 days 00:03:45.389000
        25%         0 days 16:00:47.628250
        50%         1 days 12:27:33.874500
        75%         3 days 14:14:14.750500
        max        39 days 09:24:06.877000
        Name: diff, dtype: object

And now I can simply compute the correlation with time since last
masturbation and concentration & mindfulness during meditation:

        >>> combined[['mindfulness_rating', 'concentration_rating', 'diff']].corr(numeric_only=False)
                              mindfulness_rating  concentration_rating      diff
        mindfulness_rating              1.000000              0.687853  0.088458
        concentration_rating            0.687853              1.000000 -0.049699
        diff                            0.088458             -0.049699  1.000000

As one can see, the correlation between time since last masturbation
and concentration/mindfulness are weak and contradictory, and I
weakly conclude that masturbation does not influence meditation quality
noticeably in practice regimes like mine. One might criticize my analysis
for not including periods of long abstinence from ejaculation, which
I guess is fair. So we can simply restrict the dataset to meditations
4 or more days after the last masturbation. We still have n=329, which
is appreciable.

        >>> combined_long=combined.loc[combined['diff']>pd.Timedelta('4d')]
        >>> combined_long['diff'].describe()
        count                           329
        mean     12 days 19:50:39.986796352
        std       8 days 20:16:12.256869649
        min          4 days 01:15:13.941000
        25%          6 days 09:45:24.187000
        50%          9 days 21:45:40.422000
        75%         14 days 12:50:55.863000
        max         39 days 09:24:06.877000
        Name: diff, dtype: object
        >>> combined_long[['mindfulness_rating', 'concentration_rating', 'diff']].corr(numeric_only=False)
                              mindfulness_rating  concentration_rating      diff
        mindfulness_rating              1.000000              0.542909  0.169900
        concentration_rating            0.542909              1.000000 -0.040382
        diff                            0.169900             -0.040382  1.000000

The correlation of ≅0.17 of abstinence-time with concentration is
still not strong enough to convince me, but perhaps points in some
interesting direction.

What if we look at exclude up to 30 days?

        mindfulness_correlations=[]
        concentration_correlations=[]
        sample_sizes=[]
        for i in range(0,30):
                combined_long=combined.loc[combined['diff']>pd.Timedelta(str(i)+'d')]
                sample_sizes.append(len(combined_long))
                mindfulness_correlations.append(combined_long[['mindfulness_rating', 'concentration_rating', 'diff']].corr(numeric_only=False)['mindfulness_rating']['diff'])
                concentration_correlations.append(combined_long[['mindfulness_rating', 'concentration_rating', 'diff']].corr(numeric_only=False)['concentration_rating']['diff'])


Plotting:

        import matplotlib.pyplot as plt

        fig=plt.figure(figsize=(8,8))
        _, ax1 = plt.subplots()
        ax2=ax1.twinx()
        ax2.set_ylabel('Sample size')
        ax1.plot(mindfulness_correlations, color='red', label='Mindfulness correlations')
        ax1.plot(concentration_correlations, color='blue', label='Concentration correlations')
        ax1.set_xlabel('Time since last masturbation (days)')
        ax1.set_ylabel('Correlation (Pearson)')
        ax2.plot(sample_sizes, color='green', label='Sample size')
        ax1.legend()
        ax2.legend()
        plt.savefig('time_correlations.png')

!["Plot of three variables: Concentration correlations, mindfulness correlations and sample sizes, with the x-axis being days since last masturbation. The mindfulness correlations merely oscillate between 0 and 0.2, while the concentration correlations rise from below zero at one day to more than 0.3 at ~20 days, just to fall back to 1.5 after that. Sample sizes start high at 1600, and fall rapidly to near zero.](./img/masturbation_and_meditation/time_correlations.png "Plot of three variables: Concentration correlations, mindfulness correlations and sample sizes, with the x-axis being days since last masturbation. The mindfulness correlations merely oscillate between 0 and 0.2, while the concentration correlations rise from below zero at one day to more than 0.3 at ~20 days, just to fall back to 1.5 after that. Sample sizes start high at 1600, and fall rapidly to near zero.")

Now *this* is interesting! Even just eye-balling suggests that abstaining
from masturbation might improve concentration, but has no effect on
mindfulness. That could be worth testing, so I'd like someone to do an
experiment on this (keeping a strict meditation schedule and randomizing
4-week pairs for masturbation/abstinence), since the sample sizes in
the upper ranges are so small (62 at 20 days, 45 at 25 days).

But I won't do it in the forseeable future, since other experiments have
higher priority.

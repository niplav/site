[home](./index.md)
------------------

*author: niplav, created: 2019-09-09, modified: 2022-04-05, language: english, status: notes, importance: 2, confidence: log*

> __Notes and ideas for texts & programs that will be written decades
> in the future, as well as music.__

Todo
=====

Site
-----

* Add tooltips to links (Title of Text)
* Find out how to make the site more inclusive
* (a) link for archives?
* Get rid of "we", use "I" instead.
* Improve citation (both to wikipedia and to papers)
* Make all scripted programs banged
* Description of images in italics below
* Move from Python2 to Python3
* Add two targets for make: `offline` and `online`
* Convert all the expensive image generating scripts into single ones that only run once, with multiple outputs
	* Done:
		* Range and Forecasting Accuracy
		* Daygame Cost-Benefit Analysis
* Switch to MathJax 3?
* Edit texts:
	* Considerations on Cryonics
		* Mainly done
* Flashcards:
	* Add tags for chapters/sort by chapters
	* Prune flagged cards?
* Add content tables to pages?
* Add RSS feed (ugh)
	* `https://www.interglacial.com/tpj/26/`
	* `https://github.com/html2rss/html2rss`
	* `https://github.com/html2rss/html2rss`
	* `http://fetchrss.com/`
	* `https://www.linux.com/news/building-command-line-generator-rss-feeds-0/`
	* `https://lynxbee.com/bash-script-to-generate-rss-feed-compatible-xml-using-unique-urls-of-a-website/#.Yl_EYlxBxH5`
	* `https://www.makeuseof.com/tag/how-to-create-an-rss-feed-for-your-site-from-scratch/`
	* `https://florian-dahlitz.de/articles/create-feeds-for-your-blog`
* Add metadata to hosted PDFs/videos
* List of writings by importance/finishedness
	* List of texts by year/author
* Replace “” quotes by "" quotes, “” is for quotes within quotes
* Improve linting
	* Incorporate `https://www.gwern.net/static/build/markdown-lint.sh`
	* `https://www.html-tidy.org/`
	* `https://github.com/amperser/proselint/`
* Import Meditavo data
* Move read pdfs into the doc folder, maybe restructure?
	* Not the full books obviously
* Find for a way to allow for LaTeX in code blocks that doesn't break everything immediately

Existing Texts
--------------

* Range and Forecasting Accuracy
	* Add explanatory image for the [illustrative example](./range_and_forecasting_accuracy.html#Three-Different-Analyses-An-Illustrative-Example)
	* Move the [PredictionBook download code](./range_and_forecasting_accuracy.html#For-PredictionBook) to the [PredictionBook API](https://github.com/bellroy/predictionbook/blob/master/API.md)
	* Rewrite the code in Python
	* Find Muehlhauser email with additional source
	* Extend the analysis to more datapoints
		* Extend the analysis to predictions with confidence intervals
		* Extend the analysis to real Metaculus data
		* Extend to more datasets
	* Add a paragraph on the difference in quality between the two datasets, Metaculus is better
	* Make more readable
	* Prevent the OOD prediction, either
		* find a scoring rule that maps into all of ℝ
		* curve-fit something other than a linear function
	* Add a literature review
		* `https://rethinkpriorities.org/publications/how-does-forecast-quantity-impact-forecast-quality-on-metaculus`
		* `https://rethinkpriorities.org/publications/an-analysis-of-metaculus-predictions-of-future-ea-resources`
		* `https://rethinkpriorities.org/publications/an-examination-of-metaculus-resolved-ai-predictions`
		* `https://rethinkpriorities.org/publications/data-on-forecasting-accuracy-across-different-time-horizons`
		* `https://rethinkpriorities.org/publications/potentially-great-ways-forecasting-can-improve-the-longterm-future`
		* `https://rethinkpriorities.org/publications/why-short-range-forecasting-can-be-useful-for-longtermism`
		* `/usr/local/doc/unread/calibration_scoring_rules_for_practical_prediction_training_greenberg_2018.pdf`
		* `https://en.wikipedia.org/wiki/J._Scott_Armstrong#Forecasting`
		* `http://foresightr.com/2016/05/06/a-brief-history-of-forecasting`
		* `https://onlinelibrary.wiley.com/doi/abs/10.1111/risa.12127`
		* Prediction: The long and short of it (Anthony Millner/Daniel Heyen, 2020)
		* `https://www.philadelphiafed.org/surveys-and-data/real-time-data-research/survey-of-professional-forecasters`
* Considerations on Cryonics
	* Add a literature review
		* `https://www.tandfonline.com/doi/pdf/10.1080/01459741003715391`
		* `https://www.tandfonline.com/doi/full/10.1080/23311886.2016.1167576`
		* `https://books.google.de/books?id=9C0ABAAAQBAJ&pg=PA281&lpg=PA281&dq=Cryonics+cost+benefit+calculation&source=bl&ots=IIIVQtzzXt&sig=ACfU3U3KMGKCBWhP1tvegvKvHTyCLtZNGA&hl=en&sa=X&ved=2ahUKEwjc_O6v743qAhUKYcAKHXFVDsUQ6AEwDXoECAMQAQ#v=onepage&q=Cryonics%20cost%20benefit%20calculation&f=false`
	* Think about incorporating the Metaculus questions on Cryonics into the probability
		* Revival
			* `https://www.metaculus.com/questions/3330/will-any-person-that-has-been-cryopreserved-for-more-than-1-year-be-resuscitated-or-emulated-before-2200/`
			* `https://www.metaculus.com/questions/1626/before-1-january-2050-will-any-human-cryonically-preserved-for-at-least-1-year-be-successfully-revived/`
			* `https://www.metaculus.com/questions/455/if-you-die-today-and-get-cryonically-frozen-will-you-wake-up/https://www.metaculus.com/questions/3332/will-james-bedford-be-revived-or-emulated-before-2200/`
			* `https://www.metaculus.com/questions/3331/when-will-the-first-person-that-has-been-cryopreserved-for-more-than-1-year-be-resuscitated-or-uploaded/`
			* `https://www.metaculus.com/questions/3382/what-will-the-earliest-preservation-date-of-any-resuscitated-cryonics-patient-be/`
		* Preservation:
			* `https://www.metaculus.com/questions/3333/when-will-the-number-of-people-in-cryopreservation-preserved-before-2019-fall-to-less-than-50-of-the-current-value/`
		* Signup:
			* `https://www.metaculus.com/questions/3478/how-many-patients-will-be-in-cryonic-suspension-at-the-cryonics-institute-in-2030/`
			* `https://www.metaculus.com/questions/4052/if-cryonics-is-at-some-point-offered-for-free-what-percentage-of-americans-will-be-signed-up-within-10-years/`
	* Different value of money at different ages?
	* Why not a Pascal's mugging?
		* No adversary
		* Probability not _that_ low
		* Here assumed rather low bound on payoff to prevent
	* Update to new Alcor payment structure
	* Extend to other options/providers
		* Full-body presveration
		* Cryonics Institute
		* Oregon Cryonics
		* Tomorrow Biostasis
		* Southern Cryonics
		* Kriorus (maybe not though, after the recent debacle)
			* Expand the section on the Guesstimate model
	* Incorporate updated Metaculus probabilities
	* Make interactive calculator
* Abstinence from Masturbation and Success from Cold Approach
	* Test
		* This is a likert scale, so read that Wikipedia article first
			* Then change the statistical test
		* Instead of Student's t-test a survival analysis?
			* Such as a Kaplan-Meyer method & log-rank test?
			* Or a one-sided test?
		* Cox-regression (proportional hazard).
		* Will the data sets be normally distributed?
			* → If not, use Mann-Whitney U-Test.
	* What about abstinence ←→ masturbation ←→ pornography?
	* Pre-register
		* PredictionBook
		* Reddit
	* Change so that in the male case, there's nothing beyond collecting contact info (no date invite/date)
	* Elaborate on asking for contact info/date process
	* Literature review
		* `https://en.wikipedia.org/wiki/Masturbation`
		* `https://en.wikipedia.org/wiki/Pornography`
		* `/usr/local/doc/unread/blackpill/physical_attractiveness_research_adams_1977.pdf`
		* `/usr/local/doc/unread/sexual_activity_is_inversely_related_to_womens_perceptions_of_male_facial_attractiveness_hess_et_al_2007.pdf`
* Daygame Cost-Benefit Analysis
	* Incorporate new daygame stats from blogs
	* Upload own data
	* Adjust curve to fit Roy Walker & Thomas Crown data better
	* different diminishing returns in code, make all logarithmic/radical/hyperbolic?
	* Expand or axe Fixed Costs & Variable Costs section
	* Create & explain Guesstimate Models
	* Upload data to Appendix C

Texts
-----

### Forecasting

* Forecasting is Worse is Better
	*	The [Brier score](https://en.wikipedia.org/wiki/Brier_score) was invented
		in 1950, [Bayes' theorem](https://en.wikipedia.org/wiki/Bayes'_theorem)
		was first described in 1763, and [probability
		theory](https://en.wikipedia.org/wiki/Probability_theory) was properly
		invented at the beginning of the 18th century.
	*	However, attempting to use forecasting to seriously determine the
		probability of future events, training & selecting
		people for their forecasting ability and creating
		procedures that incorporate both intuition-based
		and model-based predictions have only been around
		since the mid 1980s <!--TODO: citation needed-->,
		mostly popularized by the work of [Philip
		Tetlock](https://en.wikipedia.org/wiki/Ehpilp_E._Tetlock).
	*	Tetlock-style forecasting is "Worse is Better"
		If we can't develop explicit numerical models, why
		not train people in becoming good at estimating the future,
		but this time with probabilistic estimates?
* Why not Earlier Forecasting?
	* Maybe not Big Advantage?
	* Needs Infrastructure: Takes months/years to bring fruits
	* People would be wrong
	* Focus on explicit models instead
* Forecasting, Science and Crystal Balls
* Forecasting Contra Credentials
	* Forecasting Stays Relevant to the Topic
	* Forecasting Remembers, the Public May Not
	* Forecasting has Faster Feedback
	* Is Forecasting Harder to Game?
	* Less Susceptible to Social Biases like Charisma
* Comparing Forecasting Accuracy Between the Good Judgment Project and Metaculus
	* `https://www.openphilanthropy.org/blog/forecasting-covid-19-pandemic`
	* `https://pandemic.metaculus.com/questions/`
* Extracting Probabilities from Stock Markets
* The "At-the-time best possible forecast"
	* Not literally best possible forecast
	* But for humans at the time with the available information
* An aggregation of all of Scott Alexander's forecasting results in one place

### Population

* Antinatalism and Consent
* Wither Humanity? (Alternatively, “Ponderings on Population”)
	* Would a bigger humanity be a good idea?
	* Against:
		* Coordination
		* Resources
		* Safety from Malthusian Trap
	* For:
		* Growth
			* Specialization
		* Aggregative Arguments
* About Longtermist's Children
	* Disclaimer:
		* If people want to have children for egoistic reasons, it is not useful to argue against
		* Trying to convince people to not do things they deeply desire is bad, even under consequentialist reasoning
	* People argue that effective altruists (and especially longtermists) ought to have children
		* Most arguments for having children are bad
	* However:
		* Children are expensive, opportunity cost
			* Perhaps better: invest time/energy into life-extension tech
				* Or spreading ones memes
					* Memes under heavy selective pressure too, though
		* Traits we like are only moderately heritable, and will be washed out in a few generations (especially under selective pressure)
			* On each EA-related trait 50% heritability → very likely not EA (seems like specific combination of personality characteristics)
		* Parents seem to have relatively little influence on the values of their children (Is this true?)
		* Humanity will very likely not die out due to people stopping to breed
			* Indeed, It seems to me much more likely that if we wait long enough, we fall back into the malthusian trap
	* Why I Dislike This Argument
		* It comes from the genre of "Let's outbreed the other/bad people", which is very molochian
		* It leads to a malthusian trap/pure replicator hell with no value and no option to get out (in the long run)
	* However, maybe in the medium run this makes sense (not short enough for the really important stuff to happen during our lifetimes, not long enough for us to worry about malthusian traps)
		* Even then, however, just trying to build better institutions is more useful?
	* Would people prefer procreating to indefinite longevity?
* Modelling the Dream-Time (Population will probably start growing again)
	* How likely is another malthusian trap, how much time do we have got?
	* What kinds of scenarios lead to malthusian condition?
		* Base case biological humans
		* Base case without aging
		* Em case
	* What can be done against?
		* Population control
		* Monitoring
	* Reasons against worrying
		* Too far in the future
		* Number of children not heritable
* Population Ethics Test Suite
	* Look at comments on “An Impossibility Theorem for Welfarist Axiologies” (Arrhenius 2000)
* Three-level population ethics
	* Symmetrical critical level
	* If any life below -critlevel, level 3
	* If all lifes above critlevel, level 1
	* Otherwise level 2
	* Average in Level 2, total in Level 1/3?
	* Prevents hijacking through efficient just-positive lives
	* Violates Mere Addition Principle
	* Has a symmetry (critlevel & -critlevel are symmetric), but also 2 discontinuities
	*	Also somewhat counter-intuitive: Adding a person with
		critlevel-ε can make a populations welfare infinitely
		worse
	* Of course, still repugnant conclusion with critlevel+ε, but that's okay
	*	But also many -critlevel+ε lives infinitely better than one
		life -critlevel-ε (actively repugnant conclusion)
	*	And also one person with critlevel+ε infinitely better
		than many with critlevel-ε
	* `tlpe::{:[(&/x)<-cl;+/x:|(-cl)<(&/x)<cl;ω++/x;(2*ω)++/x}`
* Semi-Natalism
	* If I reason out that I am not the type of agent that would have children otherwise, I should have children
	* If I indeed reason out that I am the type of agent that would have children, I should not have children
	* Reasoning: If propensity to have children is heritable, this kind of decision will prevent my ancestors from becoming pure replicators
	* It is slightly paradoxical, though

### Alignment

* Impact Measures Depend on, Rather Than Specify, Inaction Baselines
* Requirements for AI Safety via Debate
* Thoughts About Reward Hacking
* Faster algorithm for ontology mapping, first described in [de Blanc 2011](http://intelligence.org/files/OntologicalCrises.pdf)
* Implement the project described in [Environmental Goals](https://arbital.com/p/environmental_goals/)
* GPT for STEM data?
* Is the F-invariance described in Utility Indifference (Armstrong 2010) tiling?
* Enumerating different ways of collapsing graphs representing inconsistent preferences into consistent preferences
	* E.g. a>b>c>a must be cut in one place, pretty much indifferent about where to cut?
	* Or merge DAGs into a path graph
	* Continuous case: vector field over the probability simplex of options
	* In the 2-option probability simplex, continuity is violated if at some point the vector field "turns around"
	* Make consistent by rotating vectors so that the integral over vector strength/volume/degree of rotation is minimal
	* Nontransitivity is probably maximal curl at some point in the vector field
	* Also look at:
		* Graphon
		* Dense graph
		* Extremal graph theory
	* This also feels relevant to Ontological crises/shifts: Is there a canonical way to map from the human preference simplex to the AI preference simplex, if we know the concept equivalences? (A is just 30% B and 70% C, so we can split the simplex into another dimension here…)
* Scaling laws for debate
	* AI safety via debate (Geoffrey Irving/Paul Christiano/Dario Amodei, 2018) test debate on an MNIST classifier with depths 4 and 6, what are the scaling laws for the depth and size of models?

### Pick Up

* In Praise of Encouragement
* Game Seems to be a Middle-Class Phenomenon
* Don't Give Out Your Contact Information, Take Hers
* On the Importance of Pick Up
	* Combines Near (Sex) with Far (Abstract thinking)
* Women actually enjoy getting chatted up, or are indifferent to it
* Not masturbating for a while really improved my eye contact
	* Caveat though
* Leaving my phone at home made me dick around less on my phone will doing daygame
* Yad Stop Flag
* Wild and Unsupported Conjecture: Learning Pickup is Mostly Rewriting Your Life-History Strategy

### Time Experience

* Subjective time experience for advanced meditators
	* Wittmann & Schmidt 2013
* Interventions to Slow Down the Age-Related Speedup of Subjective Time
	* That theoryengine post
	* Slowing the Speedup of Subjective Time With Age
		* Meditation
		* New experiences
		* Drugs?

### Philosophy

#### Ethics

* Bounded Population Axiology

#### Consciousness

* Matter is Philosophically Unnecessary
* The Hard Problem of Consciousness Still Persists Without Matter
* Panpsychism is a Class of Theories of Consciousness, not a Theory of Consciousness
* Intentional vs. Non-Intentional Consciousness
	* The reason why, even if, strictly speaking, trees are "conscious", we don't have to worry about damaging them as much as we have to worry about damaging animals

### Arguments

* Why Still Choose C?
	* Long-term reliability/stability
	* Performance
	* Portability
	* → Caveat: Only portable if very reliably/portably written
		* I.e. stick to the standard, no GNUisms
* Unix is Not About Reimplementing Unix
	* Examples for claim:
		* [Node JS](http://blog.izs.me/post/48281998870/unix-philosophy-and-nodejs)
		* [The Internet](https://victorops.com/blog/internet-age-unix-philosophy/)
		* [Vim](https://www.reddit.com/r/vim/comments/22w1li/a_fair_comparison_between_vim_and_emacs/cgqyqst/)
		* `https://gist.github.com/rjsteinert/f3823f3cdc9971779c17`
	* ["Do one thing, and do it well. Use text streams, since that is the universal interface"](http://www.catb.org/esr/writings/taoup/html/ch01s06.html)
	* Most systems reimplement unix ("Those who don't understand unix are doomed to reimplement it, poorly.")
* Libertarianism is too Simple
	*	Libertarianism is a very simple method of organising society,
		so it must have been tried in the history of societies. However,
		none of those societies have survived, which makes it an
		unsuccessful way of structuring societies
	* Counter-argument: Humans are consistently biased against liberty
	*	Counter-argument: Libertarianism is very well suited for
		*modern* (capitalist, technological) societies, which haven't
		existed for very long
* Limit “Philosophy” and “Art”
* Against Advertising
	* Strong claim: Advertising is always bad
	* Weak claim: Advertising in public spaces is bad
	* Does this hold up to a good consequentialist calculation?
* Against News
	* Priming → News+Wikipedia≤Wikipedia
* On the Importance of
	* Qualia Engineering
	* Track Records, Forecasting and Prediction Markets
	* The Difference in Sexual Behavior Between Men and Women
* Missing the Movement
	* "Most Hedonists end up sad!"
	* "Utilitarianism leads to bad results!"
	* "Rationalism leads to believing wrong things!"
	* Related text: [Incremental Progress and the Valley](https://www.lesswrong.com/s/pvim9PZJ6qHRTMqD3/p/oZNXmHcdhb4m7vwsv)
* In Favor of Gish-Gallop
	* `https://en.wikipedia.org/wiki/Gish_gallop`
* The Hedonic Treadmill and Politics
	* Inequality
	* Pareto Improvements
	* Hedonic Treadmill
	* Progress
	* Easterlin Paradox
	* Status Games
* In Praise of Cost-Benefit Analyses
* Creating Utility Monsters or Repugnant Beings
	* Marginal returns of investment on the well-being of single persons are probably monotonically increasing/decreasing
	* If so, we end up with utility monsters or in a repugnant conclusion
	* If not, we are lucky
* Separating Arguments From Inconsistency and Questions About Inconsistency
	* The thing Hanson does when arguing about ethics
* Reflections on Pseudonymity
	* “You don't know the pseudonyms I assume, you don't know the pseudonyms I assume…for you. Are you happier now \ About the gods who are dying \ What do you dream of \ Festing with omniscient beer” (?) (text from Bite Hard by Franz Ferdinand)
* In Non-Adversarial Universes, Systematic Trying Dominates Other Approaches
	* In short: trying to think better/act better can expected to yield monotonically increasing results with effort put in
	* Result: Utilitarianism works by its own standards, rationalism works by its own standards
* The Overlap Argument for Learning Latin does not Hold
* The Existing-Uranium Argument Against Nuclear Waste Skepticism
* Why Mars' Moons Should Be Destroyed
* Why We Need New Anthems
	* Most national anthems suck, let's make some more original ones
		* Review `https://en.wikipedia.org/wiki/List_of_national_anthems`
* Models With Huge Error Bars are Better Than No Models At All
* Some Epistemic Warning Signs in the Effective Altruism and Rationality Communities
	* People are Friends
	* People Date Each Other
	* Very Few People have Public Epistemic Track Records
	* Hot Messes
		* Leverage
		* Zizians
		* Psychotic Breaks in Berkeley
* Do Things in Groups
* Some Useful Rationality Concepts
	* Feedback Loops
		* Thick vs. Thin/Fast vs. Slow/Signal vs. Noise
	* Option Value
	* The Is-Ought Distinction
* Why Not Prepping?

> [lcamtuf 2018](https://lcamtuf.coredump.cx/prep/ "Disaster planning for regular folks")
distinguishes between three different kinds of disaster scenarios:
small-scale events, mass calamities, and the "zombie apocalypse".

#### Contra

* Contra Yudkowsky on Axelrodian Tolerance
* In Favor of Selling Glee/Contra Alexander on Hedonic Acquisitions
	* Pointing out problems with the ideas in [The Price Of Glee In China](http://slatestarcodex.com/2016/03/23/the-price-of-glee-in-china/)
	*	General idea: When you find out that making people wealthier
		doesn't make them happier, you start thinking about how to make
		them happier instead of trying to find reasons why making them
		wealthier is still a good idea.
	* Read the post carefully
	* Read up on the research
	* Perhaps re-emphasize as "Easterlin Paradox"?
* Contra Morse on Fame
	* `https://210ethan.github.io/thoughts/famous.html`
* Contra Alexander on Epistemic Minor Leagues
	* https://astralcodexten.substack.com/p/epistemic-minor-leagues?s=r
	* Reality is really f\*\*\*ing high-dimensional, so there's a bunch of nooks and crannies nobody has explored before

### Analyses

* Dumpster Diving
* Hitch Hiking
* Keyboards
	* Hardware
		* Hands too near each other
		*	Staggered keys maybe increase learning time, possibly
			increase typing time (sqr(2) instead of 1 movement distance)
	* Software
		* Layouts are a problem
		* Two modes: key position on keyboard & character presented by key
* Table Diving
* Walking Barefoot
* Actuarial tables for dictators
* Ideology Transition Graphs
	* When people move along ideologies, which paths do they take?
	* How long do they stay at certain ideologies?
	* What are the overall transition probabilities, what are the "sinks" (look up on markov chains)
	* Survey on /r/CapitalismVSocialism
	* One part with selected ideologies:
		* Centrism, Apolitical
		* Social Democracy, Socialism, Communism
		* Liberalism, Left Liberalism, Anarchism
		* Libertarianism, Minarchism, Anarcho-Capitalism
		* Conservativism, Alt-Right, National Socialism, Fascism
	* One part with freely choosable ideologies
* Dice Chains
	*	Throw n dice as long as the sum of their values is higher
		than the previous throw. What is the probability
		distribution on the length of the run?
	* Simulation from ../prog/dicechain/dicechain.lua
* 	Algorithm for distributing production of goods among different
	producers according to comparative advantage
	* producers: {2,n}
	* products: {2,n}
	* transformation curves: {linear, marginal, any}
	* indifference curves: {linear, fixed number, any}
* Building A Big Tower
	* 500 years, ~\$1t, stable technology, build a tower as big as possible
	* considerations
		* location
			* some mountains nearby for material
			* very stable ground (tower doesn't sink into the ground)
		* energy production
			* nuclear, probably
	* base of the tower probably square
		* length 5-10 km
	* pyramid shaped
		* 100 m for every layer, 20-50m distance to the edge of the last layer
	* big blocks
		* use lava to form them, from pulverized mountains
			* pump up powder/sand/little stones or magma?
			* in the former case, one also needs electricity at the top
* Nuking the Amazon Cost-Benefit Analysis
* What is the most common word I don't use?
* How Strong is the Gender Difference In Sex Drive?
	* `/usr/local/doc/unread/blackpill/is_there_a_gender_difference_in_strength_of_sex_drive_baumeister_et_al_2001.pdf`
	* `/usr/local/doc/unread/blackpill/in_heterosexual_relationships_men_masturbate_more_than_women_waterink_2014.pdf`
* Do eggs burst when they're not poked before boiling?
	* Blinded, person needs to poke & write down, but not tell
	* Student's t-test
	* N=200
	* Pre-register
* Precommit to Enlightenment
	*	precommit to performing the steps from TMI & MCTB2 for
		10000 hours over 10 years (~2h every day on average, plus
		2 retreats a year), then report back what the effects were
	* frame as experiment (is that actually legit?)
* Proposed Solutions to Pascal's Mugging
	* Bite the Bullet
	* Abandon Utility-Maximization
	* Bounded Probability
	* Bounded Utility
	* Abstain From Assigning Probabilities to Some Events
		* Probability of X is undefined
	* Maxipok
	* Links to relevant texts here:
		* `https://gwern.net/mugging`
		* `https://gwern.net/Mugging-DP`
		* `https://nintil.com/pascals-mugging/`
		* `https://nickbostrom.com/papers/pascal.pdf`
		* `https://en.wikipedia.org/wiki/Pascal%27s\_mugging`
		* `https://patrickjuli.us/2019/11/10/pascals-mugging/`
		* `https://www.lesswrong.com/posts/9WZAqFzNJ4KrhsqJ7/pascal-s-mugging-solved`
		* `https://www.lesswrong.com/posts/gjyvXPqvCZPEtCKLB/tactics-against-pascal-s-mugging`
		* `https://risingentropy.com/pascals-mugging/`
		* `https://wiki.lesswrong.com/wiki/Pascal%27s\_mugging`
		* `https://wmbriggs.com/post/20492/`
		* `https://medium.com/@SunBurntSky/pascals-mugging-787c37e76bc3`
		* `https://utilitarianism.fandom.com/wiki/Pascal%27s\_Mugging`
		* `https://www.lesswrong.com/posts/Ap4KfkHyxjYPDiqh2/pascal-s-muggle-infinitesimal-priors-and-strong-evidence`
		* `https://www.lesswrong.com/posts/KDzXTWSTg8ArwbhRR/pascal-s-muggle-short-version`
		* `https://www.lesswrong.com/posts/CaPgNwxEFHh3Ahvf7/pascal-s-muggle-pays`
		* `https://www.lesswrong.com/posts/8FRzErffqEW9gDCCW/against-the-linear-utility-hypothesis-and-the-leverage`
		* `https://www.lesswrong.com/posts/NoYXhJLtoKpLoZhRf/pascal-s-mugging-finite-or-unbounded-resources`
		* In defence of fanaticism (Hayden Wilkinson, 2020)
* Creatine & Vegetarianism IQ?
* Survey advanced meditators about their attainments and their monetary worth
	* That is, how much is your meditative attainment worth to you?
		* `https://old.reddit.com/r/TheMindIlluminated/comments/su8f1j/to_seek_or_to_not_seek_enlightenment/hx995y6/?context=3`
		* `https://www.shinzen.org/the-dark-night/`
		* `https://www.youtube.com/watch?v=SmaZ6am_KIQ&lc=UgyhA5CfJXShZN9loVd4AaABAg.9DWh5Ao7Klk9DXRaKBauqZ`
* Masturbation Spacing
	* Space masturbation to make it more enjoyable
	* Form:
		* Spacing between 2 and 12 days
		* 10 spacings
		* Between changing spacing, 1 or 2 1-day spacings
		* Record:
			* Spacing [2..12]
			* Enjoyment of orgasm [-5..5]
			* Counterfactual experience during everyday life [-5..5]
			* Type of pornography {none,text,audio,image,video}
	* Precommit to:
		* n: 6 9 11 8 3 10 5 12 7 4 2
		* i: 11 4 5 7 12 6 3 2 10 9 8
		* v: 12 9 8 11 7 2 4 6 10 3 5
		* t: 10 4 7 3 8 9 5 11 2 6 12
		* a: 4 2 3 8 9 11 10 7 12 6 5
	* `set k 0; for i in 4 2 3 8 9 11 10 7 12 6 5; for j in (seq 1 10); set k (echo "\$k+\$i" | bc); date -I'date' -d "2028-11-17 +$k days"; end; end | xsel -psb`
* Ingredients to Moloch
	* Tragedy of the Commons
	* Nash Equilibria
	* Unilateralist's Curse
	* Pure Replicator Hell
	* Convergent Instrumental Goals
* Egoistic Cost-Benefit Analysis of focusing on AI alignment
* Voting Cost-Benefit Analysis
	* Altruistic, egoistic
* Timeline of the Odyssee
* Roomba Cost-Benefit Analysis
* A History of the Term “Rationalist”
* Weather Affects Daygame Success/Divorce Rates?
* Wireheading
	* [Electrical Brain Stimulation](https://en.wikipedia.org/wiki/Electrical_brain_stimulation)
	* [Wireheading](https://en.wikipedia.org/wiki/Wirehead_\(science_fiction\))
	* [Brain Stimulation Reward](https://en.wikipedia.org/wiki/Brain_stimulation_reward)
	* Questions:
		* How much wireheading research has been/is being done?
		* Why is there so little wireheading research/why is it not very prominent?
		* Do animals (especially humans) develop tolerance to intracranial stimulation?
		* Do animals (especially humans) develop an addiction to intracranial stimulation?
		* Is wireheading reversible? (in principle, in practice so far)
		* How long can one wirehead until it leads to negative health outcomes (in principle, in practice)
		* How good does intracranial stimulation feel? (compared to other positive experiences)
		* Is wireheading actually pleasurable or just compelling? (in the sense that one wants to continue being wireheaded although it doesn't strictly "feel good")
		* How does intracranial stimulation work?
	* Desiderata:
		* Reversibility
		* Non-adaption
		* Non-addiction
		* Safety
		* Ability preservation
		* Anti-slipperiness
* Describe and write some code for the n-polytopal conjecture
	* Just generalise Pollock's polyhedral conjecture for n-dimensional polytopes
	* Also try to prove the case for triangular numbers first to get a feel for it?
* Try to find pollution levels in LOCAL\_CITY
* Expected value of plastic surgery for men
* How Many Proton Decays?
	* How many proton decays should we expect to have happened in the universe so far?
	* Proton decay follows a geometric distribution
	* When will the last proton decay?
* Test computationally whether causal networks have more correlations or causations, project from [here](https://www.gwern.net/Causality#what-a-tangled-net-we-weave-when-first-we-practice-to-believe)
* Which percentage of random normal-form games are potential games?
* Double Blind Self-Experiment with Wellbutrin

### Ideas

* Ends of Discussions
	* Dissolving the question
		* Discussion about the meaning of a word
		* Disagreement about an arbitrary category (morality/aethetics)
	* Bet
	* Agreement
	* Related to "Varieties of Argumentative Experience"
* The End of History Fallacy
* The “If Everyone Just” Argument
	* The argument just assumes one of the biggest problems away: coordination and cooperation
	* Related: [Malthusianisms](https://www.scottaaronson.com/blog/?p=418)
	* Related: `https://squareallworthy.tumblr.com/post/163790039847/everyone-will-not-just`
* Information and Markets:
	* Explanation
		* Information as a non-scarce good
	* Existing solution
		* Copyright
		* Patents
	* Problems with patents/copyright
		* creates a temporary monopoly
		* → all regular problems with monopolies as result
			* no competition
			* therefore, less/no innovation
			* higher prices
			* prevention of further work based on the innovation
			*	copying is inherent to (all but quantum) information,
				preventing it is theoretically (and for the most part also
				practically) impossible
			*	possible overcompensation: some people get a lot more money
				than appropriate for the work they put in, some get nothing
			* it's ontologically confused
	* Possible solutions:
		* Pay for production
			* Patreon
			* Kickstarter
		* Premium models
		* Advertising
			* Problem: getting harder the more products come into the information domain
		* Open-source model: free work
	* This is essentially a discussion about how to finance public goods
* Aesthematics
	* Infinite Fractal Meta Recursion
		* This is possibly just the ordinal numbers
	* Mendeljew Operator
	* Supersymmetric Copying
* Preference Frustration Auctions
* The Tyranny of the Mill
	* The Hedonic Treadmill is very good & very bad
* Writing system based on all binary trees with maximal height 2
	* no 's' sounds
* Moving the Lever Closer
	*	Due to an asymmetry in human decision making, making somebody
		causally more responsible for a negative action makes them less
		likely to take that action
	* Related: The bystander effect
* Salty fries
	* Buy something, that creates a need for something else (software <-> support, salty fries <-> drinks)
* Running Away from Your Problems
	* Examples (?)
		* Anti-biotics
		* de Grey anti-aging proposal
* Cryptographic Agreement on Bribing
* Encoding Conditionals Using Modulo
* Auras as synesthesia between visual perception and emotional perception
	* Maybe a survey?
* Refactoring Rational Feelings
	*	Relation between emotions, goals, strategy/planning, moral
		development etc.
* Yang Wenli and Reinhard von Lohengramm—Taoism and Confucianism?
	* Yang's "Win without fighting" is Wu Wei
* The Argument from Explanation of Intuition
	*	When you explain an intuition by its causal origin (e.g. a moral
		one by evolutionary psychology), it often loses its bite
* Sitting in X
	* You analyze everything under light of X
	* You believe that everyone else also intuitively analyzes everything under the light of X
* The Generalized Concept of Addiction
* Implications of Attainable Utility Preservation on practical rationality
	* Further argument why death is bad:
		* Removes many degrees of freedom for action
	* Preserve option value, avoid irreversible actions
		* Be conservative:
			* Preserve humans, ecosystems, language, culture (losing them is really bad, perhaps)
	* These are especially important for humans since our values change, in somewhat forseeable ways
* An Unreasonable Proposal
	* Merge India and the European Union
* Writing Notes
	* Concatenating Different Explanations
* `$k$` grass-cutting robots on `$n$`-dimensional manifolds
* Improving Coordination Over Time is a Longtermist Crux
	* Solution: If coordination is eventually easy with a non-negligible probability, it's not a problem
* Should the EA Community Buy Large AI Labs?
	* Use the Rocket Squid quote from Erogamer
* The UTMs-simulate-each-other solution to the Python-with-Witch problem
	* Look up LW shortform comment on this
* Clanishness vs. tribalism and relatedness in Dunbars number sized groups
* Upwing and downwing as new political fronts
	* Hat-grab at John David Pressman
* EA Cause Area Idea: Buy 0-day exploits and inform the companies

### Collections

* Simple Unsolved Math Problems
* Differences Between GNU and POSIX `make`
* Better Mathematical Notation
	*	Mathematical notation is not a planned and systematic
		endeavour, but the result of a long process of generation
		and selection of different notations. Here I collect
		contemporary ideas for better notation, and discuss old &
		discarded methods of writing mathematics.
	* Discarded Methods
		* `https://en.wikipedia.org/wiki/Begriffsschrift`
		* `https://en.wikipedia.org/wiki/Newton%27s_notation#Newton's_notation`
		* `https://github.com/prathyvsh/notation`
	* New Notations
		* General
			* `https://www.stephenwolfram.com/publications/mathematical-notation-past-future/`
			* `/usr/local/doc/unread/towards_a_better_notation_for_mathematics_olah_2010.pdf`
		* Triangle of Power
			* `https://www.youtube.com/watch?v=sULa9Lc4pck`
			* `https://math.stackexchange.com/questions/30046/alternative-notation-for-exponents-logs-and-roots`
			* `http://www.solidangl.es/2015/04/a-radical-new-look-for-logarithms.html`
	* Read
		* `/usr/local/doc/unread/notation/notation_as_a_tool_of_thought_iverson_1986.pdf`
	* Substitution of variables in formulas: order is _bad_ & _wrong_
* Recommendations
	* Activities/Movies/Series/Podcasts/Books/Blogposts
* Cool Things Humans Can Learn
	* Inspiration from [here](https://www.lesswrong.com/posts/knLZY52Yx9G23u3Ka/insufficiently-awesome?commentId=4AevGHrCQMbWaoan9)
* Notes on a Grand Plan to Learn Everything
	* Exploration
		* Read Wikipedia with [this method](./notes.html#Getting-an-Overview-Over-Everything)
		* Read SEP
			* randomly?
	* Learning
		* Reading textbooks (Natural sciences and engineering)
			* Mathematics
				* `https://intelligence.org/research-guide/`
				* `https://www.ocf.berkeley.edu/~abhishek/chicmath.htm`
				* `https://math.ucr.edu/home/baez/books.html#math`
			* Science
				* Physics
					* Feynman Lectures on Physics
					* `https://www.susanjfowler.com/blog/2016/8/13/so-you-want-to-learn-physics`
					* `https://www.ocf.berkeley.edu/~abhishek/chicphys.htm`
					* `https://math.ucr.edu/home/baez/books.html#physics`
				* Chemistry
				* Social Sciences
					* Economics
				* Life Sciences
					* Biology
						* `https://old.reddit.com/r/biology/wiki/faq#Suggestedtextbooks`
						* Campbell Biology
						* Molecular Biology of the Gene
						* Molecular Biology of the Cell
						* Principles of Biochemistry (Leininger)
						* Evolutionary Biology (Futuyma)
						* Zoology
					* Ecology
					* Paleontology
				* Earth Sciences
					* Geology
					* Meteorology
				* Psychology
					* Cognitive Psychology
					* Developmental Psychology
					* Neuropsychology
					* Industrial-Organizational Psychology
					* Social Psychology
					* Forensic Psychology
					* Evolutionary Psychology
						* Evolutionary Psychology (Buss)
			* Engineering
				* Computer Science
					* `https://teachyourselfcs.com/`
				* Electrical Engineering
				* Mechanical Engineering
				* Chemical Engineering
				* Bioengineering
				* Civil Engineering
				* Geoengineering
				* Medicine
		* Doing the exercises
	* Rehearsal
		* Creating flashcards from the textbooks, rehearsing them
			* Flashcard creation is pretty liberal in what is accepted
			* Use a system that supports images/LaTeX
				* Anki
			* bifot: bifot is flashcards of textbooks
			* pof: pile of facts (from Wikipedia)
			* φf: Philosophy facts (from SEP)
	* Testing
		* Forecasting
			* Metaculus
			* Spend relatively long on each question (15 minutes)
* Anecdotes About the Running Times of Test Suites in the Software Industry
* Ways in which people have misspelled "Kurzgesagt" on the internet
* Ranking, Reviewing and Rating Patricia Taxxon's Music
* Meanings of "so" in German
* Heuristics for Friendly Conversation on the Internet
* Much More Than You Wanted to Know
	* Vandwelling
	* UBI
	* Climate Change Impacts
	* Shipping
	* The Uyghurs and China
	* Cryonics in Germany
	* Cryonics in Europe
	* Extremely Long-Lived Institutions
	* Easterlin Paradox
	* Brain Stimulation as Meditation Enhancement
	* Rotwelsch
	* Picoeconomics
* Elon Musk Forecast Correction Function
	* Code: `1.8239233 * (forecasted-forecast_made) + 48.0502205` (days)
	* [Original](https://web.archive.org/web/20210302224031/https://anthony.boyles.cc/Essays/portfolio/ElonMuskForecastCorrectionFunction.html)
* Auctioning off Your Body
	* `https://www.humanmicrobes.org/`
	* Kidney
		* See `Gary Becker & Julio Jorge Elías (Summer 2007). "Introducing incentives in the market for live and cadaveric organ donations". Journal of Economic Perspectives. 21 (3): 3–24. doi:10.1257/jep.21.3.3. PMID 19728419.`
	* Sperm, Eggs
	* Plasma/Blood
* Nuclear Waste FAQ
* List of three-letter names for Unix related people (dmr, ken, rsc, there are probably others?)
* Heuristics for Long-Term Websites
	* Host images/pdfs/videos/audio files locally (this makes it easier to archive the site via `wget`!)
	* Use static webpages with minimal javascript, and optimally no external javascript
	* No CMSs, or SquareSpace, or BlogSpot/WordPress/…
	* `https://www.gwern.net/Design`
	* No dynamically loading images for f\*cks sake

### Notes

* Be Liberal in what you Accept, but Conservative in what you Emit
* Believing Something Doesn't Mean You to Tell it to Everyone
* You Actually Don't Need to Convice Idiots
* Hug the Objective
	* When trying to achieve something, work directly on that thing
	* Related to: yak-shaving
	* "Do the real thing" by Scott Young
	* Buffers by Rollo Tomassi
* No One Knows & No One Can Know
	* This argument infuriates me: did you try to find out what people actually know?
* Sometimes People have the same Credences but still Disagree
* Teaching Oneself vs. Being Taught
	* Two different mindsets
* Blogging as an Act of Benevolence
	* Mindset of "making a gift"
* Most People Have No Power At All
	* Therefore it's probably not very important what most people think
* Hail Cyclists
	* Positive Externalities: Environment, Attractiveness
* Hail Long Content
	* Most Topics are Too Short for Books
* Hail FAQs
* Boo Discord
	* Why on earth did this software become the replacement for forums?
* There is no Continous Probability Distribution without a Mode
* Sharing Beliefs vs. Evidence vs. Models vs. Ontologies
	* With examples:
		* Beliefs: Very common, but no crisp example?
		* Evidence: Most of Metaculus comments, most of Wikipedia
		* Models: Textbooks
		* Ontologies: Grand philosophy books (e.g. The Sequences, the Tao te Ching, Die Welt als Wille und Vorstellung)
* Growth
	* How long can growth continue if the maximal value of an atom is fixed?
	* Growth might slow to cubic (sphere expanding at constant fraction of c)
* Panpsychism is a property of theories of consciousness, not a theory of consciousness
* Defining long content
	* Conditions point to a cluster in thingspace
	* Comprehensive: long and detailed, providing sources, visualizations, code, predictions, etc.
	* Optimal: attempts to be a piece of content on the pareto frontier of what it is talking about)
	* Updated: even if it doesn't pertain to current events, the author is either still working on it or had worked on it for a long time
* Mastery is Exceedingly Rare

> Very few will aspire to real mastery themselves. Very few will take the
time to learn even the basics of meditation theory. Even fewer will go on
retreats. Of those that do, only a handful will get their concentration
strong enough to attain to basic jhanas or ñanas. Of these, only a
couple will be able to cross the A&P, handle and investigate the Dark
Night, attain Equanimity, and get stream entry. Of those who attain
stream entry, a reasonable number will progress to the middle paths,
but not many will attain arahantship. Call me cynical, but this was true
in the Buddha's time and it remains true today.

*— Daniel Ingram, “Mastering the Core Teachings of the Buddha”, 2018*

> Improving your game is really really hard. It may be the hardest thing
you ever attempt. I'd estimate only 20% of men are even capable of
processing the basic concepts to reach an understanding of Game. Of
those men who theoretically "get" the idea of Game, probably only 20%
of them will do enough in-field work to become better with women. Of that
tiny sample, probably only 10% will actually become Good With Women. This
means that only 1 out of 250 men will even reach the intermediate level of
Game. Even those odds likely overstate the number of Players in the world.

*— Nick Krauser, “Daygame Mastery”, 2014*

### Reports

* How I organize my information diet
* Becoming Marginally More Productive
	* Follow Alexey Guzey's Advice, Leave the House
	* Internet Abstinence
* Buying Socks of One Kind
* Tracking A Lot
* Chatting Up Random People
	*	Asking the Hamming Question, "What is art?", "What is
		justice?", or simply, "Would you like to hold a conversation?"
* Weekly 1-on-1s
* Kissing Hands as Greeting/Goodbye
* Future:
	* Remembering Names
	* Fixing My Voice
	* Experiments with Butt Stuff
	* Fixing my Posture
	* 52 Weeks of Meditation Techniques
		* Concentration of the Breath
		* Concentration on Sound
		* Concentration on Heartbeat
		* Fast Noting
		* Slow Labelling
		* Metta
		* Bodyscanning
		* Kasina on Candle Flame
		* Kasina on Colored Disk
		* Kasina on Water
		* Open Monitoring
			* Clear the desk, just watch out for pre-thoughts
		* Do Nothing
		* Zen stuff?
		* Mantra stuff?
		* Transcendental meditation stuff?
		* Chanting?
		* Visualization?
		* Yogic stuff? (Mudra)
* Lessons in Instrumental Rationality from Approaching 360 Women in the Street
	* I Solved a Big Problem in My Life: Not Having Sex

### Misc

* Evolution as a Tautology
	* Structures that are Better at Self-Replication will Eventually be More Common than the Ones Which are Not
* A Collection of Screenshots from “Legend of the Galactic Heroes”
* Very Specific Psychedelic Qualia
	* №1: “Inverse Capgraps Syndrome”
		*	You locate a specific person while also being fully able to understand
			that the person is not visible, audible, and can not be felt or smelled.
			For example, you would say: "I perceive Steven sitting on the chair"
			while not seeing Steven, hearing or feeling him, and being fully aware
			of these facts.
	* №2: “The Infinite Room-Accordion Thinks Itself”
	* №3: “Very Very Long Now”
	* №4: “Young & Blocky Consciousness“
* Coding Standards
	* General Project Setup
	* C
	* Shell Scripting
* Mistakes
* Open Questions
	* Why Not Nano-Apartments?
	* Why Not Prepping?
	* ~/etc/notes/questions
* Good Ideas
	* Some ideas I've read about & found good
	* Forecasting
		* Track records
		* Prediction platforms
		* Prediction markets (`https://en.wikipedia.org/wiki/Prediction_market`)
		* Decision markets
		* Futarchy
	* Voting methods
		* Approval voting
		* Maybe quadratic voting, although I haven't looked into it too much
	* Taxes
		* Pigovian taxes instead of strict rules on damaging public goods
			* How computationally tractable are these?
			* Which computational complexity?
		* Harberger taxes (COST)
			* The thing Glen Weyl is talking about
	* Sokalling
		* Look up tweet by David Chapman
		* Adversarial submitting of fraudulent papers to journals
	*	Besides stdin, stdout and stderr, add usrin and usrout as
		standard unix files: latter is for confirming decisions,
		status bars etc. I read this proposal a few years back,
		but can't find it again.
	*	Programming languages without operator precedence:
		APL/K/J. Why? One less detail to keep in mind, structured
		data flow. Downside: Inconsistency with mathematics,
		not relevant in languages with little use of operators.
	*	Status tags ({prototype, in progress, maintenance,
		finished, hiatus, abandoned}) for open source projects.
	* Mental tool: How would you solve this if you had a hypercomputer?
		* Unbounded Analysis on arbital, problem relaxation as a tactic on LW
	* Cryonics
	* Daygame
* Cryonics Zine
* The Grand Picture
* Fundamentals

> we should be far more explicit about the assumed background against
> which we intend to communicate.

*— John Nerst, [“30 Fundamentals”](https://everythingstudies.com/2018/07/16/30-fundamentals/), 2018*

### Explorables

* For modern methods of causal inference from statistical data (especially Pearl?)

### Interviews

* /u/JhanicManifold
* /u/MakeTotalDestr0i
* /u/redditselloutbiddy
* TheRedQuest
* Brian Tomasik
* CronoDAS

### Fiction

* A Religion
	*	A pseudo-mathematical religion combining several
		unrelated ideas is presented and explained.
		Inspired by [Unsong](http://unsongbook.com/)
	* Ingredients
		* Timelessness
			* Plotinus
		* Tegmark's Mathematical Universe
			* `/usr/local/doc/unread/physics/our_mathematical_universe_tegmark_2014.epub`
		* Symmetry Theory of Valence
			* `/usr/local/doc/unread/principia_qualia_johnson_2017.pdf`
		* Scott Alexander's Solution to Theodicy
			* `https://slatestarcodex.com/2015/03/15/answer-to-job/`
	* Explanation
		* Creation
		* God
		* Heaven
			* Compute "path" of mind from existence in the world as a mathematical shape into n-dimensional (72-dimensional?) ball
			* hedonium has maximal symmetry, which should just be the ball, but little information content
			* hold this computation in timelessness so that the mind experiences the path indefinitely long
		* Hell
* Dishwasher Paper Titles
	* Maybe with Abstracts
* Homeless Super-Mathematicians
	* Perhaps in the SCP format?
* Blue Reality
	* Like the Red Reality SCP, but people in there are really well (think MDMA)
* The Intentionality of the Tyrannical Object
	* SCP format
	* Abstract Tyrannical Object as a thing in the real world
	* Has the property of intentionality (except for celibate men?)
	* Text by german early 20th century continental philosopher about this object
	* Fragments by a 11th century german monk about this
* Guten Morgen
* All-Feeler
	* Object that untwists topological boundaries in phenomenological space
* Qui Custodiet?
	*	A group of AI alignment researchers by accident
		stumbles upon cognitive enhancement and willpower direction
		technologies. Because AGI seems imminent, they reluctanctly start
		using the technology. They manage to always stay a step or two
		ahead of the AI systems growing in capability, but continue
		having to self-modify in order to devise new strategies. The
		world watches as increasingly unaligned alignment researchers and
		unaligned artificial intelligence battle for attainable utility…
* A History of Names
* Destructive Uplift Theory of the Boötes Void
* A Fanfiction of Edge of Tomorty: Rick Die Rickpeat, explaining the dangers of hypercomputation
	* If you have a closed timelike curve, you are probably uncleashing computational titans the likes of which you can not fathom, beings that would snack superintelligences like potato chips
	* See also: Causal Noose by qntm, NP-complete Problems and Physical Reality Aaronson 2006
* Skalpell Bizeps

> 11-uhr-luft liegt rauh auf dem parkplatzboden. in den ritzen des
asphalt streitet sich krepierender löwenzahn mit ausgeblichenen
zigarettenstummeln um platz. abblätternde farbe liegt dazwischen,
obwohl die altbauten noch ein paar hundert meter entfernt liegen.

* myzel

> moderne kapitalistische verteilung ist weder zentralisiert noch
dezentralisiert, sie ist myzelisch, verwaberndes, meist unsichtbares
gewebe in einem fruchtbaren umfeld, mit anhäufungen, ballungen und
kumulationen von produktionszentren—zur festigkeit verdichtetes
gewebe dort fassbar, wo es sich am wenigsten äußert. werden als
eine kontingente verschmelzung von fast-sein und konkretheit"

### Translations

* Kodomulo Manifesto (translation of “A Hacker Manifesto” into Esperanto)
* Translate Endliche Gruppe I into English

### Archiving

* Type up John Nash's Thesis in LaTeX
* Make page explaining "Shoulding at the Universe"
* Make page explaining "Cryptonormativity"
* Make a page explaining "Mental Motions"
	* Find mentions of this, and write up what the term means.
* squid314 dedicated site (only good posts/posts that don't doxx Scott too much, ask him about it)
* Chronological archives of blogs
	* TheRedQuest
	* hbdchick
	* Traditions of Conflict
* Best of collections from blogs
	* TheRedQuest
	* Overcoming Bias
	* hbdchick
* A wiki for pickup terminology
* Kiwix versions of LessWrong, Alignment Forum, Effective Altruism Forum

Data Sets
----------

Collect data on

* Bag Spreading
* [Daygame](./daygame_cost_benefit.html#Appendix-C-Empirically-Checking-the-Assumptions)
* [Masturbation and Attractiveness](./masturbation_and_attractiveness.html#Method)
* [Subjective Life Expectancy](./estimated_life_expectancy.html#Data-Collection-Method)
* Meditation
* [Masturbation](./data/masturbations.csv)
* A Large Dataset of Forecasts and Outcomes
* Large STEM Dataset
	* For training large ML models that are less likely to be [human models](https://www.lesswrong.com/posts/BKjJJH2cRpJcAnP7T)

Flashcards
-----------

* Convert [Issa Rice's Analysis Flashcards](https://github.com/riceissa/tao-analysis-flashcards) to Anki
* Flashcard sets for:
	* Artificial Intelligence: A Modern Approach
	* Naive Set Theory
	* Reactive Systems
	* Population Genetics
	* Multivariable Calculus
	* Pattern Recognition and Machine Learning
	* The Jazz Piano Book
	* A Primer in Social Choice Theory
	* Parameterized Algorithms

Music
-----

### Clarinet

* Clarinet Concerto (Mozart)

### Piano

* The People United Will Never be Defeated (Rzewski)
* Das Wohltemperirte Clavier (Bach)
* Beethoven Piano Sonatas (Beethoven)
* Impromptus (Schubert)
* Nocturnes (Chopin)
* Gymnopédies/Gnosiemmes (Satie)
* Rhapsodie in Blue (Gershwin)

Languages to Learn
-------------------

* French
* Esperanto
* Latin
* Serbocroatian
* Toki Pona
* Lojban
* Ithkuil

Programming
-----------

* cap
	*	simple language for assembling different files into one. syntax very
		sed/ed like, mostly like this: `[line,]line@file[<|^|>][line,]line[|comm]`
		where line is a regex enclosed in '/' with an optional number suffix
		or a line number, file is a filename and comm is a shell command in
		single quotes. the text from each file is inserted into a buffer and
		printed at the end of the cap script.
* toc
	*	time out cat, which prints its input unless there was no
		input for more than argv[1] seconds (try different
		versions, settle for the most exact version that is
		not unbearably slow).
* lvst
	* print levensthein distances of strings
	* option '-f' for the field separator
	* can be used for fuzzy search
	* usage:

			$ lvst "test"
			foo
			3:test:foo
			bar
			4:test:bar

* cy
	* A very simple version control system, written in rc. inspiration from put and get, from "the unix programming environment".
	* supports 3 operations
		* init (initialize a repository)
		* put (make a commit)
		* get (go back to a certain commit)
	* tracks changes within files and deletion/creation of files
	* reason: git/hg are good, but way too huge for private, simple, linear, personal repositories.
	* inspiration: svn/rvn/eie<!--TODO: links for these-->
* fle
	* suckless pager
	* commands
		* [f]orwards
		* [b]ackwards
		* [u]p
		* [d]own
		* [j] (line up)
		* [k] (line down)
		* [g] (first line)
		* [G] (last line)
		* [/] for searching
		* [n]ext and [p]revious match
	* support for arbitrary length files, loading lazily, unicode is displayed properly, big lines are dealt with properly.
* recog
	* program that accepts one backus-naur form grammar and checks if it's input or other files match that grammar.
	* BNF -(Convert to Chomsky Normal Form)> CNF -(Cocke-Younger-Kasami algorithm)> Boolean
	* Relevant material:
		* RFC 2234
		* RFC 4234
		* RFC 5234
		* RFC 7405
	* Possible BNF forms:
		* ABNF (RFCs)
		* EBNF
		* naive & simple form (similar to the one used on Wikipedia)
			* <symbol\>
			* optionality: '?'
			* repetition: '+'
			* repetition with optionality: '*'
			* alternative symbols: '|'
			* assignment: '::='
			* "string"
* sif
	* simple text processing filter that takes only one instruction
	* (single instruction filter)
	* instruction form:
		* `[^]/str/[,[^]/str/]((a|i|c)/str/)|d|p`
		* str is a literal string here (no regex)
		* a=>append, i=>insert, c=>change, d=>delete, p=>print
		* '^' means that the following str is excluded from the matched text
	* sif does not do input/output buffering and does treat whitespace as any other character.
	* normally, everything is printed, unless the option '-n' is used.
* pau
	* vis-digraph reads from the terminal input directly and emulates the input of the corresponding character
		* uses table from RFC 1345
			* Seems not extendable, damn
	* if vis-digraph extendable, add:
		* Interrobang	‽	?!
		* Join	⋈	><
		* Expected value	𝔼	|E
		* Real numbers	ℝ	|R
		* Integers	ℤ	|Z
		* Natural numbers	ℕ	|N
		* Triple e	≡	3=
		* Approximately e	≈	~~
		* Subscript a	ₐ	_a / as
		* Subscript e	ₑ	_e / es
		* Subscript h	ₕ	_h / hs
		* Subscript k	ₖ	_k / ks
		* Subscript l	ₗ	_l / ls
		* Subscript m	ₘ	_m / ms
		* Subscript n	ₙ	_n / ns
		* Subscript o	ₒ	_o / os
		* Subscript p	ₚ	_p / ps
		* Subscript s	ₛ	_s / ss
		* Subscript t	ₜ	_t / ts
		* Superscript i	ⁱ	^i
		* Superscript n	ⁿ	^n
	*	daemon that catches such digraphs and emulates them as
		if they were typed, using vis-digraph
* mtfs
	* plan9 file server for a file that returns the current metric time on read
* libbruch
	* rational numbers with libzahl
	* some functions:
		* badd(bruch a, bruch b, bruch c): a:=b+c
		* bsub(bruch a, bruch b, bruch c): a:=b-c
		* bdiv(bruch a, bruch b, bruch c): a:=b÷c
		* bmul(bruch a, bruch b, bruch c): a:=a⋅c
		* binv(bruch a, bruch b): a=b^(-1)
	* more functions:
		*	bset, bseti, bsets, bsetu, bstr, bfloor, bceil,
			bmod, bcmp, bcmpu, bsqrt, binit, bfree, bsave,
			bload, bsetup, bunsetup, berror, bperror
* nager
	* sxhkd for the mouse
	* syntax: `[MOUSEEVENT] [, MOUSEEVENT] [ /*possibly nested*/ COMMAND ]`
* erle
	* rlwrap alternative, takes ideas from the fish shell interactive mode
	* normal readline like behavior (but using something simpler, like linenoise/dietline)
	* history file is loaded during startup
	* 	`<text>[UP]` shows the last command containing `<text>`,
		again `[UP]` the one before that, and so on
	*	`<word1> <word2>[TAB]` expands `<word2>` into the last word
		(string separated from the others with a newline/space)
		beginning with `<word2>`
	*	no input for more than half a second/a second shows a suggestion
		of the last command beginning with the current line.
	* ideas for speeding it up:
		* use `char**` for storing each history and words
		* benchmark and optimise, of course
* pandeck
	* convert files from different spaced repetition softwares into another
		* fulgurate .crd
		* mnemosyne
		* anki
		* [orbit](https://withorbit.com/)
* unitspheretransform
	* VR application that visualizes the transformation of the unit sphere in 3-dimensional space
	* also unit circle transform
	* color code the original vectors
	* interpolate them?
* hedonium
	* look up different information-processing centric ideas about consciousness
	* combine them with the symmetry theory of valence
	* implement the best approximation of these
* minspantree
	* implement all algorithms for the minimum spanning tree in a functional programming language
	* like sml/ocaml
	* `/usr/local/doc/unread/cs/state_of_the_art_algorithms_for_minimum_spanning_trees_eisner_1997.pdf`
* nenio
	* a suckless prolog implementation
	* ISO prolog
* rien
	* suckless sml implementation, sml '97
	* maybe build on mosml
* curve
	* C with significant whitespace
	* indentation instead of braces
	* optional semicolons & optional parentheses around for/while/if/switch
* jmp
	* j/z for rc
	* jumps into frecent directories
	* should also work on plan9
* ladder
	* datastructure where key and value are interchangeable
	* two arrays/slice, sorted, where each element has a pointer to the corresponding element in the other list
	* searching has the speed of binary search
	* insertion has the speed of the underlying datastructure, but twice
* openspace
	* 	Given a rectangle with many inscribed rectangles, what is the
		biggest open rectangle in there?
	* Seems like a packing problem
* species
	* browsable tree of all currently known biological species
	* starting from the highest classification
* texdown
	* small TeX library that offers basic markdown-like functionality:
		* Numbered lists
		* Unnumbered lists
		* code listings
		* quotes
		* bold/italic text
		* links
		* images
		* paragraph headings
* librule
	* C library for raku rules
	* read about:
		* backtracking
		* regex implementation (swtch.com?)
		* raku rules
	* example program: far (find after rule, grep; but with raku rules)
	* github.com/zorgnax/librx
* nest
	* program dealing with nested data structures
	* similar to lisp, but without execution
	* am I NIHing this?
* noise
	* utility for producing white/pink/brown/&c noise
* spiel
	* utility for logging/visualizing daygame stats
* orakel
	* utility for making/ranking/visualizing forecasts
* dukkha
	* utility for logging/visualizing meditation stats
	* get inspiration from meditavo
* tomate
	* little pomodoro utility
* sent2tex
	* converts a sent presentation to a pdf presentation
*	1on1match: Platform that connects people who'd like to do 1-on-1s,
	by personality style
* Offline version of guesstimate
*	A reddit bot on /r/gonewildstories that does a gender analysis for
	the writing and posts the result
* choiceworth
	* A small program implementing the method by MacAskill, Ord & Bykvist 2020 in “Moral Uncertainty”
	* Using MEC, variance voting, and the Borda rule
* socialchoice: Library implementing most of the concepts from social choice theory, e.g. (not inclusive):
	* Tournament graphs
	* Top cycle, Banks set, Uncovered set
	* Majority voting, plurality, Borda score, Kemeny rule
	* Methods for checking manipulability, single-peakedness
* interweave
	* A utility that takes a list of files and "interweaves" their lines (or by some other separator)
	* E.g. "a\nb\n" and "1\n2\n3\n4\n" will become "a\n1\n2\nb\n3\n4\n"
* Computing Shapley Values in Klong
	* First argument: the function, second argument: the given values, third argument: the fallback values.
	* `shapleyval::{f::x;g::y;d::z;{s::!#g;s::ps(&~s=x)}'!#y}`
	* `shapleyval({(x@2)+(*x)^x@1};[2 4 4];[1 1 0])`
* A distributed issue tracking system
	* See [Wellons 2009](https://nullprogram.com/blog/2009/02/14/)
	* Why didn't this happen in the first place?
	*	Probably just because centralized systems outperform
		decentralized ones, even when the underlying structure
		is decentralized, as in git/GitHub, and Github then
		focused on the issue tracking/continuous builds component
		* Github already had a [commoditized complement](https://www.gwern.net/Complement)
	* Check out [ditz](http://ditz.rubyforge.org/)/cil/ticgit and others (bug from the suckless page?)
* ssam
	* A stream version of sam: ssam : sam :: sed : ed
	* Like, a proper one, not just a thin shell script wrapped around sam
	* Maybe this exists already?

### Klong Libraries

* combin.kg
	* combinatorics library for klong
	* exponentiation
	* tetration
	* n-tation
	* factorial
	* binomial coefficient
	* stirling numbers (1st/2nd kind)
	* eulerian numbers (1st order, 2nd order)
	* catalan numbers
	* counting partitions
* date.kg
	* date/time library for klong: convert different date formats to another
* utf8.kg
	* unicode decoding/encoding library
	* see how myrddin/lua/libutf/plan9 did it
* linalg.kg
	* linear algebra library for klong
	* function for the determinant
	* function for gaussian elimination
	* function for matrix multiplication
	* function for matrix inversion
	* function for the calculation of polynomial division
* statests.kg
	* library for statistical tests

### Contributions

* mupdf
	* implement unicode search
	* improve search overall, lacking
	* why don't ← and → work for next/prev page?
* myrddin
	* documentation: "and modern features with a high cost-benefit ratio"
	* cost/benefit is high? Clarify
* vis
	* add C-a and C-e for beginning of line and end of line in insert mode
	* add C-← and C-→ for jumping words in insert mode (equivalent of b and e)
	* fix syntax highlighting for ocaml with single quotes: 'a takes the whole line
	* Syntax highlighting of inline code in markdown is annoying (dark blue background!)
		* Submit pull request for existing fix (which makes it mauve)
	* plugin for adding markdown wikipedia link easily
* sad
	* implement features that weren't finished
	* care for it
* toxcore
	* maybe
	* single/group
	* chat/audio/video
	* not much more, really
* neo2
	* port neo2 to plan9/9front/Haiku OS
* git
	* Add heatmap flag for git blame (for recency)
* WebTeX
	* Make it able to display `\bigsqcap`, `\bigplus`, `\bigmult`
* Help administering schelling.pt, it needs it
* klong
	* receiving output of shell commands (maybe via pipe?)
	* self adverb (options are :!, :&, :,, :;, :<, :>, :?)
		* :< and :> should be reserved for something symmetric
		* :; is not fit because ; is not really a verb or adverb
		* :!, :&, :? and :, are the best options
	* support for complex numbers
		* logarithms for complex numbers
	* nplot
		* Support for multiple bargraphs
		* Bargraphs with negative values
		* Logarithmic scales for graphs
		* setrgb doesn't work properly: after setting the color once, it can only be reset to black
		* Example:

				.l("nplot")
				grid([0 100 10];[0 100 10])
				text(250;60;"Foo")
				setrgb(0;0;1)
				text(200;250;"Bar")
				setrgb(1;1;0)
				text(100;100;"Baz")
				draw()

	* nstat
		* n% confidence interval
		* polynomial/exponential/logarithmic (?) fit for a dataset
	* Range is extremely slow for anything but integers, why?
	* error with klong: `#'s58'!40` returns `kg: error: call: type error: [6 :triad %call1 %pop1]`
		* bug, report
	* Pivot in the gauss/elim implementations
* fzf
	* Why doesn't fzf cope well with shuffled or repeated letters?
	* 'niiiiiplav' and 'nlapiv' both take me to the wrong directory, they're obviously meant for my home directory
* txtnish
	* add a `mentions` command
* Mood Patterns
	* Add option to change the notification sound
* dc 9base manpage:
	* typo in the order of operations in the manpage

> \+ - / * % ^
>	Add subtract multiply divide remainder or exponentiate the top
>	two values on the stack.

* Make GNU fmt respect unicode:
	*	Formatting
		"∸∸∸∸∸ ∸∸∸∸ ∸∸∸∸ ∸∸∸∸∸
		∸∸∸∸∸ However, in a sense, maxichoice
		contraction functions in general produce contractions"

produces

	∸∸∸∸∸ ∸∸∸∸ ∸∸∸∸ ∸∸∸∸∸
	∸∸∸∸∸ However, in a sense, maxichoice contraction
	functions in general produce contractions

### Languages to Learn

* Myrddin
* Scheme
* SML
* Forth
* Prolog

Wikipedia Articles
-------------------

### Create

* Enhanced/Extended Suffix Array
* Shapley Saddle
* List of Animals by Number of Eyes
* Weisfeiler-Lehman algorithm
* Brandes' algorithm
* IC/IC\* algorithm
* do operator
* Back-door/Front-door criterion
* Place premium
* Pigou bound
* Myerson's Lemma
* Bulow-Klemperer Theorem
* Prophet Inequality
* Population Ethics pages
	* Sadistic conclusion
	* Critical-threshold approaches
* Daniel Ingram
* Pragmatic Dharma (?)
* Kenneth Folk

### Improve

* [Maximal pair](https://en.wikipedia.org/wiki/Maximal_pair)
	* Add examples
	* Add description of MUMs
* Judea Pearl
* Patri Friedman site states he considers himself a rationalist, but that links to the page on philosophical rationalism, while I suspect this refers to the LW variety
* In the page on Single-parameter Utility, the formulas contain non-\text multi-letter variables. Fix that.
	* Same for Monotonicity (mechanism design)
* What the fuck is going on with the The Gods Themselves page?
* Wikipedia pages on symbols in mathematics and physics are sprawling and confused, clean them up
* Use the definition from “Algorithmic Game Theory” of correlated equilibrium in the article Correlated equilibrium, the current explanation uses (but doesn't introduce) s_i
	* Yeah, the current explanation is barely comprehensible
* On Wikipedia page for Graph Kernel, correct "Leman" to "Lehman" (first, check whether this is actually wrong).
* Find Ian Goodfellow's true year of birth
* Add missing national anthems to `https://en.wikipedia.org/wiki/List_of_national_anthems`

Answers
--------

* Answer `https://old.reddit.com/r/slatestarcodex/comments/u3xpn3/effective_altruists_and_worrying_about_nuclear/i4t4u2p/`
* Answer `https://old.reddit.com/r/slatestarcodex/comments/u3xpn3/effective_altruists_and_worrying_about_nuclear/i4sxf5n/`
* Answer `https://www.lesswrong.com/posts/pSdxQfbvC5qBBdehq/what-is-the-most-significant-way-you-have-changed-your-mind?commentId=G97DgBgPvWbugkZEd`
* Answer `https://forum.effectivealtruism.org/posts/aNu3HCGjLCn45EMNp/reward-long-content` Nick Whitaker & salonium

Arbital
--------

* Utility indifference on Arbital contains a few typos

Metaculus Questions
-------------------

* A question that tries to gauge how much Metaculus forecasters are incentivized by points vs. simply accuracy
* A question about the discovery of a [perfect cuboid](https://en.wikipedia.org/wiki/Euler_brick#Perfect_cuboid)
* A question about the average temperature in 2050 in central Europe (Gulf Stream reversal)
* A question about SGSS (?) data for virginity/no sex in last year for 2025-2030
* A question about antibiotic resistant strains
* Some questions about the performance of BCIs

Structure
---------

* Top-level:
	* Translations
		* English to Esperanto
	* Music
		* Clarinet
		* Piano

General
-------

* Send typos to people, let them correct them

In-World Projects
------------------

* Destroy the moons of Mars
* Found a community of algae farmers that speak a Icelandic-Basque pidgin
* Add Ithkuil script to the UCSUR
* Bring the rest of the Latin super/subscripts into Unicode

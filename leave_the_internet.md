[home](./index.md)
------------------

*author: niplav, created: 2021-03-02, modified: 2021-10-14, language: english, status: notes, importance: 6, confidence: possible*

> __.__

Leave The Internet
==================

<!--
https://www.lesswrong.com/posts/Jq73GozjsuhdwMLEG/superstimuli-and-the-collapse-of-western-civilization
https://www.youtube.com/watch?v=wf2VxeIm1no
https://www.youtube.com/watch?v=VpHyLG-sc4g
https://www.lesswrong.com/posts/HBxe6wdjxK239zajf/what-failure-looks-like
GPT-3
https://builtin.com/data-science/recommender-systems
https://medium.com/dataseries/how-youtube-is-addictive-259d5c575883
https://medium.com/@nrs007/recommender-systems-and-their-impacts-on-autonomy-51a69c64038
https://towardsdatascience.com/introduction-to-recommender-systems-6c66cf15ada?gi=792420939b20
https://www.wiley.com/en-us/Recommender+System+with+Machine+Learning+and+Artificial+Intelligence%3A+Practical+Tools+and+Applications+in+Medical%2C+Agricultural+and+Other+Industries-p-9781119711575
[Internet addiction](https://en.wikipedia.org/wiki/Internet_addiction_disorder)
https://www.lesswrong.com/posts/HBxe6wdjxK239zajf/what-failure-looks-like?commentId=CB8ieALcHfSSuAYYJ#CB8ieALcHfSSuAYYJ
https://www.lesswrong.com/posts/qKvn7rxP2mzJbKfcA/persuasion-tools-ai-takeover-without-agi-or-agency
[Attention span](https://en.wikipedia.org/wiki/Attention_span)
https://www.lesswrong.com/posts/YicoiQurNBxSp7a65/is-clickbait-destroying-our-general-intelligence
-->

> New religions and mystery cults explode across the planet; much of
the Net is unusable, flattened by successive semiotic jihads.

*– [Charles Stross](https://en.wikipedia.org/wiki/Charles_Stross), [“Accelerando”](https://en.wikipedia.org/wiki/Accelerando) p. 169, 2005*

The Basic Argument
------------------

### Two Different Growth Modes

### Humans Minds are Full of Holes

What is To Be Done?
-------------------

### Make Phasing Out Possible

### Lag Behind 5 Years

How?
----

### Download Stuff

As an example, here's the things I have downloaded for offline reading:

* Remaining episodes of the [podcasts I listen to](./podcasts_list.html)
* All music I want to listen to
* A large collection (several thousands) of books and papers I want to read
* [Websites I like](./sites.html)

To download a website, I usually used the command wget<!--TODO: link-->:

	wget --page-requisites -e robots=off -p -k -c -r --mirror -p --html-extension -R '*replytocom*,*like_comment*,*p=*,*test-preview=*,*test-expand=*,*url=*,*share=*,*commentId=*,*sortedBy=*,*after=*,*before=*,*limit=*,*filter=*,*showPostCount=*,*useTagName=*,*///*,*social-media/*,*updated-max=*,*max-results=*,*reverse-paginate=*,*showComment=*,*filters_and=*,*following%5C*,*https:%5C*,*fsnapshot*' -P . www.example.com

This excludes downloading the same page for every comment with wordpress
sites, and different versions of the allPosts pages for the EA forum and
LessWrong. Unfortunately, both the EA forum and LessWrong are not very
amenable to being downloaded this way, and I will have to experiment
with other approaches. It also sadly can't distinguish between resources
(like images) hosted on other sites and other websites, and so those are
missing (if `-H` is turned on, it begins downloading the entire internet).

To download a webpage, I use this command:

	wget -H -e robots=off -p -k www.example.com/resource.html

### Have a Designated “Internet Location” Which is Not At Home

Optionally: Separate work with internet, work without internet, fun with
internet, fun without internet spaces

Possible Counterarguments
--------------------------

### Brain “Software” Very Flexible

### Addictive Process Takeover=Doom

### But Won't Regulators Outlaw?

### Giving Up Much

Retrospective
--------------

Started 2021-05-21.

AI Disaster Scenario: Human Progress Stalls Due To Attention-Destroyers
-----------------------------------------------------------------------

AI systems become capable enough to sap out most of human
attention/ability to work, this prevents more capable AI systems from
being built, but also destroys any options for progress.

This might end up in an equilibrium.

Appendix A: Defining “Addictive Process”
-----------------------------------------

### Modified-Self Approval

#### Transparency

#### Weak Amplification

#### Approval Chaining

#### Why This Definition is Still Unsatisfactory

### Distinguishing Information Hazards from Attention Hazards

### Present-Time Examples

#### Food Optimizer

#### Sexuality Optimizer

#### Attention Optimizer

#### Status Optimizer

### Possible Future Examples

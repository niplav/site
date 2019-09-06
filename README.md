Content and Code for a Website
==============================

These files contain articles, images, recordings and code for a website.
It currently has no domain (yet), but that should take only 1 or 2 years.

Building
--------

To rebuild the articles, call

	make sitedata

There are several more targets: `make total` generates all important
files, but doesn't install them. `make puttit` generates the important
files and installs the images, and `make clean` removes the generateable
files from the repo. `make sitedata` takes a couple of seconds, `make
total` and `make puttit` take a couple of minutes (and both need an
internet connection).

Prerequisites
-------------

Building requires [markdown_py](https://pypi.org/project/Markdown/)
for `sitedata`, and [Klong](http://t3x.org/klong/index.html) and
[BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) for
`total`.

License
-------

The content on this website is licensed under [Creative Commons
4.0](https://creativecommons.org/licenses/by/4.0/). The code is
licensed under the [MIT license](./LICENSE).

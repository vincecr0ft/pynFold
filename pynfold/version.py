from __future__ import absolute_import, division, print_function

# Format expected by setup.py and doc/source/conf.py: string of form "X.Y.Z"
_version_major = 0
_version_minor = 1
_version_micro = ''  # use '' for first of series, number for 1 and above
_version_extra = 'dev'
# _version_extra = ''  # Uncomment this for full releases

# Construct full version string from these.
_ver = [_version_major, _version_minor]
if _version_micro:
    _ver.append(_version_micro)
if _version_extra:
    _ver.append(_version_extra)

__version__ = '.'.join(map(str, _ver))

CLASSIFIERS = ["Development Status :: 3 - Alpha",
               "Environment :: Console",
               "Intended Audience :: Science/Research",
               "License :: OSI Approved :: MIT License",
               "Operating System :: OS Independent",
               "Programming Language :: Python",
               "Topic :: Scientific/Engineering"]

# Description should be a one-liner:e
description = 'pynFold: implementation of various solutions to unfoldng\
and the inverse problem '
# Long description will go up on the pypi page
long_description = """

PynFold
========
pynFold (pronounced pen-fold) is a pythonic implementation of (eventually)
many of the RooUnfold ROOT Unfolding Framework aiming to compare unfolding
methods with those provided outisde of high energy physics and to increase
to robustness of a flexible re-usable codebase.

The fbu algorithm implemented here is the fully basian unfolding method
based code developed by Clement Helsens, Davide Gerbaudo, and Francesco Rubbo

Unfolding relates to the problem of estimating probability distributions
in cases where no parametric form is available,
and where the data are subject to additional random fluctuations due
to limited resolution.
The same mathematics can be found under the general heading of
inverse problems, and is also called deconvolution or unsmearing.

This type of equation is also known as the Fredholm integral of the first kind.
The Kernel K, acts as a smoothing matrix in the forward detector and
we can interpret its elements as a matrix of probabilites,
strictly positive between 0 and one.
Inverting the matrix (if possible) resutls in strictly non-probabilistic terms
that, instead of smothing, add large high frequency components due to
arbitrarily small fluctuations.
The goal of unfolding is to impose some knowledge about the smoothness of this
matrix onto the inversion to suppress such high frequency elements.

This project is currently under development.
If you would like to be involved please contact vincent.croft at cern.ch.

License
=======
``pynfold`` is licensed under the terms of the MIT license. See the file
"LICENSE" for information on the history of this software, terms & conditions
for usage, and a DISCLAIMER OF ALL WARRANTIES.

All trademarks referenced herein are property of their respective holders.

Copyright (c) 2018--, Vincent Alexander Croft,
New York University Department of Physics and DIANA-HEP
"""

NAME = "pynfold"
MAINTAINER = "Vince Croft"
MAINTAINER_EMAIL = "vincecroft@gmail.com"
DESCRIPTION = description
LONG_DESCRIPTION = long_description
URL = "http://github.com/vincecr0ft/pynFold"
DOWNLOAD_URL = ""
LICENSE = "MIT"
AUTHOR = "Vince Croft"
AUTHOR_EMAIL = "vincecroft@gmail.com"
PLATFORMS = "OS Independent"
MAJOR = _version_major
MINOR = _version_minor
MICRO = _version_micro
VERSION = __version__
REQUIRES = ["numpy", "matplotlib", "pymc", "scipy"]

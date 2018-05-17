# pynFold - Unfolding with python
[![Build Status](https://travis-ci.org/vincecr0ft/pynFold.svg?branch=master)](https://travis-ci.org/vincecr0ft/pynFold)

![Oh, crumbs!](https://c1.staticflickr.com/1/588/23404929566_5c9dfed1ef_o.jpg) 

pynFold (pronounced *pen*-fold) is a pythonic implementation of (eventually) many of the [RooUnfold](http://hepunx.rl.ac.uk/~adye/software/unfold/RooUnfold.html) ROOT Unfolding Framework aiming to compare unfolding methods with those provided outisde of high energy physics and to increase robustness by eliminating dependencies on the ROOT libraries basing algorithms only on numpy and minimal additional libraries. 

The base algorithm implemented here is the fully basian unfolding method based on work by Clement Helsens, Davide Gerbaudo, and Francesco Rubbo [fbu](https://github.com/gerbaudo/fbu)

Unfolding relates to the problem of estimating probability distributions in cases where no parametric form is available, and where the data are subject to additional random fluctuations due to limited resolution. The same mathematics can be found under the general heading of inverse problems, and is also called deconvolution or unsmearing.

![integral equation](https://wikimedia.org/api/rest_v1/media/math/render/svg/dbba1aee3760825a222253bad7fab68e9f0437dd)

when *g(t)* and *K(t|s)* are known. This type of equation is also known as the [Fredholm integral](https://en.wikipedia.org/wiki/Fredholm_integral_equation) of the first kind. The Kernel *K*, acts as a smoothing matrix in the forward detector and we can interpret its elements as a matrix of probabilites, strictly positive between 0 and one. Inverting the matrix (if possible) resutls in strictly non-probabilistic terms that instead of smothing add large high frequency components due to arbitrarily small fluctuations. The goal of unfolding is to impose some knowledge about the smoothness of this matrix onto the inversion to suppress such high frequency elements.   

This project is currently under development. If you would like to be involved please contact vincent.croft at cern.ch or contact me on slack. 

this project depends on numpy, scipy and pymc
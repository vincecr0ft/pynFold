# PynFold
``pynfold`` ``fold``

An interface for pythonic solutions to the inverse problem also known as unfolding. 

``pynfold.fold``(*type*, *response*, *x_shape*, *y_shape = None*,
			 *data = None*, *data_hist = None*, *data_bins = None*)

All parameters are optional but cannot return unless sufficient information is supplied.

- **Parameters**:
  - **type**: 
    * *Naive (naive)* - Matrix Inversion, Correction Factors
    * *Dimensionality* - Truncated SVD, Richardson-Lucy/D'Agostini
    * *Composite* - Tikonov/damped LSQ, Fully Bayesian, RUN
  - **response**
    * a two dimensional mapping true:measured in lists of numpy arrays
    * can also be set using ``fold.set_response(xy)``
    * a response matrix can be supplied using ``fold.set_response_matrix(A)``
    * a response function can be supplied using ``fold.set_response_function(foo)`` this is evaluated for a uniform distribution over the required range. 
  - **x_shape** - discretisation of function in x. In Nystrom methods these are the abscissas for the quadrature rule and in Galerkin methods the span of the basis vectors. This is the desired shape and should be of lower dimensionality then the ``y_shape``.
  - **y_shape** - discretisation of function in x. In Nystrom methods these are the abscissas for the quadrature rule and in Galerkin methods the span of the basis vectors. If a histogram of data points is supplied then the shape is taken to match this..
  - **data** - the distribution to unfold.
    * *data* - a data vector which can be discretised by either Nystrom or Galerkin methods.
    * *data_hist* - a vector of bin contents e.g. the outcome of a particle detector experiment with implicit Nystrom discretisation. 
    * *data_bins* - shape of data vector. ``y_shape`` is matched to this shape.

- **Methods**:
  - **Fill(x, y), Miss(x)** - set response manually for individual events (float) *x* and *y*. (RooUnfold Legacy mode)
  - **response_matrix()** 
    - **returns A** - a matrix of probabilities of dim(m, n) = dim(y), dim(x)
  - **Unfold()** - Performs deconvolution of data given the response according to specified algorithm.
  - **h_reco()**
    * **Returns g** - a histogram of shape ``x_shape`` estimated from the ``Unfold()`` step
  - **b_reco()**
    * **Returns g** - a b-spline of with knots as ``x_shape`` estimated from the ``Unfold()`` step.

## Notes

### Unfolding Folklore
Prof. Dr. Volker Blobel compiled a list of rules of thumb to be used when approaching the inverse problem in high energy physics. 

1. Use at least 100 times more events in your response (MC) than you have data if possible.
2. To avoid an underconstrained system you should use at least twice as many data points(bins) as you have estimators (truth bins).
3. The response, though independent from the data, should be derived over a distribution as close to the target distribution as possible. (The uniform distribution used when a `response_function` is set to the fold is rarely optimal.)

## Work in progress. 

### Currently (partly) Available

- ``Naive - Matrix Inversion`` and ``Composite - damped LSQ`` are currently available through ``scipy.sparse.linalg.lsmr``
- ``HistogramPdf`` for Nystrom discretisation implemented but lacking functor+minimiser to fit a pseudo inverse.
- ``response_matrix`` is currently the only available kernel. Weighted polynomials (as used in RUN) and kde under preparation. 
- Fully Bayesian Unfolding was available under ``version 1.6`` but has been temporarilly removed to avoid dependency issues. 

### up-coming

- ``TSVD`` and ``D'Agostini`` - methods are implemented but lacking accurate variance/covariance calculations.
- ``Fit mode`` - construct the likelihood for the estimators and retrieve full minos intervals.
- ``spline-mode`` - discretise data and reconstructed functions using b-splies as basis functions in Galerkin expansion. 
- ``Regularisation Optimisation`` - Control/Visualise the effect of varying regularisation strengths.
- **Background estimates**, **Systematics** and **multidimensional distributions**

# Examples

A typical smearing function:
```
def smear(xt):
    xeff = 0.3 + (1.0 - 0.3) / 20. * (xt + 10.0)  # efficiency                                                     
    x = np.random.rand()
    if x > xeff:
        return None
    xsmear = np.random.normal(-2.5, 0.2)
    return xt + xsmear
```

define data and response
```
x = np.random.normal(0.3, 2.5,1000)
data = np.array([smear(i) for i in x])
data_hist, bins = np.histogram(data[data != np.array(None)], 10)
```

now define a simple default fold and check each input in tern.
```
f = fold()
f.set_data_hist(data_hist, bins)
f.set_response(np.array([x,data]))
```

though the 'true' distribution isn't used in the Unfolding calculation, the optimised binning is useful.
```
true_hist, x_bins = np.histogram(x, 5)
f.set_x_shape(shape=x_bins)
```
our response is obtained as:
```
print f.response_matrix()
```

and we can test the output in forward mode.
```
print data_hist
print 'should equal'
print true_hist
print 'times'
print f.response_matrix()
```
perform calculation
```
A = f.response_matrix()
f = np.asarray(true_hist)
print 'let us try it!'
print  f*A
```
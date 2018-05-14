from pynfold import fold
import numpy as np
# from matplotlib import pyplot as plt
# import ROOT

def smear(xt):
    # type: float -> float
    xeff = 0.3 + (1.0 - 0.3) / 20. * (xt + 10.0)  # efficiency
    x = np.random.rand()
    if x > xeff: return None
    xsmear = np.random.normal(-2.5, 0.2)
    return xt + xsmear

f = fold(method = 'iterative')
f.set_response(2, -10, 10)
f.iterations = 4

for i in xrange(10):
    xt = np.random.normal(0.3, 2.5)
    x = smear(xt)
    if x != None:
        f.fill(x, xt)
    else:
        f.miss(xt)

f.data = np.asarray([10,10])
print 'data is', f.data

f.run()
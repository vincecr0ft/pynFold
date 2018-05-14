from pynfold import fold
import numpy as np
from matplotlib import pyplot as plt

def smear(xt):
    # type: float -> float
    xeff = 0.3 + (1.0 - 0.3) / 20. * (xt + 10.0)  # efficiency
    x = np.random.rand()
    if x > xeff: return None
    xsmear = np.random.normal(-2.5, 0.2)
    return xt + xsmear


f = fold(method='invert')
f.set_response(40, -10, 10)

for i in xrange(100000):
    xt = np.random.normal(0.3, 2.5)
    x = smear(xt)
    if x != None:
        f.fill(x, xt)
    else:
        f.miss(xt)

f.data = f.measured.x
plt.plot(range(40), f.data, label='data')

f.run()
print 'the hist is', f.invert.reco_hist()
h = f.invert.reco_hist()
plt.plot(range(40), h, label='inverted')
plt.plot(range(40), f.truth.x, label='truth')
plt.legend()
plt.show()

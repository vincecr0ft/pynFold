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


f = fold(method='regularised')
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

for i in np.linspace(0.,1.5,5):
    f.tau = i
    f.run()
    h = f.regularised.reco_hist()
    plt.plot(range(40), h, marker='o',label=r'$\tau$ at {}'.format(i))
plt.plot(range(40), f.truth.x, label='truth')
plt.legend()
plt.show()

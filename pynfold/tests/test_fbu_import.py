from pynfold import fold
import numpy as np
# from matplotlib import pyplot as plt


def smear(xt):
    # type: float -> float
    xeff = 0.3 + (1.0 - 0.3) / 20. * (xt + 10.0)  # efficiency
    x = np.random.rand()
    if x > xeff:
        return None
    xsmear = np.random.normal(-2.5, 0.2)
    return xt + xsmear


f = fold()
f.set_response(4, -10, 10)

for i in range(1000):
    xt = np.random.normal(0.3, 2.5)
    x = smear(xt)
    if x is not None:
        f.fill(x, xt)
    else:
        f.miss(xt)

f.data = [100, 150, 200, 250, 300, 350, 400, 450]
# uncomment these when the tests work
# f.run()
# trace = f.fbu.trace
# print trace
#
# plt.hist(trace[1], bins=20, alpha=0.85, normed=True)
# plt.ylabel('probability')
# plt.show()

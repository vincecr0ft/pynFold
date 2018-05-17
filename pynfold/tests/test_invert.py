from pynfold import fold
import numpy as np
from matplotlib import pyplot as plt


def smear(xt):
    # type: float -> float
    xeff = 0.3 + (1.0 - 0.3) / 20. * (xt + 10.0)  # efficiency
    x = np.random.rand()
    if x > xeff:
        return None
    xsmear = np.random.normal(-2.5, 0.2)
    return xt + xsmear


dim = 40
f = fold(method='invert')
f.set_response(dim, -10, 10)

for i in range(10000):
    xt = np.random.normal(0.3, 2.5)
    x = smear(xt)
    if x is not None:
        f.fill(x, xt)
    else:
        f.miss(xt)

f.data = f.measured.x
fig, ax = plt.subplots()
# fig.facecolor = 'white'
ax.plot(range(dim), f.data, label='data')

f.run()
h = f.invert.reco_hist()

ax.plot(np.linspace(0, dim, dim / 2), h, marker='o', label='inverted')
ax.plot(np.linspace(0, dim, dim / 2), f.truth.x, label='truth')

left, bottom, width, height = [0.08, 0.53, 0.35, 0.35]
ax2 = fig.add_axes([left, bottom, width, height])
ax2.imshow(np.matrix(f.response).T, interpolation='nearest', origin='low',
           extent=[f.xlo, f.xhi, f.xlo, f.xhi], cmap='Reds')
ax2.yaxis.tick_right()
plt.title(r"$R(x_\mathrm{meas}|y_\mathrm{true})$")

ax.legend()
plt.savefig('invert.png')

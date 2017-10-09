from fold import fold, printdiana
import numpy as np
#printdiana()

import matplotlib.pyplot as plt

response1 = fold(20,-10.,10)
print response1.fold.x

def smear(xt):
    xeff = 0.3 + (1.0 - 0.3) / 20 * (xt + 10.0)
    x = np.random.rand()
    if x > xeff: return None
    xsmear = np.random.normal(-2.5, 0.2)
    return xt + xsmear

for i in np.random.normal(0.0, 5.0, 10000):
    x = smear(i)
    if x == None :
        response1.miss(i)
    else:
        response1.fill(x, i)

print response1.fold.x
plt.imshow(response1.fold.x.T, interpolation='nearest', origin='low',cmap="plasma")
plt.show()

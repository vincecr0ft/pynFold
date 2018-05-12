from pynfold import fold
import numpy as np
from matplotlib import pyplot as plt
import ROOT

f = fold.fold()


def smear(xt):
    xeff = 0.3 + (1.0 - 0.3) / 20. * (xt + 10.0)  # efficiency
    x = np.random.rand()
    if x > xeff: return None
    xsmear = np.random.normal(-2.5, 0.2)
    return xt + xsmear


f.set_response(10, -10, 10)

for i in xrange(100000):
    xt = ROOT.gRandom.BreitWigner(0.3, 2.5)
    x = smear(xt)
    if x != None:
        f.fill(x, xt)
    else:
        f.miss(xt)

print 'response is', f.response.x
print 'y ', f.measured.x
print 'x ', f.truth.x
# gauss = np.random.normal(0., 2., 100000)
f.data = f.measured.x
# print 'gauss is',gauss
# f.data, bins = np.histogram(gauss, bins=4)
print 'data is', f.data
# f.response = [[0.0, 0.013, 0.0, 0.0], [0.0, 0.6, 0.49, 0.0], [0.0, 0.0, 0.223, 0.69], [0.0, 0.0, 0.0, 0.186]]
f.data = np.linspace(1000, 5000, 10).tolist()
# f.response = [[0.1,0.0,0.0,0.0],[0.0,0.1,0.0,0.0],[0.0,0.0,0.1,0.0],[0.0,0.0,0.0,0.1]]

f.run()
trace = f.fbu.trace
print trace

plt.hist(trace[1], bins=200, alpha=0.85, normed=True)
plt.ylabel('probability')
plt.show()

"""
f.fbu.background = {'bckg1':[20,30],'bckg2':[10,10]}
f.fbu.backgroundsyst = {'bckg1':0.5,'bckg2':0.04} #50% normalization uncertainty for bckg1 and 4% normalization uncertainty for bckg2
f.fbu.objsyst = {
    'signal':{'syst1':[0.,0.03],'syst2':[0.,0.01]},
    'background':{
            'syst1':{'bckg1':[0.,0.],'bckg2':[0.1,0.1]},
            'syst2':{'bckg1':[0.,0.01],'bckg2':[0.,0.]}
    }
}

f.run()

unfolded_bin1 = f.fbu.trace[1]

bckg1 = f.fbu.nuisancestrace['bckg1']
plt.hexbin(bckg1,unfolded_bin1,cmap=plt.cm.YlOrRd)
plt.show()

from pynfold import Regularization as R
f.fbu.regularization = R.Regularization('Tikhonov',parameters=[{'refcurv':0.,'alpha':0.1}])
f.fbu.regularization = R.Regularization('Tikhonov',parameters=[{'refcurv':0.,'alpha':0.1},{'refcurv':0.2,'alpha':0.1}])

"""

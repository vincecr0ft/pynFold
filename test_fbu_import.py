from pynfold import pynFold
from matplotlib import pyplot as plt
f = pynFold.Fold()
f.data = [100,150]

f.response = [[0.08,0.02], [0.02,0.08]]
f.lower = [0,0]
f.upper = [3000, 3000]

f.run()
trace = f.trace
print trace

plt.hist(trace[1],bins=20, alpha=0.85, normed=True)
plt.ylabel('probability')
plt.show()

f.background = {'bckg1':[20,30],'bckg2':[10,10]}
f.backgroundsyst = {'bckg1':0.5,'bckg2':0.04} #50% normalization uncertainty for bckg1 and 4% normalization uncertainty for bckg2
f.objsyst = {
    'signal':{'syst1':[0.,0.03],'syst2':[0.,0.01]},
    'background':{
            'syst1':{'bckg1':[0.,0.],'bckg2':[0.1,0.1]},
            'syst2':{'bckg1':[0.,0.01],'bckg2':[0.,0.]}
    }
}

f.run()

unfolded_bin1 = f.trace[1]
bckg1 = f.nuisancestrace['bckg1']
plt.hexbin(bckg1,unfolded_bin1,cmap=plt.cm.YlOrRd)
plt.show()

from pynfold import Regularization as R
f.regularization = R.Regularization('Tikhonov',parameters=[{'refcurv':0.,'alpha':0.1}])
f.regularization = R.Regularization('Tikhonov',parameters=[{'refcurv':0.,'alpha':0.1},{'refcurv':0.2,'alpha':0.1}])


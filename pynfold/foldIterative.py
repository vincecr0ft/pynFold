from fold import fold
from histogram import OneHist
import numpy as np

class PynFoldIterative:
    def __init__(self, thisfold, measured, iterations = 4):
        if isinstance(thisfold, fold):
            self.fold = thisfold
        else:
            print "not a valid pynfold response!"
            pass
        try:
            self.measured = OneHist(measured)
        except:
            print "could not convert that measured histogram"
            pass
        self.iterations = iterations
        self.unfolded = False

    def unfold(self):
        meas = self.measured.x # the bin contents of the measured histograms
        M = self.measured.nbins# the number of bins to be predicted                                                                  
        mu = [meas.sum()/M for i in range(M)]
        p = [1./M for i in range(M)]
        R = self.fold.fold.x
        truth = self.fold.truth.x
        nt = self.fold.nt
        epsilons = [R[i,:].sum()/truth[i] for i in range(nt)]
        measured = self.measured.x
        for iteration in range(self.iterations):
            for i in range(M):    # which bin in the reco distribution
                sumoverj = 0.0
                for j in range(nt): #which bin in the true distribution
                    sumoverk = np.asarray([R[j,k]*p[k] for k in range(M)]).sum()
                    if sumoverk > 0: 
                        sumoverj += measured[j]*R[j,i]*p[i]/sumoverk
                    else: sumoverj += 0.0
                mu[i] = sumoverj/epsilons[i] if epsilons[i] > 0 else 0
            for j in range(M):                
                p[j] = mu[j]/np.asarray(mu).sum() if np.asarray(mu).sum() > 0 else 0.

            self.reco = mu     
            
    def reco_hist(self):
        if self.unfolded: return self.reco
        else:
            self.unfold()
            return self.reco
            

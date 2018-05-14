from discretefunctions import f1x
import numpy as np

class iterative:
    def __init__(self, thisfold, measured, iterations = 4):
        self.fold = thisfold
        try:
            self.measured = f1x(measured)
        except:
            print "could not convert that measured histogram"
            pass
        self.iterations = iterations
        self.unfolded = False

    def __call__(self):
        meas = self.measured.x # the bin contents of the measured histograms
        M = self.measured.npoints# the number of bins to be predicted
        mu = [meas.sum()/M for i in range(M)]
        p = [1./M for i in range(M)]
        R = np.matrix(self.fold.response)
        truth = self.fold.truth.x
        nt = self.fold.truth.x.size
        print 'R',R
        print 'truth', truth
        print 'nt', nt
        epsilons = [R[i,:].sum()/truth[i] for i in range(nt)]
        print 'epsilon', epsilons
        measured = self.measured.x
        for iteration in range(self.iterations):
            for i in range(M):    # which bin in the reco distribution
                sumoverj = 0.0
                for j in range(nt): #which bin in the true distribution
                    sumoverk = [R[j,k]*p[k] for k in range(M)]
                    sumoverk = sum(sumoverk)
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
            self.__call__()
            return self.reco
            
def divide_zeros(matrix, vector):
    return np.divide(matrix, vector[None, :], out=np.zeros_like(matrix), where = vector != 0)
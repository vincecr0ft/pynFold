import numpy as np
import logging
import sys
import traceback

from scipy.linalg import svd
from error_calculation import variance_of_matrix

class richardson_lucy:
    def __init__(self, A, data_hist, epsilons, iterations=4):
        self.A = np.asarray(A).T
        self.data = np.asarray(data_hist)
        self.epsilons = np.asarray(epsilons)
        self.iterations = iterations
        self.x_shape = A.shape[0]
        self.unfolded = False

    def __call__(self):
        mu = np.asarray([self.data.sum() / self.x_shape
                         for i in range(self.x_shape)], dtype=float)
        var = np.zeros(len(mu))
        for i in range(self.iterations):
            mu, var = self.evaluate_mus(mu, var)
        self.reco = mu
        self.var = var
        self.unfolded = True
        return self.reco, self.var

    def reco_hist(self):
        if self.unfolded:
            return self.reco
        else:
            self.__call__()
            return self.reco

    def evaluate_mus(self, mu, var):
        p = mu / mu.sum()
        new_mus = divide_zeros(
            (divide_zeros(
                (self.A * p),
                (self.A * p).sum(axis=1)[:, None]
            ) * self.data[:, None]).sum(axis=0),
            self.epsilons)
        var_here = np.square(variance_of_matrix(divide_zeros(self.A*p ,(self.A*p).sum(axis=1)[:,None]))) + np.square(var)
        return (new_mus, np.sqrt(var_here))

class TSVD:
    def __init__(self, A, data_hist, truncations=2):
        self.A = np.asarray(A)
        self.f = np.asarray(data_hist)
        self.truncations = int(truncations)
        self.unfolded = False
    def __call__(self):
        U, s, VT = svd(self.A)
        print 'origininal matrix', self.A
        Sigma = np.zeros((self.A.shape[0], self.A.shape[1]))
        Sigma[:self.A.shape[0], :self.A.shape[0]] = np.diag(s)
        if len(s) <= self.truncations:
            n_elements = 1
        else:
            n_elements = len(s) - self.truncations
        Sigma = Sigma[:, :n_elements]
        VT = VT[:n_elements, :]
        B = U.dot(Sigma.dot(VT))
        print 'truncated matrix', B
        #now that we have a truncated matrix we invert
        Bp_inv = np.linalg.pinv(B)

        try:
            mus = self.f * np.matrix(Bp_inv)
            mus = np.asarray(mus)[0]
            var = variance_of_matrix(B)
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
            logging.error(''.join(line for line in lines))
            logging.info('Solving for sparse matrix instead')
            from scipy.sparse.linalg import lsqr
            x = lsqr(B.T, self.f, calc_var = True)
            mus = x[0]
            var = x[-1]
        self.reco = mus
        self.var = var

        return mus, var

    def reco_hist(self):
        if self.unfolded:
            return self.reco
        else:
            self.__call__()
            return self.reco            
        
def divide_zeros(A, B):
    return np.divide(A, B, out=np.zeros_like(A), where=B != 0)

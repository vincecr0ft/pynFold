import numpy as np
import logging

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
            mu, var = self.evaluate_mus(mu)
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

    def evaluate_mus(self, mu):
        p = mu / mu.sum()
        return (divide_zeros(
            (divide_zeros(
                (self.A * p),
                (self.A * p).sum(axis=1)[:, None]
            ) * self.data[:, None]).sum(axis=0),
            self.epsilons),
            variance_of_matrix(divide_zeros((self.A*p),
                             (self.A*p).sum(axis=1)[:, None])))
        
def divide_zeros(A, B):
    return np.divide(A, B, out=np.zeros_like(A), where=B != 0)

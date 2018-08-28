import numpy as np
from scipy.sparse.linalg import lsqr
import logging


class tikonov:
    def __init__(self,
                 A, f, lam=0.5):
        self.A = np.matrix(A).T
        self.f = f
        self.lamda = lam
        logging.info('initialising damped least squares unfolding')

    def __call__(self):
        nominal_sum = lsqr(self.A, self.f)[0].sum()
        x = lsqr(self.A, self.f, damp=self.lamda, calc_var=True)
        mus = x[0] * (nominal_sum / x[0].sum())
        var = x[-1]
        return (mus, var)

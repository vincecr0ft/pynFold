import numpy as np
from scipy.sparse.linalg import lsqr
from error_calculation import variance_of_matrix

import logging
import sys
import traceback

class tikonov:
    def __init__(self,
                 A, f, lam=0.5):
        self.A = A
        self.f = f
        self.lamda = lam
        logging.info('initialising damped least squares unfolding')

    def __call__(self):
        logging.info('unfolding')
        nominal_sum = lsqr(self.A.T, self.f)[0].sum()
        x = lsqr(self.A.T, self.f, damp = self.lamda, calc_var = True)
        mus = x[0] * (nominal_sum / x[0].sum())
        var = x[-1]
        return (mus, var)

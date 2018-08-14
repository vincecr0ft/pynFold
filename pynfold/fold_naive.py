import numpy as np
from error_calculation import variance_of_matrix

import logging
import sys
import traceback

class inversion:
    def __init__(self,
                 A, f):
        self.A = A
        self.f = f

    def __call__(self):
        Ap_inv = np.linalg.pinv(self.A)
        mus  = self.f*Ap_inv
        mus = np.asarray(mus)[0]
        try:
            var = variance_of_matrix(self.A.T)
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
            logging.error(''.join(line for line in lines))
            logging.info('Solving for sparse matrix instead')
            from scipy.sparse.linalg import lsqr
            x = lsqr(self.A.T, self.f, calc_var = True)
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

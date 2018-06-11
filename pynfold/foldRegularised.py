from .discretefunctions import f1x
import numpy as np
from scipy.sparse.linalg import lsqr


class regularised:
    def __init__(self, response, measured, tau=.1):
        self.tau = tau
        self.response = np.matrix(response)
        try:
            self.measured = f1x(inputarray=measured)
        except Exception as e:
            print(e)
            print(type(measured))
            print("could not convert that measured histogram")
            pass
        self.unfolded = False

    def __call__(self):
        meas = np.asarray(self.measured.x)
        nominal_sum = lsqr(self.response, meas)[0].sum()
        solution = lsqr(self.response, meas, damp=self.tau, calc_var=True)
        self.reco = solution[0]*nominal_sum/solution[0].sum()
        self.var = solution[-1]
        self.unfolded = True

    def reco_hist(self):
        if self.unfolded:
            return self.reco
        else:
            self.__call__()
            return self.reco

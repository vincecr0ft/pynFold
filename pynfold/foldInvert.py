from .discretefunctions import f1x
import numpy as np
from scipy.sparse.linalg import lsqr


class invert:
    def __init__(self, response, measured):
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
        try:
            inverse = np.linalg.inv(self.response)
            self.reco = (inverse * meas.T).T
            self.cov = ABAT(inverse, measured.cov)
            self.var = np.diag(self.cov)
        except Exception as e:
            print(e)
            print('matrix not invertable')
            print('using least squares')
            solution = lsqr(self.response, meas, calc_var=True)
            self.reco = solution[0]
            self.var = solution[-1]
        self.unfolded = True

    def reco_hist(self):
        if self.unfolded:
            return self.reco
        else:
            self.__call__()
            return self.reco

    def ABAT(self, A, B):
        return np.multiply( A, np.multiply( B, A.T))

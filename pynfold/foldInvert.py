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
        except Exception as e:
            print(e)
            print('matrix not invertable')
            print('using least squares')
            self.reco = lsqr(self.response, meas)[0]
        self.unfolded = True

    def reco_hist(self):
        if self.unfolded:
            return self.reco
        else:
            self.__call__()
            return self.reco

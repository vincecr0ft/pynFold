from scipy.linalg import svd
from numpy.linalg import inv
import numpy as np
import logging

def variance_of_matrix(A):
    # -------------------------------- #
    # variance is diagonal of (A'A)^-1 #
    # From SVD:                        #
    #     A = U.S.V'                   #
    #     A'A = VSU'USV'               #
    # since S is diagonal and U is orth#
    #     A'A = VS^2V'                 #
    #    (A'A)^-1 = VS^-2V'            #
    # -------------------------------- #

    U, S, VT = svd(A)
    S2 = np.diag(S*S)
    V = VT.T
    try:
        covar = V.dot(inv(S2)).dot(VT)
    except:
        logging.info('singular value matrix det is 0')
        logging.info('using pseudo inverse for error')
        covar = V.dot(np.linalg.pinv(S2)).dot(VT)
    return np.diag(covar)

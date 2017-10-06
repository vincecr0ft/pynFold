from Histogram import OneHist

import ROOT
import numpy as np

testnphist = np.histogram([1,2,1],bins=[0,1,2,3])
print "testing np hist", OneHist(testnphist)

testnp = np.array([1,2,1])
print "testing np array", OneHist(testnp)

testhist = ROOT.TH1D("test","test",10,0,10)
print "testing root array",OneHist(testhist)

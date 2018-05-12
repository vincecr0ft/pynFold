from pynfold.fold import fold
import ROOT

r = fold(4,-10.,10)
def smear(xt):
  xeff = 0.3 + (1.0-0.3)/20*(xt+10.0)  #  efficiency                                                                                  
  x = ROOT.gRandom.Rndm()
  if x>xeff: return None
  xsmear = ROOT.gRandom.Gaus(-2.5,0.2)     #  bias and smear 
  return xt + xsmear

for i in xrange(100):
  xt = ROOT.gRandom.BreitWigner(0.3, 2.5)
  x = smear(xt)
  if x!=None:
    r.fill(x, xt)
  else:
    r.miss(xt)


print r.response.x

import numpy as np
m = np.matrix(r.response.x)
P = m / r.truth.x[None,:]

print m



print "################################"
print 'truth is', r.truth.x

print 'response is', m
print 'which gives', P

print 'measured is', r.measured.x
print "################################"


print 'truth times response should equal measured'
new_m = P*np.matrix(r.truth.x).T
print new_m.T

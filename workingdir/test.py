from histogram import OneHist

import ROOT
import numpy as np

print "################################# "
print "######### Test One Adding ####### "
print "################################# "

test = OneHist(np.asarray([1,2,2,3,3,3,4,4,5]),bins=[1,2,3,4,5,6])
print "trying to add histograms"
print "##################################"
print "this histogram is ",test.x

print "Trying One hist first"
nptest = OneHist(np.random.normal(0,3,20),bins=test.bins)
test.add(nptest)
print "did it work?",test.x

print "Now with array"
test = OneHist(np.asarray([1,2,2,3,3,3,4,4,5]),bins=[1,2,3,4,5,6])
nptest = [1,1,1,2,2]
test.add(nptest)
print "did it work?",test.x

print "Finally with ROOT"
test = OneHist(np.asarray([1,2,2,3,3,3,4,4,5]),bins=[1,2,3,4,5,6])
roottest = ROOT.TH1D("x","x",5,1,6)
for i in [1,1,1,2,2]:
    roottest.Fill(i)
test.add(roottest)
print "did it work?",test.x


print "################################# "
print "######### Test Two Filling ###### "
print "################################# "

test = OneHist(np.asarray([1,2,2,3,3,3,4,4,5]),bins=[1,2,3,4,5,6])
print "trying to fill histogram"
print "##################################"
print "this histogram is ",test.x

for i in [1,1,1,2,2]:
    test.fill(i)
print "did it work?",test.x

import numpy as np

class OneHist:
  def __init__(self, inputhist=None, xlo=0, xhi=10, nbins = 10, bins=None):
    if bins and isinstance(bins, list):
      self.nbins = len(bins) - 1
      self.bins = bins
      self.x = np.zeros(self.nbins)
    else:
      self.nbins = nbins
      self.bins = np.linspace(xlo, xhi, nbins+1)
      self.x = np.zeros(nbins)
      
    if inputhist is None:
      return

    if isinstance(inputhist, np.ndarray):
      self.loadNP(inputhist)
    elif isinstance(inputhist, tuple):
      if len(inputhist) == 2 and isinstance(inputhist[0], np.ndarray):
        self.loadNPhist(inputhist)
    else:
      self.loadROOT(inputhist)

  def loadNP(self, inputhist):
    ahist = np.histogram(inputhist)
    x, bins = ahist
    self.x = x
    self.bins = bins

  def loadNPhist(self, inputhist):
    x, bins = inputhist
    self.x = x
    self.bins = bins

  def loadROOT(self, inputhist):
    try:
      import ROOT
      try:
        if isinstance(inputhist, ROOT.TH1D):
          nbins = inputhist.GetNbinsX()
          self.nbins = nbins
          ax = inputhist.GetXaxis()
          bins = []
          contents = []
          for i in range(nbins+1):
            bins.append(ax.GetBinUpEdge())
            if i > 0:
              contents.append(inputhist.GetBinContent(i))
          self.bins = np.asarray(bins)
          self.x = np.asarray(contents)
      except: 
        print "not a root file"
        pass
    except:
      print "no ROOT version set up"
      pass

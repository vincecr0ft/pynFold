import numpy as np

class OneHist:
  def __init__(self, inputhist=None, xlo=0, xhi=10, nbins = 10, bins=None):

    if isinstance(bins, list) or isinstance(bins, np.ndarray):
      self.nbins = len(bins) - 1
      self.bins = np.asarray(bins)
      self.x = np.zeros(self.nbins)
    else:
      self.nbins = nbins
      self.bins = np.linspace(xlo, xhi, nbins+1)
      self.x = np.zeros(nbins, dtype=float)
      
    if inputhist is None:
      return

    if isinstance(inputhist, np.ndarray):
      self.loadNP(inputhist)
    elif isinstance(inputhist, tuple):
      if len(inputhist) == 2 and isinstance(inputhist[0], np.ndarray):
        self.loadNPhist(inputhist)
    else:
      self.loadROOT(inputhist)

    self.nevents = self.x.sum()

  def loadNP(self, inputhist):
    ahist = np.histogram(inputhist,bins=self.bins)
    x, bins = ahist
    self.x = np.asarray(x, dtype=float)
    

  def loadNPhist(self, inputhist):
    x, bins = inputhist
    self.x = np.asarray(x, dtype=float)
    self.bins = bins

  def loadROOT(self, inputhist):
    try: import ROOT
    except:
      print "no root version"
      pass
    
    if isinstance(inputhist, ROOT.TH1D):
      nbins = inputhist.GetNbinsX()
      self.nbins = nbins
      ax = inputhist.GetXaxis()
      bins = []
      contents = []
      for i in range(nbins+1):
        bins.append(ax.GetBinUpEdge(i))
        if i > 0:
          contents.append(inputhist.GetBinContent(i))
      self.bins = np.asarray(bins)
      self.x = np.asarray(contents, dtype=float)

  def fill(self, newevent):
    tmphist = np.histogram([newevent], self.bins)
    self.x += np.asarray(tmphist[0], dtype=float)

  def add(self, newhist):
    if isinstance(newhist, OneHist):
      if self.bins.all() == newhist.bins.all():
        self.x += newhist.x
      else:
        print "Histograms not the same size..."
    elif isinstance(newhist, tuple):
      if len(newhist) == 2 and isinstance(newhist[0], np.ndarray):
        self.x += newhist[0]
    elif isinstance(newhist, np.ndarray) or isinstance(newhist,list):
      self.x += np.histogram(newhist,self.bins)[0]
    else:
      try: import ROOT
      except:
        print "no root version"
        pass
      if isinstance(newhist, ROOT.TH1D):
        nbins = newhist.GetNbinsX()
        ax = newhist.GetXaxis()
        bins = []
        contents = []
        for i in range(1,nbins+1):
          contents.append(float(newhist.GetBinContent(i)))
        self.x += np.asarray(contents, dtype=float)

class TwoHist:
  def __init__(self, inputhist=None, xlo=0, xhi=10, nbins = 10, bins=None):
    if isinstance(bins, list) or isinstance(bins, np.ndarray):
      self.nbins = len(bins) - 1
      self.bins = np.asarray(bins)
      self.x = np.zeros((self.nbins,self.nbins), dtype=float)
    else:
      self.nbins = nbins
      self.bins = np.linspace(xlo, xhi, nbins+1)
      self.x = np.zeros((self.nbins,self.nbins), dtype=float)
      
    if inputhist is None:
      return

  def fill(self, xm, xt):
    tmphist = np.histogram2d([xm],[xt], (self.bins, self.bins))
    self.x += np.asarray(tmphist[0],dtype=float)


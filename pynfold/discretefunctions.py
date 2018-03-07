import numpy as np

class f1x:
  def __init__(self, inputarray=None, xlo=0, xhi=10, npoints = 10, points=None):

    if isinstance(points, list) or isinstance(points, np.ndarray):
      self.npoints = len(points) - 1
      self.points = np.asarray(points)
      self.x = np.zeros(self.npoints)
    else:
      self.npoints = npoints
      self.points = np.linspace(xlo, xhi, npoints+1)
      self.x = np.zeros(npoints, dtype=float)
      
    if inputarray is None:
      return

    if isinstance(inputarray, np.ndarray):
      self.loadNP(inputarray)
    elif isinstance(inputarray, tuple):
      if len(inputarray) == 2 and isinstance(inputarray[0], np.ndarray):
        self.loadNPhist(inputarray)
    else:
      self.loadROOT(inputarray)

    self.nevents = self.x.sum()

  def loadNP(self, inputarray):
    ahist = np.histogram(inputarray,bins=self.points)
    x, points = ahist
    self.x = np.asarray(x, dtype=float)
    

  def loadNPhist(self, inputarray):
    x, points = inputarray
    self.x = np.asarray(x, dtype=float)
    self.points = points

  def loadROOT(self, inputarray):
    try: import ROOT
    except:
      print "no root version"
      pass
    
    if isinstance(inputarray, ROOT.TH1D):
      npoints = inputarray.GetNbinsX()
      self.npoints = npoints
      ax = inputarray.GetXaxis()
      points = []
      contents = []
      for i in range(npoints+1):
        points.append(ax.GetBinUpEdge(i))
        if i > 0:
          contents.append(inputarray.GetBinContent(i))
      self.points = np.asarray(points)
      self.x = np.asarray(contents, dtype=float)

  def fill(self, newevent):
    tmphist = np.histogram([newevent], self.points)
    self.x += np.asarray(tmphist[0], dtype=float)

  def add(self, newfunc):
    if isinstance(newfunc, f1x):
      if self.points.all() == newfunc.points.all():
        self.x += newfunc.x
      else:
        print "functions not the same shape..."
    elif isinstance(newfunc, tuple):
      if len(newfunc) == 2 and isinstance(newfunc[0], np.ndarray):
        self.x += newfunc[0]
    elif isinstance(newfunc, np.ndarray) or isinstance(newfunc,list):
      self.x += np.histogram(newfunc,self.points)[0]
    else:
      try: import ROOT
      except:
        print "no root version"
        pass
      if isinstance(newfunc, ROOT.TH1D):
        npoints = newfunc.GetNpointsX()
        ax = newfunc.GetXaxis()
        points = []
        contents = []
        for i in range(1,npoints+1):
          contents.append(float(newfunc.GetBinContent(i)))
        self.x += np.asarray(contents, dtype=float)

class Axy:
  def __init__(self, inputarray=None, xlo=0, xhi=10, npoints = 10, points=None):
    if isinstance(points, list) or isinstance(points, np.ndarray):
      self.npoints = len(points) - 1
      self.points = np.asarray(points)
      self.x = np.zeros((self.npoints,self.npoints), dtype=float)
    else:
      self.npoints = npoints
      self.points = np.linspace(xlo, xhi, npoints+1)
      self.x = np.zeros((self.npoints,self.npoints), dtype=float)
      
    if inputarray is None:
      return

  def fill(self, xm, xt):
    tmphist = np.histogram2d([xm],[xt], (self.points, self.points))
    self.x += np.asarray(tmphist[0],dtype=float)


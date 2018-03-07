import numpy as np
from discretefunctions import f1x, Axy
from banner import printdiana
from foldFBU import fbu

class fold:
  def __init__(self, npoints = None, xlo = None, xhi = None, measured = None, truth = None, data = [], response= [], method = 'fbu'):
    self.response = response
    self.data = data
    if npoints and xlo and xhi:
      self.measured = f1x(npoints=npoints, xlo = xlo, xhi = xhi)
      self.truth = f1x(npoints=npoints, xlo = xlo, xhi = xhi)
      self.response = Axy(npoints=npoints, xlo = xlo, xhi = xhi)
    if 'fbu' in method.lower():
      upper = []
      lower = []
      for point in data:
        if point > 0:
          upper.append(int(point*100))
          lower.append(int(point*0.01))
        else:
          upper.append(100)
          lower.append(0)
      print 'data {}, response {}'.format(self.data, self.response)
      upper = [3000, 3000]
      lower = [0,0]
      self.run = fbu(data=data, lower=lower, upper=upper, response=self.response)


  def fill(self, xr, xt):
    if isinstance(xr,float) and isinstance(xt,float):
      self.measured.fill(xr)
      self.truth.fill(xt)
      self.response.fill(xr, xt)
  def miss(self, xt):
    self.truth.fill(xt)


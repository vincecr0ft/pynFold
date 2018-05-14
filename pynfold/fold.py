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
    self.FilledResponse = False

    self.method = method.lower()

  def run(self):
    if self.FilledResponse and not isinstance(self.response,list):
      response_hist = np.matrix(self.response.x, dtype= float)
      response_matrix =  np.divide(response_hist, self.truth.x[None,:], out=np.zeros_like(response_hist), where=self.truth.x != 0)
      self.response = response_matrix.tolist()

    if 'fbu' in self.method:
      upper = []
      lower = []  
      for point in self.data:
        if point > 0:
          upper.append(int(point*10))
          lower.append(0)
        else:
          upper.append(100)
          lower.append(0)
      print 'data {}, response {}'.format(self.data, self.response)
      upper = (np.ones(len(self.data))*3000).tolist()
      lower = (np.zeros(len(self.data))).tolist()

      self.fbu = fbu(data=self.data, lower=lower, upper=upper, response=self.response)
      self.fbu()


  def fill(self, xr, xt):
    self.FilledResponse = True
    if self.response is None or isinstance(self.response,list):
      print "response matrix parameters not set. please call set_response(n_points, x_low, x_high)"
    if isinstance(xr,float) and isinstance(xt,float):
      self.measured.fill(xr)
      self.truth.fill(xt)
      self.response.fill(xr, xt)
  def miss(self, xt):
    self.FilledResponse = True
    if self.response is None or isinstance(self.response,list):
      print "response matrix parameters not set. please call set_response(n_points, x_low, x_high)"
    self.truth.fill(xt)

  def set_response(self, npoints, xlo, xhi):
    # type: (int, float, float) -> (f1x, f1x, Axy)
    """
    :rtype: None
    """
    self.measured = f1x(npoints=npoints, xlo = xlo, xhi = xhi)
    self.truth = f1x(npoints=npoints, xlo = xlo, xhi = xhi)
    self.response = Axy(npoints=npoints, xlo = xlo, xhi = xhi)

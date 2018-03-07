import numpy as np
from histogram import f1x, Axy

class fold:
  def __init__(self, npoints = None, xlo = None, xhi = None, measured = None, truth = None):
    if npoints and xlo and xhi:
      self.measured = f1x(npoints=npoints, xlo = xlo, xhi = xhi)
      self.truth = f1x(npoints=npoints, xlo = xlo, xhi = xhi)
      self.fold = Axy(npoints=npoints, xlo = xlo, xhi = xhi)

  def fill(self, xr, xt):
    if isinstance(xr,float) and isinstance(xt,float):
      self.measured.fill(xr)
      self.truth.fill(xt)
      self.fold.fill(xr, xt)
  def miss(self, xt):
    self.truth.fill(xt)

def printdiana():
  print "MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM"
  print "MMddddddddhossydddh:://+shddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd"
  print "MMMMMMMMMNs...+NMMMddhys+::+ymMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM"
  print "MMMMMMMh+-+y+yMMMMMMMMMMMMNh+-/hNMMMMMMMMMMMMMMMMMMMMMNyyyMMMMNsoyMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMNdddMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM"
  print "MMMMMd/-omMMMMMMMMMMMMMMNmhhhhs:/dMMMMMMMMMMMMMMMMMMMMd...MMMMy..-dMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMmoooMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM"
  print "MMMMy-:+ssyhdNMMMMMMMMNhydNMMMMNo-oMMMMMMMMMMMMMMMMMMMd...MMMMMdhdMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMmoooMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM"
  print "MMMs.oMMMNmdyoohNMMMMdymMMMMMMMMMs.oMMMMMMMMMmyo+++oymd...MMMMd+++NMMMNmhso+++oydNMMMMN+++mmyo+++ohNMMMMMNdyo++++oymMMMMMMmoooMNdhyyyhmNMMMMMMNmhhyyyhdNMMMMMdyyhNmhyyyhdmNMM"
  print "MMd./MMMMMMMMMms/hMMhyNNmhhyyyyyhm/.hMMMMMMm/-.-:/+/--/...MMMMh...NMMMh--:/++/-../mMMMm.../--:::-..:hMMMM+.-:+++:-.-sMMMMMmoooyossssooosmMMMNhsoosyyysooyNMMMhooososyyssoosdM"
  print "MM+.ymmmmmNNNNNMm/smoyooshdmNNmmdyo./MMMMMm-../dNMMMNy-...MMMMh...NMMMMdmNMNNNm:..+MMMm...-ymNNNd:..-MMMMNhmMNNNNy...mMMMMmooosmNMMNmsoosMMMyooyNMMMMNdooyMMMhoooyNMMMMNdoood"
  print "MM:.mmmmddddddhhhssdy+dMMMMMMMMMMMM--MMMMMs..-NMMMMMMMs...MMMMh...NMMMmyo//////-../MMMm...hMMMMMMh...MMMMds+//////...dMMMMmoooNMMMMMMhoosMMmoooyyyyyyyyoooNMMhoosMMMMMMMMhoos"
  print "MM/.NMMMMMMMMMMMNohmdohdddmmmNNNNNN--MMMMMs..-NMMMMMMMs...MMMMh...NMMh-.-oyyyyy:../MMMm...dMMMMMMd...MMM+../syyyyy...dMMMMmoooMMMMMMMhoosMMmoooyhhhhhhhhhhNMMhoooNMMMMMMMhoos"
  print "MMs.odmNMMMMNmdyoooys/mNNmmmdddddds.+MMMMMN:../dNMMMmy-...MMMMh...NMMo../NMMMNd-../MMMm...dMMMMMMd...MMN-..hMMMMms...dMMMMmoooMMMMMMMhoosMMMyoosmNMMMMNdmMMMMhoooymNMMMNhoood"
  print "MMN:.sysossossydNdsNMy+yNMMMMMMMMN:-mMMMMMMm+-.-://:--/...MMMMh...NMMm/..:///:--../MMMm...dMMMMMMd...MMMy-.-://:--...dMMMMmoooMMMMMMMhoosMMMMdsoossyysooyNMMMhooosossssooosmM"
  print "MMMm-:dMMMMMMMMMdyNMMMNhooydNMMMm:-dMMMMMMMMMNhso+oshmmsssMMMMmsssNMMMNdso+osymyssyMMMNsssmMMMMMMNsssMMMMNhso+oshNsssmMMMMNhhhMMMMMMMmhhhMMMMMNmdhhhhhmNMMMMMhoosMNdhhhhdNMMM"
  print "MMMMm/-sNMMMMNdyhMMMMMMMMNdhsso:-/mMMMMMMMMMMMMMMMMMMMMMMMM Implemented in python by Vince Croft vincent.croft@cern.ch : New York Univerity             NNMMMhoosMMMMMMMMMMMM"
  print "MMMMMMh/-shhhhmNMMMMMMMMMMMMms::yNMMMMMMMMMMMMMMMMMMMMMMMMM fbu by Clement Helsens, Davide Gerbaudo, & Francesco Rubbo https://github.com/gerbaudo/fbu  MNMMMhoosMMMMMMMMMMMM"
  print "MMMMMMMMd+::ohmMMMMMMMMMmhs/:+hNMMMMMMMMMMMMMMMMMMMMMMMMMMM Based on RooUnfold hepunx.rl.ac.uk/~adye/software/unfold/RooUnfold.html written by Tim Ayde MMMMMNNNNMMMMMMMMMMMM"
  print "MMMMMMMMMMNds+/:://///:-/+sdNMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM"
  print "MMMMMMMMMMMMMMMMMNNNNNMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM"

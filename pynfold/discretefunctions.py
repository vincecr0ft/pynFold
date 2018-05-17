import numpy as np


class f1x:
    def __init__(self,
                 inputarray=None,
                 xlo=0, xhi=10,
                 npoints=10,
                 points=None):
        if points is None and inputarray is not None:
            npoints = len(inputarray)
            self.npoints = npoints
            self.points = np.linspace(0, npoints, npoints + 1)
        elif isinstance(points, list) or isinstance(points, np.ndarray):
            self.npoints = len(points) - 1
            self.points = np.asarray(points)
            self.x = np.zeros(self.npoints)
        else:
            self.npoints = npoints
            self.points = np.linspace(xlo, xhi, npoints + 1)
            self.x = np.zeros(npoints, dtype=float)

        if inputarray is None:
            return

        if isinstance(inputarray, np.ndarray):
            self.loadNP(inputarray)
        elif isinstance(inputarray, tuple):
            if len(inputarray) == 2 and isinstance(inputarray[0], np.ndarray):
                self.loadNPhist(inputarray)
        elif isinstance(inputarray, list):
            self.loadList(inputarray)
        else:
            self.loadROOT(inputarray)

        self.nevents = self.x.sum()

    def loadNP(self, inputarray):
        self.x = np.asarray(inputarray, dtype=float)

    def loadNPhist(self, inputarray):
        x, points = inputarray
        self.x = np.asarray(x, dtype=float)
        self.points = points

    def loadList(self, inputarray):
        self.x = np.asarray(inputarray, dtype=float)
        self.points = np.linspace(0, len(inputarray) + 1, len(inputarray) + 1)

    def loadROOT(self, inputarray):
        try:
            import ROOT
        except Exception as e:
            print(e)
            print("no root version")
            pass

        if isinstance(inputarray, ROOT.TH1D):
            npoints = inputarray.GetNbinsX()
            self.npoints = npoints
            ax = inputarray.GetXaxis()
            points = []
            contents = []
        for i in range(npoints + 1):
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
                print("functions not the same shape...")
        elif isinstance(newfunc, tuple):
            if len(newfunc) == 2 and isinstance(newfunc[0], np.ndarray):
                self.x += newfunc[0]
        elif isinstance(newfunc, np.ndarray) or isinstance(newfunc, list):
            self.x += np.histogram(newfunc, self.points)[0]
        else:
            try:
                import ROOT
            except Exception as e:
                print(e)
                print("no root version")
                pass
            if isinstance(newfunc, ROOT.TH1D):
                npoints = newfunc.GetNpointsX()
                contents = []
            for i in range(1, npoints + 1):
                contents.append(float(newfunc.GetBinContent(i)))
                self.x += np.asarray(contents, dtype=float)


class Axy:
    def __init__(self,
                 inputarray=None,
                 xlo=0, xhi=10,
                 npoints=10,
                 points=None):
        if isinstance(points, list) or isinstance(points, np.ndarray):
            self.npoints = len(points) - 1
            self.points = np.asarray(points)
            self.tpoints = np.linspace(self.points[0],
                                       self.points[-1],
                                       int(self.npoints / 2))
            self.x = np.zeros((self.npoints, int(self.npoints / 2)))
        else:
            self.npoints = npoints
            self.points = np.linspace(xlo, xhi, npoints + 1)
            self.tpoints = np.linspace(xlo, xhi, int(npoints / 2) + 1)
            self.x = np.zeros((self.npoints, int(self.npoints / 2)))
        if inputarray is None:
            return

    def fill(self, xm, xt):
        tmphist = np.histogram2d([xm], [xt], (self.points, self.tpoints))
        self.x += np.asarray(tmphist[0], dtype=float)

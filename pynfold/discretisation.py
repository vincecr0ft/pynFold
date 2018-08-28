import numpy as np

class MinimalFuncCode:
    def __init__(self, arg):
        self.co_varnames = tuple(arg)
        self.co_argcount = len(arg)

    def append(self, varname):
        tmp = list(self.co_varnames)
        tmp.append(varname)
        self.co_varnames = tuple(tmp)
        self.co_argcount = len(self.co_varnames)

class HistogramPdf(object):
    def __init__(self, binedges):
        self.hy = np.ones(len(binedges)-1)
        self.binedges = binedges
        varnames = ['bin{}'.format(i) for i in range(len(self.hy))]
        self.func_code = MinimalFuncCode(varnames)
        self.func_defaults = None

    def __call__(self, *arg):
        x = arg
        return self.hy * x

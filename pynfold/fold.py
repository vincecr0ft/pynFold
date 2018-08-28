import logging
import sys
import traceback

from response import response
from fold_naive import inversion
from fold_dimensionality import richardson_lucy, TSVD
from fold_composite import tikonov
import numpy as np


class fold:
    def __init__(self,
                 type=None,
                 response=None,
                 x_shape=None,
                 y_shape=None,
                 data=None,
                 data_hist=None,
                 data_bins=None):

        if x_shape is not None:
            if (isinstance(x_shape, tuple) and len(x_shape) == 3):
                self.set_x_shape(
                    xlow=x_shape[0],
                    xhi=x_shape[1],
                    n_points=x_shape[2])
            elif (isinstance(x_shape, list)
                  or isinstance(x_shape, np.ndarray)):
                self.set_x_shape(shape=x_shape)
            else:
                logging.error('x_shape should be either '
                              'tuple (xlo, xhi, n_npoints)\n'
                              'or a list or array of segments')
        if y_shape is not None:
            self.y_shape = self.set_y_shape(shape=y_shape)
        else:
            self.y_shape = None
        self.data = data
        if data_hist is not None and data_bins is not None:
            self.set_data_hist(data_hist, data_bins)
        else:
            self.data_hist = None

        self.method_type = None
        if type is None:
            logging.info('No unfolding method specified.'
                         u'Assume na\xfeve - matrix invert')
            self.type = 'naive'
        elif  (not isinstance(type, str)
               or not type.split(' ')[0].lower()
               in ['naive', 'dimensionality', 'composite']):
            message = ('Unfolding method not understood.\n'
                       '\nCurrent options are:\n'
                       u'    Na\xefve (naive) - '
                       'Matrix Inversion, Correction Factors\n'
                       '    Dimensionality - '
                       'Truncated SVD, Richardson-Lucy/D\'Agostini\n'
                       '    Composite - '
                       'Tikonov/damped LSQ, Fully Bayesian, RUN\n')
            logging.warning(message)
            logging.info('No unfolding method specified.'
                         u'Assume na\xefeve - matrix invert')
            self.type = 'naive'
        else:
            logging.info('setting type:{}'.format(type))
            self.type = type.split(' ')[0].strip(' ')
            if len(type.split(' ')) > 1:
                self.method_type = type.split(' ')[1].lower().strip()
                logging.info(
                    'A sub-type has been specified as:'
                    '{}'.format(self.method_type))

        if response is not None:
            try:
                self.set_response(response)
            except ValueError:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                lines = traceback.format_exception(
                    exc_type,
                    exc_value,
                    exc_traceback)
                logging.error(''.join(line for line in lines))
        else:
            self.response = None

    def set_response(self, inputarray):
        logging.info('setting response as an array of type:{}'.format(type(inputarray)))
        self.response = response(inputarray=inputarray)

    def set_response_matrix(self, matrix):
        logging.info('setting response as an matrix of type:{}'.format(type(matrix)))
        self.response = response(matrix=matrix)

    def set_response_function(self, function):
        if self.response is None:
            self.response = response(function=function)
        else:
            logging.error("Fold already has a response defined.")

    def fill(self, x, y):
        if self.response is None:
            logging.info('No response set, initialising')
            self.response = response()
        self.response.response = np.hstack([
                self.response.response,
                np.asarray([[x],[y]])])

    def miss(self, x):
        if self.response is None:
            logging.info('No response set, initialising')
            self.response = response()
        self.response.response = np.hstack(
            [self.response.response,
             np.asarray([[x],[None]])])

    def set_x_shape(self, **kwargs):
        if 'x_high' in kwargs:
            self.x_shape = np.linspace(
                kwargs['x_low'],
                kwargs['x_high'],
                kwargs['n_points'])
        elif 'shape' in kwargs:
            if (isinstance(kwargs['shape'], list)
                or isinstance(kwargs['shape'], np.ndarray)):
                self.x_shape = np.asarray(kwargs['shape'])
            else:
                logging.error('shape is a list or array of the bins or knots '
                              'in the desired distribution')

    def set_y_shape(self, **kwargs):
        if 'y_high' in kwargs:
            self.y_shape = np.linspace(
                kwargs['y_low'],
                kwargs['y_high'],
                kwargs['n_points'])
        elif 'shape' in kwargs:
            if (isinstance(kwargs['shape'], list)
                or isinstance(kwargs['shape'], np.ndarray)):
                self.y_shape = np.asarray(kwargs['shape'])
            else:
                logging.error('shape is a list or array of the bins or knots '
                              'in the desired distribution')

    def set_data_hist(self, hist, *args):
        if isinstance(hist, list) or isinstance(hist, np.ndarray):
            self.data_hist = hist
            self.n_data_points = sum(hist)
        else:
            logging.error('bin contents must be a list or np.array')

        if len(args) == 3:
            try:
                self.y_bins = np.linspace(args[0], args[1], args[2])
            except ValueError:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                lines = traceback.format_exception(
                    exc_type,
                    exc_value,
                    exc_traceback)
                logging.error(''.join(line for line in lines))
            self.n_y_bins = args[2]

            if self.y_shape is None:
                logging.info('setting y shape to that of the data hist')
            else:
                logging.info('resetting y shape to match the data hist')

            self.set_y_shape(shape=self.y_bins)

        elif (len(args) == 1 
              and (isinstance(args[0], list) 
                   or isinstance(args[0], np.ndarray)
                   )
              ):
            assert  (len(args[0]) == len(hist) + 1,
                     logging.error("those bins don't line up"
                                   "with the histogram"))
            self.y_bins = args[0]
            self.n_y_bins = len(args[0]) - 1

            if self.y_shape is None:
                logging.info('setting y shape to that of the data hist')
            else:
                logging.info('resetting y shape to match the data hist')
            self.set_y_shape(shape=args[0])
        else:
            logging.error('data hist is missing some keywords\n'
                          'shape=[],np.ndarray()\n'
                          'xlo=-10, xhi=10, n_points=11')

    def response_matrix(self):
        if self.x_shape is None or self.y_shape is None:
            logging.error('The response can\'t be defined without a shape')
        elif self.response.response_matrix is not None:
            return self.response.response_matrix
        elif (self.response.response.shape[1] == 0
              and self.response.func is None):
            logging.error('There\'s no response to put into a matrix')
        elif self.data_hist is not None:
            return self.response.create_response_matrix(
                self.x_shape,
                self.y_shape,
                self.n_data_points)
        else:
            return self.response.create_response_matrix(
                self.x_shape,
                self.y_shape)

    def bin_efficiency(self):
        if self.x_shape is None or self.y_shape is None:
            logging.error('The efficiency can\'t be defined without a shape')
        elif self.response.bin_efficiency is not None:
            return self.response.bin_efficiency
        elif (self.response.response.shape[1] == 0 
              and self.response.func is None 
              and self.response_matrix is None):
            logging.error('There\'s no response to find efficiencies for')
        else:
            return self.response.create_binned_efficiencies(
                self.x_shape,
                self.y_shape)

    def Unfold(self, *args):

        if 'nai' in self.type:
            self.method = inversion(self.response_matrix(), self.data_hist)
            return self.method()

        elif 'com' in self.type:
            if len(args) is 1:
                damping = args[0]
            else:
                damping = 0.5
            self.method = tikonov(
                self.response_matrix(),
                self.data_hist,
                damping)
            return self.method()

        elif 'dim' in self.type:
            logging.info('using dimensionality control method')
            if (self.method_type is not None 
                and self.method_type == 'tsvd'):
                if len(args) is 1:
                    truncations = args[0]
                else:
                    truncations = 1
                self.method = TSVD(
                    self.response_matrix(),
                    self.data_hist,
                    truncations)
                return self.method()
            elif self.method_type is None or self.method_type == 'rl':
                if len(args) is 1:
                    iterations = args[0]
                else:
                    iterations = 4
                self.method = richardson_lucy(
                    self.response_matrix(),
                    self.data_hist,
                    self.bin_efficiency(),
                    iterations)
                return self.method()
            else:
                logging.error('method not understood')
                logging.error('currently supported methods are:\n'
                              '    rl :'
                              'richardson-lucy, aka d\'agostini,'
                              'iterative or bayesian \n'
                              '    tsvd:'
                              'truncated singular value decomposition')
                logging.error('the current method is {}'.format(
                        self.method_type))
        else:
            logging.error('method {} not understood'.format(self.type))

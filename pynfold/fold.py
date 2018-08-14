import logging
import sys
import traceback

from response import response
from fold_naive import inversion
from fold_dimensionality import richardson_lucy
import numpy as np

class fold:

    def __init__(self,
                 type = None,
                 response = None,
                 x_shape = None,
                 y_shape = None,
                 data = None,
                 data_hist = None,
                 data_bins = None):
        self.x_shape = x_shape
        self.y_shape = y_shape
        self.data = data
        self.data_hist = data_hist
        self.y_bins = data_bins

        if type is None:
            logging.info(u'No unfolding method specified. Assume na\xfeve - matrix invert')
            self.type = 'naive'
        elif  not isinstance(type, str) or not type.lower() in ['naive', 'dimensionality', 'composite']:
            message = ('Unfolding method not understood.\n'
                       '\nCurrent options are:\n'
                       u'    Na\xefve (naive) - Matrix Inversion, Correction Factors\n'
                       '    Dimensionality - Truncated SVD, Richardson-Lucy/D\'Agostini\n'
                       '    Composite - Tikonov/damped LSQ, Fully Bayesian, RUN\n')
            logging.warning(message)
            logging.info(u'No unfolding method specified. Assume na\xefeve - matrix invert')
            self.type = 'naieve'
        else:
            logging.info('setting type:{}'.format(type))
            self.type = type

        if response is not None:
            try:
                self.set_response(response)
            except:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
                logging.error(''.join(line for line in lines))
        self.response = None

    def set_response(self, inputarray):
        logging.info('setting response as an array of type:{}'.format(type(inputarray)))
        self.response = response(inputarray = inputarray)

    def set_response_matrix(self, matrix):
        logging.info('setting response as an matrix of type:{}'.format(type(matrix)))
        self.response = response(matrix = matrix)

    def set_response_function(self, function):
        if self.response is None:
            self.response = response(function = function)
        else:
            logging.error("Fold already has a response defined.")

    def fill(self, x, y):
        if self.response is None:
            logging.info('No response set, initialising')
            self.response = response()
        self.response.response = np.hstack([self.response.response, np.asarray([[x],[y]])])        

    def miss(self, x):
        if self.response is None:
            logging.info('No response set, initialising')
            self.response = response()
        self.response.response = np.hstack([self.response.response, np.asarray([[x],[None]])])

    def set_x_shape(self, **kwargs):
        if 'x_high' in kwargs:
            self.x_shape = np.linspace(kwargs['x_low'], kwargs['x_high'], kwargs['n_points'])
        elif 'shape' in kwargs:
            if (isinstance(kwargs['shape'], list) or isinstance(kwargs['shape'], np.ndarray)):
                self.x_shape = np.asarray(kwargs['shape'])
            else:
                logging.error('shape is a list or array of the bins or knots'
                              'in the desired distribution')
    def set_y_shape(self, **kwargs):
        if 'y_high' in kwargs:
            self.y_shape = np.linspace(kwargs['y_low'], kwargs['y_high'], kwargs['n_points'])
        elif 'shape' in kwargs:
            if (isinstance(kwargs['shape'], list) or isinstance(kwargs['shape'], np.ndarray)):
                self.y_shape = np.asarray(kwargs['shape'])
            else:
                logging.error('shape is a list or array of the bins or knots'
                              'in the desired distribution')

    def set_data_hist(self, hist, *args):
        if isinstance(hist, list) or isinstance(hist, np.ndarray):
            self.data_hist = hist
            self.n_data_points = sum(hist)
        else:
            logging.error('bin contents must be a list or np.array')

        if len(args) == 3:
            try:
                self.y_bins = np.linspace(args[0],args[1],args[2])
            except:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
                logging.error(''.join(line for line in lines))
            self.n_y_bins = args[2]

            if self.y_shape is None:
                logging.info('setting y shape to that of the data hist')
            else:
                logging.info('resetting y shape to match the data hist')

            self.set_y_shape(shape=self.y_bins)

        elif len(args) == 1 and (isinstance(args[0], list) or isinstance(args[0], np.ndarray)):
            assert  len(args[0]) == len(hist) + 1, logging.error("those bins don't line up"
                                                                 "with the histogram")
            self.y_bins = args[0]
            self.n_y_bins = len(args[0]) - 1

            if self.y_shape is None:
                logging.info('setting y shape to that of the data hist')
            else:
                logging.info('resetting y shape to match the data hist')
            self.set_y_shape(shape=args[0])
        else: print 'type',type(args)
            
    def response_matrix(self):
        if self.x_shape is None or self.y_shape is None:
            logging.error('The response can\'t be defined without a shape')
        elif self.response.response_matrix is not None:
            return self.response.response_matrix
        elif self.response.response.shape[1] == 0 and self.response.func is None:
            logging.error('There\'s no response to put into a matrix')
        elif self.data_hist is not None:
            return self.response.create_response_matrix(self.x_shape, self.y_shape, self.n_data_points)
        else:
            return self.response.create_response_matrix(self.x_shape, self.y_shape)

    def bin_efficiency(self):
        if self.x_shape is None or self.y_shape is None:
            logging.error('The efficiency can\'t be defined without a shape')
        elif self.response.bin_efficiency is not None:
            return self.response.bin_efficiency
        elif self.response.response.shape[1] == 0 and self.response.func is None and self.response_matrix is None:
            logging.error('There\'s no response to find efficiencies for')
        else:
            return self.response.create_binned_efficiencies(self.x_shape, self.y_shape)

    def Unfold(self, *args):
        if self.type is 'naive':
            self.method = inversion(self.response_matrix(), self.data_hist)
            return self.method()
        elif self.type is 'dimensionality':
            if len(args) is 1:
                iterations = args[0]
            else:
                iterations = 4
            self.method = richardson_lucy(self.response_matrix(), self.data_hist, self.bin_efficiency(), iterations)
            return self.method()

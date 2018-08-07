import logging
import sys
import traceback
import numpy as np

class response:
    def __init__(self,
                 inputarray = None,
                 matrix = None,
                 function = None):

        self.response_matrix = matrix

        if inputarray is not None:
            if isinstance(inputarray, np.ndarray):
                if 2 in inputarray.shape and len(inputarray.shape) is 2:
                    if inputarray.shape[0] is not 2:
                        logging.info('assuming shape (2,n) so inverting')
                        self.response = np.swapaxes(inputarray, 0, 1)
                    else:
                        self.response = inputarray
                else:
                    logging.error('response should be a 2dim mapping true:measured')
            elif isinstance(inputarray, list):
                if (isinstance(inputarray[0], tuple) or isinstance(inputarray[0], list)) and len(inputarray[0]) == 2:
                    try:
                        self.response = np.swapaxes(np.asarray(inputarray),0,1)
                    except:
                        exc_type, exc_value, exc_traceback = sys.exc_info()
                        lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
                        logging.error(''.join(line for line in lines))
                else:
                    logging.error("response should be a 2dim mapping true:measured. Try numpy arrays or lists")

            else:
                logging.error("response should be a 2dim mapping true:measured. Try numpy arrays or lists")
        else:
            self.response = np.asarray([[],[]])

        if function is not None:
            logging.info('Function has been set.\n'
                         'Response will be generated when the ranges and'
                         'the number of events are specified.' )
            self.func = function
            if not self.test_func():
                logging.error("Function should return a float or None"
                              "to a dummy argument.")
        else:
            self.func = None

    def test_func(self):
        return (isinstance(self.func(10.), float) or self.func(10. is None))


    def create_response_matrix(self, bins_x, bins_y, n_data=0):
        if self.response_matrix is not None:
            logging.error("Response matrix already defined")
        if self.func is not None and self.response.shape[1] == 0:
            if n_data < 1:
                n_data = 10 * len(bins_y) * len(bins_x)
            x = np.random.uniform(bins_x[0], bins_x[-1], n_data)
            y = [self.func(i) for i in x]
            xy = np.asarray([x,y], dtype=float)
        else:
            xy = np.asarray(self.response, dtype=float)
        hits = xy[:,~np.any(np.isnan(xy), axis=0)] #Removing Nones (efficiency loss)
        response_hist,_,_ = np.histogram2d( hits[0,:], hits[1,:], bins=(bins_x, bins_y))
        response_hist = np.matrix(response_hist, dtype=float).T
        p_x,_ = np.histogram(xy[0,:], bins_x) # prob to find x anywhere in range
        self.response_matrix = np.divide(response_hist, p_x,
                                         out=np.zeros_like(response_hist),
                                         where=p_x!=0).T
        return self.response_matrix

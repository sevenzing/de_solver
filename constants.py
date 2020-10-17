import logging

APP_TITLE = 'ODE solver v1.0'
APP_SIZE = '1200x600' # in pixels
LOG_FORMAT = '%(levelname) -10s %(asctime)s %(name) -15s %(funcName) -10s: %(message)s'
UPDATE_BUTTON_NAME = 'Update'
RESIZE = True
LOG_LEVEL = logging.INFO

f = lambda x,y: 3 * y**(2/3)
def y_solution_getter(x_0, y_0):
    '''
    Since solution depends on constant C
    and constant depends on IVP, we need function 
    that returns function of solution
    '''
    def solution(x):
        '''
        Calculates the real solution according to IVP
        '''
        return (x + (y_0**(1/3) - x_0))**3
    
    return solution

INITIAL_VALUES = [
    2,      # x_0 
    1,      # y_0
    10,     # x_n
    50,     # number of iterations
    10,     # n_start
    100,    # n_end
    'y\' = 3y^(2/3)',
]
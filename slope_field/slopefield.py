"""
simpleplot_slope_field.py

Prototype for using simpleplot to sketch the direction field
of a separable ODE of the form dy/dx = f(x, y)

Fred Dupont

http://www.codeskulptor.org/#user41_awszdfG13G_3.py

"""

import math
import simpleplot

#DEG = 180.0 / math.pi
#RAD = math.pi / 180.0


def dydx(x, y):
    "evaluates the slope at point x, y"
    return y - 2 * x


def calculate_slopes():
    """
    builds a table (list of lists) of the slopes
    at chosen points on the interval
    """
    slopes_x_y = []
    for x in range(-10, 11, 1):
        res = []
        for y in range(-10, 11, 1):
            res.append(dydx(x, y))
        slopes_x_y.append(res)
    return slopes_x_y


def make_arrow(x0, y0, slope):
    """
    return the start and end points of a line of slope a
    centered on point x0, y0
    """
    amplitude = .65             # magnitude of the arrow
    alpha = math.atan(slope)    # slope in rad

    starts = [x0 - math.cos(alpha) * (amplitude / 2.),
             y0 - math.sin(alpha) * (amplitude / 2.)]
    ends   = [x0 + math.cos(alpha) * (amplitude / 2.),
             y0 + math.sin(alpha) * (amplitude / 2.)]

    return [starts, ends]


def make_arrows(seq):
    """
    builds a table of the arrows represented as start and end points
    ready to be plotted
    """
    arrows = []
    for x, slopes in enumerate(seq):
        for y, slope in enumerate(slopes):
            arrows.append(make_arrow(x - 10, y - 10, slope))

    return arrows


result = make_arrows(calculate_slopes())

title = "Slope Field for dy/dx = y - 2 * x"
simpleplot.plot_lines(title, 600, 600, "x", "y", result)



















"""
convexhull.py
Fred Dupont - 20160205

http://www.codeskulptor.org/#user41_ZtNL85ws0t_44.py
"""

import random
import simplegui

class Point2D:
    "represents points in 2D space"

    def __init__(self, x, y):
        self._x = x
        self._y = y

    def __eq__(self, autre):
        return self._x == autre._x and self._y == autre._y

    def __mul__(self, scalar):
        self._x = self._x * scalar
        self._y = self._y * scalar

    def __rmul__(self, scalar):
        __mul__(self, scalar)

    def __rmul__(self, scalar):
        return self.__mul__(scalar)

    def __str__(self):
        return "Point(%s, %s)" % (self._x, self._y)

    def get_x(self):
        return self._x

    def get_y(self):
        return self._y



class Point2DForHull(Point2D):

    def __mul__(self, scalar):
        self._x = self._x * scalar
        self._y = self._y * scalar

    def __rmul__(self, scalar):
        __mul__(self, scalar)

    #@classmethod
    def ccw(a, b, c):
        """
        determines if a->b->c is counter clock wise or not
        return 1  if counter clock (turn left)
        return -1 if clockwise     (turn right)
        return 0  if collinear     (no turn)
        """
        area_double = (b._x - a._x) * (c._y - a._y) - (b._y - a._y) * (c._x - a._x)
        if area_double > 0:
            return 1           # counter clock wise
        elif area_double < 0:
            return -1          # clock wise
        else:
            return 0           # collinear

    #@classmethod
    def y_order(this, autre):
        """
        checks if this point is lower on the y axis than autre
        returns 1 if this is lower
        returns -1 if autre is lower
        returns 0 if at the same level
        """
        lower = this._y - autre._y
        if lower > 0:
            return  1           # autre is lower than this
        elif lower < 0:
            return -1           # this is lower than autre
        else:
            return 0

    #@classmethod
    def x_order(this, that):
        """
        checks if this point is lower on the y axis than autre
        returns 1 if this is more to the right than that
        returns -1 if that is more to the right than this
        returns 0 if at the same level
        """
        more_to_the_righ = this._x - that._x
        if more_to_the_righ > 0:
            return 1           # this is more to the right than that
        elif more_to_the_righ < 0:
            return - 1         # that is more to the right than this
        else:
            return 0

    #@classmethod
    def polar_order(base, this, that):
        """
        self is the starting point; the bottom (right) most point
        checks the polar angle of autre wrt self

        sort by   - (x - base_x) / (y - base_y)
        where (base_x, base_y) are the coordinates of the base point.

        --> self must be the lowest y coordinates point

        returns 1  if  this angle > that angle
        returns -1 if  this angle < that angle
        returns 0  if  base, this and that are collinear
        """

        turn_left = Point2DForHull.ccw(this, base, that)

        if turn_left == 0: #collinear
#            print "THERE NOW", base, this, that
#            return turn_left
            if this == base:
#                print "THERE NOW", base, this, that
                return -1
            elif that == base:
#                print "THERE NOW", base, this, that
                return 1

            # vertically aligned--> lergest y
            elif this._x == that._x:
#                print "THERE NOW", base, this, that
                return Point2DForHull.y_order(this, that)

            # furthest away --> largest abs(x) has lowest angle
            #                   takes precedence in the convex hull
            elif (abs(this.get_x()) - abs(that.get_x())) > 0:
#                print "THERE NOW --- ", base, this, that
                return -1
            else:
#                print "THERE NOW", base, this, that
                return 1


        else:
#            print "here"
            return turn_left


        return Point2DForHull.ccw(this, base, that)


class CloudOfPoints:

    # find lowest y
    # sort by Polar Angle wrt point w lowest y

    # data structure so that add maintains order.
    # and lowest y is updated

    def __init__(self):
        self._points = []
        self._point_low_y = None
        self._renormalization_scalar = None

    def add_point(self, point):
        self._points.append(point)

    def set_base(self):
        """
        sets the base point as the lowest on the y axis, then the furthest on the right
        """
        for idx, point in enumerate(self._points):
            if self._point_low_y is None or self._point_low_y.get_y() > point.get_y():
                self._point_low_y = point
                self._points[0], self._points[idx] = self._points[idx], self._points[0]

            # points with same y, take the one at the rightmost x
            elif self._point_low_y.get_y() == point.get_y() and point.get_x() > self._point_low_y.get_x():
                self._point_low_y = point
                self._points[0], self._points[idx] = self._points[idx], self._points[0]

    def get_base(self):
        return self._point_low_y

    def sort_in_polar_order(self):
        self._points.sort(cmp = self._point_low_y.polar_order)
#        print self

    def normalize(self):
        "renormalizes the point cloud to values in ]-1, 1[ for x & y"
        ## attention precisiom of numerical values here
        self.find_xmax_ymax()
        points = [point * (1 / self._renormalization_scalar)
                 for point in self._points]
        self._points = self._points[:]

    def find_xmax_ymax(self):
        max_x = float("-inf")
        max_y = float("-inf")
        for point in self:
            if point.get_x() > max_x:
                max_x = point.get_x()
            if point.get_y() > max_y:
                max_y = point.get_y()
        self._renormalization_scalar = float(max(max_x, max_y))

    def get_renormalization(self):
        return self._renormalization_scalar

    def __iter__(self):
        for point in self._points:
            yield point

    def __str__(self):
        return "".join([str(point) + "\n" for point in self._points])


class ConvexHull(CloudOfPoints):
    """
    calculates the convex hull of a cloud of points
    """

    def __init__(self):
        CloudOfPoints.__init__(self)
        self._hull = []   # list used as a stack

    def pre_process(self):
        self.set_base()
        self.normalize()
        self.sort_in_polar_order()

    def calculate_convex_hull(self):
        """
        calculates the convex hull of a cloud of points
        using Graham Scan Algorithm
        """
        self.pre_process()
        self._hull.append(self._points[0])
        self._hull.append(self._points[1])

        for idx in range(2, len(self._points), 1):
            top = self._hull.pop()
            while Point2DForHull.ccw(self._hull[-1], top, self._points[idx]) < 0:
                top = self._hull.pop()
            self._hull.append(top)
            self._hull.append(self._points[idx])

        self._hull.append(self._points[0])

#        for elt in self._hull:
#            print elt

    def get_hull(self):
        return self._hull






class ConvexHullGUI:

    def __init__(self, cloud, width = 1000, height = 1000):
        self._cloud = cloud

        self._width = width
        self._height = height
        self._canvas_margin = 50
        self._setup_gui()

        self._hull = [self._extract_coord(point) for point in self._cloud.get_hull()]


        self._start()

    def _setup_gui(self):
        self._frame = simplegui.create_frame("Convex Hull", self._width, self._height)

        self._is_vis_axis = True
        self._but_axis = self._frame.add_button("Show Axis", self._show_axis)

        self._is_vis_polar_order = False
        self._but_polar_order = self._frame.add_button("Show Polar Order", self._show_polar_order)

        self._is_vis_convex_hull = False
        self._but_convex_hull = self._frame.add_button("Show Convex Hull", self._show_convex_hull)

        self._frame.add_label("")
        self._but_new_dataset = self._frame.add_button("Get New Dataset", self._get_new_dataset)

        self._frame.set_draw_handler(self._draw)


    def _extract_coord(self, point):
        "helper to extract coordinates from a point object"
        return self._place([point.get_x(), point.get_y()])

    def _place(self, coord, margin = True):
        """
        helper to translate coordonnees to the canvas
        margin = True  --> offset the graph from the edges
        margin = False --> no offset, draw up to the edge
        """
        if margin:
            return (coord[0] * (self._width - self._canvas_margin) // 2 + self._width // 2,
                    self._height // 2 - coord[1] * (self._height - self._canvas_margin) // 2)
        else:
            return (coord[0] * (self._width) // 2 + self._width // 2,
                    self._height // 2 - coord[1] * (self._height) // 2)

    def _draw(self, canvas):

        if self._is_vis_axis:
            self._draw_axis(canvas)

        # draw the cloud of points
        for point in self._cloud:
            canvas.draw_circle(self._extract_coord(point), 1, 1, "White")

        if self._is_vis_polar_order:
            for idx, point in enumerate(self._cloud):
                canvas.draw_line(self._extract_coord(self._cloud.get_base()), self._extract_coord(point), 1, "Cyan")
                canvas.draw_text(str(idx), self._extract_coord(point), 12, "Cyan")

        if self._is_vis_convex_hull:
            canvas.draw_polyline(self._hull, 3, "Red")





    def _draw_axis(self, canvas):
        """
        draws the x and y axis and the units
        """
        canvas.draw_line(self._place([1, 0], False), self._place([-1, 0], False), 1, "Yellow")
        canvas.draw_line(self._place([0, 1], False), self._place([0, -1], False), 1, "Yellow")
        for idx in range(-10, 11, 1):
            canvas.draw_line(self._place([idx / 10.0, -0.01]), self._place([idx / 10.0, 0.01]), 1, "Yellow")
            canvas.draw_text(str(idx / 10.0), self._place([(idx / 10.0) - 0.03, -0.03]), 12, "Yellow")
            canvas.draw_line(self._place([-0.01, idx / 10.0]), self._place([0.01, idx / 10.0]), 1, "Yellow")
            canvas.draw_text(str(idx / 10.0), self._place([-0.05, idx / 10.0]), 12, "Yellow")

    def _show_axis(self):
        "self._but_axis button handler"
        self._is_vis_axis = not self._is_vis_axis

    def _show_polar_order(self):
        "self._but_polar_order button handler"
        self._is_vis_polar_order = not self._is_vis_polar_order

    def _show_convex_hull(self):
        "self._but_convex_hull button handler"
        self._is_vis_convex_hull = not self._is_vis_convex_hull

    def _get_new_dataset(self):
        "self._but_new_dataset button handler"
        get_new_dataset()

    def _start(self):
        self._frame.start()


def get_new_dataset():
    points = ConvexHull()

    low, high = -1, 1
    num_points = random.randrange(10, 150)
    pts = [(random.random() * random.choice([low, high]), \
                random.random() * random.choice([low, high])) for _ in range(num_points)]
    points._points = [Point2DForHull(p[0], p[1]) for p in pts]
    points.calculate_convex_hull()

    ConvexHullGUI(points)



if __name__ == "__main__":

#    # test GUI
#    points = CloudOfPoints()
#    pts = [(random.random() * random.choice([-1, 1]), \
#            random.random() * random.choice([-1, 1])) for _ in range(10)]
#    points._points = [Point2DForHull(p[0], p[1]) for p in pts]
#    points.normalize()
#    points.set_base()
#    points.sort_in_polar_order()
#
#    ConvexHullGUI(points)


#    # test Convex Hull
#    h = ConvexHull()
#    pts = [(0, 3), (2, 7), (12, -12), (6, 14), (7, 2), (4, 3), (3, 0), (-3, 0), (0, -3), (-3, 6), (1, 6)]
#
#    for elt in pts:
#        h.add_point(Point2DForHull(*elt))
#
#
#    h.calculate_convex_hull()


#    points = ConvexHull()
#    pts = [(random.random() * random.choice([-1, 1]), \
#            random.random() * random.choice([-1, 1])) for _ in range(1000)]
#    points._points = [Point2DForHull(p[0], p[1]) for p in pts]
#    points.calculate_convex_hull()
#
#    ConvexHullGUI(points)



    get_new_dataset()













    print "test sort by polar_angle :"

    points = CloudOfPoints()
    pts = [(0, 3), (2, 7), (5, 1), (6, 4), (4, 3), (3, 0), (1, 1), (1, 6)]
    points._points = [Point2DForHull(p[0], p[1]) for p in pts]
    points.set_base()

#    print "low_y = ", points._point_low_y
#    print points
    points.sort_in_polar_order()
#    print
#    print points

    res = [(3, 0), (5, 1), (6, 4), (4, 3), (2, 7), (1, 6), (0, 3), (1, 1)]
    result = [Point2DForHull(*args) for args in res]
    verify = len(result) == len(points._points)
    for point_pair in zip(points._points, result):
        verify = verify and (point_pair[0].__eq__(point_pair[1]))
#        print point_pair[0], point_pair[1]
    print "  Simple case, no degenerates    -->  ", verify


    # test sort by polar_angle Degenerate cases
    # repeat values
    points = CloudOfPoints()
    pts = [(0, 3), (0, 5), (2, 5), (1, 1), (2, 7), (5, 1), (0, 5), (6, 4), (4, 3), (3, 0), (1, 1), (1, 6)]
    points._points = [Point2DForHull(p[0], p[1]) for p in pts]
    points.set_base()

#    print "low_y = ", points._point_low_y
#    print points
    points.sort_in_polar_order()
#    print
#    print points

    res = [(3, 0), (5, 1), (6, 4), (4, 3), (2, 7), (2, 5), (1, 6), (0, 5), (0, 5), (0, 3), (1, 1), (1, 1)]
    result = [Point2DForHull(*args) for args in res]
    verify = len(result) == len(points._points)
    for point_pair in zip(points._points, result):
        verify = verify and (point_pair[0].__eq__(point_pair[1]))
#        print point_pair[0], point_pair[1]
    print "  Degenerates - Repeat values    -->  ", verify


#    # collinear 1 --> with base point on x axis
    print "  Degenerates - Collinear"
    points = CloudOfPoints()
    pts = [(0, 3), (0, 5), (2, 5), (2, 0), (2, 7), (5, 1), (6, 4), (4, 3), (3, 0), (1, 1), (1, 6)]
    points._points = [Point2DForHull(p[0], p[1]) for p in pts]
    points.set_base()

#    print "low_y = ", points._point_low_y
#    print points
    points.sort_in_polar_order()
#    print
#    print points

    res = [(3, 0), (5, 1), (6, 4), (4, 3), (2, 7), (2, 5), (1, 6), (0, 5), (0, 3), (1, 1), (2, 0)]
    result = [Point2DForHull(*args) for args in res]
    verify = len(result) == len(points._points)
    for point_pair in zip(points._points, result):
        verify = verify and (point_pair[0].__eq__(point_pair[1]))
#        print point_pair[0], point_pair[1]
    print "    - on left of base point      -->  ", verify

#    # collinear 2 --> with base point on x axis
    points = CloudOfPoints()
    pts = [(0, 3), (0, 5), (2, 5), (2, 7), (5, 1), (6, 4), (4, 3), (3, 0), (1, 1), (1, 6)]
    points._points = [Point2DForHull(p[0], p[1]) for p in pts]
    points.set_base()

#    print "low_y = ", points._point_low_y
#    print points
    points.sort_in_polar_order()
#    print
#    print points

    res = [(3, 0), (5, 1), (6, 4), (4, 3), (2, 7), (2, 5), (1, 6), (0, 5), (0, 3), (1, 1)]
    result = [Point2DForHull(*args) for args in res]
    verify = len(result) == len(points._points)
    for point_pair in zip(points._points, result):
        verify = verify and (point_pair[0].__eq__(point_pair[1]))
#        print point_pair[0], point_pair[1]
    print "    - above base point           -->  ", verify


#    # collinear 3 --> neither horiz nor vertical
    points = CloudOfPoints()
    pts = [(0, 3), (2, 7), (5, 1), (6, 4), (7, 2), (4, 3), (3, 0), (1, 1), (-3, 6), (1, 6)]
    points._points = [Point2DForHull(p[0], p[1]) for p in pts]
    points.set_base()

#    print "low_y = ", points._point_low_y
#    print points
    points.sort_in_polar_order()
#    print
#    print points

    res = [(3, 0), (7, 2), (5, 1), (6, 4), (4, 3), (2, 7), (1, 6), (-3, 6), (0, 3), (1, 1)]
    result = [Point2DForHull(*args) for args in res]
    verify = len(result) == len(points._points)
    for point_pair in zip(points._points, result):
        verify = verify and (point_pair[0].__eq__(point_pair[1]))
#        print point_pair[0], point_pair[1]
    print "    - aligned with a +/- slope   -->  ", verify

    print "-----------------------------------------------------------"
    print

##########################################################################
    # test find_xmax_ymax
    points = CloudOfPoints()
    pts = [(0, 3), (2, 7), (12, -12), (6, 14), (7, 2), (4, 3), (3, 0), (1, 1), (-3, 6), (1, 6)]
    points._points = [Point2DForHull(p[0], p[1]) for p in pts]
    points.find_xmax_ymax()

##########################################################################


    def testing():
        print "test: ccw -----------------------------#"
        a = Point2DForHull(4, 0)
        b = Point2DForHull(5, 6)
        c = Point2DForHull(3, 2)
        print Point2DForHull.ccw(a, b, c)  #  1 --> ccw, turn left
        print Point2DForHull.ccw(a, c, b)  # -1 --> cw,  turn right

        a = Point2D(4, 0)
        b = Point2D(5, 6)
        c = Point2D(12, 2)
        print Point2DForHull.ccw(a, b, c)  # -1 --> cw,  turn right
        print Point2DForHull.ccw(a, c, b)  #  1 --> ccw, turn left

        a = Point2DForHull(4, 0)
        b = Point2DForHull(4, 6)
        c = Point2DForHull(4, 2)
        print Point2DForHull.ccw(a, b, c)  #  0 --> collinear on the same vertical

        print

        print "test y_order: -------------------------#"
        a = Point2DForHull(4, 0)
        b = Point2DForHull(4, 6)
        print Point2DForHull.y_order(a, b)  # a lower than b
        print Point2DForHull.y_order(b, a)  # b NOT lower than a
        print Point2DForHull.y_order(a, a)  # a at same y level as a

        print

        print "test x_order: -------------------------#"
        a = Point2DForHull(4, 6)
        b = Point2DForHull(-4, 0)
        print Point2DForHull.x_order(a, b)  # a more to the right than b
        print Point2DForHull.x_order(b, a)  # b NOT more to the tight than a
        print Point2DForHull.x_order(b, b)  # b at same x level than b

        print

        print "test polar_order: ---------------------#"
        print "==>> General cases:"
        base = Point2DForHull(4, -6)
        b = Point2DForHull(5, 6)
        c = Point2DForHull(3, 4)
        print base.polar_order(b, c)
        print base.polar_order(c, b)

        print "==>> Special cases:"
        print "  --> base is not the lowest point (y wise)"
        base = Point2DForHull(4, 0)
        b = Point2DForHull(-4, -6)
        c = Point2DForHull(-4, 2)
        try:
            print base.polar_order(b, c)
        except AssertionError:
            print "base must be lower than both this and that"
        try:
            print base.polar_order(c, b)
        except AssertionError:
            print "base must be lower than both this and that"

        c = Point2DForHull(-4, -2)
        try:
            print base.polar_order(b, b)
        except AssertionError:
            print "base must be lower than both this and that"
        try:
            print base.polar_order(c, b)
        except AssertionError:
            print "base must be lower than both this and that"

        print "\n####################################"
        print "#    cases not handled well yet    #"
        print "####################################"

        print "  --> vertically collinear = same x  <<== larger y is part of hull"
        base = Point2DForHull(4, -6)
        b = Point2DForHull(4, 6)
        c = Point2DForHull(4, 4)
        print base.polar_order(b, c)  # points are vertically collinear


        print "  --> all points at same y level:"
        base = Point2DForHull(4, -6)
        b = Point2DForHull(5, -6)
        c = Point2DForHull(3, -6)
        print "-------------------------------->  this---base---that"

        try:
            print base.polar_order(c, b)
        except ValueError:
            print "special case collinear points"

        print "-------------------------------->  that---base---this"
        try:
            print base.polar_order(b, c)
        except ValueError:
            print "special case collinear points"


        base = Point2DForHull(2, -6)
        b = Point2DForHull(3, -6)
        c = Point2DForHull(5, -6)
        print "-------------------------------->  base---this---that"
        try:
            print base.polar_order(b, c)
        except ValueError:
            print "special case collinear points"

        print "-------------------------------->  base---that---this"
        try:
            print base.polar_order(c, b)
        except ValueError:
            print "special case collinear points"

        base = Point2DForHull(10, -6)
        print "-------------------------------->  this---that---base"
        try:
            print base.polar_order(b, c)
        except ValueError:
            print "special case collinear points"

        print "-------------------------------->  that---this---base"
        try:
            print base.polar_order(c, b)
        except ValueError:
            print "special case collinear points"


    testing()

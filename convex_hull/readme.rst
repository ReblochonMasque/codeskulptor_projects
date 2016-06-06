Convex Hull
===========
Implements the visualization of a convex hull of a cloud of points

`convex hull <http://www.codeskulptor.org/#user41_ZtNL85ws0t_44.py>`_

codeskulptor implementation of python classes did not allow to override `__mul__` in the subclass of `Point`

.. image:: ./resources/convexhull.png

Sort for right angle is implemented using `cmp` operator:
.. code-block:: Python

    def sort_in_polar_order(self):
        self._points.sort(cmp = self._point_low_y.polar_order)


This could be replaced with something like this:

.. code-block:: Python

    import math
    import random
    pi = math.pi
    coords = [(1, 0),
              (1, 1),
              (2, 2),
              (0, 1),
              (-1, 1),
              (-1, 0),
              (-1, -1),
              (0, -1),
              (1, -1),
              ]
    for x, y in coords:
        print (x, y), math.atan2(y, x) % (pi*2), math.hypot(x, y)
    random.shuffle(coords)
    coords.sort(key=lambda x_y:
               (math.atan2(x_y[1], x_y[0]) % (pi*2), math.hypot(*x_y)))
    print coords

It would be fun to animate the GUI like in this `video <https://www.youtube.com/watch?v=p7RPHYzkJpU>`_


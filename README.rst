=====================
codeskulptor_projects
=====================

**A collections of experiments and python projects with codeskulptor**

Voronoi:
^^^^^^^^
A naive implementation of voronoi diagrams `<http://www.codeskulptor.org/#user41_fXerGg8nRY_2.py>`_

.. image:: ./voronoi/resources/Voronoi-Diagram-squares---offset-_-10---250-x-250.png

Convex Hull:
^^^^^^^^^^^^
A GUI/Canvas visualization of the convex hull of a cloud of points

.. image:: ./convex_hull/resources/convexhull.png

Observer pattern
^^^^^^^^^^^^^^^^
- `Publisher class <https://github.com/ReblochonMasque/codeskulptor_projects/blob/master/observer_pattern/observer.py>`_ --> elaborate/complex: various types of callbacks, different args and kwargs
- `Publisher class <https://github.com/ReblochonMasque/codeskulptor_projects/blob/master/observer_pattern/observersimple.py>`_ --> simple: one type of callback, one type of args 

MVC pattern for Rock Paper Scissors Lizard Spock
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Using the `observer.Publisher class <https://github.com/ReblochonMasque/codeskulptor_projects/blob/master/observer_pattern/observer.py>`_, implements a game of RPSLS with the observer pattern and outputs the outcome both in console and on a GUI canvas.

.. image:: ./RPSLS_MVC/resources/RPSLS_GUI.png

MVC pattern for Guess The Number Game
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Using the `observer.Publisher class <https://github.com/ReblochonMasque/codeskulptor_projects/blob/master/observer_pattern/observersimple.py>`_, implements a game of **Guess The Number** with the observer pattern and outputs the outcome both in console and on a GUI canvas.
The GUI provides hints on demand and shows an animated graphical representation of a binary search.

.. image:: ./Guess_The_Number_with_MVC_Pattern/resources/GTN_GUI.png
    :width: 400px
    :align: center
    :height: 300px
    :alt: GTN GUI screenshot

Slope Field
^^^^^^^^^^^

prototype that opens the possibility to enrich `simpleplot <http://www.codeskulptor.org/docs.html#tabs-Python>`_ 's limited capabilities.
It draws the slope field of a separable ordinary differential equation of the form: dy/dx=f(x,y)

It uses forward Euler integration to draw a set of solutions on the slope field

.. image:: ./slope_field/resources/Simpleplot-Slope-Field-with-solutions.png

"""
scalable_widgets.py
resizable - scalable - movable Widgets

Fred Dupont

last workable:
http://www.codeskulptor.org/#user41_gWz3nlsvxJ_15.py
"""

import simplegui
import random


class Widget:
    "a resizable widget displaying a ball in a box"

    _H_SIZE = 150
    _V_SIZE = 100
    _BB = [[0, _V_SIZE], [0, 0], [_H_SIZE, 0], [_H_SIZE, _V_SIZE]]

    def __init__(self, anchor, scale = 1):
        self._anchor = anchor
        self._scale = scale
        self._h_size = int(Widget._H_SIZE * self._scale)
        self._v_size = int(Widget._V_SIZE * self._scale)
        self._bounding_box = [corner[:] for corner in Widget._BB[:]]
        self._scale_bounding_box()

        self.view_bounding_box_and_anchor_point = False

    def _scale_bounding_box(self):

        self._left_border   = self._anchor[0]
        self._right_border  = self._anchor[0] + self._h_size
        self._bottom_border = self._anchor[1]
        self._top_border    = self._anchor[1] - self._v_size
        # 0 = bottom left
        self._bounding_box[0][0] = self._left_border
        self._bounding_box[0][1] = self._bottom_border
        # 1 = top left
        self._bounding_box[1][0] = self._left_border
        self._bounding_box[1][1] = self._top_border
        # 2 = top right
        self._bounding_box[2][0] = self._right_border
        self._bounding_box[2][1] = self._top_border
        # 3 = bottom right
        self._bounding_box[3][0] = self._right_border
        self._bounding_box[3][1] = self._bottom_border

    def draw(self, canvas):
        if self.view_bounding_box_and_anchor_point:
            self._draw_bb(canvas)

    def _draw_bb(self, canvas):
        canvas.draw_polygon(self._bounding_box, 1, "Grey")
        canvas.draw_circle(self._anchor, 3, 2, "Red", "Blue")

    def _scale_widget(self, object):
        return object * self._scale

    def update_anchor(self, new_anchor):
        self._anchor = new_anchor[:]
        self._scale_bounding_box()


class Ball:

    _RADIUS = 10
    _COLORS = ['Aqua', 'Black', 'Blue', 'Fuchsia', 'Gray', 'Green',
               'Lime', 'Maroon', 'Navy', 'Olive', 'Orange', 'Purple',
               'Red', 'Silver', 'Teal', 'White', 'Yellow']

    def __init__(self, scale):
        self._radius = Ball._RADIUS * scale
        self._pos = None
        self._vel = None
        self._colors = [random.choice(Ball._COLORS), random.choice(Ball._COLORS)]

    def set_pos(self, pos):
        self._pos = pos[:]

    def set_vel(self, vel):
        self._vel = vel[:]

    def get_pos(self):
        return self._pos

    def get_vel(self):
        return self._vel

    def get_radius(self):
        return self._radius

    def get_colors(self):
        return self._colors

    def update(self):
        if abs(self._vel[0]) > 6:
            self._vel[0] = 6 * abs(self._vel[0]) / self._vel[0]
        if abs(self._vel[1]) > 6:
            self._vel[1] = 6 * abs(self._vel[1]) / self._vel[1]
        self._pos[0] += self._vel[0]
        self._pos[1] += self._vel[1]

    def draw(self, canvas):
        canvas.draw_circle(self.get_pos(), self.get_radius(), 3, self.get_colors()[0], self.get_colors()[1])



class Bouncing_balls(Widget):

    velo = [-2, -1, 1, 2]

    def __init__(self, canvas_w, canvas_h, anchor, scale, num_balls = 1):
        Widget.__init__(self, anchor, scale)
        self._canvas_w = canvas_w
        self._canvas_h = canvas_h
        self._vel = [0, 0]

        self._num_balls = num_balls
        self._balls = []
        self._spawn_balls()

    def move_it(self):
        self._vel = [random.choice(Bouncing_balls.velo), random.choice(Bouncing_balls.velo)]

    def stop_it(self):
        self._vel = [0, 0]

    def _spawn_balls(self):
        for _ in range(self._num_balls):
            self.add_ball()

    def add_ball(self):
            ball = Ball(self._scale)
            ball.set_pos([random.randrange(self._left_border + ball.get_radius(),
                                           self._right_border - ball.get_radius()),
                          random.randrange(self._top_border + ball.get_radius(),
                                           self._bottom_border - ball.get_radius())])
            ball.set_vel([random.choice(Bouncing_balls.velo), random.choice(Bouncing_balls.velo)])
            self._balls.append(ball)

    def less_balls(self):
        if len(self._balls) > 0:
            self._balls.pop()

    def _update(self):

        if self._left_border <= 0 or self._right_border >= self._canvas_w:
            self._vel[0] *= -1
        if self._top_border <= 0 or self._bottom_border >= self._canvas_h:
            self._vel[1] *= -1

        self._anchor[0] += self._vel[0]
        self._anchor[1] += self._vel[1]
        self._scale_bounding_box()

        for ball in self._balls:
            pos = ball.get_pos()
            vel_x, vel_y = ball.get_vel()
            pos[0] += vel_x
            pos[1] += vel_y
            rad = ball.get_radius()

            if (pos[0] - rad) <= self._left_border or (pos[0] + rad) >= self._right_border:
                pos[0] -= vel_x
                vel_x = - vel_x + self._vel[0]
            if (pos[1] + rad) >= self._bottom_border or (pos[1] - rad) <= self._top_border:
                pos[1] -= vel_y
                vel_y = - vel_y + self._vel[1]
            ball.set_vel([vel_x, vel_y])
            ball.update()

    def draw(self, canvas):

        self._update()
        if self.view_bounding_box_and_anchor_point:
            self._draw_bb(canvas)
        for ball in self._balls:
            ball.draw(canvas)

    def show_hide_b_box(self):
        self.view_bounding_box_and_anchor_point = not self.view_bounding_box_and_anchor_point


class GUI:

    def __init__(self, width = 900, height = 900):
        self._width = width
        self._height = height
        self._widgets = []
        self._setup_gui()
        self._start()

    def _setup_gui(self):
        for _ in range(20):
            self._more_widgets()
        for widget in self._widgets:
            widget.move_it()

        self._frame = simplegui.create_frame("scalable and movable widgets", self._width, self._height, 50)
        self._frame.set_draw_handler(self._draw)
        self._frame.add_button("move it move it!", self._move_it, 45)
        self._frame.add_button("stop it stop it!", self._stop_it, 45)
        self._frame.add_button("more moar MOAR!", self._more_widgets, 45)
        self._frame.add_button("less now, LESS!", self._less_widgets, 45)
        self._frame.add_button("more moar BALLS!", self._more_balls, 45)
        self._frame.add_button("less LESS BALLS!", self._less_balls, 45)
        self._frame.add_button("show hide little secret!", self._show_hide_little_secret, 45)

    def _show_hide_little_secret(self):
        for widget in self._widgets:
            widget.show_hide_b_box()

    def _draw(self, canvas):
        for widget in self._widgets:
            widget.draw(canvas)

    def _more_balls(self):
        if len(self._widgets) > 0:
            random.choice(self._widgets).add_ball()

    def _less_balls(self):
        if len(self._widgets) > 0:
            random.choice(self._widgets).less_balls()

    def _move_it(self):
        for widget in self._widgets:
            widget.move_it()

    def _stop_it(self):
        for widget in self._widgets:
            widget.stop_it()

    def _less_widgets(self):
        random.shuffle(self._widgets)
        self._widgets.pop()

    def _more_widgets(self):
        scale = random.randrange(1, 15) / 10.
        self._widgets.append(Bouncing_balls(self._width, self._height,
                                                [random.randrange(0, self._width - int(Bouncing_balls._H_SIZE * scale)),
                                                 random.randrange(int(Bouncing_balls._V_SIZE * scale), self._height)],
                                 scale,
                                 random.randrange(1, 12)))

    def _start(self):
        self._frame.start()


GUI()
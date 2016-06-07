"""
guessthenumberMVC.py
Guess The Number,
An implementation of the Model View Controller (MVC)
and the Observer Design Patterns

http://www.codeskulptor.org/#user41_wVQMZrnQHg_31.py
"""

import math
import random
import simplegui


class Publisher:       # Observable
    """registers subscribers to notify"""

    def __init__(self):
        self._subscribers = dict()

    def register(self, subscriber, callback = None):
        self._subscribers[subscriber] = callback

    def unregister(self, subscriber):
        del self._subscribers[subscriber]

    def notify(self, args):
        for subscriber, callback in self._subscribers.items():
            if callback is None:
                subscriber.update(args)
            else:
                callback(args)


class ConsoleView:
    "outputs messages in the console"
    def update(self, messages):
        for message in messages:
            print message


class GUIView:
    "obtains input from user and outputs messages on the canvas"
    # deals with obtaining guesses
    # deals with changing game_range

    def __init__(self, range = 100, width = 800, height = 500):
        self._width, self._height = width, height
        self._range = 100

        self._guess_publisher = Publisher()
        self._range_publisher = Publisher()
        self._new_game_publisher = Publisher()

        self._setup_variables()
        self._setup_gui_elements()
        self._setup_control_elements()
        self._start()

    def _setup_variables(self):
        self._guess = None
        self._messages = []
        self._reset_cursor_pos()

    def _setup_gui_elements(self):
        self._frame = simplegui.create_frame("Guess The Number Game", self._width, self._height)
        self._frame.set_canvas_background('White')
        self._frame.set_draw_handler(self._draw)

    def _setup_control_elements(self):
        self._show_history = False
        self._input_box = self._frame.add_input("Input your best guess", self._input_guess, 100)
        self._frame.add_button("Range is [0,100)", self._range100)
        self._frame.add_button("Range is [0,1000)", self._range1000)
        self._history_button = self._frame.add_button("Turn History ON", self._toggle_history)

    def _draw(self, canvas):
        for message in self._messages:
            self._next_line()
            canvas.draw_text(message, self._cursor_pos, 14, "Black")
        self._reset_cursor_pos()

        if self._show_history:
            self._draw_history(canvas)

    def _draw_history(self, canvas):

        distance = 740 - 260

        color1 = "Green"
        color2 = "Red"

        #Line1
        start_1 = [260, 80]
        end_1 = [740, 80]

        canvas.draw_line(start_1, end_1, 20, "Red")
        canvas.draw_text(str(self._history[0][0]), (start_1[0] - 30, start_1[1] + 5), 16, "Black")
        canvas.draw_text(str(self._history[0][1]), (end_1[0] +10, end_1[1] + 5), 16, "Black")

        median = (self._history[-1][0] + self._history[-1][1]) / 2
        med_pos = [260 + median * distance / self._range, end_1[1] - 15]
        canvas.draw_text(str(median), med_pos, 16, "Black")

        #Line2
        down_by = 100
        start_2 = [260, 80 + down_by]
        end_2 = [740, 80 + down_by]

        canvas.draw_line(start_2, end_2, 20, "Green")
        canvas.draw_text(str(self._history[-1][0]), (start_2[0] - 30, start_2[1] + 5), 16, "Black")
        canvas.draw_text(str(self._history[-1][1]), (end_2[0] +10, end_2[1] + 5), 16, "Black")

        start_m = [260, 80]
        end_m = [740, 80]

        start_m[0] = 260 + self._history[-1][0] *distance / self._range
        end_m[0]   = 260 + self._history[-1][1] *distance / self._range
        canvas.draw_line(start_m, end_m, 20, "Green")

        to_left  = [260 + self._history[-1][0] * distance / self._range, 90]
        canvas.draw_line(to_left, (start_2[0], start_2[1] - 10), 2, "Green")
        to_right = [260 + self._history[-1][1] * distance / self._range, 90]
        canvas.draw_line(to_right, (end_2[0], end_2[1] - 10), 2, "Green")


    def _next_line(self):
        self._cursor_row += 12
        self._cursor_pos = [self._cursor_col, self._cursor_row]

    def _reset_cursor_pos(self):
        self._cursor_col, self._cursor_row = 10, 10
        self._cursor_pos = [self._cursor_col, self._cursor_row]

    def _input_guess(self, guess):
        self._guess = guess
        self._notify_guess()
        self._input_box.set_text("")

    def _notify_guess(self):
        self._guess_publisher.notify(self._guess)
        self._guess = None

    def _range100(self):
        self._range = 100
        self._reset()

    def _range1000(self):
        self._range = 1000
        self._reset()

    def reset(self):
        self._reset()

    def _reset(self):
        self._setup_variables()
        self._setup_gui_elements()
        self._setup_control_elements()
        self._start()

    def _notify_range(self):
        "alerts of a game_range change"
        self._range_publisher.notify(self._range)

    def update(self, message):
        for msg in message:
            self._messages.append(str(msg))
        #self._messages.append("")

    def receive_history(self, history):
        self._history = history[:]

    def _start(self):
        self._messages = []
        self._notify_range()
        self._frame.start()

    def _toggle_history(self):
        label = "Turn History ON" if self._show_history else "Turn History OFF"
        self._history_button.set_text(label)
        self._show_history = not self._show_history




class GuessTheNumberMVController:
    "runs the game and interfaces between model, console and GUI"

    def __init__(self):
        self._guesses = []
        self._guess = None
        self._current_nb_tries = 0
        self._setup_callbacks()
        self._history = []
        self._new_game()

    def _setup_callbacks(self):
        self._model = GuessTheNumber()
        self._console = ConsoleView()
        self._gui = GUIView()

        self._gui._guess_publisher.register(self, self.receive_guess)
        self._gui._range_publisher.register(self, self.receive_range)

        self._out_publisher = Publisher()
        self._out_publisher.register(self._console) #, self._console.update)
        self._out_publisher.register(self._gui    ) #, self._gui.update)

        self._gui._new_game_publisher.register(self, self.new_game)

        self._history_publisher = Publisher()
        self._history_publisher.register(self._gui, self._gui.receive_history)


    def receive_guess(self, guess):
        if guess.isdigit():
            self._guess = int(guess)
            message = "Guess was = " + str(guess)
            self._out_publisher.notify([message])
            self._handle_guess()

    def _handle_guess(self):

        self._current_nb_tries += 1
        max_guesses = self._model.get_max_tries()
        guesses_left = max_guesses - self._current_nb_tries

        messages = []
        message = "Number of remaining guesses is "
        message += str(guesses_left) + "/" + str(max_guesses)
        messages.append(message)


        if self._model.compare_to(self._guess) == 0:
            messages += ["you win!", "", ""]
            self._out_publisher.notify(messages)
            self._current_nb_tries = 0
            messages = []
            self._gui.reset()

        elif guesses_left == 0:
            messages += ["you ran out of guesses. The number was " + str(self._model.get_secret()), "", ""]
            self._out_publisher.notify(messages)
            self._current_nb_tries = 0
            messages = []
            self._gui.reset()

        elif self._model.compare_to(self._guess) < 0:
            self._history.append( (max(self._guess, self._history[-1][0]), self._history[-1][1] ) )
            messages.append("Higher")

        elif self._model.compare_to(self._guess) > 0:
            self._history.append( (self._history[-1][0], min(self._guess, self._history[-1][1] ) ) )
            messages.append("Lower")


        messages.append("")
        self._out_publisher.notify(messages)
        self._publish_history()

    def _publish_history(self):
        self._history_publisher.notify(self._history)

    def receive_range(self, range):
        self._model.set_range(range)
        self._new_game()

    def _get_remaining_guesses(self):
        return self._model.get_max_tries() - self._current_nb_tries

    def new_game(self, args):
        self._new_game()

    def _new_game(self):
        self._history = [(0, self._model.get_range())]
        self._publish_history()
        self._current_nb_tries = 0
        messages = []
        message = "New game. Range is from [0 to " + str(self._model.get_range()) + ")"
        messages.append(message)
        message = "Number of remaining guesses is " + str(self._get_remaining_guesses())
        messages.append(message)
        messages.append("")
        self._out_publisher.notify(messages)


class GuessTheNumber:
    "The model - holds the game logic"

    def __init__(self, guess_range = 100):
        self._guess_range = guess_range
        self._secret_number = None
        self._set_secret_number()

    def _set_secret_number(self):
        "generates a secret number within the defined range"
        self._secret_number = random.randrange(1, self._guess_range)

    def get_secret(self):
        return self._secret_number

    def set_range(self, range):
        "resets the guess_range to range and generates a new secret number"
        self._guess_range = range
        self._set_secret_number()

    def get_range(self):
        "returns the range of the current game"
        return self._guess_range

    def get_max_tries(self):
        "return the max tries allowed for self.range"
        return int(math.ceil(math.log(self._guess_range, 2)))

    def compare_to(self, guess):
        """
        compares guess with _secret_number
            return -1 ( < 0) if guess is lower
            return  1 ( > 0) if guess is higher
            return  0 ( == ) if guess is correct
        """
        return guess - self._secret_number



GuessTheNumberMVController()




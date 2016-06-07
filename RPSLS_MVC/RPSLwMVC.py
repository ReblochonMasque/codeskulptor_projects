"""
RPSLwMVC.py
game of  Rock-paper-scissors-lizard-Spock
implements Listener Pattern
implements Model View Controller Pattern
Author = Fred Dupont
Date   = 2016 01 29
http://www.codeskulptor.org/#user41_JYCjTQ4qS5_12.py

"""

__version__ = "00.01.02"

import user41_EScALr9fig4uDf8_4 as pub
import random
import simplegui


class RPSLSController:
    """
    manages a RSPSL game, what objects need the output,
    creates and broadcasts the output
    """

    #@classvariables
    winner = {0 : "Player and computer tie!",
              1 : "Player wins!",
              2 : "Player wins!",
              3 : "Computer wins!",
              4 : "Computer wins!"}

    tie = ""
    explain = {(2, 4) : "Scissors cuts paper",
               (0, 2) : "Paper covers rock",
               (0, 3) : "Rock crushes lizard",
               (1, 3) : "Lizard poisons Spock",
               (1, 4) : "Spock smashes scissors",
               (3, 4) : "Scissors decapitate lizard",
               (2, 3) : "Lizard eats paper",
               (1, 2) : "Paper disproves Spock",
               (0, 1) : "Spock vaporizes rock",
               (0, 4) : "Rock crushes scissors",
               (0, 0):tie, (1, 1):tie, (2, 2):tie, (3, 3):tie, (4, 4):tie,
               5 : "beats "}

    def __init__(self):

        self._setup_values()
        self._model = ModelRPSLS()
        self._console = ConsoleOutput()
        self._event_publisher = pub.Publisher(["output console"])
        self._gui = RSPSLgui(self._event_publisher)

        self._setup_out_callbacks()
        self._setup_in_callbacks()

    def _setup_out_callbacks(self):
        "registers events that will notify listeners"
        self._event_publisher.register("output_console", self._console, self._console.output)
        self._event_publisher.register("output_gui",     self._gui,     self._gui.get_winner_notice)
        self._event_publisher.register("left_bet",       self._gui,     self._gui.get_left_bet)
        self._event_publisher.register("right_bet",      self._gui,     self._gui.get_right_bet)
        self._event_publisher.register("winner",         self._gui,     self._gui.get_winner_notice)

    def _setup_in_callbacks(self):
        "registers events to listen to"
        self._gui.listener.register("gui_bet", self, self.get_autre_bet)

    def _setup_values(self):
        ""
        self._model_bet = None
        self._autre_bet = None
        self._winner = ""
        self._why    = ""

    def get_autre_bet(self, autre_bet):
        "receives a bet from outside - here, only the self._gui"
        self._autre_bet = autre_bet
        self._manage_bets()

    def _manage_bets(self):
        """
        Enters here once a player bet has been received
        --> obtains a model bet
        --> checks for a winner
        --> broadcasts the messages
        """
        self._get_model_bet()
        self._winner = RPSLSController.winner[self._model.compare_bets(self._autre_bet)]
        self._get_explanation()
        self._send_notices()
        self._setup_values()

    def _send_notices(self):
        "finalize & dispatches the events to Publisher to alert listeners"
        self._event_publisher.dispatch("left_bet", self._autre_bet)
        self._event_publisher.dispatch("right_bet", self._model_bet)
        self._event_publisher.dispatch("winner", (self._winner, self._why))

        self._event_publisher.dispatch("output_console", "Player bet is " + self._autre_bet)
        self._event_publisher.dispatch("output_console", "computer bet is " + self._model_bet)
        self._event_publisher.dispatch("output_console", self._winner + self._why + "\n")

    def _get_explanation(self):
        "helper method to build the explanation for a win"
        player_number   = self._model.name_to_number(self._autre_bet)
        computer_number = self._model.name_to_number(self._model_bet)
        explanation = (min(player_number, computer_number), max(player_number, computer_number)) \
                      if player_number != 5 else player_number
        why = RPSLSController.explain[explanation]
        why = num_to_object[computer_number] + " " + why + player_choice if why == "beats " else why
        why = " Because " + why if why != "" else why
        self._why = why

    def _get_model_bet(self):
        "obtains the betfrom the model"
        self._model_bet = self._model.get_bet()

class RSPSLgui:
    """
    Responsible for rendering events on the canvas and obtaining bets from the player
    """

    def __init__(self, listener):
        self.listener = listener
        self._width, self._height = 350, 300
        self._left_bet = None   # autre player
        self._right_bet = None  # model player
        self._winner_notice1 = ""
        self._winner_notice2 = ""

        self._setup_frame()
        self._setup_controls()
        self._start()

    def _setup_frame(self):
        self._frame = simplegui.create_frame("Rock Paper Scissors Lizard Spock",
                                              self._width, self._height, 75)
        self._frame.set_draw_handler(self._draw)

    def _setup_controls(self):
        self._rock_button     = self._frame.add_button("rock",     self._rock,     60)
        self._paper_button    = self._frame.add_button("paper",    self._paper,    60)
        self._scissors_button = self._frame.add_button("scissors", self._scissors, 60)
        self._lizard_button   = self._frame.add_button("lizard",   self._lizard,   60)
        self._spock_button    = self._frame.add_button("Spock",    self._spock,    60)

    def _rock(self):
        "_rock_button handler"
        self.notify_bet("rock")

    def _paper(self):
        "_paper_button"
        self.notify_bet("paper")

    def _scissors(self):
        "_scissors_button handler"
        self.notify_bet("scissors")

    def _lizard(self):
        "_lizard_button handler"
        self.notify_bet("lizard")

    def _spock(self):
        "_spock_button handler"
        self.notify_bet("Spock")

    def _reset_winner_notices(self):
        self._winner_notice1 = ""
        self._winner_notice2 = ""

    def _start(self):
        self._frame.start()

    def get_left_bet(self, bet):
        "obtain the player bet"
        self._left_bet = bet

    def get_right_bet(self, bet):
        "obtain the computer bet"
        self._right_bet = bet

    def get_winner_notice(self, args):
        "obtain notice of the winner"
        self._winner_notice1, self._winner_notice2 = args

    def notify_bet(self, event):
        "broadcasts a bet event"
        self.listener.dispatch("gui_bet", event)

    def _draw(self, canvas):
        canvas.draw_text("Player Bet", (30, 50), 20, "Cyan")
        canvas.draw_text("Computer Bet", (150, 50), 20, "Green")

        if self._left_bet is None:
            self._left_bet = "None"
        canvas.draw_text(self._left_bet, (40, 90), 20, "Cyan")
        if self._right_bet is None:
            self._right_bet = "None"
        canvas.draw_text(self._right_bet, (170, 90), 20, "Green")

        if self._winner_notice1 != "":
            self._draw_winner(canvas)

    def _draw_winner(self, canvas):
        "helper to draw winner on canvas"
        canvas.draw_text(self._winner_notice1, (20, 150), 30, "Cyan")
        canvas.draw_text(self._winner_notice2, (50, 180), 14, "Cyan")


class ConsoleOutput:
    """Responsible for rendering events on the console"""

    def output(self, message):
        print message


class ModelRPSLS:
    "the model - generates all RPSLS data"

    #@classvariables
    num_to_object = {0 : "rock", 1 : "Spock", 2 : "paper", 3 : "lizard", 4 : "scissors"}
    object_to_num = dict((v, k) for k, v in num_to_object.items())

    def __init__(self):
        self._range = 5
        self._bet = None

    def _make_bet(self):
        return random.randrange(0, self._range)

    def get_bet(self):
        "returns a string representing the Model bet"
        self._bet = self._make_bet()
        return self.number_to_name(self._bet)

    def compare_bets(self, autre):
        "calculates who wins - returns an int"
        "0 = tie, (1, 2) = autre wins, (3, 4 & >) = self wins"
        return (self.name_to_number(autre) - self._bet) % 5

    #@classmethod
    def name_to_number(self, name):
        "returns the number corresponding to name"
        return ModelRPSLS.object_to_num[name]

    #@classmethos
    def number_to_name(self, number):
        "returns the name corresponding to number"
        return ModelRPSLS.num_to_object[number]


controller = RPSLSController()


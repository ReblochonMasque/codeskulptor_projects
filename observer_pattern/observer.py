"""
observer.py
Observer Pattern Implementation

Fred Dupont - 2016 01-28

subscribers can register to be notified of several types of events
and use a variety of receiving methods
Events are strings

http://www.codeskulptor.org/#user41_EScALr9fig4uDf8_4.py
"""

__version__ = "0.0.1"


class Publisher:
    """
    Subscribers can register events and callback methods
    matches events types with callbacks
    """

    def __init__(self, events):
        self._events = set(events)
        self._subscribers = dict((event, dict()) for event in events)

    def _get_subscribers(self, event):
        "returns the dictionary of callbacks associated with this event"
        try:
            return self._subscribers[event]
        except KeyError:
            self._add_event(event)
            return self._subscribers[event]

    def register(self, event, who, callback = None):
        """
        registers an event, subscriber & callback
        default callback = update()
        """
        if callback is None:
            callback = getattr(who, 'update')
        self._get_subscribers(event)[who] = callback

    def unregister(self, event, who):
        "removes a subscriber for a given event"
        try:
            del self._get_subscribers(event)[who]
        except KeyError:
            pass

    def _add_event(self, event):
        "adds an event to the set of events"
        if event not in self._events:
            self._events.add(event)
            self._subscribers[event] = dict()

    def dispatch(self, event, args):
        "calls all registered subscribers for this event"
        #print "\nnotify", event
        for who, callback in self._get_subscribers(event).items():
            callback(args)



if __name__ == "__main__":
    "Testing code"

    class __Sub1:
        """
        has an update method
        responds to event "lunch"
        """
        def update(self, message):
            print "updating Sub1:", message


    class __Sub2:
        """
        doesn't have an update method
        responds to event "lunch"
        responds to event "dinner"
        """

        def go_have_lunch(self, message):
            print "having lunch:", message

        def go_have_dinner(self, message):
            print "having dinner:", message

        def go_to_bed(self, the_time):
            if the_time > 20:
                print "going to bed at", the_time, "heures"


    pub = Publisher(["lunch", "dinner"])
    sub1 = __Sub1()
    sub2 = __Sub2()

    pub.register("lunch", sub1)
    pub.register("lunch", sub2, sub2.go_have_lunch)
    pub.register("dinner", sub2, sub2.go_have_dinner)
    pub.dispatch("lunch", "lunch is ready")
    pub.dispatch("dinner", "dinner is served")
    print
    pub.unregister("lunch", sub2)
    pub.dispatch("lunch", "lunch is ready")
    pub.dispatch("dinner", "dinner is served")

    pub.unregister("lunch", sub2)

    pub.register("bed_time", sub2, sub2.go_to_bed)
    pub.dispatch("bed_time", 21)





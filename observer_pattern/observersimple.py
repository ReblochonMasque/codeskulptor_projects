"""
observersimple.py
An implementation of the Observer Design Patterns

http://www.codeskulptor.org/#user41_SDGV3w1Qcj_1.py
"""


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


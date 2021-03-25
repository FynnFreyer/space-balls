from api.communication.events import Event


class CollisionEvent(Event):
    def __init__(self, source: object):
        self.source = source

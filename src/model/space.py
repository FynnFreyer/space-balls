import pyglet

from api.communication.events import EventSource
from api.communication.events import EventHandler

from typing import List
from model.body import Body

class Space(EventSource):
    def __init__(self, dimensions=(-1, -1)):
        self.bodies = list()  # type: List[Body]
        self.handlers = list()  # type: List[EventHandler]
        self.dimensions = dimensions

    def add_body(self, kind=Body, *args, **kwargs):
        body = kind(*args, **kwargs, space=self)
        self.bodies.append(body)
        return body

    def add_many(self, bodies: List[Body]):
        self.bodies.extend(bodies)

    def update(self, dt):
        for body in self.bodies:
            body.checkbounds(*self.dimensions, strategy=body.wrap)
            body.update(dt)

    def on_event(self, event):
        for handler in self.handlers:
            handler.handle(event)


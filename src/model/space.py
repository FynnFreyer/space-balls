import pyglet

from api.communication.events import EventSource
from api.communication.events import EventHandler

from typing import List, Tuple, Mapping


from model.body import Body


class Space(EventSource):
    def __init__(self, dimensions: Tuple[int, int] = (-1, -1), drag: float = 0, gravity: float = 0):
        self.bodies = list()  # type: List[Body]
        self.handlers = list()  # type: List[EventHandler]
        self.dimensions = dimensions
        self.drag = drag
        self.gravity = gravity
        self.gravity_mapping = {}  # type: Mapping[Body, List[Body]]

    def add_body(self, kind=None, *args, **kwargs):
        if kind is None:
            raise TypeError('Needs a kind')
        body = kind(*args, **kwargs, space=self)
        self.bodies.append(body)
        return body

    def add_many(self, bodies):
        self.bodies.extend(bodies)

    def update(self, dt):
        for body in self.bodies:
            body.checkbounds(*self.dimensions, strategy=body.wrap)
            body.update(dt)

    def on_event(self, event):
        for handler in self.handlers:
            handler.handle(event)

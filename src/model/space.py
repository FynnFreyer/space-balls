import pyglet

from typing import List
from model.body import Body

class Space:
    def __init__(self, window: pyglet.window.Window=None, dimensions=(-1, -1)):
        self.batch = pyglet.graphics.Batch()
        if window is None:
            self.window = pyglet.window.Window()  # type: pyglet.window.Window
        else:
            self.window = window  # type: pyglet.window.Window

        self.bodies = list()  # type: List[Body]
        self.dimensions = dimensions

    def add_body(self, kind=Body, *args, **kwargs):
        body = kind(*args, **kwargs, space=self, batch=self.batch)
        self.bodies.append(body)
        return body


    def add_many(self, bodies: List[Body]):
        self.bodies.extend(bodies)

    def update(self, dt):
        for body in self.bodies:
            body.checkbounds(*self.dimensions, strategy=body.wrap)
            body.update(dt)

    def draw(self):
        self.batch.draw()


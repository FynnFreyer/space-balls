from model.body import *

from pyglet.window import key
from pyglet.event import EventDispatcher, EVENT_HANDLED


class Ship(Body):
    def __init__(self, speed=1, *args, **kwargs):
        super(Ship, self).__init__(*args, **kwargs)
        self.speed = speed
        self.rot_speed = 180
        self.key_pressed = key.KeyStateHandler()
        self.event_handlers = [self, self.key_pressed]
        self.acceleration_factor = 0

    def update(self, dt):
        super().update(dt)

    def on_key_press(self, symbol, modifier):
        pass

    def on_key_release(self, symbol, modifier):
        pass


class Bullet(Body):
    pass


class Meteor(Body):
    pass


class Star(Body):
    def __init__(self, *args, **kwargs):
        kwargs['mass'] = 10000
        super(Star, self).__init__(*args, **kwargs)

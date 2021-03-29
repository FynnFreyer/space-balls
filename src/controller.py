from model.body import *

import numpy as np
from pyglet.window import key


class Player(Body):
    def __init__(self, speed=500, rot_speed=180, *args, **kwargs):
        super(Player, self).__init__(*args, **kwargs)
        self.speed = speed
        self.rot_speed = rot_speed
        self.key_pressed = key.KeyStateHandler()
        self.event_handlers = [self, self.key_pressed]

    def update(self, dt):
        direction = Vector(np.cos(self.rotation), np.sin(self.rotation))
        dv = direction * self.speed
        dr = np.deg2rad(self.rot_speed * dt)
        if self.key_pressed[key.UP] and not self.key_pressed[key.DOWN]:
            self.pulses.append(dv)
        if self.key_pressed[key.DOWN] and not self.key_pressed[key.UP]:
            self.pulses.append(dv * -1)
        if self.key_pressed[key.LEFT] and not self.key_pressed[key.RIGHT]:
            self.rotation += dr
        if self.key_pressed[key.RIGHT] and not self.key_pressed[key.LEFT]:
            self.rotation -= dr
        super().update(dt)


class Bullet(Body):
    pass


class Meteor(Body):
    pass


class Resource(Body):
    pass


class Star(Body):
    def __init__(self, *args, **kwargs):
        kwargs['mass'] = 10000
        super(Star, self).__init__(*args, **kwargs)

    def update(self, dt):
        pass


# TODO
"""
kommunikation zwischen den controllern über events
collisionevent

"""
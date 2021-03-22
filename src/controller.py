from model.body import *
from view import resources
from api.communication.events import EventSource
import pyglet
from pyglet.window import key
from pyglet.event import EventDispatcher, EVENT_HANDLED


class Ship(Body):
    def __init__(self, speed=1, *args, **kwargs):
        super(Ship, self).__init__(*args, **kwargs)
        self.speed = speed
        self.rot_speed = 180
        self.key_pressed = key.KeyStateHandler()
        self.event_handlers = [self, self.key_pressed]

    def on_key_press(self, symbol, modifier):
        print('Ship.on_key_press', symbol)
        if symbol == key.UP:
            self.acceleration = self.direction * self.speed
        elif symbol == key.DOWN:
            self.acceleration = self.direction * -self.speed
        elif symbol == key.LEFT:
            self.rotational_velocity = self.rot_speed
        elif symbol == key.RIGHT:
            self.rotational_velocity = -self.rot_speed
        return EVENT_HANDLED



    def on_key_release(self, symbol, modifier):
        print('Ship.on_key_release', symbol)
        if symbol == key.UP or symbol == key.DOWN:
            self.acceleration = (0, 0)
        elif symbol == key.LEFT or symbol == key.RIGHT:
            self.rotational_velocity = 0
        return EVENT_HANDLED


class Bullet(Body):
    pass

class Meteor(Body):
    pass

class Star(Body):
    def __init__(self, *args, **kwargs):
        kwargs['mass'] = 10000
        super(Star, self).__init__(*args, **kwargs)


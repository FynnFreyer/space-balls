
from model.body import *

class Controller:
    def __init__(self):
        pass

class Ship(Body):
    def __init__(self, speed=20, *args, **kwargs):
        super(Ship, self).__init__(*args, **kwargs)
        self.speed = speed
        self.key_pressed = key.KeyStateHandler()
        self.event_handlers = [self, self.key_pressed]

    def update(self, dt):
        if self.key_pressed[key.UP] and not self.key_pressed[key.DOWN]:
            self.acceleration = self.direction * self.speed * dt
        elif self.key_pressed[key.DOWN] and not self.key_pressed[key.UP]:
            self.acceleration = self.direction * -self.speed * dt
        elif (self.key_pressed[key.UP] and self.key_pressed[key.DOWN]) or \
                (not self.key_pressed[key.UP] and not self.key_pressed[key.DOWN]):
            self.acceleration = Vektor2D(0, 0)

        if self.key_pressed[key.LEFT] and not self.key_pressed[key.RIGHT]:
            self.rotate_degrees(180 * dt)
        elif self.key_pressed[key.RIGHT] and not self.key_pressed[key.LEFT]:
            self.rotate_degrees(-180 * dt)
        elif (self.key_pressed[key.LEFT] and self.key_pressed[key.RIGHT]) or \
                (not self.key_pressed[key.LEFT] and not self.key_pressed[key.RIGHT]):
            pass

        super(Ship, self).update(dt)

    def on_key_press(self, symbol, modifier):
        pass

    def on_key_release(self, symbol):
        pass

class Bullet(Body):
    pass

class Meteor(Body):
    pass

class Star(Body):
    def __init__(self, *args, **kwargs):
        kwargs['mass'] = 10000
        super(Star, self).__init__(*args, **kwargs)


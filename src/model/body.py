import pyglet
from pyglet.window import key

from model.utils import Vektor2D
from view import resources


class Body:
    def __init__(self, location=(0, 0), velocity=(0, 0), acceleration=(0, 0), direction=(0, 1), mass=0, space=None, img=resources.img_ship_B, *args, **kwargs):
        #super(Body, self).__init__(img=img, *args, **kwargs)
        self.space = space

        self.mass = mass

        self._location = Vektor2D(*location)
        self._velocity = Vektor2D(*velocity)
        self._acceleration = Vektor2D(*acceleration)
        self._momentum = self.mass * self.velocity
        self._impulse = self.mass * self.acceleration
        self._direction = Vektor2D(*direction).normalized




    def add_shape(self, shape, *args, **kwargs):
        self.shape = shape(*args, **kwargs)

    @property
    def location(self):
        return self._location

    @location.setter
    def location(self, other, *args, **kwargs):
        x, y = self._set('_location', other, *args, **kwargs)
        self.x = x
        self.y = y

    @property
    def velocity(self):
        return self._velocity

    @velocity.setter
    def velocity(self, other, *args, **kwargs):
        self._set('_velocity', other, *args, **kwargs)

    @property
    def acceleration(self):
        return self._acceleration

    @acceleration.setter
    def acceleration(self, other, *args, **kwargs):
        self._set('_acceleration', other, *args, **kwargs)

    @property
    def momentum(self):
        return self._momentum

    @momentum.setter
    def momentum(self, other, *args, **kwargs):
        self._set('_momentum', other, *args, **kwargs)

    @property
    def impulse(self):
        return self._impulse

    @impulse.setter
    def impulse(self, other, *args, **kwargs):
        self._set('_impulse', other, *args, **kwargs)

    @property
    def direction(self):
        return self._direction

    @direction.setter
    def direction(self, other, *args, **kwargs):
        direction = self._set('_direction', other, *args, **kwargs)

    def _set(self, field, other, *args, **kwargs):
        try:
            x, y = other
        except TypeError:
            x, y = kwargs['x'], kwargs['y']
        except KeyError:
            x, y = args[0], args[1]
        except IndexError:
            raise

        value = Vektor2D(x, y)
        setattr(self, field, value)
        return value

    @property
    def sprite_rotation(self):
        return -self.direction.rotation_degrees + 90


    def rotate(self, rotation):
        self.direction = self.direction.rotate(rotation)

    def rotate_degrees(self, rotation):
        self.direction = self.direction.rotate_degrees(rotation)

    def update(self, dt):
        self.velocity += self.acceleration
        self.location += self.velocity

    def collides_with(self, other) -> bool:
        pass

    def wrap(self, max_x, max_y):
        self.x %= max_x
        self.y %= max_y

    def bounce(self, x, y):
        pass

    def checkbounds(self, x, y, strategy=wrap):
        if (x, y) != (-1, -1) and strategy is not None:
            strategy(x, y)

class Star(Body):
    def __init__(self, *args, **kwargs):
        kwargs['mass'] = 10000
        super(Star, self).__init__(*args, **kwargs)


class Ship(Body):
    def __init__(self, speed=20, *args, **kwargs):
        kwargs['img'] = resources.img_ship_C
        super(Ship, self).__init__(*args, **kwargs)

        self.speed = speed

        self.key_pressed = key.KeyStateHandler()
        self.space.window.push_handlers(self.key_pressed)

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

        print('Direction:', self.direction)
        print('Degrees:', self.direction.rotation_degrees)


        super(Ship, self).update(dt)

    def on_key_press(self, symbol, modifier):
        print('Ship.on_key_press')

    def on_key_release(self, symbol, modifier):
        pass
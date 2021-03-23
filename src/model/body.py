from model.utils import Vektor2D


class Body:
    def __init__(self, space=None, location=(0, 0), velocity=(0, 0), acceleration=(0, 0), direction=(0, 1), mass=0, *args, **kwargs):
        if space is None:
            raise TypeError('Needs a space')
        else:
            self.space = space

        self.mass = mass

        self._location = Vektor2D(*location)
        self._velocity = Vektor2D(*velocity)
        self._acceleration = Vektor2D(*acceleration)
        self._momentum = self.mass * self.velocity
        self._impulse = self.mass * self.acceleration
        self._direction = Vektor2D(*direction).normalized

        self.rotational_velocity = 0

    def update(self, dt):
        self.velocity += self.acceleration
        self.location += self.velocity
        self.rotate_degrees(self.rotational_velocity * dt)
        #self.rotate_degrees(15)
        print(self.x, self.y)

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




import numpy as np

from typing import List, Tuple, Mapping, Any
from model.utils import Vector


class Body:
    def update(self, dt):
        self.position += self.velocity * dt

    def __init__(self, space=None, shape=None,
                 position=(0, 0), velocity=(0, 0), mass=1, radius=32, rotation=0, rotational_velocity=0,
                 *args, **kwargs):
        if space is None:
            raise TypeError('Needs a space')
        else:
            self.space = space

        self.radius = radius

        x, y = position
        self.x, self.y = x, y
        self._position = Vector(x, y)

        vx, vy = velocity
        self.vx, self.vy = x, y
        self._velocity = Vector(vx, vy)

        self._mass = mass
        self._momentum = self.velocity * self.mass

        self._rotation = rotation
        self._rotational_velocity = rotational_velocity

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, position: Vector):
        self.x, self.y = self._set('_position', position)

    @property
    def velocity(self):
        return self._velocity

    @velocity.setter
    def velocity(self, velocity: Vector):
        self.vx, self.vy = self._set('_velocity', velocity)
        self._momentum = self.velocity * self.mass

    @property
    def mass(self):
        return self._mass

    @mass.setter
    def mass(self, mass: float):
        self._mass = mass
        self._momentum = self.velocity * self.mass

    @property
    def momentum(self):
        return self._momentum

    @property
    def rotation(self):
        return self._rotation

    @property
    def rotation_degrees(self):
        return np.rad2deg(self.rotation)

    @property
    def sprite_rotation(self):
        return -self.rotation_degrees + 90

    def rotate(self, rotation):
        self.direction = self.direction.rotate(rotation)

    def rotate_degrees(self, rotation):
        self.direction = self.direction.rotate_degrees(rotation)

    def wrap(self, max_x, max_y):
        self.x %= max_x
        self.y %= max_y

    def bounce(self, max_x, max_y):
        x, y = self.position
        vx, vy = self.velocity
        if x < 0:
            x = 0
            vx = -vx
        if x > max_x:
            x = max_x
            vx = -vx
        if y < 0:
            y = 0
            vy = -vy
        if y > max_y:
            y = max_y
            vy = -vy
        self.position = (x, y)
        self.velocity = (vx, vy)

    def checkbounds(self, x, y, strategy=wrap):
        if (x, y) != (-1, -1) and strategy is not None:
            strategy(x, y)

    def contains_point(self, point) -> bool:
        return self.position.distance_squared(point) <= self.radius ** 2

    def collides_with_line(self, line) -> bool:
        if self.contains_point(line.start) or self.contains_point(line.end):
            return True

        center_to_start = self.position - line.start
        t = (center_to_start * line.direction) / (line.direction * line.direction)

        if t < 0 or 1 < t:
            return False

        closest_point_to_center = line.start + (line.direction * t)
        return self.contains_point(closest_point_to_center)

    def collides_with(self, other) -> bool:
        if not self.position.distance(other.position) <= self.radius + other.radius:
            return False
        else:
            direction = self.position.distance_vector(other.position)
            point_of_collision = self.position + (direction / 2)
            return True


    def _set(self, field, other, *args, **kwargs):
        try:
            x, y = other
        except TypeError:
            x, y = kwargs['x'], kwargs['y']
        except KeyError:
            x, y = args[0], args[1]
        except IndexError:
            raise

        value = Vector(x, y)
        setattr(self, field, value)
        return value


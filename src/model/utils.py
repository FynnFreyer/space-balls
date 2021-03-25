import sys
import numpy as np

from math import sqrt, sin, cos, acos, atan2, degrees, radians
from collections import namedtuple
from abc import ABC, abstractmethod


def compare(x, y, epsilon=sys.float_info.min):
    return abs(x - y) <= epsilon * max(1.0, abs(x), abs(y))


class Vector(namedtuple('Vector', ['x', 'y'])):

    def __abs__(self):
        return sqrt(self.x ** 2 + self.y ** 2)

    def __add__(self, other):
        ox, oy = other
        return Vector(self.x + ox, self.y + oy)

    def __sub__(self, other):
        ox, oy = other
        return Vector(self.x - ox, self.y - oy)

    def __mul__(self, other):
        try:
            ox, oy = other
            return self.x * ox + self.y * oy
        except TypeError:
            return Vector(self.x * other, self.y * other)

    def __truediv__(self, other):
        try:
            ox, oy = other
            return Vector(self.x / ox, self.y / oy)
        except TypeError:
            return Vector(self.x * other, self.y * other)

    def __eq__(self, other):
        ox, oy = other
        return compare(self.x, ox) and compare(self.y, oy)

    def rotation(self, center=(0, 0)):
        dx, dy = self - center
        return np.arctan2(dy, dx)

    def rotation_degrees(self, center=(0, 0)):
        return np.rad2deg(self.rotation(center))

    def rotate(self, rad: float, center=(0, 0)):
        x, y = center
        dx, dy = self - center

        px = (dx * np.cos(rad) - dy * np.sin(rad)) + x
        py = (dx * np.sin(rad) + dy * np.cos(rad)) + y

        return Vector(px, py)

    def rotate_degrees(self, deg: float, center=(0, 0)):
        return Vector(*self.rotate(np.deg2rad(deg), center))

    def angle(self, other):
        return np.arccos((self * other) / (abs(self) * abs(other)))

    def angle_degrees(self, other):
        return np.rad2deg(self.angle(other))

    @property
    def normalized(self):
        return self * (1 / abs(self))

    def distance_vector(self, other):
        return self - other

    def distance(self, other=(0, 0)):
        return abs(self - other)

    def distance_squared(self, other=(0, 0)):
        dx, dy = self - other
        return dx ** 2 + dy ** 2


class Line:
    support: Vector
    direction: Vector

    def __init__(self, support: Vector, direction: Vector):
        self.support = Vector(*support)
        self.direction = Vector(*direction)

        self.start = self.support
        self.end = self.support + self.direction

        x1, y1 = self.start
        x2, y2 = self.end
        dx, dy = x2 - x1, y2 - y1
        m = dy / dx
        b = y2 - m * x2

        self.m = m
        self.b = b

    @classmethod
    def from_start_end(cls, start, end):
        e = Vector(*end)
        return cls(start, e.distance_vector(start))

    def contains_point(self, point) -> bool:
        x, y = point
        return round(y, 8) == round(self.m * x + self.b, 8)

    def collides_with_line(self, line) -> bool:
        return not compare(self.m, line.m) or compare(self.b, line.b)

class Ray(Line):
    def __init__(self):
        pass
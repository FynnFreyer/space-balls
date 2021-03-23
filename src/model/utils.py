import sys

from math import sqrt, sin, cos, asin, acos, atan2, degrees, radians, pi, tau, copysign
from collections import namedtuple


def compare(x, y, epsilon=sys.float_info.min):
    return abs(x - y) <= epsilon * max(1.0, abs(x), abs(y))


class Vektor2D(namedtuple('Vektor2D', ['x', 'y'])):

    def __abs__(self):
        return sqrt(self.x ** 2 + self.y ** 2)

    def __add__(self, other):
        ox, oy = other
        return Vektor2D(self.x + ox, self.y + oy)

    def __sub__(self, other):
        ox, oy = other
        return Vektor2D(self.x - ox, self.y - oy)

    def __mul__(self, other):
        try:
            ox, oy = other
            return self.x * ox + self.y * oy
        except TypeError:
            return Vektor2D(self.x * other, self.y * other)

    def __eq__(self, other):
        ox, oy = other
        return compare(self.x, ox) and compare(self.y, oy)

    def __truediv__(self, other):
        ox, oy = other
        return Vektor2D(self.x / ox, self.y / oy)

    @property
    def rotation(self, other=(0, 0)):
        dx, dy = self - other
        return atan2(dy, dx)

    @property
    def rotation_degrees(self):
        return degrees(self.rotation)

    def rotate(self, radians):
        combined_rotation = self.rotation + radians
        return Vektor2D(cos(combined_rotation), sin(combined_rotation)) * abs(self)

    def rotate_degrees(self, degrees):
        return self.rotate(radians(degrees))

    def rotate_around(self, radians, other=(0, 0)):
        x, y = other
        dx, dy = self - other

        xp = (dx * cos(radians) - dy * sin(radians)) + x
        yp = (dx * sin(radians) + dy * cos(radians)) + y

        return Vektor2D(xp, yp)

    def rotate_around_degrees(self, degrees):
        return self.rotate_around(radians(degrees))

    def angle(self, other):
        return acos((self * other) / (abs(self) * abs(other)))

    def angle_degrees(self, other):
        return degrees(self.angle(other))

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

    def on_line(self, line):
        return False


class Shape:
    def contains_point(self, point) -> bool:
        raise NotImplementedError

    def collides_with_line(self, line):
        raise NotImplementedError


class Line(Shape):
    def __init__(self, support: Vektor2D, direction: Vektor2D):
        self.support = Vektor2D(*support)
        self.direction = Vektor2D(*direction)

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
        e = Vektor2D(*end)
        return cls(start, e.distance_vector(start))

    def contains_point(self, point) -> bool:
        x, y = point
        return round(y, 8) == round(self.m * x + self.b, 8)

    def collides_with_line(self, line):
        return not compare(self.m, line.m) or compare(self.b, line.b)


class Circle(Shape):
    def __init__(self, radius: float, center: Vektor2D):
        self.radius = radius
        self.center = center

    def contains_point(self, point) -> bool:
        return self.center.distance_squared(point) <= self.radius ** 2

    def collides_with_line(self, line):
        if self.contains_point(line.start) or self.contains_point(line.end):
            return True

        center_to_start = self.center - line.start
        t = (center_to_start * line.direction) / (line.direction * line.direction)

        if t < 0 or 1 < t:
            return False

        closest_point_to_center = line.start + (line.direction * t)
        return self.contains_point(closest_point_to_center)


class Box(Shape):
    def __init__(self, center: Vektor2D, size: Vektor2D, rotation: float = 0):
        self.center = center
        self.size = size
        x, y = center
        dx, dy = size / 2
        self.min_x, self.max_x = x - dx, x + dx
        self.min_y, self.max_y = y - dy, y + dy
        self.rotation = rotation

    def contains_point(self, point) -> bool:
        local_point = Vektor2D(*point)
        x, y = local_point.rotate_around_degrees(self.rotation, other=self.center)
        return (self.min_x <= x and x <= self.max_x) and \
               (self.min_y <= y and y <= self.max_y)

    def collides_with_line(self, line):
        raise NotImplementedError


if __name__ == '__main__':
    v = Vektor2D(0, 1)
    print(v)
    print(v.rotation_degrees)
    for i in range(12):
        v = v.rotate_degrees(30)
        print(v)
        print(round(v.rotation_degrees, 8))

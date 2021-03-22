from math import sqrt, sin, cos, asin, acos, atan2, degrees, radians, pi, tau, copysign
from collections import namedtuple

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

    @property
    def rotation(self):
        return atan2(self.y, self.x)

    @property
    def rotation_degrees(self):
        return degrees(self.rotation)

    def rotate(self, rotation):
        combined_rotation = self.rotation + rotation
        return Vektor2D(cos(combined_rotation), sin(combined_rotation)) * abs(self)

    def rotate_degrees(self, rotation):
        return self.rotate(radians(rotation))

    def angle(self, other):
        return acos((self * other) / (abs(self) * abs(other)))

    def angle_degrees(self, other):
        return degrees(self.angle(other))

    @property
    def normalized(self):
        return self * (1/abs(self))

    def distance_vector(self, other):
        ox, oy = other
        return Vektor2D(ox - self.x, oy - self.y)

    def distance(self, other=(0, 0)):
        return abs(self.distance_vector(other))


if __name__ == '__main__':
    v = Vektor2D(0, 1)
    print(v)
    print(v.rotation_degrees)
    for i in range(12):
        v = v.rotate_degrees(30)
        print(v)
        print(round(v.rotation_degrees, 8))



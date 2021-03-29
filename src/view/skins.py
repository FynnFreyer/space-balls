import pyglet

from view.resources import *
from controller import *


class Skin:
    def __init__(self, img=empty_space, scale=1):
        self.img = img
        self.scale = scale

    def to_sprite(self, *args, **kwargs):
        kwargs['img'] = self.img
        return pyglet.sprite.Sprite(*args, **kwargs)

    @classmethod
    def get_skin(cls, body):
        if type(body) == Body:
            return cls.DefaultSkin()
        elif type(body) == Player:
            return cls.ShipSkinA()
        elif type(body) == Meteor:
            return cls.MeteorSkinA()
        elif type(body) == Bullet:
            return cls.BulletSkinA()
        elif type(body) == Star:
            return cls.StarSkin()

    class DefaultSkin:
        def __init__(self):
            self.img = white_circle

    class ShipSkinA:
        def __init__(self):
            self.img = red_circle_indexed

    class ShipSkinB:
        def __init__(self):
            self.img = ship_B

    class MeteorSkinA:
        def __init__(self):
            self.img = ship_B

    class BulletSkinA:
        def __init__(self):
            self.img = ship_C

    class StarSkin:
        def __init__(self):
            self.img = red_circle


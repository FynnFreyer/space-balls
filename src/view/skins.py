import pyglet

from view.resources import *
from model.body import *
from controller import *

class Skin:
    def __init__(self, img=empty_space, scale=1, *args, **kwargs):
        self.img = img
        self.img = img.scale

    def to_sprite(self, *args, **kwargs):
        kwargs['img'] = self.img
        return pyglet.sprite.Sprite(*args, **kwargs)

    @classmethod
    def get_skin(cls, body, *args, **kwargs):
        if type(body) == Body:
            return Skin(*args, **kwargs)
        elif type(body) == Ship:
            return ShipSkinA()
        elif type(body) == Meteor:
            return MeteorSkinA()
        elif type(body) == Bullet:
            return BulletSkinA()


class ShipSkinA(Skin):
    def __init__(self):
        self.img = ship_A


class MeteorSkinA(Skin):
    def __init__(self):
        self.img = ship_B


class BulletSkinA(Skin):
    def __init__(self):
        self.img = ship_C


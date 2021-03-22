import pyglet

from model.space import Space
from model.body import *

from view.resources import *

class View:
    """
    The view is what actually gets rendered.
    It takes a space and optionally a specific body in that space to focus on.
    It translates the space coordinates into screen coordinates.
    """

    def __init__(self, space: Space, focus: Body=None, batch: pyglet.graphics.Batch=None):
        self.space = space
        self.focus = focus
        self.batch = batch

    def draw(self):
        if self.focus is None:
            self.space.draw()
        else:
            sprites = list()
            for body in self.space.bodies:
                sprite = pyglet.sprite.Sprite(img=body.img)



            raise NotImplementedError

def get_img(body: Body):
    if type(body) == Body:
        return
    if type(body) == Ship:
        return img_ship_B

class Ship_View(pyglet.sprite.Sprite):
    def __init__(self, *args, **kwargs):

        super(Ship_View, self).__init__(*args, **kwargs)

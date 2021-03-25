import pyglet

from model.space import Space
from view.resources import *
from view.skins import *


class View:
    """
    The view is what actually gets rendered.
    It takes a space and optionally a specific body in that space to focus on.
    It translates the space coordinates into screen coordinates.
    """

    def __init__(self, space: Space, focus: Body = None, batch: pyglet.graphics.Batch = None,
                 window: pyglet.window.Window = None):
        self.space = space  # type: Space
        self.focus = focus  # type: Body
        self.window = window

        if batch is None:
            self.batch = pyglet.graphics.Batch()
        else:
            self.batch = batch

        self.sprite_map = {}  # type: Dict[Body, pyglet.sprite.Sprite]
        self._init_sprite_map()
        self._calculate_sprite_coordinates()

    def draw(self):
        self._calculate_sprite_coordinates()
        self.batch.draw()

    def _calculate_sprite_coordinates(self):
        if self.focus is not None:
            displacement = self.focus.position - Vector(self.window.width / 2, self.window.height / 2)
        for body, sprite in self.sprite_map.items():
            if self.focus is None:
                sprite.x, sprite.y = body.position
                sprite.rotation = body.sprite_rotation
            else:
                sprite.x, sprite.y = body.position - displacement
                sprite.rotation = body.sprite_rotation

    def _init_sprite_map(self):
        for body in self.space.bodies:
            skin = Skin.get_skin(body)
            x, y = body.position
            sprite = pyglet.sprite.Sprite(img=skin.img, x=x, y=y, batch=self.batch)
            sprite.rotation = body.sprite_rotation
            self.sprite_map[body] = sprite


class GameWindow(pyglet.window.Window):
    pass

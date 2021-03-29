import pyglet

from pyglet.window import Window
from pyglet.graphics import Batch
from pyglet.sprite import Sprite

from model.space import Space
from view.resources import *
from view.skins import *


class View:
    """
    The view is what actually gets rendered.
    It takes a space and optionally a specific body in that space to focus on.
    It translates the space coordinates into screen coordinates.
    """

    def draw(self):
        self._calculate_body_positions()
        self.batch.draw()

    def __init__(self, space: Space, focus: Body = None, scale=1, batch: Batch = None,
                 window: Window = None):
        self.space = space  # type: Space
        self.focus = focus  # type: Body
        self.scale = scale  # type: float

        if window is None:
            self.window = Window()
        else:
            self.window = window  # type: Window
        self.window_center = Vector(window.width / 2, window.height / 2)

        if focus:
            self.displacement = self.focus.position - self.window_center
            self.focus_center = self.focus.position
        else:
            self.displacement = Vector(0, 0)
            self.focus_center = self.window_center

        if batch is None:
            self.batch = Batch()
        else:
            self.batch = batch

        self.sprite_map = {}  # type: Mapping[Body, pyglet.sprite.Sprite]
        self._init_sprite_map()
        self._calculate_body_positions()

    def _init_sprite_map(self):
        for body in self.space.bodies:
            skin = Skin.get_skin(body)
            x, y = body.position - self.displacement
            sprite = pyglet.sprite.Sprite(img=skin.img, x=x, y=y, batch=self.batch)
            sprite.rotation = body.sprite_rotation
            self.sprite_map[body] = sprite

    def _calculate_body_positions(self):
        for body, sprite in self.sprite_map.items():
            sprite.x, sprite.y = self._to_screen_coordinates(*body.position)
            sprite.scale = self.scale
            sprite.rotation = body.sprite_rotation

    def _draw_grid(self):
        pass

    def _to_screen_coordinates(self, x, y):
        if self.focus:
            self.displacement = self.focus.position - self.window_center
            self.focus_center = self.focus.position
        return (Vector(x, y) - self.focus_center) * self.scale + self.window_center


class GameWindow(pyglet.window.Window):
    pass

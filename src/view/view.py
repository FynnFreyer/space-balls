import pyglet

from pyglet.window import Window
from pyglet.graphics import Batch
from pyglet.shapes import Line

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
        self._init_grid(10, 10)
        self._draw_grid(10, 10)
        self._calculate_body_positions()
        self.batch.draw()

    def __init__(self, space: Space, focus: Body = None, scale=1, batch: Batch = None,
                 window: Window = None):
        self.space = space  # type: Space
        self.focus = focus  # type: Body
        self.scale = scale  # type: float

        self._init_batch(batch)
        self._init_window(window)

        self.displacement = Vector(0, 0)  # type: Vector
        self.focus_center = self.window_center  # type: Vector

        self.sprite_map = {}  # type: Mapping[Body, pyglet.sprite.Sprite]
        self._init_sprite_map()
        self._update_focus()
        self._calculate_body_positions()

    def _init_batch(self, batch):
        if batch is None:
            self.batch = Batch()  # type: Batch
        else:
            self.batch = batch  # type: Batch

    def _init_window(self, window):
        if window is None:
            self.window = Window()  # type: Window
        else:
            self.window = window  # type: Window
        self.window_center = Vector(window.width / 2, window.height / 2)  # type: Vector


    def _init_sprite_map(self):
        for body in self.space.bodies:
            skin = Skin.get_skin(body)
            x, y = self.to_screen_coordinates(*body.position)
            sprite = pyglet.sprite.Sprite(img=skin.img, x=x, y=y, batch=self.batch)
            sprite.rotation = body.sprite_rotation
            self.sprite_map[body] = sprite

    def _calculate_body_positions(self):
        for body, sprite in self.sprite_map.items():
            sprite.x, sprite.y = self.to_screen_coordinates(*body.position)
            sprite.scale = self.scale
            sprite.rotation = body.sprite_rotation

    def _draw_grid(self, x_lines, y_lines):
        self._update_focus()
        dx, dy = self.displacement

        x_step = self.window.width // x_lines
        y_step = self.window.height // y_lines

        width = self.window.width
        height = self.window.height

        for i, x_line in enumerate(self._grid_lines_vertical):
            x = (dx + i * x_step) % width
            x_line.x = x
            x_line.x2 = x
        for i, y_line in enumerate(self._grid_lines_horizontal):
            y = (dy + i * y_step) % height
            y_line.y = y
            y_line.y2 = y

    def _update_focus(self):
        if self.focus:
            self.displacement = self.focus.position - self.window_center
            self.focus_center = self.focus.position

    def from_screen_coordinates(self, x, y):
        self._update_focus()
        return Vector(x, y) + self.displacement

    def to_screen_coordinates(self, x, y):
        self._update_focus()
        return (Vector(x, y) - self.focus_center) * self.scale + self.window_center

    def on_mouse_scroll(self, x, y, dx, dy):
        if (dx > 0 or dy > 0) and self.scale <= 5:
            self.scale += 0.1
        elif (dx < 0 or dy < 0) and self.scale >= 0.1:
            self.scale -= 0.1

    def _init_grid(self, x_lines, y_lines):
        self._grid_lines_vertical = list()
        self._grid_lines_horizontal = list()

        width = self.window.width
        height = self.window.height

        for x_line in range(x_lines):
            self._grid_lines_vertical.append(Line(0, 0, 0, height, width=10, batch=self.batch))
        for y_line in range(y_lines):
            self._grid_lines_horizontal.append(Line(0, 0, width, 0, width=10, batch=self.batch))


class GameWindow(pyglet.window.Window):
    pass

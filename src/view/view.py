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
        self._draw_grid(100, 100)
        self._calculate_body_positions()
        self.grid.draw()
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

        self._init_sprite_map()
        self._init_grid(10, 10)

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
        self.sprite_map = {}  # type: Mapping[Body, pyglet.sprite.Sprite]
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

    def _draw_grid(self, x_step, y_step):
        self._update_focus()
        dx, dy = self.displacement

        width = self.window.width
        height = self.window.height
        # print(self.scale)

        """

        vertical_lines = int(width / self.scale / x_step) + 1
        horizontal_lines = int(height / self.scale / y_step) + 1

        for i in range(vertical_lines):
            x_scaled = x_step * self.scale
            x = (dx % x_step) + 0 * x_step
            Line(x, 0, x, height, width=10 * self.scale).draw()
        for i in range(horizontal_lines):
            y_scaled = y_step * self.scale
            y = ((dy // y_scaled) * y_scaled) + i * y_scaled - dy
            y = 0
            Line(0, y, width, y, width=10 * self.scale).draw()
            
        """
        vertical_lines = int(width * (1 / self.scale)) // x_step
        vertical_lines_before = dx // x_step
        x_offset = dx % x_step
        # print(vertical_lines_before)
        horizontal_lines = height // y_step
        horizontal_lines_before = dy // y_step

        for i in range(vertical_lines):
            x = dx - x_offset + (i+1) * x_step
            x, _ = self.to_screen_coordinates(x, 0)
            Line(x, 0, x, height, width=10 * self.scale).draw()





        pass

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
        if (dx > 0 or dy > 0) and self.scale < 5:
            self.scale = round(self.scale + 0.1, 2)
        elif (dx < 0 or dy < 0) and self.scale > 0.1:
            self.scale = round(self.scale - 0.1, 2)

    def _init_grid(self, x_lines, y_lines):
        self._grid_lines_vertical = list()
        self._grid_lines_horizontal = list()
        self.grid = Batch()

        width = self.window.width
        height = self.window.height

        for x_line in range(x_lines):
            self._grid_lines_vertical.append(Line(0, 0, 0, height, width=10*self.scale, batch=self.grid))
        for y_line in range(y_lines):
            self._grid_lines_horizontal.append(Line(0, 0, width, 0, width=10*self.scale, batch=self.grid))


class GameWindow(pyglet.window.Window):
    pass

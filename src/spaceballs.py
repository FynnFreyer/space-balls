import pyglet

from model.space import Space
from view.view import View
from controller import Ship
from random import randint

display = pyglet.canvas.get_display()
screens = display.get_screens()
window = pyglet.window.Window(1920, 1080, "Tester", resizable=False, screen=screens[-1], fullscreen=True)

space = Space()
ship_1 = space.add_body(kind=Ship, position=(500, 500), velocity=(200, 0))  # type: Ship
#ship_2 = space.add_body(kind=Ship, position=(800, 532), velocity=(100, 0))  # type: Ship
#ship_3 = space.add_body(kind=Ship, position=(1300, 700, ), velocity=(-500, -200))  # type: Ship

bodies = list()
for i in range(20):
    x = randint(0, 1920)
    y = randint(0, 1080)
    v1, v2 = randint(-100, 100), randint(-100, 100)
    space.add_body(kind=Ship, position=(x, y), velocity=(v1, v2))


window.event(ship_1.on_key_press)
window.event(ship_1.on_key_release)

window.push_handlers(ship_1.event_handlers)
view = View(space=space, window=window, focus=None)


@window.event
def on_draw():
    window.clear()
    view.draw()


if __name__ == "__main__":
    # Update the game 120 times per second
    pyglet.clock.schedule_interval(space.update, 1 / 120)

    # Tell pyglet to do its thing
    pyglet.app.run()

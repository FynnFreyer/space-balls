import pyglet

from model.space import Space
from view.view import View
from controller import Ship

display = pyglet.canvas.get_display()
screens = display.get_screens()
window = pyglet.window.Window(1920, 1080, "Tester", resizable=False, screen=screens[-1], fullscreen=True)

space = Space()
ship = space.add_body(kind=Ship, position=(500, 500), velocity=(200, 0))  # type: Ship
ship2 = space.add_body(kind=Ship, position=(800, 532), velocity=(100, 0))  # type: Ship

window.event(ship.on_key_press)
window.event(ship.on_key_release)

window.push_handlers(ship.event_handlers)
view = View(space=space, window=window)


@window.event
def on_draw():
    window.clear()
    view.draw()


if __name__ == "__main__":
    # Update the game 120 times per second
    pyglet.clock.schedule_interval(space.update, 1 / 120)

    # Tell pyglet to do its thing
    pyglet.app.run()

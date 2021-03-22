import pyglet

from model.space import Space
from model.body import *
from view.view import View

window = pyglet.window.Window(800, 600, "Tester", resizable=False)

space = Space(window=window)
ship = space.add_body(kind=Ship, location=(300, 300))

view = View(space)

@window.event
def on_draw():
    window.clear()
    view.draw()

if __name__ == "__main__":
    # Update the game 120 times per second
    pyglet.clock.schedule_interval(space.update, 1/120)

    # Tell pyglet to do its thing
    pyglet.app.run()

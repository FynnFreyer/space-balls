import pyglet

from model.space import Space
from model.body import Body
from view.view import View
from controller import Player, Star
from random import randint

display = pyglet.canvas.get_display()
screens = display.get_screens()
window = pyglet.window.Window(1920, 1080, "Spaceballs", resizable=False, screen=screens[-1], fullscreen=True)

space = Space()
ship_1 = space.add_body(kind=Player, position=(500, 400), velocity=(200, 0))  # type: Player
star = space.add_body(kind=Star, position=(0, 0), velocity=(0, 0))  # type: Player
#ship_3 = space.add_body(kind=Body, position=(1300, 700, ), velocity=(-500, -200))  # type: Ship

#bodies = list()
#for i in range(6):
#    x = randint(0, window.width)
#    y = randint(0, window.height)
#    v1, v2 = randint(-100, 100), randint(-100, 100)
#    space.add_body(kind=Body, position=(x, y), velocity=(v1, v2))


#window.event(ship_1.on_key_press)
#window.event(ship_1.on_key_release)

#window.push_handlers(ship_1.event_handlers)
for handler in ship_1.event_handlers:
    window.push_handlers(handler)
view = View(space=space, window=window, focus=ship_1, scale=1)
window.push_handlers(view)


@window.event
def on_draw():
    window.clear()
    view.draw()

event_logger = pyglet.window.event.WindowEventLogger()
#window.push_handlers(event_logger)

if __name__ == "__main__":
    # Update the game 120 times per second
    pyglet.clock.schedule_interval(space.update, 1 / 120)

    # Tell pyglet to do its thing
    pyglet.app.run()

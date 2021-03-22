import pyglet

def center_image(image):
    """Sets an image's anchor point to its center"""
    image.anchor_x = image.width / 2
    image.anchor_y = image.height / 2

pyglet.resource.path = ['../resources', '../resources/audio', '../resources/sprites', '../resources/sprites/ships', '../resources/sprites/meteors', '../resources/sprites/enemies']
pyglet.resource.reindex()

empty_space = pyglet.resource.image('empty.png')
center_image(empty_space)

img_ship_A = pyglet.resource.image('ship_A.png')
center_image(img_ship_A)

img_ship_B = pyglet.resource.image('ship_B.png')
center_image(img_ship_B)

img_ship_C = pyglet.resource.image('ship_C.png')
center_image(img_ship_C)

from pyglet.image import ImageData
from pyglet.sprite import Sprite
from pyglet import resource

window_width, window_height = 576, 576
offset_x, offset_y = 64, 64

resource.path = ['../assets']
resource.reindex()


def set_center(img: ImageData):
    img.anchor_x = img.width // 2
    img.anchor_y = img.height // 2


def rescale_sprite_64(sprite: Sprite, width, height):
    sprite.scale_x = 64 / width
    sprite.scale_y = 64 / height


def load_sprite(path: str, rescale=False):
    img = resource.image(path)
    sprite = Sprite(img=img)

    if rescale:
        rescale_sprite_64(sprite, img.width, img.height)

    return sprite


def get_py_y_value(my_y_value):
    return window_height - 64 - my_y_value


def get_my_y_value(py_y_value):
    return window_height - 64 - py_y_value


def get_col(x_value):
    return (x_value - offset_x) // 64


def get_row(y_value):
    return (y_value - offset_y) // 64

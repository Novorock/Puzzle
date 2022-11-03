from pyglet.image import ImageData
from pyglet.sprite import Sprite
from pyglet import resource
from pyglet import font

window_width, window_height = 576, 576
offset_x, offset_y = 64, 64

resource.path = ['../assets']
resource.reindex()

resource.add_font('small_pixel.ttf')
SMALL_PIXEL = font.load('Small Pixel')


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


GROUND = []
for i in range(8):
    GROUND.append(resource.image('ground_0%s.png' % i))

BLOCK = resource.image('block_02.png')
RED_PIECE = resource.image('pieces/red_piece.png')
GREEN_PIECE = resource.image('pieces/green_piece.png')
BLUE_PIECE = resource.image('pieces/blue_piece.png')
SELECTION = resource.image('selection.png')
RED_PIECE_SELECTED = resource.image('pieces/red_piece_selected.png')
GREEN_PIECE_SELECTED = resource.image('pieces/green_piece_selected.png')
BLUE_PIECE_SELECTED = resource.image('pieces/blue_piece_selected.png')

MOVEMENT_SPEED = 150
BLOCKED = [1, 2]
EMPTY, FIRST_KIND, SECOND_KIND, THIRD_KIND = 0, 21, 22, 23


def get_py_y_value(my_y_value):
    return window_height - 64 - my_y_value


def get_my_y_value(py_y_value):
    return window_height - 64 - py_y_value


def get_col(x_value):
    return (x_value - offset_x) // 64


def get_row(y_value):
    return (y_value - offset_y) // 64

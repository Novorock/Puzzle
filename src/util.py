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


GROUND_TILE = load_sprite('ground_06.png')
BLOCK_TILE = load_sprite('block.png', rescale=True)
BLOCK_RED = load_sprite('block_red_signature.png')
BLOCK_GREEN = load_sprite('block_green_signature.png')
BLOCK_BLUE = load_sprite('block_blue_signature.png')
RED_PIECE = load_sprite('pieces/red_piece.png')
GREEN_PIECE = load_sprite('pieces/green_piece.png')
BLUE_PIECE = load_sprite('pieces/blue_piece.png')
SELECTION = load_sprite('selection.png')
RED_PIECE_SELECTED = load_sprite('pieces/red_piece_selected.png')
GREEN_PIECE_SELECTED = load_sprite('pieces/green_piece_selected.png')
BLUE_PIECE_SELECTED = load_sprite('pieces/blue_piece_selected.png')

MOVEMENT_SPEED = 100
GROUND, BLOCK, RED_SIGN, GREEN_SIGN, BLUE_SIGN = 0, 10, 11, 12, 13
KIND_1, KIND_2, KIND_3 = 21, 22, 23


def get_py_y_value(my_y_value):
    return window_height - 64 - my_y_value


def get_my_y_value(py_y_value):
    return window_height - 64 - py_y_value


def get_col(x_value):
    return (x_value - offset_x) // 64


def get_row(y_value):
    return (y_value - offset_y) // 64
